# System Architecture and Power/Airflow Budget

## Purpose

This document captures the foundational engineering calculations that constrain
component selection across all disciplines. The three critical numbers —
**heater wattage**, **airflow rate**, and **blower static pressure** — must be
established before detailed subsystem design can proceed.

These are first-pass estimates for a 1/4 lb (113g) green coffee batch on 120V AC.

---

## 1. Heater Power Budget

### Approach

Estimate the power needed to heat a stream of air from ambient to roast-process
temperature at the required airflow rate.

### Knowns and Assumptions

| Parameter | Value | Source |
|-----------|-------|--------|
| Batch size | 113 g green coffee | Design decision |
| Target process air temp (TC1) | 200–250°C | Typical fluid-bed roast range |
| Ambient air temp | 20°C | Assumed room temp |
| Required ΔT | 180–230°C | Process air minus ambient |
| Available mains | 120V / 15A circuit | US residential standard |
| Max continuous draw | ~1440W at 12A | Leave headroom on 15A breaker |

### Thermal Calculation

Power to heat air:

    P = ṁ × Cp × ΔT

Where:
- ṁ = mass flow rate of air (kg/s)
- Cp = specific heat of air ≈ 1005 J/(kg·°C)
- ΔT = temperature rise (°C)

For a target airflow of ~35 CFM (see Section 2 below):

    35 CFM ≈ 0.0165 m³/s
    ρ_air at 20°C ≈ 1.2 kg/m³
    ṁ ≈ 0.0165 × 1.2 = 0.0198 kg/s

Power for ΔT = 200°C:

    P = 0.0198 × 1005 × 200 ≈ 3980 W

Power for ΔT = 180°C:

    P = 0.0198 × 1005 × 180 ≈ 3580 W

### Problem: 120V Constraint

At 120V / 15A, we have at most ~1500W available (with blower and controls overhead,
realistically ~1200-1400W for the heater).

This means we **cannot** heat 35 CFM of air to 250°C. We must either:

1. **Reduce airflow** — use the minimum airflow needed for fluidization
2. **Accept lower process air temps** — rely on longer roast times
3. **Both** — minimize airflow, accept moderate temps, and tune from there

### Revised Estimate: Minimum Viable Airflow

For 113g of green coffee in a ~3" diameter chamber, fluidization likely requires
significantly less than 35 CFM. Estimates from similar small roasters suggest
**15-25 CFM** may be sufficient (see Section 2).

At 20 CFM:

    20 CFM ≈ 0.00944 m³/s
    ṁ ≈ 0.00944 × 1.2 = 0.01133 kg/s

Power for ΔT = 200°C:

    P = 0.01133 × 1005 × 200 ≈ 2277 W

Still too high. At ΔT = 120°C (process air at 140°C — low but possibly workable
with extended roast and recirculated heat from the bean mass):

    P = 0.01133 × 1005 × 120 ≈ 1365 W  ✓ Fits 120V budget

### Working Heater Specification

| Parameter | Target | Notes |
|-----------|--------|-------|
| Heater power | **1200–1400W** | Constrained by 120V/15A |
| Heater element type | Nichrome on mica former (Warrior heat gun) | Salvaged from HF SKU 56434 |
| Heater voltage | 120V AC | Switched by zero-cross SSR |
| Expected process air ΔT | 100–150°C at working airflow | Actual achievable temp depends on airflow, losses |

### Implications

- The 120V constraint makes this a **thermally modest** system
- Roast times will likely be **longer than commercial fluid-bed roasters** (8-15 min vs 5-8 min)
- Insulating the heater can and plenum will matter for efficiency
- The distributor plate and chamber should minimize heat loss
- **This is acceptable for v1** — the goal is to characterize and learn, not to match commercial speed

---

## 2. Airflow Budget

### Fluidization Requirements

For green coffee beans (~7mm equivalent diameter, ~1.1-1.3 g/cm³ density):

**Minimum fluidization velocity (Umf)** for coffee beans is approximately
**0.8–1.2 m/s** based on published fluidization studies and small-roaster
experience.

