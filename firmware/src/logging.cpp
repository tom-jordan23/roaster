#include "logging.h"
#include "config.h"
#include "sensors.h"
#include "heater.h"
#include "blower.h"
#include "safety.h"

static unsigned long last_log_ms = 0;

void logging_init() {
    last_log_ms = 0;
}

void logging_update() {
    unsigned long now = millis();
    if (now - last_log_ms < LOG_INTERVAL_MS) return;
    last_log_ms = now;

    // Output CSV-style data line:
    // timestamp_ms, tc1, tc2, tc3, heater_pct, blower_pct, safety_state
    //
    // TODO: Replace with Artisan-compatible protocol (Modbus or serial command/response)
    // For now, continuous CSV stream for development and testing.

    Serial.print(now);
    Serial.print(',');

    for (int i = 0; i < TC_COUNT; i++) {
        float temp = sensors_get_temp(i);
        if (isnan(temp)) {
            Serial.print("NaN");
        } else {
            Serial.print(temp, 1);
        }
        Serial.print(',');
    }

    Serial.print(heater_get_duty());
    Serial.print(',');
    Serial.print(blower_get_speed());
    Serial.print(',');
    Serial.println((int)safety_get_state());
}
