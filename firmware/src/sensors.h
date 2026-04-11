#ifndef ROASTER_SENSORS_H
#define ROASTER_SENSORS_H

#include <Arduino.h>

// Initialize SPI bus and MAX31855 instances
void sensors_init();

// Poll all thermocouples — call at SENSOR_POLL_INTERVAL_MS
void sensors_update();

// Get latest temperature reading for a TC (0=TC1, 1=TC2, 2=TC3)
// Returns NAN if sensor is in fault
float sensors_get_temp(uint8_t index);

// Get cold-junction (reference) temperature
float sensors_get_cold_junction(uint8_t index);

// Check if a TC has a fault condition (open, short, read error)
bool sensors_has_fault(uint8_t index);

#endif // ROASTER_SENSORS_H
