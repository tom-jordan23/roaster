#include <unity.h>
#include "safety.h"
#include "heater.h"
#include "sensors.h"
#include "blower.h"

// Note: These tests run on the ESP32 target via PlatformIO.
// Sensor readings come from real hardware — for unit testing of safety logic
// in isolation, a mock sensor layer is needed (future work, see TP-004).

void test_initial_state_is_startup() {
    // F4: Safety starts in STARTUP state, not OK
    safety_init();
    TEST_ASSERT_EQUAL(SafetyState::STARTUP, safety_get_state());
    TEST_ASSERT_FALSE(safety_is_ok());
    TEST_ASSERT_FALSE(safety_heater_allowed());
    TEST_ASSERT_FALSE(safety_startup_complete());
}

void test_fault_disables_heater() {
    safety_init();
    safety_trigger_fault(SafetyState::FAULT_OVERTEMP);
    TEST_ASSERT_FALSE(safety_is_ok());
    TEST_ASSERT_FALSE(safety_heater_allowed());
}

void test_fault_trigger_sets_correct_state() {
    safety_init();

    safety_trigger_fault(SafetyState::FAULT_TC);
    TEST_ASSERT_EQUAL(SafetyState::FAULT_TC, safety_get_state());

    safety_init();
    safety_trigger_fault(SafetyState::FAULT_AIRFLOW);
    TEST_ASSERT_EQUAL(SafetyState::FAULT_AIRFLOW, safety_get_state());

    safety_init();
    safety_trigger_fault(SafetyState::FAULT_RATE);
    TEST_ASSERT_EQUAL(SafetyState::FAULT_RATE, safety_get_state());
}

void test_reset_fails_without_valid_conditions() {
    // F8/E2: safety_reset() should fail when conditions are not validated.
    // With no sensor hardware connected, TCs will be faulted, so reset
    // should return false.
    safety_init();
    safety_trigger_fault(SafetyState::FAULT_TC);
    TEST_ASSERT_FALSE(safety_reset());
    TEST_ASSERT_FALSE(safety_is_ok());
}

void test_heater_not_allowed_during_startup() {
    // F4: Heater must not be allowed during startup grace period
    safety_init();
    TEST_ASSERT_FALSE(safety_heater_allowed());
    TEST_ASSERT_EQUAL(SafetyState::STARTUP, safety_get_state());
}

void setup() {
    // Initialize subsystems needed by safety
    sensors_init();
    heater_init();
    blower_init();

    UNITY_BEGIN();
    RUN_TEST(test_initial_state_is_startup);
    RUN_TEST(test_fault_disables_heater);
    RUN_TEST(test_fault_trigger_sets_correct_state);
    RUN_TEST(test_reset_fails_without_valid_conditions);
    RUN_TEST(test_heater_not_allowed_during_startup);
    UNITY_END();
}

void loop() {}
