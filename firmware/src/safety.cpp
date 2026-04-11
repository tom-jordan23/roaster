#include "safety.h"
#include "config.h"
#include "sensors.h"
#include "heater.h"

static SafetyState current_state = SafetyState::OK;

void safety_init() {
    current_state = SafetyState::OK;
    // Ensure heater is off at startup
    heater_force_off();
}

SafetyState safety_check() {
    if (current_state != SafetyState::OK) {
        // Already in fault — keep heater off, wait for reset
        heater_force_off();
        return current_state;
    }

    // Check TC1 (process air) over-temp
    float tc1 = sensors_get_temp(0);
    if (tc1 > SAFETY_MAX_PROCESS_TEMP_C) {
        safety_trigger_fault(SafetyState::FAULT_OVERTEMP);
        return current_state;
    }

    // Check TC3 (exhaust) over-temp
    float tc3 = sensors_get_temp(2);
    if (tc3 > SAFETY_MAX_EXHAUST_TEMP_C) {
        safety_trigger_fault(SafetyState::FAULT_OVERTEMP);
        return current_state;
    }

    // Check for TC faults (open circuit, short, read errors)
    for (int i = 0; i < TC_COUNT; i++) {
        if (sensors_has_fault(i)) {
            safety_trigger_fault(SafetyState::FAULT_TC);
            return current_state;
        }
    }

    // TODO: Check airflow / blower status when hardware is defined
    // This will likely be a tachometer signal or current sense

    return current_state;
}

void safety_trigger_fault(SafetyState fault) {
    current_state = fault;
    heater_force_off();
}

bool safety_reset() {
    // Only allow reset if conditions are actually clear
    // (temps below threshold, TCs reading valid, etc.)
    // For now, simple reset — will be tightened during testing
    current_state = SafetyState::OK;
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
