#ifndef ROASTER_CONFIG_H
#define ROASTER_CONFIG_H

// =============================================================
// Pin Assignments
// IMPORTANT: Update these when electrical schematic is finalized
// =============================================================

// SPI bus (shared by all MAX31855 boards)
#define PIN_SPI_CLK   18
#define PIN_SPI_MISO  19
// MOSI not used by MAX31855 (read-only)

// MAX31855 chip select lines
#define PIN_TC1_CS    5     // TC1: Process air (post-heater, pre-plenum)
#define PIN_TC2_CS    16    // TC2: Bean bed (lower chamber)
#define PIN_TC3_CS    17    // TC3: Exhaust

// Heater SSR control
#define PIN_SSR       22    // Zero-cross SSR gate (active high)

// Blower control
#define PIN_BLOWER    23    // PWM output → MOSFET gate → 12V blower (DR-003)

// =============================================================
// Safety Thresholds
// =============================================================

#define SAFETY_MAX_PROCESS_TEMP_C   280.0f  // TC1 over-temp shutdown
#define SAFETY_MAX_EXHAUST_TEMP_C   250.0f  // TC3 over-temp shutdown
#define SAFETY_TC_FAULT_TIMEOUT_MS  2000    // Max time with bad TC reading before fault

// =============================================================
// Control Parameters
// =============================================================

#define HEATER_PERIOD_MS        1000    // Burst-fire cycle period (1 second)
#define SENSOR_POLL_INTERVAL_MS 250     // 4 Hz sensor polling (report at 2 Hz)
#define LOG_INTERVAL_MS         500     // 2 Hz data output to serial
#define SERIAL_BAUD             115200

// =============================================================
// Cooling Cycle (DR-005)
// =============================================================

#define COOL_TARGET_TEMP_C      50.0f   // TC2 threshold to signal "beans cool"
#define COOL_BLOWER_PERCENT     100     // Blower duty during cooling

// =============================================================
// Thermocouple Count
// =============================================================

#define TC_COUNT 3

#endif // ROASTER_CONFIG_H
