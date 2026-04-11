# TP-001: Airflow Uniformity and Fluidization Test

## Purpose
Verify that the plenum, baffles, and distributor plate produce reasonably uniform
upward airflow capable of fluidizing a 113g charge of green coffee beans.

## Prerequisites
- Mechanical assembly complete (chamber, plenum, plate, exhaust path)
- Blower installed and controllable
- No heater operation required (cold test)

## Equipment
- Blower with speed control
- Tissue paper strips or lightweight streamers
- Optional: anemometer or pitot tube for velocity spot-checks
- Ammeter (clamp or inline) for blower current

## Test Procedure

### Test 1.1: Distributor Plate Uniformity (No Beans)
1. Set blower to 50% speed
2. Hold tissue strips at multiple points across the plate surface (center, edges, quadrants)
3. Record qualitative airflow at each point: strong / moderate / weak / dead
4. Repeat at 30%, 70%, 100% blower speed
5. Photograph or sketch the flow pattern

**Pass criteria:** No dead zones larger than ~20% of plate area. No single-point
jetting that dominates the flow field.

### Test 1.2: Fluidization with Beans
1. Load 113g green coffee beans into the chamber
2. Starting at 30% blower speed, slowly increase speed
3. Record the speed at which beans begin to move (minimum fluidization)
4. Record the speed at which the full bed is well-fluidized (good circulation)
5. Record the speed at which beans begin to blow out of the chamber (entrainment)
6. Note: Are beans circulating evenly, or channeling/dead-zoning?

**Pass criteria:** A usable operating window exists between onset of fluidization
and entrainment. Bed motion is reasonably even (no persistent dead zone > 25% of bed).

### Test 1.3: Blower Characterization
1. At each speed setting (0%, 25%, 50%, 75%, 100%), record:
   - Blower current draw (amps)
   - Qualitative noise level
   - Any vibration or mechanical issues

## Data to Record

| Test | Blower % | Observation | Current (A) | Notes |
|------|----------|-------------|-------------|-------|
| 1.1  |          |             |             |       |
| 1.2  |          |             |             |       |
| 1.3  |          |             |             |       |

## Failure Response
- If dead zones are severe: redesign baffle geometry or plate hole pattern
- If fluidization window is too narrow: consider chamber diameter change
- If blower is insufficient: evaluate alternative blower

## Traceability
- Design: `docs/mechanical/plenum.md`, `docs/mechanical/distributor-plate.md`
- System: `docs/system/architecture.md` (airflow budget)
