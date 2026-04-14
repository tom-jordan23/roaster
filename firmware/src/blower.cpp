#include "blower.h"
#include "config.h"

static uint8_t speed_percent = 0;

void blower_init() {
    // E11: Use explicit LEDC configuration for 25 kHz PWM.
    // analogWrite() on ESP32 defaults to ~1 kHz which is audible and
    // suboptimal for brushless DC motor control.
    ledcSetup(BLOWER_PWM_CHANNEL, BLOWER_PWM_FREQ, BLOWER_PWM_RESOLUTION);
    ledcAttachPin(PIN_BLOWER, BLOWER_PWM_CHANNEL);
    ledcWrite(BLOWER_PWM_CHANNEL, 0);
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
    uint8_t pwm_val = map(speed_percent, 0, 100, 0, 255);
    ledcWrite(BLOWER_PWM_CHANNEL, pwm_val);
}

bool blower_is_running() {
    return speed_percent > 0;
}
