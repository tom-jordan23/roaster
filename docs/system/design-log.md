# Design Log

Running record of design decisions, findings, and rationale. Newest entries first.

---

## 2026-05-05 — DR-013 tangential-entry plenum variant for A/B test

### Decision

**Cut two plenum bodies from the same stovepipe scrap and A/B test inlet
geometry:**

- **Plenum A (baseline):** radial side inlet + DR-009 wall-mounted deflector
  ramp opposite the inlet. Spec unchanged from DR-012.
- **Plenum B (variant):** tangential side inlet, no internal ramp. Inlet jet
  enters along the wall to induce swirl; plenum volume + swirl handle jet
  dissipation in place of the DR-009 spoiler.

Both bodies cut to identical 8" dia × 6" tall so inlet geometry is the only
variable. Same caps, same DR-008 clamp ring, same distributor plate.

### Rationale

The DR-012 ramp is a known-good jet spoiler but the 7× plenum:chamber volume
ratio gives us margin to try a more aerodynamic alternative. Swirling
fluidized bed (SFB) literature reports better radial mixing and more uniform
bed temperature with tangential entry; cyclone separators and the West Bend
Poppery's accidentally-tangential blower discharge are familiar analogues.
With abundant scrap on hand, A/B is cheaper than picking blind.

Test variable: fluidization uniformity at the bean bed (visual + bed
temperature spread if we have multiple probes by then). Decision criterion:
visibly more uniform bed motion or measurably tighter bed-temp spread →
tangential wins for v2; otherwise stick with the ramp.

### Fabrication note — tangential is not just an offset hole

A hole saw cuts perpendicular to the local wall surface, so positioning the
hole off-center on the cylinder circumference still produces a **radial**
stub. Three options for genuine tangential entry, in increasing fab effort:

1. **Angled hole-saw cut.** Pilot perpendicular for bite, then tilt the saw
   toward tangent as it cuts through. Hole comes out elongated; seal the
   stub joint with high-temp RTV. Selected for plenum B — adequate for an
   A/B and reversible-ish.
2. **Flat-and-flange.** Cut a rectangular window on the tangent line, rivet
   a small sheet-metal flange flat to it, mount the stub perpendicular to
   the flange. Reserved for v2 if tangential wins.
3. **Internal turning vane.** Drill radial, add a curved sheet-metal vane
   inside that turns the flow tangential. Vane sees full hot jet — gauge
   accordingly. Not selected; defeats the goal of testing pure tangential.

### Status

Plenum A and B to be cut from the same stock so wall thickness / oxide layer
match. Cure burn (DR-012 M7) before assembly applies to both. Document
which is which with a punch mark or paint dot — visual cues are easy to
forget after the caps go on.

---

## 2026-05-02 — DR-008 ring geometry correction (Option A)

PLEN-002 / PLEN-003 specs had ring ID equal to plate dia (both 2.37" for the
2.5" chamber pair; both 2.87" for the 3.0" pair). Geometrically inconsistent —
with ring ID = plate dia, the plate has no rest surface and would fall through.

**Corrected (Option A — plate sits inside chamber bottom):**

- Top cap hole = chamber OD (2.5" / 3.0") — chamber slides through with slip fit.
- Ring mounted to **underside** of the cap face. Ring ID < chamber ID:
  **2.0" for the 2.5" pair, 2.5" for the 3.0" pair.** Ring's inner face
  protrudes ~0.25" inward of the cap hole as an annular ledge.
- Plate dia = chamber ID (PLATE-001A 2.37" / PLATE-001B 2.87"); drops inside
  the chamber from above and lands on the ring face.
- Chamber bottom rim sits on the same ring face around the plate edge —
  for the 2.5" chamber, the rim's outer edge (R = 1.25") aligns with the cap
  hole edge and the rim's inner edge (R = 1.185") meets the plate edge.

Plate-to-chamber-wall is slip fit. Leak path around the plate edge is
negligible compared to the deliberate distributor perforations.

