#ifndef ROASTER_CONTROL_H
#define ROASTER_CONTROL_H

#include <Arduino.h>

// Control modes
enum class ControlMode {
    MANUAL,     // Operator sets heater % and blower % directly
    // Future modes:
    // PID_PROCESS_AIR,  // Closed-loop on TC1
    // PROFILE,          // Follow a time-temperature profile
};

// Initialize control layer
void control_init();

// Process one control cycle — called every loop
void control_update();

// Manual mode commands
void control_set_heater(uint8_t percent);
void control_set_blower(uint8_t percent);

// Query
ControlMode control_get_mode();

#endif // ROASTER_CONTROL_H
