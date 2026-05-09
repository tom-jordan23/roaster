# Baseplate Layout — Mechanical and Electronics Placement

## Purpose

Top-down layout of the v1 roaster baseplate: where each major component sits,
where the electronics tray goes, and how mains and signal wiring are routed.

This doc is **manual-first text + diagrams**. The OpenSCAD model
(`roaster-assembly.scad`) does not yet reflect this layout; SCAD changes are
gated on the vacuum motor being in hand (DR-011, design-log
2026-04-29). Once the motor is measured, both the SCAD model and this doc
should be updated together.

References: `docs/system/architecture.md` §3, `docs/electrical/schematics/power-schematic.md`,
`docs/system/design-log.md` (DR-005, DR-007, DR-008, DR-009, DR-011), `bom/bom-master.csv`.

---

## 1. Constraint Audit Against the SCAD Model

Numbers below reflect the as-built **12" × 18" steel deck** cut from the
24" BASE-001 stock, mounted on a 1"-class angle-iron frame with rear and
front extensions for the motor and electronics tray respectively (the
remaining 6" of stock is reserved for the frame extension stock and
gussets). The motor (BLW-001) and heater element (HTR-001) are now in hand
and measured; previous placeholder geometries are replaced with measured
values.

| Parameter | Value | Notes |
|-----------|-------|-------|
| Deck | 305 × 457 mm (12" × 18") | Steel sheet cut from the BASE-001 24" stock; the air train sits on this, and motor/electronics live on frame extensions outboard of it |
| Frame | 1"-class angle iron: perimeter on the deck + a rear extension for the motor + a front extension for the electronics tray | M1 stiffening + structural carry for off-deck loads. Final extension lengths set by §3 below |
| Legs | 3× threaded rod tripod, extending above and below baseplate | DR-013 tip-resistance strategy: rods continue up past the baseplate to a clamp around the cone reducer or upper chamber. Tripod gives lateral stability without the complications of running the chamber tube down into the plenum (TC-002 mount, chamber swap). Below the baseplate, same rods are the feet — adjustable for leveling |
| Plenum footprint | 203 mm dia × 152 mm tall (8" × 6") | DR-012 — round black stovepipe, both ends capped; vertical axis |
| `heater_can_length` | 178 mm (7") | **Measured 2026-05-07** — 1.5" × 6" Warrior element pack + ~0.5" each end for inlet/outlet fittings; 2.5" OD SS exhaust pipe (HTR-CAN-001) |
| `blower_dia` × `blower_height` | 152 × 152 mm (6" × 6"), vertical-axis cylinder | **Measured 2026-05-07** — aftermarket Lamb 116336-01-pattern bypass-cooled vacuum motor (BLW-001) in hand; outlet exits radially at heater-can centerline elevation |

### Air-train pack length and frame extensions

Working from the design pack length along the long (Y) axis, with the
motor and plenum on extensions outboard of the deck:

    rear extension ─ deck (457 mm) ─ front extension
    ┌──── motor 152 ────┬─── heater can 178 ──┬── plenum 203 ──┐ ── electronics tray ──┐
    │ entirely on rear  │     on deck         │   on deck      │  on front extension   │
    └ extension (~152)  │ (Y=25 to Y=203)     │ (Y=228 to 431) │  (Y=470 to ~595)      ┘

- **Motor** (Zone A, rear): mounted entirely on the rear angle-iron extension,
  body centered ~75 mm rear of the deck rear edge. Outlet faces forward and
  joins the heater can at the deck rear edge via a short flex elbow + hose
  clamp. **Rear extension length: ~152 mm (6").**
- **Heater can** (Zone B): on the deck, axis along Y, occupies Y = 25 mm to
  Y = 203 mm (25 mm rear margin for the motor-outlet joint).
- **Plenum** (Zone C): on the deck, vertical axis, with the side-entry stub
  (PLEN-005) crossing Y = 203 mm to Y = 228 mm. Plenum body (8" dia) occupies
  Y = 228 mm to Y = 431 mm — sits comfortably inside the 457 mm deck with
  ~26 mm front-edge margin to the heat-barrier line.
- **Electronics tray** (Zone D): on a front angle-iron extension, ~125 mm
  (5") deep, behind the heat barrier shield. Mounting it on an extension
  (rather than cramming it into the 26 mm of deck remaining) is the cleanest
  way to preserve the original 5"-deep enclosure while keeping the deck
  reserved for the air train. **Front extension length: ~125 mm (5").**

Total assembly footprint along Y: 152 (rear ext) + 457 (deck) + 125 (front
ext) = **734 mm (28.9")**. This is comparable in length to the originally
planned 24" baseplate but with the heat-bearing portion (deck + air train)
restricted to the 18" steel sheet — the angle-iron extensions carry only
cool-zone loads (motor body which runs at 60–80°C ambient, electronics
tray which targets <40°C internal).

### Why this layout

1. **Motor off the deck.** The motor is the heaviest single part and is the
   primary tipping moment contributor. Placing it on a rear angle-iron
   extension, with the rear pair of tripod legs straddling it, anchors the
   motor weight directly to the legs rather than cantilevering it over the
   deck edge.
2. **Plenum on deck, near front-of-deck.** The plenum carries the chamber
   stack — the tallest, most tip-prone subassembly — so it stays inboard of
   the deck where the front pair of tripod legs and the chamber-band clamp
   (DR-013) provide rigid support.
3. **Heat-barrier sheet between the plenum and the electronics tray.** The
   barrier bolts to the deck front edge with grommeted pass-throughs for the
   SSR drive pair and the TC leads (see §4.1). Putting the electronics tray
   on a front extension preserves the ~1" air gap and keeps the barrier free
   of cable congestion.
4. **Steel deck reserved for the hot zones (B + C).** The deck takes the
   thermal load (heater can + plenum, both >150°C surface temps even
   insulated). Cool-zone components (motor envelope at 60–80°C, electronics
   at <40°C) sit on angle-iron extensions outboard of the deck where the
   thermal gradient is small.

---

## 2. Layout Zones

The full assembly footprint is divided into four functional zones along the
long (Y) axis, front (operator) to rear. Zones B and C live on the 12" × 18"
steel deck; Zones A and D live on angle-iron frame extensions outboard of
the deck:

```
       +Y (operator / front edge)
       ┌─ FRONT EXTENSION (~5" × 12" angle-iron tray support) ─┐
       │  ZONE D — ELECTRONICS TRAY        ~5" × 12"           │
       │                                                       │
       ╠═══════════════════ heat barrier ══════════════════════╣ ← deck front edge
       ║  ZONE C — PLENUM + CHIMNEY        ~8" dia, on deck    ║
       ║          (8" round stovepipe per DR-012;              ║
       ║           tripod legs straddle it — DR-013)           ║
       ║                                                       ║
       ║  ZONE B — HEATER CAN + SSR        ~7" × 4", on deck   ║   air-train axis
       ║                                                       ║
       ╠═══════════════════════════════════════════════════════╣ ← deck rear edge
       │  ZONE A — BLOWER + AC CONTROL     6" dia motor body   │
       │          (vertical axis) + TRIAC dimmer + line filter │
       │  [MAINS ENTRY: cord grip → DPST → fuse]               │
       └─ REAR EXTENSION (~6" × 12" angle-iron motor cradle) ──┘
       -Y (rear edge)
```

| Zone | Location | Function | Thermal class | EMI class |
|------|----------|----------|--------------|-----------|
| A    | Rear extension (off deck) | Blower, TRIAC dimmer, line filter, mains entry, CT, ferrites | Warm (motor body 60–80°C) | **Hot** (TRIAC + brushed motor) |
| B    | Deck (Y = 25–203 mm) | Heater can, SSR + heatsink, snubber, airstream thermal fuse, TC1 | **Hot** (can surface >200°C even insulated) | Quiet |
| C    | Deck (Y = 228–431 mm) | Plenum, chimney, distributor plate, baffle, TC2, exhaust + chaff collector + TC3 | Hot (plenum 150–200°C, chimney 100–200°C) | Quiet |
| D    | Front extension (off deck) | ESP32, MAX31855 ×3, 5V PSU, SSR drive buffer, CT bias network, USB out | **Cool** (target <40°C) | **Quiet** (target) |

The heat barrier is a vertical sheet-metal shield bolted to the deck front
edge between Zones C and D, with grommeted pass-throughs for the SSR DC
drive pair and the TC probe leads. The shield is bonded to chassis ground.
Putting Zone D on the front extension (rather than on the deck itself)
preserves the original ~1" air gap behind the barrier without crowding the
plenum.

---

## 3. Air-Train Component Placement (Zones A–C)

### 3.1 Blower (Zone A — rear extension)

| Aspect | Spec |
|--------|------|
| Component | BLW-001 (aftermarket Lamb 116336-01-pattern bypass-cooled vacuum motor) — **in hand 2026-05-07** |
| Body geometry | Cylindrical, **6" dia × 6" tall** (152 × 152 mm); shaft vertical |
| Mounting position | Centered on the rear angle-iron extension, ~75 mm rear of the deck rear edge; body centerline aligned with the air-train Y axis |
| Mounting hardware | Bolted to a sheet-metal saddle or strap, sitting on the angle-iron extension. Tripod rear legs straddle the motor on either side |
| Outlet routing | BLW-HOUS-001 fan shell on top of motor; outlet is **axial** (vertical, parallel to motor shaft, off-center on the dome face). BLW-ELBOW-001 1.5in silicone 90° elbow turns the discharge horizontal-forward, then BLW-COUP-001 1.5→2.5in silicone reducer carries it across the deck rear edge to the heater can inlet at heater-can centerline elevation. (Axial-outlet shape was confirmed via product-photo inspection 2026-05-09 — DR-015) |
| Cooling exhaust | Directed away from operator and Zone D (down through a clearance gap in the rear extension, or sideways out −X) |
| Vibration isolation | Rubber feet or grommeted bolts at the saddle/extension interface; the universal motor will vibrate |
| Frame bonding | BOND-001 — ring terminal under a frame screw to the chassis-ground bus |

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
| Element | HTR-001 Warrior 1500W nichrome on mica former, **measured 2026-05-07: 1.5" wide × 6" long element pack** |
| Can length | **178 mm (7")** — 6" element + ~0.5" each end for inlet/outlet transition fittings |
| Can OD | 2.5" (~64 mm) SS exhaust pipe |
| Mounting | Cradled in two formed sheet-metal saddles bolted to deck; saddles lined with high-temp gasket to avoid metal-to-metal heat conduction |
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

The plenum (DR-012: 8" dia × 6" tall black-stovepipe section, both ends
pipe-capped) sits centered on the +Y portion of the baseplate, vertical
axis. The chimney (distributor plate → roast chamber → cone reducer →
chaff expansion chamber → mesh screen) rises from the top cap, which is
drilled to the chamber OD and carries the clamping ring on its underside.
This zone is driven by DR-008, DR-009, DR-012 and is unchanged by DR-011.

Round footprint vs. the prior rectangular steam-pan plan: the 8" diameter
exceeds the 6"×7" rectangular Zone-C estimate by ~1" on the X axis but
remains comfortably inside the 12" baseplate width once the +X wire lanes
(§5) are accounted for.

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
| ~~Motor footprint and outlet geometry~~ | ~~DR-011: salvaged motor not yet on bench~~ | **In hand 2026-05-07** — 152 × 152 mm vertical-axis cylinder; outlet geometry confirmed sufficient for vertical-axis mount |
| ~~Heater-can length~~ | ~~HTR-001 not yet torn down~~ | **Measured 2026-05-07** — element 1.5" × 6"; HTR-CAN-001 length set to 178 mm (7") |
| ~~Plenum body sourcing~~ | ~~PLEN-001 thrift hunt pending~~ | **Resolved by DR-012** — black stovepipe scrap on hand; 8" × 6" target |
| ~~Baseplate sheet sourcing~~ | ~~BASE-001 not yet sourced~~ | **Sourced 2026-05-02; cut to 12" × 18" deck 2026-05-07** — angle iron from same stock for perimeter + rear (motor) and front (electronics) extensions |
| Frame extension fabrication | Rear extension (~6") and front extension (~5") not yet built | Cut and weld/bolt angle iron onto the deck perimeter; install motor saddle on rear extension; install electronics-tray cradle on front extension |
| Electronics enclosure dimensions | SSR heatsink size and PSU brick size both still nominal | Parts received (most are now in hand 2026-05-07; lay them out and finalize the project box dims) |
| SW-001 placement (rear vs front face) | Reachability vs. cable-length tradeoff | Decide once Zone-A panel orientation is fixed by motor geometry |
| Verification of <40°C inside Zone D | Depends on heat-barrier effectiveness | TP-001 — instrument enclosure interior with a TC during a soak run |
| ~~L-bracket / ballast plan for stability (M1)~~ | ~~Depends on final mass distribution~~ | **Resolved by DR-013** — threaded-rod tripod legs continuing up to a chamber clamp provide lateral tip resistance. Final rod length and clamp height set once chamber stack is assembled |
| Tripod foot positions | Depends on final extension geometry | Front pair straddle the plenum on the deck; rear pair straddle the motor on the rear extension. Final coordinates set once the angle iron is cut |

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