**Plate float watch (TP-001 add):** at the design dP across the plate
(~1" WC ≈ 250 Pa) over the 2.37" plate area, upward force is ~0.5 kgf —
greater than the plate's own ~50 g weight. With beans loaded, the bed pins
the plate; **at startup or empty operation, the plate may float and bypass
the bed.** Watch for this in TP-001; mitigation options if it happens are a
chamber-wall pin through the plate edge, a heavier plate, or a small lip
riveted to the ring.

**Fastening:** Ring is 1/8" SS plate with 3 tapped M4 holes on a bolt circle
outside the cap drill. Machine screws descend from above through the cap
face into the ring threads. No nuts inside the plenum — preserves the
DR-008 ring + plate swap without breaking the DR-012 bottom-cap RTV seal.

PLEN-002, PLEN-003, architecture.md §8 Top Assembly table updated.

---

## 2026-05-02 — DR-012 plenum body: round stovepipe replaces SS steam pan

### Decision

**DR-012: Replace 1/6 SS steam table pan (DR-007) with 8" diameter × 6" tall
black-stovepipe section, both ends pipe-capped.** The bolted-clamp-ring
assembly (DR-008) and deflector ramp baffle (DR-009) carry over with mounting-
substrate changes only. Architecture.md §8 and baseplate-layout.md §1, §3.5,
§6 updated; BOM PLEN-001, PLEN-004, BAFFLE-001 updated.

### Rationale

Black single-wall stovepipe scrap became available at zero cost, displacing
the steam-pan plan (PLEN-001, $4-8 + thrift hunt). The change also resolves
a long-standing geometric awkwardness — a rectangular plenum under a round
chamber.

Diameter sized at **8"**:

| Dia | Floor area | Plenum:chamber (3" chamber) | Verdict |
|-----|-----------|------------------------------|---------|
| 6"  | 28 in²    | 4×                           | Marginal — DR-009 ramp has only 1.5" annular margin |
| 8"  | 50 in²    | 7×                           | ✓ Selected — past textbook 3-5× ratio, fits 6×7" Zone-C budget |
| 10" | 79 in²    | 11×                          | Diminishing returns; +50% wall area = more parasitic loss + insulation |

Height set at **6"** by stacking constraints:
- ≥1× inlet diameter (~2.5") between inlet centerline and distributor plate
  for jet dissipation
- ≥2" between inlet centerline and floor for the DR-009 ramp to develop
- +1" headroom for the optional T2 secondary perforated baffle without
  redesign

### Material — black stovepipe specifically

Bare / oxide-blackened mild steel, ~26 ga, rated ~1000°F continuous
(single-wall stove duty). Plenum operates 150-200°C — massively under-spec.

**Excluded materials:** galvanized HVAC duct (zinc outgases at ~390°F /
200°C, exactly where we operate; metal-fume risk in air that passes through
the bean bed before the chimney). Aluminized furnace-plenum pipe would also
be acceptable but stovepipe was on hand.

**Cure burn before assembly** (M7, carried over from PLEN-001 notes): cheap
stovepipe ships with a thin rolling-oil film that smokes off on first heat.
Burn outdoors with a propane torch until smoke stops, before any food-path
roasting.

### Mechanical assembly

The pipe caps double as the structural top and floor — the cap's crimped
skirt seals to the pipe and the flat cap face provides the riveting / bolting
substrate that the steam-pan rim previously gave us:

```
              Chamber tube (2.5" or 3.0" OD SS)
                    │
       ┌────────────┴────────────┐
       │  Top cap: drilled to    │  ← clamp ring (PLEN-002/003) attaches to
       │  chamber OD, ring       │     underside of cap face around the hole
       │  attached underneath    │
       ├─────────────────────────┤
       │                         │
       │     ◊  T2 perf baffle   │  ← future, ~1" below distributor
       │                         │
   ────┤   8" dia × 6" tall      │  ← side-entry stub (PLEN-005),
       │   black stovepipe       │     2.5" hole-saw through wall
       │                         │
       │     ╲                   │
       │      ╲ Deflector ramp   │  ← DR-009, pop-riveted opposite inlet
       │       ╲                 │
       └─────────────────────────┘
              Bottom cap                ← crimped + high-temp RTV + 3 sheet-
                                          metal screws / rivets through skirt
              ↑ 6"
```

- **Top cap:** 2.5" or 3.0" hole drilled to chamber OD; clamp ring on
  underside. **Use M4/M5 machine screws + nyloc nuts, not pop rivets**, so
  the ring + plate pair remains swappable per DR-008. Pop rivets are an
  acceptable one-and-done alternative if v1 commits to a single chamber size.
- **Bottom cap:** slip-fit, sealed at seam with high-temp RTV, retained with
  3 sheet-metal screws or rivets through the cap skirt.
- **Side-entry hole:** 2.5" bi-metal hole saw through the cylindrical wall,
  sized to PLEN-005 stub OD.
- **Snap-lock seam:** if a section is cut from a longer length, lock the
  seam at the cut with a sheet-metal screw so it can't spring open.

### DR-008 / DR-009 carry-over

- **Clamping ring (DR-008):** unchanged spec; attaches to underside of top
  cap face instead of pan flange. Still gasket-sealed via PLEN-004.
- **Deflector ramp (DR-009):** unchanged 3"×4" SS bent to 45°; pop-riveted
  to the cylindrical wall opposite the inlet. Curved wall vs. flat pan wall
  is immaterial — the ramp seats on a chord and the small standoff at the
  edges does not affect jet redirection.

### Cost impact

PLEN-001: $4-8 → $0 (scrap pipe + 2 caps; ~$6 retail if not on-hand).

---

## 2026-05-02 — Sourcing update: baseplate stock + heat gun in hand

- **BASE-001 sourced:** 12" × 24" steel sheet + 1"-class angle iron acquired.
  Sheet is 4" longer than the 20" SCAD assumption (baseplate-layout.md §1),
  giving real Zone-A margin for the vertical-axis vacuum motor (DR-011)
  rather than the borderline 190 mm overhang the prior dimension implied.
  Angle iron earmarked for perimeter stiffening — 12×24" sheet steel of this
  gauge will flex; angle along the long edges plus cross-members at zone
  boundaries gives bending stiffness without ballast. Final framing layout
  deferred until motor footprint is measured.
- **HTR-001 sourced:** Warrior 1500W heat gun (SKU 56434) in hand. Teardown
  is the next mechanical task: measure element resistance (target ~9.6 Ω
  cold for 1500 W / 120 V at room temp), photograph mica former dimensions
  and mounting-tab geometry, identify intake/exhaust footprint. Outputs feed
  HTR-CAN-001 build dimensions and the Zone-B 190 mm placeholder in
  baseplate-layout.md §1.

---

## 2026-04-29 — DR-011 blower upgrade: vacuum motor + TRIAC

### Decision

**DR-011: Replace 12V DC centrifugal blower (DR-003) with bypass-cooled
salvaged universal-AC vacuum motor + TRIAC speed control.** Architecture.md §3
rewritten; BOM, sourcing notes, power schematic, and block diagram updated.

### Rationale

T1 (architecture.md §3) flagged that the Wathai 120 × 32 mm 12 V centrifugal
blower (BLW-001, B08P1S5DBN) had an unverified P-Q curve at the system
operating point. On closer review, blowers of this physical size shut off
around 1.0–1.5" WC and deliver only 0.3–0.6" WC at the 12–18 CFM operating
point — below the 1.5–2.5" WC system minimum and with no margin for chaff
mesh loading (T8), distributor-plate variation, or the deeper bed in the 2.5"
chamber. This was a genuine blocker, not a paper one.

Three upgrade paths considered:
1. **Bypass-cooled vacuum motor + TRIAC** ($0–10 salvage, 20–80" WC headroom).
   Cost: AC complexity (zero-cross + TRIAC), brushed-motor EMI, larger
   envelope. ✓ Selected.
2. **24V high-pressure DC centrifugal** (Delta BFB1024-class + driver, $25–50,
   2–4" WC). Keeps everything LV-side. ✗ Conflicts with DR-001 cost target.
3. **Two 120 × 32 mm blowers in series** (~$15–20 incremental). Sums pressure
   but stalls in two places, no real headroom. ✗ Insufficient margin.

### Architecture changes

- **Air system:** unchanged (serial path).
- **Power domains:** Domain 2 changes from 12V DC to mains AC + TRIAC. PSU-002
  (12V/3A) deleted. Mains load increases by ~1–4 A (vacuum motor draw) — still
  within the 15A circuit budget alongside the heater (~12.5 A) only if the
  blower is run at modest duty during heating; verify total draw at TP-001.
- **Control:** ESP32 GPIO 23 reassigned from MOSFET PWM to TRIAC PWM input.
  GPIO 4 added for zero-cross interrupt. GPIO 34 added for ZMCT103C current
  sense (airflow interlock).
- **Safety:** `blower_is_running()` switches from PWM-duty inspection to
  CT RMS threshold. New FAULT_CT_OPEN if commanded-on with no current.
- **EMI:** Snap-on ferrites on all TC SPI cables (E13 cable shielding becomes
  necessary but not sufficient). Line filter on motor leads.
- **Grounding:** Motor frame bonded to mains earth (universal motors have
  nontrivial leakage current — bonding is safety-critical).

### Bypass-cooled is non-negotiable

Flow-through (single-stage) shop-vac motors cool the brushes with the working
airstream and shed brush carbon into it. Coffee application requires a
**bypass / two-stage** motor where a dedicated cooling impeller is isolated
from the working impeller. Inspect candidate motors and confirm the two
airpaths are separate before committing.

### BOM impact

| Action | BOM line | Notes |
|--------|----------|-------|
| Modified | BLW-001 | Now: salvaged bypass-cooled vacuum motor, $0–10, status Thrift hunt |
| Deleted | PSU-002 | 12V/3A supply no longer needed |
| Deleted | Q1-001, R1-001, R2-001, D1-001 | MOSFET drive, gate resistors, flyback diode (12V blower drive parts) |
| Added | BLW-CTRL-001 | RobotDyn-style TRIAC dimmer module, 8A, ZC detect, ~$5–10 |
| Added | CT-001 | ZMCT103C 5A split-core current transformer, ~$3–8 |
| Added | FERR-001 | Snap-on ferrite chokes (set of 5–10), ~$5 |
| Added | FILT-001 | AC line filter / X+Y cap module on motor leads, ~$3–6 |
| Added | BOND-001 | Motor frame bonding lug + ring terminal, ~$1 |

Net cost impact: roughly neutral to slightly cheaper depending on the salvage
luck on the motor itself.

### Pending follow-on work — gated on parts in hand

**Hold all firmware and mechanical-fit work until the salvaged motor + the
DR-011 control kit (TRIAC dimmer, ZMCT103C, line filter, ferrites) are
physically on the bench.** The control-side details (PWM frequency / phase
math, CT burden value, ADC range, EMI envelope) depend on the actual hardware
and will be re-evaluated then. Re-open this entry as the trigger.

1. **Salvage hunt FIRST:** bypass-cooled motor from Habitat ReStore / curb /
   junk shop vac. Inspect dual-airpath separation before committing.
2. **Order DR-011 control kit:** validate ASINs for BLW-CTRL-001 (TRIAC
   dimmer), CT-001 (ZMCT103C), FILT-001 (line filter), FERR-001 (ferrites)
   per `bom/sourcing-notes.md` "Pending validation" table.
3. **Firmware (gated):** rewrite `blower.c` for phase-angle TRIAC drive off the
   zero-cross ISR; rewrite `blower_is_running()` against the CT ADC.
   Re-evaluate pin assignments, PWM strategy, and CT thresholding with the
   real boards in hand.
4. **SCAD model (gated):** the 150 mm × 200 mm best-estimate vacuum-motor
   envelope is a placeholder. Re-measure once a real motor is in hand.
5. **TP-001 update (gated):** P-Q characterization (formerly a critical gate)
   becomes "find the operating duty-cycle range." The motor will exceed
   system requirements at 100%; the question is where to operate it.

### What changed from previous decisions

- DR-003 (separate 12V brushless blower, MOSFET + PWM) — **superseded**.
  The "$15 over a thrift find buys us LV-only simplicity" trade was the wrong
  call once the P-Q gap became evident.
- DR-004 (three power domains: 120V AC heater, 12V DC blower, 3.3V DC
  controls) — **revised to two power domains**: 120V AC (heater + blower) and
  3.3V/5V DC (controls). The blower moves up to mains.
- E11 (LEDC PWM at 25 kHz for blower) — superseded; the new blower driver is
  phase-angle TRIAC, not high-frequency PWM. The 25 kHz LEDC infrastructure
  in firmware can be deleted.
- E9 (SS34 flyback diode upgrade) — moot; no flyback needed without the DC
  blower.

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
