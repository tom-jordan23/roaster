#include <Arduino.h>
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

    // Initialize all subsystems
    sensors_init();
    heater_init();
    blower_init();
    control_init();
    logging_init();
    command_init();

    // Safety init last — it verifies starting conditions
    safety_init();

    Serial.println("# Init complete. Manual mode active.");
    Serial.println("# Commands: HEAT <0-100>, BLOW <0-100>, STATUS, RESET, STOP");
}

void loop() {
    unsigned long now = millis();

    // Sensor polling (4 Hz)
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
