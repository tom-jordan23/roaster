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

### Chamber Cross-Section — Two Candidates

We are sourcing **two standard stainless steel tube sizes** and will test both.
This avoids committing to a chamber diameter before we have fluidization data.

**2.5" OD tubing** (ID ~2.37" / 60mm) — the thermal-efficiency candidate:

    Area = π × (0.030)² = 0.00283 m²

    Volumetric flow at 1.5× Umf = 1.5 m/s:
    Q = 1.5 × 0.00283 = 0.00424 m³/s ≈ 9.0 CFM

    Bed depth for 113g (bulk density ~0.65 g/cm³):
    V_bed = 113 / 0.65 = 174 cm³
    Depth = 174 / 28.3 ≈ 6.1 cm

    Power for ΔT = 200°C at 9 CFM:
    ṁ = 0.00424 × 1.2 = 0.00509 kg/s
    P = 0.00509 × 1005 × 200 ≈ 1023 W  ✓ Well within 120V budget

**3.0" OD tubing** (ID ~2.87" / 73mm) — the safe-fluidization candidate:

    Area = π × (0.0365)² = 0.00419 m²

    Volumetric flow at 1.5× Umf = 1.5 m/s:
    Q = 1.5 × 0.00419 = 0.00628 m³/s ≈ 13.3 CFM

    Bed depth for 113g:
    Depth = 174 / 41.9 ≈ 4.2 cm

    Power for ΔT = 200°C at 13 CFM:
    ṁ = 0.00628 × 1.2 = 0.00754 kg/s
    P = 0.00754 × 1005 × 200 ≈ 1515 W  ⚠ Tight on 120V — may need ΔT ≤ 170°C

### Comparison

| Parameter | 2.5" OD (60mm ID) | 3.0" OD (73mm ID) |
|-----------|-------------------|-------------------|
| Tube stock | Standard, cheap | Standard, cheap |
| Bed depth (113g) | ~6.1 cm | ~4.2 cm |
| CFM at 1.5× Umf | ~9 CFM | ~13 CFM |
| Watts for ΔT=200°C | ~1023W | ~1515W |
| Thermal headroom on 120V | Excellent | Tight |
| Fluidization risk | Deeper bed — harder | Shallower — easier |

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

Blower-side CFM needed (at ambient):

    2.5" chamber: ~6-9 CFM at blower → ~9-13 CFM at plate (hot)
    3.0" chamber: ~9-13 CFM at blower → ~13-19 CFM at plate (hot)

### Working Airflow Specification

| Parameter | Target | Notes |
|-----------|--------|-------|
| Blower output (cold) | **6–15 CFM** | Must cover both chamber sizes at operating backpressure |
| Velocity at plate (hot) | **1.2–2.0 m/s** | Good fluidization range |
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
| Flow rate | **6–15 CFM** at operating pressure | Must cover both chamber sizes |
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

---

## 4. Summary: Key Constraining Numbers

These are the DG-0 decision parameters. All downstream design must be
consistent with these values.

| Parameter | Working Value | Hard Constraint? |
|-----------|-------------|-----------------|
| Batch size | 113g green | Design decision |
| Mains power | 120V / 15A | Yes (US residential) |
| Heater power | 1200–1400W | Yes (120V limited) |
| Airflow (cold, blower side) | 6–15 CFM | Range covers both chamber sizes |
| Airflow velocity at plate (hot) | 1.2–2.0 m/s | Estimated, verify by test |
| Chamber ID (primary) | 2.5" OD / ~60mm ID | Better thermal performance |
| Chamber ID (backup) | 3.0" OD / ~73mm ID | Easier fluidization |
| Blower static pressure | 1.5–2.5" WC | Estimated from system drops |
| Process air temp (TC1) | 140–220°C achievable | Limited by heater power vs airflow |
| TC sample rate | ≥2 Hz | Artisan compatibility |

---

## 5. Open Questions for DG-0 Review

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
6. **Plenum adapter design:** How to mount both chamber sizes on the same plenum —
   adapter ring, two plate sizes, or stepped seat?