**T5 — Operating margin:** The original 1.5× Umf target is thin. Target
**1.8–2.5× Umf** for stable fluidization with margin for bed weight changes.
All velocity calculations must use hot-air density at process temperature
(~0.7–0.8 kg/m³ at 150–200°C), not ambient density. Previous calculations
applied this correction inconsistently.

### Chamber Cross-Section — Two Candidates

We are sourcing **two standard stainless steel tube sizes** and will test both.
This avoids committing to a chamber diameter before we have fluidization data.

**2.5" OD tubing** (ID ~2.37" / 60mm) — the thermal-efficiency candidate:

    Area = π × (0.030)² = 0.00283 m²

    Volumetric flow at 2.0× Umf = 2.0 m/s (T5: revised from 1.5×):
    Q = 2.0 × 0.00283 = 0.00566 m³/s ≈ 12.0 CFM

    Bed depth for 113g (bulk density ~0.65 g/cm³):
    V_bed = 113 / 0.65 = 174 cm³
    Depth = 174 / 28.3 ≈ 6.1 cm

    T3: L/D ratio = 6.1 / 6.0 ≈ 1.0 — WARNING: Geldart D particles (coffee beans)
    slug at L/D > 0.5-0.8. The 2.5" chamber has a significant slugging risk.

    Power for ΔT = 200°C at 12 CFM:
    ṁ = 0.00566 × 1.2 = 0.00679 kg/s
    P = 0.00679 × 1005 × 200 ≈ 1364 W  ✓ Within 120V budget

**3.0" OD tubing** (ID ~2.87" / 73mm) — the safe-fluidization candidate:

    Area = π × (0.0365)² = 0.00419 m²

    Volumetric flow at 2.0× Umf = 2.0 m/s (T5: revised from 1.5×):
    Q = 2.0 × 0.00419 = 0.00838 m³/s ≈ 17.7 CFM

    Bed depth for 113g:
    Depth = 174 / 41.9 ≈ 4.2 cm

    T3: L/D ratio = 4.2 / 7.3 ≈ 0.57 — within acceptable range for fluidization.

    Power for ΔT = 200°C at 17.7 CFM:
    ṁ = 0.00838 × 1.2 = 0.01006 kg/s
    P = 0.01006 × 1005 × 200 ≈ 2022 W  ⚠ Exceeds 120V budget

    T4: After 100-230W parasitic losses (heater can, plenum, duct walls), achievable
    process air ΔT drops to ~160-175°C. Insulating heater can and plenum is mandatory
    for the 3.0" chamber to reach usable roast temperatures.

### Comparison

| Parameter | 2.5" OD (60mm ID) | 3.0" OD (73mm ID) |
|-----------|-------------------|-------------------|
| Tube stock | Standard, cheap | Standard, cheap |
| Bed depth (113g) | ~6.1 cm | ~4.2 cm |
| L/D ratio | ~1.0 ⚠ slugging risk (T3) | ~0.57 ✓ safe range |
| CFM at 2.0× Umf (T5) | ~12 CFM | ~18 CFM |
| Watts for ΔT=200°C | ~1364W | ~2022W |
| Thermal headroom on 120V | Good | Exceeded — needs insulation (T4) |
| Fluidization risk | Deeper bed — harder, slugging | Shallower — easier |

**Decision:** Test both. The 2.5" gives us significantly better thermal performance
if it fluidizes well. The 3.0" is the safe fallback. TP-001 will determine the winner.

The plenum and distributor plate mounting interface should accommodate both tube sizes
(e.g., adapter ring or two plate sizes).

### Temperature Correction

Hot air is less dense. At process temperature (~150-200°C), air density drops to
~0.7-0.8 kg/m³. The volumetric flow rate at the distributor plate is **higher**
than at the blower inlet for the same mass flow.

This actually helps: the blower pushes cool air at lower volume, and the heated
air expands to provide higher velocity at the plate.

Blower-side CFM needed (at ambient, corrected for hot-air density T5):

    2.5" chamber: ~8-12 CFM at blower → ~12-17 CFM at plate (hot)
    3.0" chamber: ~12-18 CFM at blower → ~18-25 CFM at plate (hot)

