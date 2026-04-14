# DR-010: Formal Design Review — v1 Fluid-Bed Coffee Roaster

**Date:** 2026-04-12
**Disposition date:** 2026-04-13
**Status:** REVIEW DISPOSITIONED — All findings addressed. A1 and A2 rejected; all others incorporated.
**Review type:** Multi-panel design review (electrical safety, thermal/airflow, firmware, mechanical, alternatives)
**Scope:** Full system architecture, firmware, BOM, and build approach

---

## Executive Summary

The design is architecturally sound and well-documented for a v1 prototype. The
air path, power domain separation, sensor strategy, and iterative philosophy are
all well-reasoned. However, five review panels identified **8 critical findings**,
**13 major findings**, and **12 minor findings** that should be addressed before
powered testing.

The three highest-priority actions are:
1. **Add a hardware watchdog** that independently de-energizes the heater if the
   ESP32 stops responding
2. **Fix the firmware safety bugs** (NAN bypass, airflow interlock, startup race,
   forced_off latch)
3. **Verify blower P-Q performance** before committing to any other component sizing

A significant simplification opportunity exists: **use the intact heat gun body
as the heater can** and **consider a PID controller for v1 controls**, deferring
the ESP32 instrumentation system to v1.5.

---

## Review Panel Reports

### Panel 1: Electrical Safety

| # | Finding | Severity | Action |
|---|---------|----------|--------|
| E1 | No hardware watchdog — ESP32 hang leaves 1500W heater energized | CRITICAL | Add external WDT (TPL5010 or MAX6369) or enable ESP32 TWDT; must independently de-energize SSR |
| E2 | `safety_reset()` unconditionally clears fault state | CRITICAL | Gate on actual temp readings below safe threshold with hysteresis |
| E3 | `forced_off` flag never cleared — heater permanently disabled after any fault | CRITICAL | `safety_reset()` must clear `forced_off` only after validating safe conditions |
| E4 | No airflow interlock — heater can run with blower off | CRITICAL | Firmware: check `blower_is_running()` minimum. Hardware: tachometer or current sense |
| E5 | 15A fuse on 15A circuit with 13A continuous load (87% of rating, NEC requires ≤80%) | MAJOR | Use 20A circuit + 12 AWG cord, or limit heater to stay under 12A continuous |
| E6 | Thermal fuse on can body, not in airstream — thermal lag may delay trip in no-airflow scenario | MAJOR | Add second thermal fuse in the heated airstream; consider lower rating (192–216°C) |
| E7 | SSR drive at 3.3V is marginal for many commodity SSRs | MAJOR | Buffer with NPN/MOSFET to drive SSR from 5V rail, or verify specific SSR input curve |
| E8 | Single-pole disconnect — if cord polarity is reversed, switch doesn't isolate heater | MAJOR | Use double-pole disconnect switch |
| E9 | Flyback diode 1N5819 rated 1A, blower draws 1-2A | MINOR | Upgrade to SS34 (3A Schottky) |
| E10 | No RC snubber on SSR output | MINOR | Add 47Ω + 0.01µF/400V X2-rated across SSR output |
| E11 | `analogWrite()` on ESP32 defaults to ~1kHz, not the 25kHz stated in schematic | MINOR | Use explicit `ledcSetup()`/`ledcAttachPin()`/`ledcWrite()` for 25kHz PWM |
| E12 | `safety_init()` calls `heater_force_off()` at boot, permanently latching the forced_off flag | MINOR | Remove `heater_force_off()` from `safety_init()` — `heater_init()` already ensures safe state |
| E13 | SPI bus noise near 1500W burst-fire switching — single glitch triggers TC fault | MINOR | Add consecutive-fault counter (e.g., 3 bad reads) before declaring fault; use shielded cable |

### Panel 2: Thermal & Airflow Engineering

| # | Finding | Severity | Action |
|---|---------|----------|--------|
| T1 | Blower P-Q performance unverified — 120mm×32mm 12V centrifugal may not deliver 13-15 CFM at 2" WC | CRITICAL | **Measure actual blower P-Q curve before committing to any other sizing** |
| T2 | Plenum single-baffle design unlikely to equalize pressure — 5-10× velocity ratio at inlet | MAJOR | Add second baffle or perforated diffusion plate inside plenum; validate in TP-001 |
| T3 | 2.5" tube L/D ratio ~1.0 risks slugging (Geldart D particles slug at L/D > 0.5-0.8) | MAJOR | 3.0" tube is better geometry (L/D ~0.57) but has thermal budget issues |
| T4 | 3.0" chamber cannot reach 200°C ΔT after 100-230W parasitic losses on 1500W heater | MAJOR | Insulate heater can and plenum; or accept 160-175°C process air (slower roasts) |
| T5 | 1.5× Umf operating margin is thin; hot-air density corrections inconsistently applied | MAJOR | Target 1.8-2.5× Umf; recompute all velocities at process temperature |
| T6 | Moisture release during roasting absorbs ~30-40W equivalent (unaccounted) | MINOR | Not fatal; document as known loss |
| T7 | Bean mass changes 12-18% during roasting, altering fluidization velocity requirements | MINOR | Monitor and adjust blower mid-roast; document expected behavior |
| T8 | 30×30 mesh may clog with chaff oils, progressively increasing back-pressure | MINOR | Plan for mid-roast mesh cleaning or use coarser mesh |

