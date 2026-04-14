#include "command.h"
#include "config.h"
#include "control.h"
#include "heater.h"
#include "blower.h"
#include "safety.h"
#include "sensors.h"

static char cmd_buffer[64];
static uint8_t cmd_pos = 0;

void command_init() {
    cmd_pos = 0;
    memset(cmd_buffer, 0, sizeof(cmd_buffer));
}

static void process_command(const char* cmd) {
    // HEAT <percent>
    if (strncmp(cmd, "HEAT ", 5) == 0) {
        int val = atoi(cmd + 5);
        if (val < 0 || val > 100) {
            Serial.println("ERR HEAT value must be 0-100");
            return;
        }
        control_set_heater((uint8_t)val);
        Serial.print("OK HEAT ");
        Serial.println(val);
        return;
    }

    // BLOW <percent>
    if (strncmp(cmd, "BLOW ", 5) == 0) {
        int val = atoi(cmd + 5);
        if (val < 0 || val > 100) {
            Serial.println("ERR BLOW value must be 0-100");
            return;
        }
        control_set_blower((uint8_t)val);
        Serial.print("OK BLOW ");
        Serial.println(val);
        return;
    }

    // STATUS
    if (strcmp(cmd, "STATUS") == 0) {
        Serial.print("DATA ");
        Serial.print(millis());
        for (int i = 0; i < TC_COUNT; i++) {
            Serial.print(',');
            float t = sensors_get_temp(i);
            if (isnan(t)) Serial.print("NaN");
            else Serial.print(t, 1);
        }
        Serial.print(',');
        Serial.print(heater_get_duty());
        Serial.print(',');
        Serial.print(blower_get_speed());
        Serial.print(',');
        Serial.println((int)safety_get_state());
        return;
    }

    // RESET
    if (strcmp(cmd, "RESET") == 0) {
        if (safety_reset()) {
            Serial.println("OK RESET");
        } else {
            Serial.println("ERR RESET conditions not clear");
        }
        return;
    }

    // STOP
    if (strcmp(cmd, "STOP") == 0) {
        heater_force_off();
        blower_set_speed(0);
        Serial.println("OK STOP");
        return;
    }

    Serial.print("ERR unknown command: ");
    Serial.println(cmd);
}

void command_update() {
    while (Serial.available()) {
        char c = Serial.read();
        if (c == '\n' || c == '\r') {
            if (cmd_pos > 0) {
                cmd_buffer[cmd_pos] = '\0';
                process_command(cmd_buffer);
                cmd_pos = 0;
            }
        } else if (cmd_pos < sizeof(cmd_buffer) - 1) {
            cmd_buffer[cmd_pos++] = c;
        }
        // F9: Characters beyond buffer capacity are silently discarded.
        // No overflow possible — cmd_pos is bounded by sizeof(cmd_buffer) - 1.
    }
}
