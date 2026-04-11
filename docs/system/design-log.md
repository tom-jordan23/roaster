# Design Log

Running record of design decisions, findings, and rationale. Newest entries first.

---

## 2026-04-11 — Plenum, baffle, and mechanical assembly decisions

### Decisions made

1. **DR-007: 1/6 size SS steam table pan as plenum body.** A standard 1/6 size,
   4" deep stainless steel steam table pan (~6.4" x 6.3" x 4") from restaurant
   supply, $4-8. 18/8 stainless, food-safe, rated for sustained heat. Provides
   generous volume for pressure equalization. Pan oriented right-side-up (open
   top faces up).

2. **DR-008: Bolted clamping ring assembly, no welding.** The distributor plate
   and roast chamber are held by a flat SS ring bolted across the pan rim with
   3-4 bolts through the flange. The ring's inner hole is sized to seat the
   distributor plate and the chamber tube. Swapping between 2.5" and 3.0"
   chambers means swapping the ring + plate pair. High-temp gasket material
   (fiberglass or ceramic fiber) between ring and pan rim for sealing.

   This resolves open question #6 (plenum adapter design): mechanical clamping
   ring, not welded adapter or stepped seat.

3. **DR-009: Deflector ramp baffle.** A single piece of SS sheet metal, bent to
   ~45°, mounted opposite the side-entry hole inside the plenum. Redirects the
   inlet jet downward toward the pan floor; air spreads across the full floor
   area then rises uniformly toward the distributor plate. Bolted or riveted
   in place.

   If TP-001 shows uneven fluidization, a horizontal perforated baffle can be
   added as a second equalization stage ~1" below the distributor plate. This
   is a future option, not built into v1 initially.

### Assembly concept (no welding required)

```
    ┌──── Roast Chamber Tube ────┐
    │    (sits inside ring)       │
    ├─────────────────────────────┤
    │    Distributor Plate        │  ← Perforated disc, rests on clamping ring
    ├─────────────────────────────┤
    │    Clamping Ring + Gasket   │  ← Bolted to pan rim (3-4 bolts)
    ╞═════════════════════════════╡  ← Pan rim/flange
    │         ╲                   │
    │          ╲ Deflector ramp   │  ← 45° bent SS, bolted opposite inlet
    │           ╲                 │
    ○ ← Side-entry from heater   │
    │                             │
    └─────────────────────────────┘
```

Tools required: drill, step bit or hole saw, tin snips, vise, wrench.
No welding, no brazing, no special fabrication.

### Open questions resolved

- Plenum adapter design (architecture.md Q6): **Resolved.** Bolted clamping
  ring with swappable ring + plate pairs for each chamber size.

---

## 2026-04-11 — Cooling, chaff collection, and air system design decisions

### Decisions made

1. **DR-005: Blower-only cooling cycle, no bypass damper for v1.** After SSR
   cutoff the heater can retains ~13-23 kJ of thermal energy. At 10-15 CFM
   forced convection, this dissipates in ~15-30 seconds — short enough that
   blower-only cooling (heater off, blower 100%) will bring 113g of beans from
   ~200°C to <50°C within 100-140 seconds. This is within the industry target
   of 90-150 seconds for small batches. A bypass damper or separate air paths
   are deferred until TP-002 cooldown data proves they're needed.

   **Mechanical hedge:** The blower-to-heater-can joint should use a hose clamp
   connection (not welded) so the heater can be physically disconnected for
   bypass cooling if thermal lag is worse than estimated.

   **Firmware addition:** A `COOL` command — sets heater to 0%, blower to 100%,
   logs cooldown curves, and notifies operator when TC2 < 50°C.

2. **DR-006: Expansion chamber + mesh screen for chaff collection.** 113g of
   green coffee produces ~0.5-0.9g of chaff, mostly at first crack. A removable
   expansion chamber at the exhaust captures chaff by velocity reduction:
   - ~4" OD × 5" tall stainless cylinder (step-up from roast chamber diameter
     drops air velocity to 2-4 ft/sec, chaff settles out)
   - 30×30 stainless mesh screen inside the top as a secondary capture plate
   - Removable for tap-and-empty cleaning between roasts
   - Negligible backpressure impact on fluidization

   This matches the proven approach used in Fresh Roast SR series and popcorn
   pumper conversions. A cyclone separator is overkill at 113g scale and adds
   significant backpressure.

### What changed from previous session

- Exhaust path is now explicitly a two-stage system: expansion chamber (chaff
  drops out) then mesh screen (secondary capture), both in a removable unit.
- Cooling is a defined operating mode, not just "turn the heater off."
- Heater can joint specified as hose clamp (not permanent) to preserve bypass
  option for future.

---

## 2026-04-11 — Heating and blower design decisions

### Decisions made

1. **DR-002: Warrior heat gun as heater element donor.** Harbor Freight Warrior
   1500W dual-temp heat gun (SKU 56434, ~$10) selected as the heating element
   source. Nichrome coil on mica former, 1000°F max, 11.25A at 120V. At $10
   this is essentially parts cost for the nichrome wire, mica former, and
   thermal cutout. Replaces the earlier "thrift store hair dryer" plan — the
   Warrior is cheap enough to buy new and has predictable, documented specs.