### Panel 3: Firmware Architecture

| # | Finding | Severity | Action |
|---|---------|----------|--------|
| F1 | NAN bypasses overtemp check — `NAN > 280.0f` is `false` per IEEE 754 | CRITICAL | Guard: `if (isnan(tc1) \|\| tc1 > SAFETY_MAX_PROCESS_TEMP_C)` |
| F2 | No hardware watchdog — ESP32 hang leaves SSR in last state | CRITICAL | Enable ESP32 TWDT with 2-5s timeout; feed in main loop |
| F3 | No airflow interlock in firmware | CRITICAL | Add `blower_is_running()` check to `safety_check()` |
| F4 | Startup race — all TCs start faulted, safety_check() faults immediately, forced_off latches permanently | CRITICAL | Init safety first; add startup grace period (N good reads before allowing heater) |
| F5 | `forced_off` never cleared by `safety_reset()` | MAJOR | Clear `forced_off` in `safety_reset()` only after validating conditions |
| F6 | Stale sensor data — safety checks 249ms-old data in worst case | MAJOR | Poll sensors every loop, or timestamp and reject stale readings |
| F7 | No rate-of-change detection (dT/dt) for runaway detection | MAJOR | Track previous temp; fault if rate exceeds configurable threshold (e.g., >10°C/s) |
| F8 | `safety_reset()` always succeeds — no condition validation | MINOR | Gate on actual temperatures and fault states |
| F9 | Command buffer overflow — 64-byte fixed buffer with no explicit overflow handling | MINOR | Discard input beyond 63 chars; low risk (requires physical access) |

### Panel 4: Mechanical & Fabrication