### Working Airflow Specification

| Parameter | Target | Notes |
|-----------|--------|-------|
| Blower output (cold) | **8–18 CFM** | Must cover both chamber sizes at 2.0× Umf (T5 revised) |
| Velocity at plate (hot) | **1.6–2.5 m/s** | T5: 1.8-2.5× Umf target for stable fluidization |
| Chamber options | **2.5" OD (~60mm ID)** and **3.0" OD (~73mm ID)** | Test both, standard SS tube stock |
| Adjustable range | **30–100% of max** | Need to tune fluidization quality per chamber |

---

## 3. Blower Static Pressure Budget

### Pressure Drops Through the System

| Component | Estimated Pressure Drop | Notes |
|-----------|------------------------|-------|
| Heater can | 0.1–0.3" WC | Open duct with element obstruction |
| Plenum entry + baffles | 0.1–0.3" WC | Side-entry turning loss + baffle resistance |
| Distributor plate | 0.3–0.8" WC | Depends on open area ratio (target 5-15%) |
| Bean bed | 0.2–0.8" WC | Depends on bed depth and bean size (deeper in 2.5" chamber) |
| Exhaust path | 0.1–0.2" WC | Screen + ducting |
| **Total system** | **0.8–2.1" WC** | |

### Working Blower Specification

| Parameter | Target | Notes |
|-----------|--------|-------|
| Static pressure | **1.5–2.5" WC** at operating CFM | Must handle full system backpressure |
| Flow rate | **8–18 CFM** at operating pressure | T5: revised to cover 2.0× Umf for both chambers |
| Control | PWM via MOSFET from ESP32 | 12V DC brushless, no AC control needed |
| Noise | Tolerable for indoor use | Not a hard requirement for v1 |

### Blower Selection (DR-003)

**Selected:** 12V brushless DC centrifugal blower (~120mm x 32mm form factor,
e.g. WDERAIR or Wathai). Controlled via logic-level MOSFET (e.g. IRLZ44N) and
PWM from ESP32 GPIO. Flyback diode across fan leads. Powered by a 12V/3A
AC-DC switching supply (see Power Domains below).

**Selection criteria:** Must produce ~13-15 CFM at ~2" WC static pressure (to cover
the 3.0" chamber) with controllable speed down to ~6 CFM (for the 2.5" chamber).

**Rationale:** 12V DC keeps the blower entirely on the low-voltage side, avoiding
AC triac control complexity. Cost delta vs. scavenged AC motor is ~$15-20 —
worth it for simpler electronics and direct ESP32 PWM control.

**T1 — CRITICAL: Blower P-Q verification.** The 120mm × 32mm 12V centrifugal
blower P-Q curve is unverified. A typical blower of this size may not deliver
18 CFM at 2" WC (the 3.0" chamber operating point). **Measure actual blower
performance before committing to any other component sizing.** If the blower
cannot reach the required operating point, options include:
1. A larger or higher-pressure blower
2. Reducing system backpressure (more open distributor plate, lower bed depth)
3. Accepting the 2.5" chamber as primary (lower CFM requirement)

---

## 3.5. Known Thermal Losses and Mid-Roast Effects (DR-010)

These factors are documented as known but not fatal to v1. They should be
accounted for in test plan interpretation and control tuning.

### T4 — Parasitic Heat Losses

The heater can body, plenum walls, duct connections, and distributor plate all
absorb and radiate heat. Estimated parasitic losses: **100–230W** depending on
insulation and ambient conditions.

**Action:** Insulate heater can exterior and plenum walls with fiberglass wrap.
This is especially important for the 3.0" chamber, where the thermal budget
is already tight.

### T6 — Moisture Release

Green coffee contains ~10-12% moisture by weight. During roasting, moisture
release absorbs approximately **30–40W equivalent** of energy (latent heat of
vaporization). This is unaccounted for in the basic thermal budget but is not
fatal — it slightly reduces effective process air temperature during drying
phase.

### T7 — Bean Mass Changes During Roasting

