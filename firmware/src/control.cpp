#include "control.h"
#include "config.h"
#include "heater.h"
#include "blower.h"
#include "safety.h"

static ControlMode mode = ControlMode::MANUAL;

void control_init() {
    mode = ControlMode::MANUAL;
}

void control_update() {
    // In manual mode, heater and blower commands are set directly
    // via control_set_heater() and control_set_blower() from the
    // command interface. Nothing to compute here.

    // Future: PID loop on TC1 for process air temperature control
    // Future: Profile follower for automated roast curves
}

void control_set_heater(uint8_t percent) {
    if (!safety_is_ok()) return;
    heater_set_duty(percent);
}

void control_set_blower(uint8_t percent) {
    blower_set_speed(percent);
}

ControlMode control_get_mode() {
    return mode;
}
