#include "heater.h"
#include "config.h"
#include "safety.h"

static uint8_t duty_percent = 0;
static bool forced_off = false;
static bool output_state = false;
static unsigned long period_start_ms = 0;

void heater_init() {
    pinMode(PIN_SSR, OUTPUT);
    digitalWrite(PIN_SSR, LOW);
    duty_percent = 0;
    forced_off = false;
    output_state = false;
}

void heater_set_duty(uint8_t percent) {
    if (percent > 100) percent = 100;
    duty_percent = percent;
}

uint8_t heater_get_duty() {
    return duty_percent;
}

void heater_update() {
    // Safety override — always check first
    if (forced_off || !safety_heater_allowed()) {
        digitalWrite(PIN_SSR, LOW);
        output_state = false;
        return;
    }

    unsigned long now = millis();
    unsigned long elapsed = now - period_start_ms;

    // Start new period
    if (elapsed >= HEATER_PERIOD_MS) {
        period_start_ms = now;
        elapsed = 0;
    }

    // Burst-fire: ON for (duty_percent / 100) of the period
    unsigned long on_time = (unsigned long)duty_percent * HEATER_PERIOD_MS / 100;

    if (elapsed < on_time && duty_percent > 0) {
        digitalWrite(PIN_SSR, HIGH);
        output_state = true;
    } else {
        digitalWrite(PIN_SSR, LOW);
        output_state = false;
    }
}

void heater_force_off() {
    forced_off = true;
    duty_percent = 0;
    digitalWrite(PIN_SSR, LOW);
    output_state = false;
}

void heater_clear_forced_off() {
    // F5/E3: Only called by safety_reset() after validating all conditions are safe.
    // Does NOT re-enable the heater — just clears the latch so future commands work.
    forced_off = false;
}

bool heater_is_on() {
    return output_state;
}
