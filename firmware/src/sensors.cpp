#include "sensors.h"
#include "config.h"
#include <Adafruit_MAX31855.h>

static Adafruit_MAX31855 tc1(PIN_SPI_CLK, PIN_TC1_CS, PIN_SPI_MISO);
static Adafruit_MAX31855 tc2(PIN_SPI_CLK, PIN_TC2_CS, PIN_SPI_MISO);
static Adafruit_MAX31855 tc3(PIN_SPI_CLK, PIN_TC3_CS, PIN_SPI_MISO);

static Adafruit_MAX31855* tc_array[TC_COUNT] = { &tc1, &tc2, &tc3 };

static float temps[TC_COUNT] = { NAN, NAN, NAN };
static float cold_junctions[TC_COUNT] = { NAN, NAN, NAN };
static bool faults[TC_COUNT] = { true, true, true }; // Faulted until first good read

void sensors_init() {
    for (int i = 0; i < TC_COUNT; i++) {
        tc_array[i]->begin();
    }
}

void sensors_update() {
    for (int i = 0; i < TC_COUNT; i++) {
        double reading = tc_array[i]->readCelsius();
        if (isnan(reading)) {
            faults[i] = true;
        } else {
            temps[i] = (float)reading;
            cold_junctions[i] = (float)tc_array[i]->readInternal();
            faults[i] = false;
        }
    }
}

float sensors_get_temp(uint8_t index) {
    if (index >= TC_COUNT) return NAN;
    return faults[index] ? NAN : temps[index];
}

float sensors_get_cold_junction(uint8_t index) {
    if (index >= TC_COUNT) return NAN;
    return cold_junctions[index];
}

bool sensors_has_fault(uint8_t index) {
    if (index >= TC_COUNT) return true;
    return faults[index];
}
