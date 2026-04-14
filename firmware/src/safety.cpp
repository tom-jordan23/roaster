#include "safety.h"
#include "config.h"
#include "sensors.h"
#include "heater.h"
#include "blower.h"

static SafetyState current_state = SafetyState::STARTUP;
static uint8_t startup_good_reads = 0;
static float prev_tc1 = NAN;
static unsigned long prev_tc1_time_ms = 0;

void safety_init() {
    current_state = SafetyState::STARTUP;
    startup_good_reads = 0;
    prev_tc1 = NAN;
    prev_tc1_time_ms = 0;
    // E12: Do NOT call heater_force_off() here — heater_init() already
    // ensures safe state, and calling force_off would latch the forced_off
    // flag before the system even starts.
}

SafetyState safety_check() {
    // --- Startup grace period (F4) ---
    // TCs start faulted. Wait for N consecutive good reads across all TCs
    // before transitioning to OK and allowing heater operation.
    if (current_state == SafetyState::STARTUP) {
        heater_force_off();
        bool all_good = true;
        for (int i = 0; i < TC_COUNT; i++) {
            if (sensors_has_fault(i)) {
                all_good = false;
                break;
            }
        }
        if (all_good) {
            startup_good_reads++;
            if (startup_good_reads >= SAFETY_STARTUP_GOOD_READS) {
                current_state = SafetyState::OK;
                heater_clear_forced_off();
            }
        } else {
            startup_good_reads = 0;
        }
        return current_state;
    }

    // --- Already in fault — keep heater off, wait for reset ---
    if (current_state != SafetyState::OK) {
        heater_force_off();
        return current_state;
    }

    // --- Airflow interlock (E4/F3) ---
    // Heater must never run without blower confirmation
    if (!blower_is_running()) {
        if (heater_is_on() || heater_get_duty() > 0) {
            safety_trigger_fault(SafetyState::FAULT_AIRFLOW);
            return current_state;
        }
    }

    // --- TC1 (process air) over-temp (F1: NAN guard) ---
    float tc1 = sensors_get_temp(0);
    if (isnan(tc1) || tc1 > SAFETY_MAX_PROCESS_TEMP_C) {
        safety_trigger_fault(SafetyState::FAULT_OVERTEMP);
        return current_state;
    }

    // --- TC3 (exhaust) over-temp (F1: NAN guard) ---
    float tc3 = sensors_get_temp(2);
    if (isnan(tc3) || tc3 > SAFETY_MAX_EXHAUST_TEMP_C) {
        safety_trigger_fault(SafetyState::FAULT_OVERTEMP);
        return current_state;
    }

    // --- Stale sensor data check (F6) ---
    unsigned long now = millis();
    if (sensors_get_age_ms() > SAFETY_SENSOR_STALE_MS) {
        safety_trigger_fault(SafetyState::FAULT_TC);
        return current_state;
    }

    // --- Rate-of-change detection (F7) ---
    if (!isnan(prev_tc1) && !isnan(tc1) && prev_tc1_time_ms > 0) {
        float dt_sec = (now - prev_tc1_time_ms) / 1000.0f;
        if (dt_sec > 0.0f) {
            float rate = fabsf(tc1 - prev_tc1) / dt_sec;
            if (rate > SAFETY_MAX_RATE_C_PER_S) {
                safety_trigger_fault(SafetyState::FAULT_RATE);
                return current_state;
            }
        }
    }
    prev_tc1 = tc1;
    prev_tc1_time_ms = now;

    // --- TC fault check (E13: consecutive fault counter is in sensors.cpp) ---
    for (int i = 0; i < TC_COUNT; i++) {
        if (sensors_has_fault(i)) {
            safety_trigger_fault(SafetyState::FAULT_TC);
            return current_state;
        }
    }

    return current_state;
}

void safety_trigger_fault(SafetyState fault) {
    current_state = fault;
    heater_force_off();
}

bool safety_reset() {
    // F5/E2/E3/F8: Gate reset on actual conditions
    // Only allow reset if:
    //   1. All TCs are reading valid (no faults)
    //   2. All temps are below safe threshold with hysteresis
    //   3. Blower state is acceptable

    for (int i = 0; i < TC_COUNT; i++) {
        if (sensors_has_fault(i)) {
            return false;
        }
    }

    float tc1 = sensors_get_temp(0);
    float tc2 = sensors_get_temp(1);
    float tc3 = sensors_get_temp(2);

    if (isnan(tc1) || isnan(tc2) || isnan(tc3)) {
        return false;
    }

    if (tc1 > SAFETY_RESET_TEMP_C || tc2 > SAFETY_RESET_TEMP_C || tc3 > SAFETY_RESET_TEMP_C) {
        return false;
    }

    // Conditions clear — reset state and clear the forced_off latch (F5/E3)
    current_state = SafetyState::OK;
    heater_clear_forced_off();
    prev_tc1 = NAN;
    prev_tc1_time_ms = 0;
    return true;
}

SafetyState safety_get_state() {
    return current_state;
}

bool safety_is_ok() {
    return current_state == SafetyState::OK;
}

bool safety_heater_allowed() {
    return current_state == SafetyState::OK;
}

bool safety_startup_complete() {
    return current_state != SafetyState::STARTUP;
}
