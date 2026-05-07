# TP-001: Airflow Uniformity and Fluidization Test

## Purpose

Quantify the plenum / baffle / distributor-plate behavior and verify that the
air system can fluidize a 113 g charge of green coffee. Produce data — plate
dP curve, exhaust CFM curve, fluidization onset, entrainment velocity — that
informs distributor plate iteration (mesh, drilled custom plate) and feeds the
heater control loop calibration in TP-002.

DR-013 D5 added pressure and airflow instrumentation to the BOM. This test
plan is built around that instrumentation; an earlier qualitative-only
version is superseded.

## Prerequisites

- Mechanical assembly complete (chamber, plenum, plate, exhaust path)
- Blower installed and TRIAC-controllable
- ESP32 firmware running with logging stream (TC channels + dP_plate channel)
- No heater operation required (cold test — Stage 1 specifically forbids heat)
- Procedural rule (DR-013 D2): no blower runs above ~30% duty without beans
  loaded until plate-float behavior is characterized in Test 1.1

## Equipment

| Instrument | BOM | Used for |
|------------|-----|----------|
| Differential pressure sensor | PRESS-001 (Sensirion SDP810-500Pa) | Plate dP, bed dP — logged via ESP32 |
| Pressure taps + tubing | PRESS-TAP-001 | Tap pairs through plenum and chamber walls |
| Vane anemometer | ANEMO-001 | Exhaust CFM at outlet — manual reading |
| Clamp ammeter | (existing) | Motor current cross-check vs. CT-001 |
| Tissue strips | — | Visual flow-pattern sketches as supplement to logged data |

### Tap configuration

Two reconfigurable tap pairs feed the single SDP810 via silicone tubing:

- **Plate dP:** + tap in plenum (just below distributor plate); − tap above
  plate (in lower chamber, above bed if loaded)
- **Bed dP:** + tap above plate; − tap above bed (upper chamber)

Swap tubing between configurations during the test. Document which
configuration each row reflects.

### Plate as flow meter (calibration target)

Once SDP810 is installed and ANEMO-001 anchors a CFM reading at one duty
point, the distributor plate becomes its own flow meter for subsequent runs:

    CFM ≈ k × √(dP_plate)

where k is calibrated from the anemometer-anchored point. This lets later
tests (TP-002 thermal, TP-006 first roast) run without the anemometer.

## Test Procedure

### Test 1.1 — Plate dP curve (no beans)

Plate dP swept against blower duty, with the procedural-rule cap honored.

1. Verify chamber is empty and plate is properly seated on ring.
2. Tubing in **plate dP** configuration.
3. Set blower duty to 10%; record dP_plate, motor current, qualitative plate
   behavior (floats? rattles? still?).
4. Step duty: 20%, 30%. **Stop at 30%** for any sign of plate float (lift,
   rattle, displacement). If plate floats: log the duty and dP at which it
   started; abort the rest of Test 1.1; deploy DR-013 D2 reactive
   mitigation (rivet ring lip, then re-run).
5. If plate stays put through 30% — plate-float concern is closed for the
   FengYoo / 22%-open configuration. Continue to Test 1.2 with beans loaded
   (which pin the plate) before stepping to higher duty.

**Pass criteria:** plate dP rises monotonically with duty; plate stays seated
through 30% duty cold; recorded curve will anchor flow-meter calibration in
1.4.

### Test 1.2 — Fluidization onset and window (beans loaded)

1. Load 113 g green coffee beans into chamber.
2. Tubing remains in **plate dP** configuration; switch to **bed dP** for one
   sweep at the end.
3. From 20% duty, step up in 5% increments. At each step record:
   - Blower duty (%)
   - dP_plate (Pa)
   - Motor current (A) cross-check vs. CT-001
   - Bed motion: still / shifting / lifting / fluidized / circulating / venting
   - Photo or short video at each step
4. Identify and record:
   - **U_mf duty** — duty at which beans first lift (minimum fluidization)
   - **Operating duty band** — duty range producing good circulation
   - **Entrainment duty** — duty at which beans start being carried into
     exhaust (must stay below this in operation)
5. At the well-fluidized duty, swap tubing to **bed dP** configuration; record
   bed dP. Compare to plate dP — ratio plate-dP / bed-dP indicates whether
   the plate is dominating the flow distribution (good) or being bypassed
   (channeling).

