# TP-005: Full System Integration Test

## Purpose
Verify that all subsystems work together as an integrated system before
attempting a real roast. This is a hot test with beans but not a roast —
the goal is system verification, not coffee production.

## Prerequisites
- TP-001 passed (airflow verified)
- TP-002 passed (thermal behavior characterized)
- TP-003 passed (electrical safety verified)
- TP-004 passed (firmware unit tests passing)
- All mechanical, electrical, and firmware subsystems assembled and individually tested
- Artisan connected and receiving data (or serial logging confirmed)

## Equipment
- Complete roaster assembly
- 113g green coffee beans
- Serial terminal or Artisan on host PC
- Fire extinguisher (mandatory)
- Timer

## Test Procedure

### Test 5.1: Cold Start Sequence
1. System powered off. Verify hard disconnect is OFF
2. Turn on hard disconnect
3. Verify ESP32 boots and reports ready state on serial
4. Verify all three TCs reading ambient (~20-25°C)
5. Verify safety state is OK
6. Command BLOW 50 — verify blower starts
7. Command STATUS — verify all fields populated and sensible

**Pass:** System boots clean, all sensors read, blower responds, serial interface works.

### Test 5.2: Fluidization Verification
1. Load 113g green coffee beans
2. Command blower to fluidization speed (from TP-001 results)
3. Verify beans are fluidizing (visual check)
4. Verify TC2 (bean bed) is reading and responding to bean motion
5. Run for 2 minutes, monitor for mechanical issues

**Pass:** Beans fluidize reliably. TC2 reads a stable value. No rattling, vibration, or bean ejection.

### Test 5.3: Heated Run with Beans
1. Beans still loaded, blower at fluidization speed
2. Command HEAT 30 — monitor TC1 rise
3. At TC1 steady state, command HEAT 50
4. Monitor TC1, TC2, TC3 for 5 minutes
5. Verify: TC1 > TC2 > TC3 makes physical sense (may vary — document actual behavior)
6. Verify Artisan (or serial log) is recording all data
7. Command HEAT 0 — monitor cool-down
8. Verify cool-down curves are smooth and physically sensible

**Pass:** All three TCs respond in a physically coherent way. Data stream is
continuous with no dropouts. Heater control is responsive.

### Test 5.4: Safety Shutdown Test (Under Load)
1. With beans, blower running, heater at 50%:
2. Temporarily lower `SAFETY_MAX_PROCESS_TEMP_C` in firmware to a value just
   above current TC1 reading (or wait for TC1 to approach threshold)
3. Verify safety system triggers and heater shuts off
4. Verify serial reports fault state
5. Verify heater commands are rejected while in fault
6. Command RESET after temps drop
7. Verify normal operation resumes

**Pass:** Safety shutdown is fast and reliable under real operating conditions.

### Test 5.5: Emergency Stop
1. System running hot with beans
2. Command STOP
3. Verify heater off AND blower off immediately
4. Time how long until chamber is safe to handle

**Pass:** STOP is immediate and complete.

### Test 5.6: Sustained Run (Soak Test)
1. Fresh start with beans
2. Run at moderate heater duty (40-60%) for 15 minutes continuous
3. Monitor for:
   - Temperature drift or oscillation
   - Mechanical vibration developing
   - Unusual smells (not coffee-related)
   - Wire or connector heating
   - Data stream dropouts
4. After 15 minutes, cool down and inspect

**Pass:** System runs stable for the full duration. No anomalies.

## Data to Record

Log the full data stream (Artisan or serial CSV) for every test.

| Test | Duration | Observations | Pass/Fail | Notes |
|------|----------|-------------|-----------|-------|
| 5.1  |          |             |           |       |
| 5.2  |          |             |           |       |
| 5.3  |          |             |           |       |
| 5.4  |          |             |           |       |
| 5.5  |          |             |           |       |
| 5.6  |          |             |           |       |

## Failure Response
- Any safety failure: STOP, diagnose, do not proceed to TP-006
- Data dropouts: check serial connection, firmware timing, buffer overflows
- Thermal anomalies: check insulation, heater coupling, TC placement
- Mechanical issues: inspect fasteners, alignment, vibration sources

## Traceability
- All prior test plans: TP-001 through TP-004
- System design: `docs/system/block-diagram.md`
