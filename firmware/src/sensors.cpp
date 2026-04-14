#include "sensors.h"
#include "config.h"
#include <Adafruit_MAX31855.h>

static Adafruit_MAX31855 tc1(PIN_SPI_CLK, PIN_TC1_CS, PIN_SPI_MISO);
static Adafruit_MAX31855 tc2(PIN_SPI_CLK, PIN_TC2_CS, PIN_SPI_MISO);
static Adafruit_MAX31855 tc3(PIN_SPI_CLK, PIN_TC3_CS, PIN_SPI_MISO);

static Adafruit_MAX31855* tc_array[TC_COUNT] = { &tc1, &tc2, &tc3 };

static float temps[TC_COUNT] = { NAN, NAN, NAN };
static float cold_junctions[TC_COUNT] = { NAN, NAN, NAN };
static uint8_t consecutive_faults[TC_COUNT] = { SAFETY_CONSEC_FAULTS_TRIP,
                                                 SAFETY_CONSEC_FAULTS_TRIP,
                                                 SAFETY_CONSEC_FAULTS_TRIP };
static unsigned long last_update_ms = 0;

void sensors_init() {
    for (int i = 0; i < TC_COUNT; i++) {
        tc_array[i]->begin();
    }
    last_update_ms = millis();
}

void sensors_update() {
    for (int i = 0; i < TC_COUNT; i++) {
        double reading = tc_array[i]->readCelsius();
        if (isnan(reading)) {
            // E13: Increment consecutive fault counter, but only declare
            // fault after SAFETY_CONSEC_FAULTS_TRIP consecutive bad reads.
            // This prevents single SPI glitches (common near 1500W burst-fire
            // switching) from tripping a fault.
            if (consecutive_faults[i] < SAFETY_CONSEC_FAULTS_TRIP) {
                consecutive_faults[i]++;
            }
        } else {
            temps[i] = (float)reading;
            cold_junctions[i] = (float)tc_array[i]->readInternal();
            consecutive_faults[i] = 0;
        }
    }
    last_update_ms = millis();
}

float sensors_get_temp(uint8_t index) {
    if (index >= TC_COUNT) return NAN;
    return sensors_has_fault(index) ? NAN : temps[index];
}

float sensors_get_cold_junction(uint8_t index) {
    if (index >= TC_COUNT) return NAN;
    return cold_junctions[index];
}

bool sensors_has_fault(uint8_t index) {
    if (index >= TC_COUNT) return true;
    return consecutive_faults[index] >= SAFETY_CONSEC_FAULTS_TRIP;
}

unsigned long sensors_get_age_ms() {
    return millis() - last_update_ms;
}
