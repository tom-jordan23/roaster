#include <Arduino.h>
#include <esp_task_wdt.h>
#include "config.h"
#include "safety.h"
#include "sensors.h"
#include "heater.h"
#include "blower.h"
#include "control.h"
#include "logging.h"
#include "command.h"

static unsigned long last_sensor_poll = 0;

void setup() {
    Serial.begin(SERIAL_BAUD);
    Serial.println("# Roaster v" ROASTER_VERSION " starting");

    // E1/F2: Enable ESP32 Task Watchdog Timer.
    // If loop() stops feeding the watchdog for WDT_TIMEOUT_S seconds,
    // the ESP32 resets — which de-energizes the SSR (GPIO defaults to
    // input/low on reset), shutting off the heater.
    esp_task_wdt_init(WDT_TIMEOUT_S, true);
    esp_task_wdt_add(NULL);

    // F4: Init safety FIRST so it can enforce startup grace period.
    // Heater and blower init ensure outputs are safe (LOW/off) at GPIO level.
    // Safety starts in STARTUP state and will not allow heater until
    // SAFETY_STARTUP_GOOD_READS consecutive clean TC reads are received.
    safety_init();
    sensors_init();
    heater_init();
    blower_init();
    control_init();
    logging_init();
    command_init();

    Serial.println("# Init complete. Startup grace period active.");
    Serial.println("# Heater locked until sensors stabilize.");
    Serial.println("# Commands: HEAT <0-100>, BLOW <0-100>, STATUS, RESET, STOP");
}

void loop() {
    // E1/F2: Feed hardware watchdog every loop iteration
    esp_task_wdt_reset();

    unsigned long now = millis();

    // F6: Poll sensors every loop iteration to minimize data staleness.
    // The MAX31855 conversion time is ~100ms, so we still gate on
    // SENSOR_POLL_INTERVAL_MS to avoid hammering SPI faster than the
    // chip can convert, but safety_check() will fault if data goes stale.
    if (now - last_sensor_poll >= SENSOR_POLL_INTERVAL_MS) {
        last_sensor_poll = now;
        sensors_update();
    }

    // Safety check — ALWAYS runs, ALWAYS authoritative
    safety_check();

    // Control logic
    control_update();

    // Actuator outputs
    heater_update();
    blower_update();

    // Data logging (2 Hz)
    logging_update();

    // Serial command processing
    command_update();
}