**Pass criteria:**
- Operating duty band exists (entrainment duty > U_mf duty by a comfortable
  margin)
- Bed motion at operating duty is reasonably even — no persistent dead zone
  > 25% of bed area visually
- Plate dP / bed dP ratio ≥ 0.3 (plate dominates) ideally; ratio < 0.1
  indicates probable channeling and triggers DR-013 D1 reactive Plan B
  (install MESH-001 disc on plate)

### Test 1.3 — Anemometer anchor (one-time CFM measurement)

1. At the well-fluidized duty point from Test 1.2, hold ANEMO-001 vane in
   the exhaust outlet stream.
2. Record exhaust velocity (m/s); compute CFM from outlet area.
3. Record dP_plate at the same duty point — this is the (CFM, dP_plate)
   anchor pair.
4. Repeat at one or two additional duty points to confirm the
   √(dP) relationship holds.

**Pass criteria:** measured CFM at operating duty falls in the 12–18 CFM
hot-equivalent range from architecture.md airflow budget. (Note: this is a
cold measurement; hot-air density correction applies for operation — see
architecture.md T5.)

### Test 1.4 — Plate flow-meter calibration

From the anchor pair(s) in Test 1.3, fit:

    k = CFM / √(dP_plate)

Record k in test results; this constant carries forward into TP-002 and
TP-006 so the anemometer is not needed for routine roasts.

### Test 1.5 — Blower characterization

At each blower duty (10%, 25%, 50%, 75%, 100% — empty chamber to avoid
entrainment at high duty):

1. Record motor current (A)
2. Record dP_plate (Pa)
3. Note qualitative noise level and any vibration or mechanical issue
4. Note whether the bypass-cooling exhaust stream is well-separated from
   the working air (DR-011 critical assumption)

## Data to Record

Logged via ESP32 (suggested CSV columns):
`timestamp, blower_duty_pct, motor_current_A, dP_plate_Pa, dP_bed_Pa,
TC1_C, TC2_C, TC3_C, notes`

Manual log (for entries that don't fit the stream):

| Test | Duty % | dP_plate (Pa) | dP_bed (Pa) | Anemo CFM | Bed motion | Plate float? | Notes |
|------|--------|---------------|-------------|-----------|------------|--------------|-------|
| 1.1  |        |               | n/a         | n/a       | n/a        |              |       |
| 1.2  |        |               |             |           |            |              |       |
| 1.3  |        |               |             |           |            | n/a          |       |
| 1.5  |        |               | n/a         | n/a       | n/a        |              |       |

## Failure Response

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Plate dP rises but bed dP stays ~0 | Channeling — air bypassing bed evenly | Install MESH-001 (DR-013 D1 Plan B); re-run 1.2 |
| Plate dP stays low across all duty | 22% open area too high for our airflow | Install MESH-001; re-run 1.1–1.3 |
| Plate floats at low duty | DR-013 D2 condition; FengYoo geometry assumed safe but didn't pan out | Rivet small SS lip to underside of clamp ring (D2 reactive); re-run 1.1 |
| No operating duty band (entrainment ≈ U_mf) | Chamber L/D too high (T3) — Geldart D slugging | Switch to other chamber size (DR-001 dual-chamber test) |
| Persistent dead zone > 25% of bed | Baffle / inlet jet not redirecting properly | Inspect DR-009 ramp; consider T2 second perforated baffle |
| Plate dP / bed dP < 0.1 with FengYoo + MESH-001 (60-mesh+) | Even mesh insufficient | Build DIY-drilled custom plate at 4% open area (DR-013 D1 Plan C) |

## Traceability

- Design: `docs/system/architecture.md` (airflow budget T1, T3, T5),
  `docs/system/design-log.md` DR-013 (this test's instrumentation source),
  DR-008 (plate-float math), DR-009 (deflector ramp), DR-011 (motor),
  DR-012 (round plenum)
- BOM: PLATE-001A/B, MESH-001, PRESS-001, PRESS-TAP-001, ANEMO-001, BLW-001
- Downstream: TP-002 thermal (uses k flow-meter constant from Test 1.4),
  TP-006 first roast (operates inside the duty band identified here)
