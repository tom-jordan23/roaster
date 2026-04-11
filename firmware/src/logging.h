#ifndef ROASTER_LOGGING_H
#define ROASTER_LOGGING_H

#include <Arduino.h>

// Initialize logging subsystem
void logging_init();

// Called at LOG_INTERVAL_MS — outputs current state to serial
void logging_update();

#endif // ROASTER_LOGGING_H