2. **DR-003: Separate 12V brushless blower, not scavenged AC motor.** The heat
   gun's built-in axial fan lacks the static pressure to fluidize a bean bed.
   A separate centrifugal blower is required. Selected a 12V brushless DC
   centrifugal blower (~$15-20, e.g. WDERAIR 120mm x 32mm) over a scavenged
   hair dryer universal motor. The 12V option costs ~$15 more than a thrift
   store find but keeps the blower on the low-voltage side, eliminating AC
   triac control complexity entirely.

3. **DR-004: Three explicit power domains.** The system has three power rails:
   - 120V AC mains → heating element via SSR
   - 12V DC → blower via MOSFET (from AC-DC switching PSU, 12V/3A sufficient)
   - 3.3V DC → ESP32 and sensors (USB or regulator)

   This cleanly separates mains-voltage control (SSR only) from low-voltage
   control (MOSFET PWM for blower, SPI for sensors, GPIO for everything).

### What changed from kickoff

- Hair dryer as combined heater+blower donor → split into dedicated heat gun
  element + dedicated 12V blower. Better for independent control, simpler
  electronics, small cost increase (~$25 vs ~$5).
- Blower driver changed from "TRIAC or DC, TBD" → definitively 12V DC via
  MOSFET + PWM from ESP32. No AC motor control needed on the blower side.
- 12V PSU moves from "only if DC blower" contingency to required BOM item.

### Open questions resolved

- Heater element sourcing (architecture.md Q2): **Resolved.** Warrior heat gun.
- Blower sourcing (architecture.md Q3): **Resolved.** 12V brushless centrifugal,
  MOSFET + PWM control.

---

## 2026-04-10 — Project kickoff and cost strategy

### Decisions made

1. **DR-001: Thrift-first cost strategy adopted.** Design around cheap available
   parts rather than specifying ideal parts and paying catalog prices. Target
   v1 BOM of $50-80. Full rationale in `design-reviews/DR-001-cost-strategy.md`.

2. **Dual chamber test approach.** Sourcing both 2.5" OD and 3.0" OD standard
   SS exhaust tube. The 2.5" gives significantly better thermal performance on
   120V (~1000W for ΔT=200°C vs ~1500W), but has a deeper bean bed (~6 cm vs
   ~4 cm) that may make fluidization harder. TP-001 will determine the winner.

3. **Hair dryer / heat gun as heater + blower donor.** A thrift store hair dryer
   ($2-5) provides both the ~1500W heater element and a matched blower motor.
   This collapses the two most expensive component selections into one cheap
   purchase. The heater can will be designed around the salvaged element geometry
   rather than the other way around.

4. **Design-to-available-parts sequence.** Because geometry depends on what parts
   we actually find, the build sequence is:
   - Source hair dryer → measure element → design heater can
   - Source plenum container → measure it → design baffles to fit
   - Source chamber tubes → confirm OD/ID → design plate and mounting
   - Order electronics (spec-driven, geometry-independent)
   - Final mechanical integration design after all parts are in hand

### Architecture established

- Repository structure created across 6 workstreams (system, mechanical,
  electrical, firmware, test, BOM/build)
- System block diagram with air, power, signal, and data paths
- Power/airflow budget calculations for both chamber sizes
- ESP32 firmware scaffold with safety, sensor, heater, blower, control,
  logging, and command modules
- 6 test plans covering airflow through first roast commissioning
- BOM with 25 line items and realistic cost estimates

### Open questions

- ~~Heater element: need to find and tear down a hair dryer to get real dimensions
  and measured wattage~~ **Resolved (DR-002):** Warrior heat gun, SKU 56434
- ~~Blower: is the hair dryer fan independently usable and speed-controllable?
  If not, a $10-15 12V brushless from Amazon is the fallback~~ **Resolved (DR-003):**
  12V brushless centrifugal, MOSFET + PWM control
- Plenum: need to find a suitable SS container and check thermal tolerance
- Plenum adapter: how to mount both 2.5" and 3.0" chamber tubes on the same
  plenum (adapter ring is the likely approach)
- Touchscreen UI: user has a 5x7" touchscreen LCD available. May add a
  Raspberry Pi as a UI tier above the ESP32 control layer. Interface type
  (HDMI, SPI, DSI) needs to be determined.

### Next actions

1. Buy Warrior heat gun from Harbor Freight (SKU 56434)
2. Tear down heat gun and document element resistance, dimensions, thermal cutout
3. Order 12V blower, MOSFET (IRLZ44N), flyback diode, 12V PSU (if not in junk drawer)
4. Order electronics (ESP32, MAX31855 x3, SSR, TCs, perforated SS sheet)
5. Source 2.5" and 3.0" SS exhaust pipe
6. Thrift store: SS containers for plenum
7. Once parts are in hand: mechanical integration design
