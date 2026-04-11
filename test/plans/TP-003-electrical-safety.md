# TP-003: Electrical Safety Test

## Purpose
Verify that the electrical system meets basic safety requirements before applying
power to the complete roaster assembly.

## Prerequisites
- All electrical wiring complete
- System NOT powered for initial checks

## Equipment
- Multimeter (resistance and continuity mode)
- Megger / insulation resistance tester (preferred) or multimeter on high-ohm range
- Clamp ammeter
- Ground-bond tester or low-resistance ohmmeter

## Test Procedure

### Test 3.1: Ground Continuity
1. Disconnect from mains
2. Measure resistance between mains earth pin and each metal chassis component:
   - Chamber body
   - Plenum body
   - Heater can body
   - Any metal enclosure panels
3. Record all readings

**Pass criteria:** All readings < 0.1 ohm

### Test 3.2: Mains-to-Low-Voltage Isolation
1. Disconnect from mains
2. Disconnect ESP32 board from circuit (to protect it)
3. Measure resistance between:
   - Mains L to any low-voltage conductor (ESP32 side)
   - Mains N to any low-voltage conductor
   - Mains L to chassis ground (should be open, not shorted)
   - Mains N to chassis ground (should be open, not shorted)
4. If megger available: test at 500V DC

**Pass criteria:** > 1 Mohm between mains and low-voltage. No shorts between L/N and ground.

### Test 3.3: Strain Relief and Mechanical Integrity
1. Inspect all cord entries for proper strain relief
2. Apply moderate tug test (~10 lb pull) to mains cord
3. Verify no terminal pulled loose
4. Inspect all wire terminations for exposed conductor, cold joints, or loose screws
5. Verify mains wire gauge is adequate for current (14 AWG minimum for 15A)

**Pass criteria:** All connections remain secure. No exposed conductors. Wire gauge correct.

### Test 3.4: First Power-On (Smoke Test)
1. Reconnect all boards
2. Verify hard disconnect is OFF
3. Plug into mains outlet (with GFCI if available)
4. Turn on hard disconnect
5. Verify ESP32 boots (serial output visible)
6. Verify no smoke, unusual smells, or sparks
7. Measure mains current draw with no heater/blower active (should be < 0.5A — PSU only)
8. Command blower to 50% — verify operation and measure current
9. Command heater to 10% for 5 seconds — verify SSR clicks and measure current
10. STOP command — verify everything shuts down

**Pass criteria:** No smoke, no sparks, currents within expected ranges, ESP32
responsive, STOP works immediately.

### Test 3.5: SSR Failure Mode Check
1. Command heater to 50%
2. Pull SSR control signal (disconnect GPIO wire to SSR gate)
3. Verify heater de-energizes immediately (SSR should default off without gate signal)
4. Reconnect and verify normal operation resumes

**Pass criteria:** SSR defaults to OFF when control signal is removed.

## Data to Record

| Test | Measurement | Value | Pass/Fail | Notes |
|------|-------------|-------|-----------|-------|
|      |             |       |           |       |

## Failure Response
- Ground continuity failure: DO NOT proceed. Fix grounding before any further testing
- Isolation failure: DO NOT proceed. Find and fix the short/leakage path
- Smoke test failure: Disconnect immediately. Diagnose root cause before retry

## Traceability
- Design: `docs/electrical/power-distribution.md`, `docs/electrical/safety-interlocks.md`
