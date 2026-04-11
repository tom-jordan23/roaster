#ifndef ROASTER_BLOWER_H
#define ROASTER_BLOWER_H

#include <Arduino.h>

// Initialize blower control output
void blower_init();

// Set blower speed (0-100%)
void blower_set_speed(uint8_t percent);

// Get current commanded speed
uint8_t blower_get_speed();

// Called every loop — manages blower output
void blower_update();

// Returns true if blower is running (speed > 0)
bool blower_is_running();

#endif // ROASTER_BLOWER_H
