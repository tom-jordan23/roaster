#include "blower.h"
#include "config.h"

static uint8_t speed_percent = 0;

void blower_init() {
    pinMode(PIN_BLOWER, OUTPUT);
    analogWrite(PIN_BLOWER, 0);
    speed_percent = 0;
}

void blower_set_speed(uint8_t percent) {
    if (percent > 100) percent = 100;
    speed_percent = percent;
}

uint8_t blower_get_speed() {
    return speed_percent;
}

void blower_update() {
    // Map 0-100% to 0-255 PWM duty
    // TODO: This is a placeholder — actual blower control depends on motor type:
    //   - DC brushless: PWM to ESC or motor driver
    //   - AC universal: TRIAC phase-angle control (needs zero-cross detection)
    //   - AC PSC: may not be speed-controllable, use damper instead
    // Revisit when blower is selected.
    uint8_t pwm_val = map(speed_percent, 0, 100, 0, 255);
    analogWrite(PIN_BLOWER, pwm_val);
}

bool blower_is_running() {
    return speed_percent > 0;
}