Beans lose 12–18% of their mass during roasting (moisture + CO₂ + volatiles).
This changes the bed weight and therefore the fluidization velocity requirement.
Beans become lighter as the roast progresses — fluidization gets easier, and
the operator may need to reduce blower speed mid-roast to avoid blowing beans
out of the chamber.

### T8 — Chaff Mesh Clogging

The 30×30 SS mesh screen may progressively clog with chaff oils during a roast,
increasing back-pressure. Plan for mid-roast mesh cleaning if roasts stall, or
test with coarser mesh (20×20) as a fallback.

---

## 4. Summary: Key Constraining Numbers

These are the DG-0 decision parameters. All downstream design must be
consistent with these values.

| Parameter | Working Value | Hard Constraint? |
|-----------|-------------|-----------------|
| Batch size | 113g green | Design decision |
| Mains power | 120V / 15A | Yes (US residential) |
| Heater power | 1200–1400W | Yes (120V limited) |
| Airflow (cold, blower side) | 8–18 CFM | T5: revised for 2.0× Umf, both chambers |
| Airflow velocity at plate (hot) | 1.6–2.5 m/s | T5: 1.8-2.5× Umf, verify by test |
| Chamber ID (primary) | 2.5" OD / ~60mm ID | Better thermal performance |
| Chamber ID (backup) | 3.0" OD / ~73mm ID | Easier fluidization |
| Blower static pressure | 1.5–2.5" WC | Estimated from system drops — T1: VERIFY before committing |
| Process air temp (TC1) | 140–220°C achievable | Limited by heater power vs airflow |
| TC sample rate | ≥2 Hz | Artisan compatibility |

---

## 5. Cooling Cycle (DR-005)

### Approach

Blower-only cooling: SSR off (heater 0%), blower at 100%. No bypass damper
for v1.

### Thermal Mass Estimate

| Component | Mass | Cp (J/g·°C) | Energy to cool 200→50°C |
|-----------|------|-------------|-------------------------|
| Nichrome wire | ~50-80g | 0.44 | ~3-5 kJ |
| Heater can body | ~100-200g | 0.50 | ~8-15 kJ |
| **Total** | | | **~13-23 kJ** |

At 10 CFM forced convection through a 200°C element:

    ṁ × Cp × ΔT = 0.0057 × 1005 × 180 ≈ 1030 W initially

Average extraction ~500-1000W → element cools in **15-30 seconds**. After that,
air reaching the beans is near ambient temperature.

### Bean Cooling Timeline (estimated)

113g beans at ~200°C, blower at 100% (10-15 CFM ambient air):
- 0-30s: Air still warm from element thermal lag; beans cool slowly
- 30-90s: Air is near ambient; beans cooling rapidly
- 90-140s: Beans reach <50°C target

**Total estimated cooling time: 100-140 seconds** (within industry 90-150s target)

### Mechanical Provision for Future Bypass

The blower-to-heater-can joint uses a hose clamp connection (not welded). If
TP-002 data shows residual heat is problematic, options include:
1. Physically disconnect heater can during cooling (simplest)
2. Add a two-position diverter valve at the blower outlet
3. Add a second ambient air inlet on the plenum

### Firmware: COOL Command

A `COOL` command sets heater to 0%, blower to 100%, and logs cooldown curves.
Operator notification when TC2 < 50°C.

---

## 6. Chaff Collection (DR-006)

### Chaff Characteristics

| Parameter | Value |
|-----------|-------|
| Chaff mass per 113g batch | ~0.5-0.9g |
| Particle size | ~30-60 microns |
| Release timing | Mostly at first crack |

### Design: Expansion Chamber + Mesh Screen

A removable exhaust unit mounted atop the roast chamber:

| Parameter | Value | Notes |
|-----------|-------|-------|
| Body | ~4" OD × 5" tall SS cylinder | Step-up from chamber diameter |
| Air velocity in chamber | 2-4 ft/sec | Velocity drop causes chaff to settle |
| Screen | 30×30 SS mesh | Secondary capture at top of expansion chamber |
| Cleaning | Tap-and-empty between roasts | Removable unit |
| Backpressure impact | Negligible | Expansion reduces velocity; screen is coarse enough |

### Why Not a Cyclone