| # | Finding | Severity | Action |
|---|---------|----------|--------|
| M1 | Overall base stability — tall asymmetric assembly will tip over | CRITICAL | Widen baseplate to 20"+ in blower direction; add ballast weight; add L-brackets |
| M2 | 2-3" hole in 22ga pan wall weakens structure and deforms under hose clamp | MAJOR | Add short stub tube through hole; use two hose clamps (inside + outside) |
| M3 | Bolted ring on rolled rim — concentrates force, will crush rim at bolt holes | MAJOR | Use fender washers + backing strips; torque gently (hand-tight + ¼ turn) |
| M4 | Chamber tube held by gravity only — 12" tube will tip under vibration or bump | MAJOR | Add 3 set screws through clamping ring, or spring clips, or friction-fit gasket wrap |
| M5 | Heater can construction undefined — riskiest fabrication step | MAJOR | Build from 2.5" exhaust pipe; mount element via mica former tabs; insulate exterior |
| M6 | Expansion chamber to chamber tube transition undefined | MAJOR | Fabricate sheet metal cone reducer; hose clamp at each end |
| M7 | Pan may have organic residue/burnishing compounds | MINOR | Burn off outdoors at full temp for 10 min before first use with beans |
| M8 | Gasket: ceramic fiber sheds respirable fibers; fiberglass is safer | MINOR | Use fiberglass stove rope/tape instead of ceramic fiber |
| M9 | TC mounting needs positive sealing and strain relief | MINOR | Compression fittings (1/8" Swagelok-style, ~$3-5 each); cable tie strain relief |
| M10 | Thermal expansion at 250°C is ~0.4% on SS — non-issue with compliant gasket joints | MINOR | No action required |
| M11 | Hose clamps adequate at 2" WC — use all-stainless at temperature | MINOR | Specify all-stainless worm-drive clamps in BOM |

### Panel 5: Alternative Approaches

| # | Recommendation | Impact | Effort Saved |
|---|---------------|--------|-------------|
| A1 | **Use intact heat gun body as heater can** — skip element extraction, keep factory thermal cutout in circuit | Eliminates heater can fabrication (M5), retains independent safety device | Significant — removes riskiest fabrication and adds free safety backup |
| A2 | **Consider PID controller (Inkbird ITC-100VH, ~$30) for v1 controls** — proven over-temp protection, no firmware to debug | Defers all firmware development; removes F1-F9 as blockers to first roast | Very significant — weeks of firmware work deferred |
| A3 | **Consider borosilicate glass tube as v1 chamber** — visual feedback accelerates learning | Can see fluidization quality and roast color development in real time | Low effort change; glass tube ~$5-10 |
| A4 | **Roast on a popcorn popper first** to calibrate senses before building | Teaches fluidization feel, first-crack sound, roast progression for ~$10 | Minimal; should happen regardless |

---

## Consolidated Action Items — Priority Order

### Must Fix Before Powered Testing

1. **Hardware watchdog** (E1, F2) — Add external WDT or enable ESP32 TWDT. The
   SSR must de-energize if firmware hangs. This is the single most important safety gap.

2. **NAN bypass bug** (F1) — Add `isnan()` guard to every temperature comparison
   in `safety_check()`. 10-minute fix that prevents the most dangerous firmware bug.

3. **Airflow interlock** (E4, F3) — At minimum, check `blower_is_running()` before
   allowing heater. Better: tachometer or current sense on the blower.

4. **Startup race condition** (F4) — Reorder `setup()` to init safety first. Add
   startup grace period requiring N consecutive good TC reads before heater enable.

5. **Fix forced_off latch** (E3, F5) — `safety_reset()` must clear `forced_off`
   only after validating temps are below threshold and TCs are reading clean.

6. **Blower P-Q verification** (T1) — Get the blower, measure its actual flow vs.
   pressure curve. Everything else depends on this number.

7. **Base stability** (M1) — Design a stable base before energizing anything.
   Wider footprint, ballast weight, lateral bracing.

### Should Fix Before First Roast

8. **Fusing margin** (E5) — Resolve 15A/15A issue (use 20A circuit or limit
   continuous heater current).

9. **SSR drive buffer** (E7) — Add NPN/MOSFET buffer for reliable 5V SSR drive.

10. **Double-pole disconnect** (E8) — Replace single-pole switch with DPST.

11. **Thermal fuse placement** (E6) — Add second thermal fuse in airstream.

12. **Plenum equalization** (T2) — Plan for a second baffle; validate in TP-001.

13. **Chamber tube retention** (M4) — Set screws or clips; never gravity alone.

14. **Stub tube for plenum side-entry** (M2) — Prevent pan wall deformation.

15. **Clamping ring load spreading** (M3) — Fender washers and backing strips.

16. **Expansion chamber mounting** (M6) — Sheet metal cone reducer.

17. **Heater can build plan** (M5) — Or adopt alternative A1 (intact heat gun body).

18. **Rate-of-change detection** (F7) — dT/dt check in safety layer.

19. **Stale sensor data** (F6) — Poll sensors every loop iteration.

20. **SPI noise resilience** (E13) — Consecutive-fault counter before tripping.

### Consider for Significant Simplification

21. **Use intact heat gun as heater can** (A1) — Eliminates riskiest fabrication,
    retains factory thermal cutout as independent safety backup.

22. **PID controller for v1 controls** (A2) — Defers all firmware as a blocker to
    first roast. ESP32 system developed in parallel, swapped in for v1.5.

23. **Glass chamber for v1** (A3) — Visual feedback on fluidization and roast
    development accelerates learning significantly.

24. **Roast on a popper first** (A4) — Calibrate senses before building.

---

## Review Process

This review was conducted using a five-panel structure designed to be repeatable
at future design gates:

| Panel | Scope | Key Question |
|-------|-------|-------------|
| Electrical Safety | Power path, grounding, protection, SSR failure modes | Will this shock or electrocute someone? Will it start a fire? |
| Thermal & Airflow | Fluidization, heat transfer, pressure drops, blower sizing | Will the physics actually work? Are the calculations right? |
| Firmware | Safety logic, sensor handling, timing, fault modes | If the software fails, what happens to the hardware? |
| Mechanical | Buildability, structural integrity, thermal tolerance | Can this be built with available tools? Will it hold together? |
| Alternatives | Simpler/safer/cheaper approaches from existing practice | Are we over-engineering where a simpler solution exists? |

**To repeat this review** at DG-1 or later gates, provide the updated design
documents to each panel with the same scope questions. Focus on:
- Findings marked "validate in TP-00X" — were they validated?
- Action items from this review — were they implemented?
- New design decisions since DR-010 — do they introduce new risks?

---

## Appendix: Finding Count Summary

| Severity | Electrical | Thermal | Firmware | Mechanical | Total |
|----------|-----------|---------|----------|------------|-------|
| CRITICAL | 4 | 1 | 4 | 1 | **10** |
| MAJOR | 4 | 4 | 3 | 5 | **16** |
| MINOR | 5 | 3 | 2 | 5 | **15** |
| **Total** | **13** | **8** | **9** | **11** | **41** |

Note: Some findings overlap between panels (e.g., hardware watchdog appears in
both Electrical and Firmware panels). The consolidated action list de-duplicates these.
