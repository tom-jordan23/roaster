#ifndef ROASTER_HEATER_H
#define ROASTER_HEATER_H

#include <Arduino.h>

// Initialize heater control GPIO — heater starts OFF
void heater_init();

// Set heater duty cycle (0-100%)
// Ignored if safety system has not cleared heater operation
void heater_set_duty(uint8_t percent);

// Get current commanded duty cycle
uint8_t heater_get_duty();

// Called every loop — manages burst-fire timing
void heater_update();

// Force heater off immediately — called by safety system
void heater_force_off();

// Clear forced_off latch — only called by safety_reset() after conditions validate (F5/E3)
void heater_clear_forced_off();

// Returns true if heater output is currently energized
bool heater_is_on();

#endif // ROASTER_HEATER_H