A cyclone separator provides 96-99% capture but adds significant backpressure,
which directly impairs fluidization in the roast chamber. At the 113g scale
with <1g of chaff per roast, a simple expansion chamber is sufficient and adds
near-zero flow restriction.

---

## 8. Plenum Assembly (DR-007, DR-008, DR-009)

### Plenum Body

| Parameter | Value | Notes |
|-----------|-------|-------|
| Body | 1/6 size SS steam table pan, 4" deep | ~6.4" x 6.3" x 4", 18/8 SS |
| Orientation | Right-side-up (open top faces up) | |
| Side-entry hole | ~2-3" dia, drilled through wall | Connects to heater can via hose clamp |
| Source | Restaurant supply or thrift store | $4-8 new |

### Top Assembly (no welding)

The open top of the pan is sealed by a bolted clamping ring that holds the
distributor plate and seats the roast chamber:

| Component | Material | Attachment | Notes |
|-----------|----------|------------|-------|
| Clamping ring | Flat SS sheet, ~1" wide annular ring | 3-4 bolts through pan flange | Inner hole sized per chamber (2.5" or 3.0") |
| Gasket | Fiberglass or ceramic fiber strip | Sandwiched between ring and rim | Seals against hot air leakage |
| Distributor plate | Perforated SS disc | Rests on ring ledge, gravity-held | Swappable for iteration |
| Chamber tube | 2.5" or 3.0" OD SS tube | Sits on/in plate, held by ring | Gravity + clamp if needed |

Swapping chamber sizes requires swapping the ring + plate pair. Each pair is
sized to its chamber OD.

### Deflector Ramp Baffle

| Parameter | Value | Notes |
|-----------|-------|-------|
| Material | SS sheet scrap, ~3" × 4" | Bent to ~45° in vise |
| Position | Inside plenum, opposite side-entry hole | Redirects jet downward to pan floor |
| Attachment | 2 bolts or pop rivets through pan wall | Must be removable for cleaning |
| Function | Jet → floor spread → uniform rise to plate | Uses full plenum volume for equalization |

**T2 — Second baffle / equalization stage:** A single deflector ramp is unlikely
to fully equalize pressure — the velocity ratio at the inlet is 5–10× the
target distributor velocity. Plan to add a second equalization feature:
- Option A: Horizontal perforated baffle ~1" below the distributor plate
- Option B: Perforated diffusion plate inside plenum between ramp and distributor

The plenum depth (4") allows room for either option without redesign. Validate
in TP-001 — if the single ramp produces acceptable fluidization uniformity,
the second baffle can be deferred.

---

## 9. Open Questions for DG-0 Review

1. ~~**Chamber diameter:** 3" is the working assumption. Should we consider 2.5"?~~
   **RESOLVED:** Sourcing both 2.5" OD and 3.0" OD standard SS tubes. Will test both.
   Plenum interface must accommodate both diameters.
2. ~~**Heater element sourcing:** What specific elements are available in the 1200-1400W
   / 120V range that fit a reasonable heater-can geometry?~~
   **RESOLVED (DR-002):** Harbor Freight Warrior 1500W heat gun (SKU 56434, ~$10).
   Nichrome on mica former. Measure element after teardown.
3. ~~**Blower sourcing:** DC brushless vs AC centrifugal — availability and cost at
   the required operating point? Must cover 6-15 CFM range with speed control.~~
   **RESOLVED (DR-003):** 12V brushless DC centrifugal (~120mm x 32mm), MOSFET + PWM.
   Requires 12V/3A AC-DC supply as additional BOM item.
4. **Insulation strategy:** How much can we recover by insulating the heater can
   and plenum? Worth calculating before finalizing heater spec.
5. **Roast time expectation:** Are 10-15 minute roast times acceptable for v1?
   (Likely yes, given the learning-platform philosophy.)
6. ~~**Plenum adapter design:** How to mount both chamber sizes on the same plenum —
   adapter ring, two plate sizes, or stepped seat?~~
   **RESOLVED (DR-008):** Bolted clamping ring across pan rim. Swap ring + plate
   pair to change chamber sizes. No welding.
