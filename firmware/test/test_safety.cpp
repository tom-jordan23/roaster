#include <unity.h>
#include "safety.h"

void test_initial_state_is_ok() {
    safety_init();
    TEST_ASSERT_EQUAL(SafetyState::OK, safety_get_state());
    TEST_ASSERT_TRUE(safety_is_ok());
    TEST_ASSERT_TRUE(safety_heater_allowed());
}

void test_fault_disables_heater() {
    safety_init();
    safety_trigger_fault(SafetyState::FAULT_OVERTEMP);
    TEST_ASSERT_FALSE(safety_is_ok());
    TEST_ASSERT_FALSE(safety_heater_allowed());
}

void test_reset_clears_fault() {
    safety_init();
    safety_trigger_fault(SafetyState::FAULT_TC);
    TEST_ASSERT_FALSE(safety_is_ok());
    safety_reset();
    TEST_ASSERT_TRUE(safety_is_ok());
}

void setup() {
    UNITY_BEGIN();
    RUN_TEST(test_initial_state_is_ok);
    RUN_TEST(test_fault_disables_heater);
    RUN_TEST(test_reset_clears_fault);
    UNITY_END();
}

void loop() {}
