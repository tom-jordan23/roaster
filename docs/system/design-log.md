# Design Log

Running record of design decisions, findings, and rationale. Newest entries first.

---

## 2026-04-13 — DR-010 formal design review response

### Summary

Formal design review (DR-010, 2026-04-12) produced 41 findings across 5 panels:
10 critical, 16 major, 15 minor. All findings accepted and incorporated except
two alternative-approach recommendations that were explicitly rejected.

### Rejected alternatives

1. **A1 REJECTED: Use intact heat gun body as heater can.** The heat gun housing
   will not be retained. The element will be extracted and mounted in a purpose-built
   heater can (2.5" SS exhaust pipe). Rationale: retaining the plastic housing
   limits thermal design flexibility, complicates mounting geometry, and the factory
   thermal cutout can be replaced by THFUSE-001 and THFUSE-002.

2. **A2 REJECTED: Use PID controller (Inkbird ITC-100VH) for v1 controls.** The
   ESP32-based control stack is retained for v1. Rationale: the ESP32 system
   provides data logging, multi-sensor monitoring, serial command interface, and
   future automation capability that a standalone PID controller cannot. The
   firmware safety bugs identified in DR-010 have been fixed directly.

### Accepted alternatives

3. **A3 ACCEPTED: Borosilicate glass tube as v1 chamber option.** Added to BOM as
   CHAM-001C. Will be tested alongside SS tubes in TP-001. Visual feedback on
   fluidization quality and roast development is valuable for the learning phase.

4. **A4 ACCEPTED: Roast on a popcorn popper first.** Added to BOM as POPPER-001.
   Calibrate operator senses (first-crack sound, roast progression, fluidization
   feel) before commissioning the custom roaster.

### Critical fixes implemented (firmware)

5. **F1: NAN bypass in over-temp check.** Added `isnan()` guard to every temperature
   comparison in `safety_check()`. NAN now triggers fault (fail-safe).

6. **E1/F2: Hardware watchdog.** Enabled ESP32 Task Watchdog Timer (TWDT) with
   5-second timeout. Fed every loop iteration. If firmware hangs, ESP32 resets —
   GPIO defaults to input/low on reset, de-energizing the SSR.

7. **E4/F3: Airflow interlock.** `safety_check()` now verifies `blower_is_running()`
   before allowing heater operation. Heater command with blower off triggers
   FAULT_AIRFLOW.

8. **F4: Startup race condition.** Safety system starts in new STARTUP state.
   Requires SAFETY_STARTUP_GOOD_READS (5) consecutive clean TC reads before
   transitioning to OK and allowing heater. Init order changed: safety_init()
   runs first.

9. **E3/F5: forced_off latch fix.** Added `heater_clear_forced_off()` function.
   `safety_reset()` clears the forced_off flag only after validating all TCs are
   reading valid and all temps are below SAFETY_RESET_TEMP_C (100°C).

10. **E12: safety_init() no longer calls heater_force_off().** This was prematurely
    latching the forced_off flag at boot. heater_init() already ensures GPIO is LOW.

### Major fixes implemented (firmware)

11. **E2/F8: safety_reset() now validates conditions.** Reset requires all TCs
    reading valid, all temps below 100°C. No longer unconditionally succeeds.

12. **F6: Stale sensor data rejection.** Sensors track last-update timestamp via
    `sensors_get_age_ms()`. Safety faults if data is older than 500ms.

13. **F7: Rate-of-change detection (dT/dt).** Safety tracks TC1 rate of change.
    Faults if rate exceeds 10°C/s (SAFETY_MAX_RATE_C_PER_S). New FAULT_RATE state.

14. **E13: Consecutive fault counter for SPI noise resilience.** Single bad SPI read
    no longer triggers TC fault. Requires SAFETY_CONSEC_FAULTS_TRIP (3) consecutive
    bad reads. Prevents false faults from EMI near 1500W burst-fire switching.

### Minor fixes implemented (firmware)

15. **E11: Proper LEDC PWM for blower.** Replaced `analogWrite()` (default ~1kHz)
    with explicit `ledcSetup()`/`ledcAttachPin()`/`ledcWrite()` at 25kHz. Above
    audible range, appropriate for brushless DC motor.

16. **F9: Command buffer overflow.** Already bounded by `cmd_pos < sizeof(cmd_buffer) - 1`
    check — characters beyond capacity silently discarded. Added clarifying comment.

### Electrical schematic changes

17. **E5: Fusing margin documented.** 12.5A continuous on 15A circuit is 83% (NEC
    requires ≤80% for continuous). Options documented: use 20A circuit, limit duty,
    or accept for bench testing.

18. **E6: Second thermal fuse (THFUSE-002).** Added 192–216°C thermal fuse in the
    heated airstream (lower rating, lower thermal lag than can-body fuse).

19. **E7: SSR drive buffer.** Added NPN transistor (2N2222) to buffer 3.3V GPIO to
    5V for reliable SSR triggering. Added Q2, R3 to schematic and BOM.

20. **E8: Double-pole disconnect.** SW-001 changed from SPST to DPST — switches
    both L and N to protect against reversed cord polarity.

21. **E9: Flyback diode upgrade.** D1 changed from 1N5819 (1A) to SS34 (3A) — blower
    draws 1-2A, 1A rating had insufficient margin.

22. **E10: RC snubber.** Added 47Ω + 0.01µF/400V X2-rated across SSR output.
    Suppresses inductive voltage spikes.

### Thermal/airflow documentation updates

23. **T1: Blower P-Q verification.** Documented as critical blocker in architecture.md.
    Must measure actual P-Q curve before committing to sizing.

24. **T2: Second plenum baffle.** Documented plan for second equalization stage if
    TP-001 shows single ramp insufficient. Added to block diagram air path.

25. **T3: L/D ratio slugging risk.** Documented in architecture.md — 2.5" chamber
    L/D ~1.0 exceeds Geldart D slugging threshold. 3.0" chamber (L/D ~0.57) is
    safer.

26. **T4: Insulation requirements.** 3.0" chamber cannot reach target temps without
    insulating heater can and plenum. Documented in architecture.md.

27. **T5: Umf operating margin.** Revised from 1.5× to 1.8–2.5× Umf. All airflow
    calculations updated for hot-air density. CFM requirements increased.

28. **T6-T8: Known thermal losses.** New section in architecture.md documenting
    moisture release (~30-40W), bean mass change (12-18%), and mesh clogging risk.

### Mechanical updates

29. **M1: Base stability.** Baseplate widened to 20"×12" in OpenSCAD model. Added
    BASE-001 to BOM with ballast and L-bracket requirements.

30. **M2: Plenum side-entry stub tube.** Added PLEN-005 to BOM — short SS tube stub
    through pan wall to prevent deformation under hose clamp.

31. **M3: Clamping ring load spreading.** Fender washers and backing strips specified
    in BOM notes for PLEN-002, PLEN-003, and FAST-001.

32. **M4: Chamber tube retention.** Added CHAM-RET-001 to BOM — set screws or spring
    clips through clamping ring. Never gravity alone.

33. **M5: Heater can build plan.** Added HTR-CAN-001 to BOM — build from 2.5" SS
    exhaust pipe, mount element via mica former tabs, insulate exterior.

34. **M6: Expansion chamber cone reducer.** Added EXH-004 to BOM — sheet metal cone
    from chamber OD to 4" expansion chamber, hose clamp at each end.

35. **M7: Pan burn-off.** Added note to PLEN-001 — burn off outdoors at full temp
    for 10 minutes before first use with beans.

36. **M8: Fiberglass gasket.** PLEN-004 changed from ceramic fiber to fiberglass
    stove rope/tape. Ceramic fiber sheds respirable particles.

37. **M9: TC compression fittings.** Added TC-FIT-001 to BOM — 1/8" Swagelok-style
    compression fittings for positive TC sealing and strain relief.

38. **M11: All-stainless hose clamps.** EXH-003 quantity increased, spec changed to
    all-stainless worm-drive (not zinc-plated) for temperature tolerance.

### BOM impact

BOM grew from 36 to 47 line items. New items added:
- THFUSE-002, Q2-001, R3-001, R-SNB-001, C-SNB-001 (electrical)
- CHAM-001C, PLEN-005, CHAM-RET-001, BASE-001, HTR-CAN-001, EXH-004, TC-FIT-001 (mechanical)
- POPPER-001 (reference/calibration)

Estimated cost impact: +$25-45, bringing target BOM to ~$75-125.

### Next actions

1. Source popcorn popper and do calibration roasts (A4)
2. Buy Warrior heat gun, tear down, measure element (unchanged)
3. Order 12V blower and **verify P-Q curve** (T1 — critical gate)
4. Order electronics including new buffer and snubber components
5. Build stable baseplate before any powered testing (M1)
6. Run TP-001 with both SS tubes and glass tube option

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
