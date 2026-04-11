# TP-004: Firmware Unit Test Plan

## Purpose
Verify correctness of firmware modules through automated unit tests and
targeted manual bench tests on real hardware.

## Prerequisites
- PlatformIO installed
- ESP32 dev board available (for on-hardware tests)
- Firmware compiles clean (`pio run`)

## Automated Unit Tests

Run with: `pio test` (from `firmware/` directory)

### Safety Module (`test/test_safety.cpp`)
- [ ] Initial state is OK after `safety_init()`
- [ ] `safety_trigger_fault()` transitions to fault state
- [ ] Fault state reports `safety_heater_allowed() == false`
- [ ] `safety_reset()` clears fault when conditions are met
- [ ] Multiple fault types are tracked correctly
- [ ] Over-temp check triggers at threshold
- [ ] TC fault detection triggers safety fault

### Sensor Module (planned: `test/test_sensors.cpp`)
- [ ] Valid reading produces correct temperature
- [ ] NaN reading sets fault flag
- [ ] Fault flag clears on next good reading
- [ ] All three TC channels independent

### Heater Module (planned: `test/test_heater.cpp`)
- [ ] Duty 0% produces no output
- [ ] Duty 100% produces continuous output
- [ ] Duty 50% produces correct on/off ratio within period
- [ ] `heater_force_off()` immediately stops output regardless of duty
- [ ] Safety override prevents output when not allowed

### Command Module (planned: `test/test_control.cpp`)
- [ ] HEAT command sets duty correctly
- [ ] BLOW command sets speed correctly
- [ ] STATUS returns well-formed data line
- [ ] RESET command calls safety reset
- [ ] STOP command forces everything off
- [ ] Malformed commands return ERR without crashing
- [ ] Buffer overflow on long input is handled

## Manual Bench Tests (on hardware)

### Bench 4.1: Serial Communication
1. Flash firmware to ESP32
2. Open serial terminal at 115200 baud
3. Verify startup messages appear
4. Send each command and verify response format
5. Send malformed commands and verify ERR responses

### Bench 4.2: Sensor Read (requires TC amplifier boards wired)
1. With TCs at room temp, verify all three read ~20-25°C
2. Hold TC1 in warm water, verify reading increases
3. Disconnect a TC, verify fault detection

### Bench 4.3: SSR Output (requires SSR wired, NO heater element)
1. Set HEAT to 50%
2. Measure SSR output with multimeter or LED indicator
3. Verify ~500ms on / ~500ms off cycle
4. Set HEAT to 0%, verify SSR stays off
5. Set HEAT to 100%, verify SSR stays on

## Data to Record

| Test | Result | Notes |
|------|--------|-------|
| Automated test suite | PASS / FAIL (attach log) | |
| Bench 4.1 | | |
| Bench 4.2 | | |
| Bench 4.3 | | |

## Traceability
- Code: `firmware/src/`, `firmware/test/`
- Architecture: `docs/software/firmware-architecture.md`
