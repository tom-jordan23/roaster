# Baseplate Layout — Mechanical and Electronics Placement

## Purpose

Top-down layout of the v1 roaster baseplate: where each major component sits,
where the electronics tray goes, and how mains and signal wiring are routed.

This doc is **manual-first text + diagrams**. The OpenSCAD model
(`roaster-assembly.scad`) does not yet reflect this layout; SCAD changes are
gated on the salvaged vacuum motor being in hand (DR-011, design-log
2026-04-29). Once the motor is measured, both the SCAD model and this doc
should be updated together.

References: `docs/system/architecture.md` §3, `docs/electrical/schematics/power-schematic.md`,
`docs/system/design-log.md` (DR-005, DR-007, DR-008, DR-009, DR-011), `bom/bom-master.csv`.

---

## 1. Constraint Audit Against the SCAD Model

Numbers pulled from `roaster-assembly.scad` (commit prior to this doc):

| Parameter | SCAD value | Notes |
|-----------|-----------|-------|
| `base_length` | 508 mm (20") | M1 widening |
| `base_width` | 305 mm (12") | M1 widening |
| `plenum_x` | 0.55 × `base_length` ≈ 280 mm from rear edge | Centerline of plenum on long axis |
| `heater_can_length` | 190 mm | Placeholder pending teardown |
| `blower_dia` × `blower_depth` | 150 × 200 mm | **Placeholder** — DR-011 best-estimate |

Resulting air-train footprint along the long axis, measured from the rear
edge of the baseplate:

    rear edge (y=0) ───── blower 200mm ───── heater can 190mm ───── plenum (y=199 to y=361) ───── front edge (y=508)

The plenum -Y face sits at y ≈ 199 mm. The heater can extends from y = 199
back to y = 9 mm. The 200 mm blower envelope then runs from y = 9 to
y = -191 — **190 mm off the rear edge of the baseplate.** This was tolerable
with the 32 mm-deep DC fan that DR-003 specified; it is not tolerable for
the salvaged universal-AC vacuum motor (DR-011).

### Resolution: vertical motor axis (preferred)

Mount the salvaged vacuum motor with its shaft **vertical**, body sitting on
the baseplate as a ~150 mm-diameter footprint instead of a 200 mm-long
horizontal cylinder. The working-impeller outlet exits radially at the
heater-can centerline elevation (~plenum_z + side_entry_z, ~127 mm above
the baseplate) and connects via a short flex elbow + hose clamp to the
heater can. Cooling-fan exhaust is directed away from the electronics tray
and the operator (down through a clearance slot in the baseplate, or
sideways out the -X edge).

Plan-view blower footprint becomes ~150 × 150 mm and the 20" baseplate
is sufficient. This is the working assumption for the rest of this doc.

**Fallback (Option B):** lengthen the baseplate to ~26". Simpler
mechanically but worsens the M1 tipping concern — the motor is the
heaviest single part and would sit at the longest moment arm. Defer
unless vertical-axis mounting turns out to be impractical with the actual
salvaged motor.

---

## 2. Layout Zones

The baseplate is divided into four functional zones along the long (Y) axis,
front (operator) to rear:

```
       +Y (operator / front edge)
       ╔════════════════════════════════════════════╗
       ║  ZONE D — ELECTRONICS TRAY     ~5" × 12"   ║   front edge
       ║                                            ║
       ║━━━━━━━━━━━━━━━ heat barrier ━━━━━━━━━━━━━━━║   sheet-metal shield
       ║                                            ║   + ~1" air gap
       ║  ZONE C — PLENUM + CHIMNEY     ~6" × 7"    ║
       ║                                            ║
       ║  ZONE B — HEATER CAN + SSR     ~7" × 4"    ║   air-train axis
       ║                                            ║
       ║  ZONE A — BLOWER + AC CONTROL  ~6" × 7"    ║
       ║                                            ║
       ║  [MAINS ENTRY: cord grip → DPST → fuse]    ║   rear edge
       ╚════════════════════════════════════════════╝
       -Y (rear edge)
```

| Zone | Function | Thermal class | EMI class |
|------|----------|--------------|-----------|
| A    | Blower, TRIAC dimmer, line filter, mains entry, CT, ferrites | Warm (motor body 60–80°C) | **Hot** (TRIAC + brushed motor) |
| B    | Heater can, SSR + heatsink, snubber, airstream thermal fuse, TC1 | **Hot** (can surface >200°C even insulated) | Quiet |
| C    | Plenum, chimney, distributor plate, baffle, TC2, exhaust + chaff collector + TC3 | Hot (plenum 150–200°C, chimney 100–200°C) | Quiet |
| D    | ESP32, MAX31855 ×3, 5V PSU, SSR drive buffer, CT bias network, USB out | **Cool** (target <40°C) | **Quiet** (target) |

The heat barrier is a vertical sheet-metal shield bolted to the baseplate
between Zones C and D, with grommeted pass-throughs for the SSR DC drive
pair and the TC probe leads. The shield is bonded to chassis ground.

---

## 3. Air-Train Component Placement (Zones A–C)

### 3.1 Blower (Zone A)

| Aspect | Spec |
|--------|------|
| Component | BLW-001 (salvaged bypass-cooled vacuum motor) |
| Mounting orientation | Shaft **vertical**; motor body footprint ~150 mm dia |
| Mounting position | Rear-center of baseplate; body centerline aligned with air-train Y axis |
| Outlet routing | Radial outlet at heater-can centerline elevation; short flex elbow + hose clamp to heater can |
| Cooling exhaust | Directed away from operator and Zone D (down, or sideways out -X) |
| Vibration isolation | Rubber feet or grommeted bolts; the universal motor will vibrate |
| Frame bonding | BOND-001 — ring terminal to chassis-ground bus |

### 3.2 AC blower control (Zone A, adjacent to motor)

| Aspect | Spec |
|--------|------|
| BLW-CTRL-001 | TRIAC dimmer module on standoffs ~50 mm from motor body |
| FILT-001 | AC line filter, inline on motor L+N leads, between fuse bus and dimmer |
| CT-001 | Split-core CT clamped on the motor's L lead **between the dimmer and the motor** so it sees the gated AC waveform |
| FERR-001 | Snap-on ferrite on motor leads between the dimmer output and the motor body |

The TRIAC dimmer must stay near the motor — short motor leads bound the
EMI source. Only three logic-level wires (PWM, ZC, GND) leave Zone A
toward Zone D.

### 3.3 Heater can (Zone B)

| Aspect | Spec |
|--------|------|
| Component | HTR-CAN-001 (built per M5: 2.5" SS exhaust pipe, element on mica former, ceramic fiber wrap exterior) |
| Mounting | Cradled in two formed sheet-metal saddles bolted to baseplate; saddles lined with high-temp gasket to avoid metal-to-metal heat conduction |
| Joints | Hose clamp at blower outlet (preserves DR-005 bypass-cooling option); hose clamp at plenum side-entry stub tube (PLEN-005, M2) |
| THFUSE-001 | Mounted on can body exterior, in series with heater (independent of MCU) |
| THFUSE-002 | Mounted in the heated airstream, downstream of the element, immediately upstream of the plenum side-entry (E6) |
| TC1 | K-type probe via TC-FIT-001 compression fitting, in the heated airstream just upstream of plenum side-entry |

### 3.4 SSR (Zone B, baseplate-side of the heat barrier)

| Aspect | Spec |
|--------|------|
| Component | SSR-001 + finned heatsink |
| Position | On the +Y side of the heater can, between can and the heat barrier |
| Heatsink orientation | Fins vertical for natural convection (~15–20 W dissipation at 12.5 A continuous) |
| Snubber | R-SNB + C-SNB across SSR output terminals (E10) |
| DC drive | Two short pigtails (SSR+, SSR-) cross the heat barrier through a grommet to Q2 buffer in Zone D |

The SSR is *not* in the electronics tray. Keeping it on the air-train side
shortens the high-current SSR-to-element wiring and concentrates the
Zone D enclosure on cool-running parts only.

### 3.5 Plenum and chimney (Zone C)

The plenum sits centered on the +Y portion of the baseplate. The chimney
(distributor plate → roast chamber → cone reducer → chaff expansion
chamber → mesh screen) rises vertically from the clamping ring. No layout
changes from the current SCAD; this zone is driven by DR-007/008/009 and
unchanged by DR-011.

| TC | Mount point |
|----|-------------|
| TC-002 | Lower chamber side wall via TC-FIT-001 (bean-bed temperature) |
| TC-003 | Exhaust stream above the chamber, via TC-FIT-001 (M9) |

### 3.6 Mains entry (rear edge of Zone A)

Cord enters the rear edge through a strain relief (STRAIN-001) and runs
**along the rear edge** to:

    cord → STRAIN-001 → SW-001 (DPST) → FUSE-001 (15A) → L bus + N bus + chassis-ground bus

SW-001 is mounted through the rear face of an enclosed Zone-A panel so it
is reachable but not bumpable. (See §6 for the case where SW-001 moves to
the front face instead.)

---

## 4. Electronics Tray (Zone D)

A small enclosed or fenced area at the operator end of the baseplate,
~5" deep × 12" wide, separated from Zone C by the heat barrier.

### 4.1 Enclosure

A vented project box (~6" × 4" × 2", or fabricated from sheet metal) bolted
to the baseplate. Vents on the +Y face only (away from the heat barrier).
Target internal temperature <40°C during a roast — verify in TP-001 with a
TC taped to the inside of the enclosure.

### 4.2 Internal placement

From rear (heat-barrier side) to front (operator side):

| Row | Component | Notes |
|-----|-----------|-------|
| Rear  | Q2 + R3 (SSR drive buffer, E7) | On the same protoboard as the ESP32; pigtails through the heat-barrier grommet to SSR DC input |
| Rear  | CT bias network (burden R + offset divider) | Short shielded run from CT-001 in Zone A; bias network references signal ground |
| Mid   | ESP-001 (ESP32-DevKitC) | On standoffs; orientation chosen so USB connector faces the front face of the enclosure |
| Mid   | TC-AMP-001 ×3 (MAX31855 boards) | Same protoboard as ESP; CS lines short (<50 mm) |
| Front | PSU-001 (5V USB charger) | Mains side of the enclosure; output USB-A or pigtailed to ESP32 VIN |
| Front face | USB-B / USB-C pass-through | Strain-relieved, to host PC running Artisan |
| Front face | Optional indicator LEDs or small status display | Future — not v1 |

### 4.3 Components that do **not** live in the electronics tray

| Component | Lives in | Why |
|-----------|----------|-----|
| BLW-CTRL-001 (TRIAC dimmer) | Zone A | Keep motor leads short; bound the EMI source |
| CT-001 | Zone A | Must be physically clamped on a motor lead |
| FILT-001 | Zone A | Inline on motor mains leads |
| FERR-001 (motor-side) | Zone A | On motor leads |
| FERR-001 (TC-side) | One on each TC SPI cable, both at the amp end and the probe end | Distributed; not localized |
| SSR-001 + heatsink | Zone B | Air-train side of heat barrier; short high-current wiring to element |
| THFUSE-001 / THFUSE-002 | Zone B | On the can body and in the airstream |
| FUSE-001 + SW-001 | Rear edge of Zone A (or front face — see §6) | Mains protection lives with mains entry |

---

## 5. Wire Routing — Three Lanes

All wiring runs along the **+X edge** of the baseplate (the long edge
opposite the air train), in three physically separated channels. This
keeps wiring entirely outside Zones B and C's hot/EMI footprint.

| Lane | Position | Carries | Wire spec |
|------|----------|---------|-----------|
| **Mains** | Elevated raceway ~25 mm above baseplate, on the +X edge | L/N from cord through fuse and switch; L+N to SSR; L+N through FILT-001 and TRIAC to motor | 14 AWG THHN, in metal conduit or solid raceway |
| **Heater control** | Short crossing of the heat barrier through a grommet, **perpendicular** to the mains lane | SSR DC input pair (5V, GND from Q2 buffer) | 22 AWG twisted pair |
| **Signal** | Plastic raceway ~25 mm **below** the mains lane, on the **outside** of the +X edge | TC SPI runs to TC1/TC2/TC3 amps (already inside the tray, so most of this lane is the TC probe leads going *up* the chimney); CT-001 secondary leads from Zone A to the bias network in Zone D; ESP32-to-dimmer logic (PWM, ZC, GND) | 22 AWG silicone hookup; shielded cable for SPI runs and CT secondary; twisted pair for ZC and PWM |

### Routing rules

- **No shared conduit** between mains and signal lanes — separate raceways.
- **Right-angle crossings only** when the signal lane must cross the
  mains lane; minimize crossing length.
- **Ferrite at every crossing** (FERR-001 inventory).
- **Ferrite at both ends of every TC SPI cable** (E13 + DR-011 EMI plan).
- **Shield grounded at one end only** (the ESP32 / amp end) to prevent
  ground loops.
- **CT-001 secondary** is a twisted shielded pair from Zone A to the bias
  network in Zone D; the secondary is referenced to signal ground via the
  bias network — **not** to chassis ground.

### Grounding bus

A single chassis-ground bus (brass strip or grounding stud) on the
**rear-right corner** of the baseplate, fed from the green wire of the
mains cord. Star topology — no daisy-chains. Bond points, each on its own
dedicated wire to the bus:

- Plenum pan ground lug
- Heater-can ground lug
- SSR heatsink (if metal)
- Blower motor frame (BOND-001)
- Heat-barrier shield
- Baseplate (if metal)

Signal ground (5V PSU GND, ESP32 GND, MAX31855 GNDs, TRIAC dimmer logic
GND) returns to a star point at the 5V PSU output, **not** to chassis
ground. Reaffirms the existing rule from `power-schematic.md`.

---

## 6. Open Issues / Pending Parts

| Item | Why it's pending | What unblocks it |
|------|-----------------|------------------|
| Motor footprint and outlet geometry | DR-011: salvaged motor not yet on bench | Salvage hunt; vertical-axis mounting plan re-validated against actual envelope |
| Heater-can length | HTR-001 not yet torn down | Warrior heat gun teardown (DR-002) |
| Electronics enclosure dimensions | SSR heatsink size and PSU brick size both still nominal | Parts received |
| SW-001 placement (rear vs front face) | Reachability vs. cable-length tradeoff | Decide once Zone-A panel orientation is fixed by motor geometry |
| Verification of <40°C inside Zone D | Depends on heat-barrier effectiveness | TP-001 — instrument enclosure interior with a TC during a soak run |
| L-bracket / ballast plan for stability (M1) | Depends on final mass distribution, especially after blower placement | Once motor is mounted; weigh assembly and check tipping moment |

---

## 7. Cross-References

- Architecture: `docs/system/architecture.md` §3, §3.1, §8
- Schematics: `docs/electrical/schematics/power-schematic.md`
- BOM line items used in this doc: HTR-001, HTR-CAN-001, BLW-001,
  BLW-CTRL-001, CT-001, FILT-001, FERR-001, BOND-001, SSR-001, ESP-001,
  TC-AMP-001 (×3), TC-001/002/003, TC-FIT-001, PSU-001, SW-001, FUSE-001,
  STRAIN-001, THFUSE-001, THFUSE-002, R-SNB-001, C-SNB-001, Q2-001,
  R3-001, PLEN-001, PLEN-005, BASE-001
- Design decisions referenced: DR-002, DR-005, DR-007, DR-008, DR-009,
  DR-011; M1, M2, M5, M9; E6, E7, E10, E13; T1
- SCAD model (to be updated when motor is in hand): `docs/mechanical/drawings/roaster-assembly.scad`
