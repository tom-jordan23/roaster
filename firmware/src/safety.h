#ifndef ROASTER_SAFETY_H
#define ROASTER_SAFETY_H

#include <Arduino.h>

// Safety system states
enum class SafetyState {
    OK,             // No faults, normal operation allowed
    FAULT_OVERTEMP, // Over-temperature detected
    FAULT_TC,       // Thermocouple fault (open/short/timeout)
    FAULT_AIRFLOW,  // Airflow loss detected
    FAULT_GENERAL   // Catch-all fault
};

// Initialize safety system — must be called before any actuator use
void safety_init();

// Called every loop iteration — checks all safety conditions
// Returns current safety state
SafetyState safety_check();

// Force the system into fault state (callable from any module)
void safety_trigger_fault(SafetyState fault);

// Reset fault state — requires operator action
// Returns true if reset was successful (conditions must be clear)
bool safety_reset();

// Query current state
SafetyState safety_get_state();
bool safety_is_ok();

// Returns true if heater is allowed to operate
bool safety_heater_allowed();

#endif // ROASTER_SAFETY_H
