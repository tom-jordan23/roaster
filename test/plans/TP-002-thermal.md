# TP-002: Thermal Characterization Test

## Purpose
Characterize heater response, thermal lag, steady-state temperatures, and overall
thermal performance of the air heating system.

## Prerequisites
- TP-001 passed (airflow verified)
- Heater installed and wired through SSR
- All three thermocouples installed and reading
- ESP32 firmware running with sensor acquisition and serial logging
- Safety over-temp shutdown verified (can be tested as part of this procedure)

## Equipment
- Full roaster assembly (no beans for most tests)
- Serial terminal or Artisan connected for data logging
- Stopwatch (or rely on firmware timestamps)
- IR thermometer (optional, for spot-checking external surface temps)
- Fire extinguisher (mandatory)

## Test Procedure

### Test 2.1: Heater Step Response (No Beans)
1. Set blower to the nominal fluidization speed from TP-001
2. Allow system to reach ambient steady state (~2 min with blower running)
3. Record baseline TC1, TC2, TC3
4. Step heater to 50% duty
5. Log TC1, TC2, TC3 every second until TC1 stabilizes (< 1°C change over 30 sec)
6. Record steady-state temps and time to reach them
7. Step heater to 0%. Log cool-down until TC1 returns within 10°C of ambient
8. Repeat steps 4-7 at 75% and 100% duty

**Key metrics:** Time constant (63% of final ΔT), steady-state TC1 at each duty,
TC2-to-TC1 ratio, TC3-to-TC1 ratio, cool-down time.

### Test 2.2: Thermal Sweep
1. Blower at nominal speed
2. Step heater through 0%, 20%, 40%, 60%, 80%, 100% in 2-minute holds
3. Record steady-state (or near-steady) TC1, TC2, TC3 at each point

**Purpose:** Map the heater duty to process air temperature curve. This is the
primary characterization data for future PID tuning.

### Test 2.3: Safety Shutdown Verification
1. Set heater to 100%, blower to nominal
2. Monitor TC1 as it climbs
3. Verify that the firmware safety layer triggers heater-off when TC1 exceeds
   `SAFETY_MAX_PROCESS_TEMP_C` (280°C default)
4. Verify the system enters fault state and heater remains off
5. Verify that RESET command clears the fault only after temps drop

**Pass criteria:** Safety shutdown fires within 2 seconds of threshold crossing.
Heater is provably off (SSR de-energized, TC1 begins dropping).

### Test 2.4: External Temperature Check
1. After 10 minutes at 80% heater duty, use IR thermometer to check:
   - Heater can exterior
   - Plenum exterior
   - Chamber exterior
   - Any wiring or connector near heat sources
2. Record temperatures

**Pass criteria:** No external surface exceeds 60°C where an operator might touch.
Wiring insulation temps are within rated range.

## Data to Record

| Test | Heater % | Blower % | TC1 (°C) | TC2 (°C) | TC3 (°C) | Time (s) | Notes |
|------|----------|----------|----------|----------|----------|----------|-------|
|      |          |          |          |          |          |          |       |

## Failure Response
- If steady-state TC1 is too low at 100%: heater undersized or too much heat loss; evaluate insulation
- If time constants are very long (> 60s to 63%): heater-to-air coupling is poor; review heater can geometry
- If safety shutdown doesn't trigger: STOP testing, debug firmware immediately
- If external temps are excessive: add insulation or heat shielding before proceeding

## Traceability
- Design: `docs/electrical/heater-circuit.md`, `docs/system/architecture.md`
- Safety: `docs/software/safety-logic.md`
