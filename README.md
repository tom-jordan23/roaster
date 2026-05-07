# Fluid-Bed Coffee Roaster

A purpose-built small electric fluid-bed coffee roaster designed for 1/4 lb (113g) batches on 120V AC. Built as an engineering instrument and learning platform — manual operation first, closed-loop automation later.

## What This Is

A ground-up roaster design with:
- Stainless steel roast chamber with a round stovepipe plenum and side-entry heated air (DR-012)
- Distributor plate and internal baffles for uniform fluidization
- Three K-type thermocouples (process air, bean bed, exhaust)
- ESP32-based control with zero-cross SSR heater switching
- Serial command interface for manual control
- Artisan-compatible data logging
- Safety interlocks that are always authoritative

This is **not** a popcorn popper mod. It's a purpose-built fluid-bed architecture designed
to produce real roast data and evolve into a closed-loop system — built on the cheap
using thrift store finds, salvaged parts, and Amazon generics wherever possible.

## Project Status

**Phase 1 — Subsystem build (parts in hand).** Repository structure, system
architecture, power/airflow budgets, firmware scaffold, and full-design-review
disposition (DR-010) all complete. As of 2026-05-07, all major parts are in
hand: Warrior heat gun (HTR-001) torn down with element measured 1.5"×6";
salvaged bypass-cooled vacuum motor (BLW-001) measured 6"×6" cylindrical;
DR-011 control kit (TRIAC dimmer, ZMCT103C CT, line filter, ferrites);
8" stovepipe plenum body + caps (DR-012); 12"×24" steel sheet cut to
12"×18" deck with the remainder feeding the angle-iron frame extensions
(DR-013 tripod legs). Next: heater-can fabrication, plenum cure-burn,
frame extension build, electronics tray assembly, then TP-001 commissioning.

## Repository Structure

```
docs/
  system/          System block diagrams, architecture, design reviews
  mechanical/      Chamber, plenum, distributor plate, exhaust design
  electrical/      Schematics, power distribution, interlocks
  software/        Firmware architecture, Artisan integration, safety logic

firmware/          ESP32 PlatformIO project
  src/             Safety, sensors, heater, blower, control, logging, command
  test/            Unit tests (Unity framework)

bom/               Bill of materials and sourcing notes
test/plans/        Test plans TP-001 through TP-006
build/             Build instructions and progress photos
```

## Architecture Overview

### Air Path
```
Ambient → Blower → Heater Can → Plenum (side-entry) → Baffles → Distributor Plate → Chamber → Exhaust
```

### Control Stack
```
ESP32 ← 3x MAX31855 (TC1, TC2, TC3)
ESP32 → Zero-cross SSR (heater duty cycle)
ESP32 → Blower driver (speed control)
ESP32 → Serial/USB → Host PC (Artisan logging)
```

### Software Layers
1. **Safety layer** — always authoritative; over-temp shutdown, TC fault detection, airflow loss protection
2. **Manual control layer** — operator sets heater % and blower % via serial commands
3. **Automation layer** — initially stubbed; future PID on process air temp

## Firmware Commands

```
HEAT <0-100>    Set heater duty cycle %
BLOW <0-100>    Set blower speed %
STATUS          Request current state
RESET           Clear safety fault (if conditions allow)
STOP            Emergency stop — heater and blower off immediately
```

## Key Design Constraints

| Parameter | Value | Notes |
|-----------|-------|-------|
| Batch size | 113g green | 1/4 lb |
| Mains power | 120V / 15A | US residential |
| Heater budget | 1200-1500W | Salvaged from hair dryer or heat gun |
| Airflow (blower side) | 6-15 CFM | Range covers both chamber sizes |
| Chamber (primary) | 2.5" OD SS tube (~60mm ID) | Better thermal efficiency |
| Chamber (backup) | 3.0" OD SS tube (~73mm ID) | Easier fluidization |
| TC sample rate | 4 Hz polling, 2 Hz output | Artisan-compatible |
| Target BOM cost | $50-80 | Thrift-first sourcing strategy |

## Test Plan

Six test plans cover the full commissioning sequence:

| Plan | Name | Scope |
|------|------|-------|
| TP-001 | Airflow | Distributor plate uniformity, fluidization verification |
| TP-002 | Thermal | Heater step response, steady-state characterization |
| TP-003 | Electrical Safety | Ground continuity, isolation, strain relief, smoke test |
| TP-004 | Firmware Unit | Automated tests + manual bench verification |
| TP-005 | Integration | Full system hot test with beans (not a roast) |
| TP-006 | First Roast | Conservative first roast through first crack |

Tests execute in order. Each depends on the prior test passing.

## Development Phases

| Phase | Goal | Gate |
|-------|------|------|
| 0 - Foundation | Repo, architecture, budgets, firmware scaffold | DG-0: Agree on chamber size, heater watts, airflow rate |
| 1 - Subsystem Design | Mechanical, electrical, firmware module design | DG-1: Lock interfaces between subsystems |
| 2 - Detail | Fabrication drawings, final schematic, BOM, unit tests | DG-2: BOM ordered, firmware tests pass |
| 3 - Build & Commission | Assembly, test execution, first roast | DG-3: First roast data reviewed |

## Cost Strategy

This is a v1 learning platform built to be cheap and iterable. Major cost savings:

- **Heater element** — Harbor Freight Warrior heat gun, donor only ($10, DR-002)
- **Blower** — bypass-cooled vacuum motor salvaged from a junk shop vac
  ($0-10, DR-011); TRIAC dimmer + ZMCT103C current sensor for control
- **Chamber** — standard SS exhaust pipe from auto parts store ($8-12 each)
- **Plenum** — 8" round black stovepipe + pipe caps ($0 from scrap; ~$6 retail) (DR-012)
- **Electronics** — Amazon generic ESP32, MAX31855, SSR, TCs ($35-50 total)
- **5V supply** — old phone charger from junk drawer ($0)

We design the mechanical assembly around whatever parts we find, not the other way
around. See [`docs/system/design-reviews/DR-001-cost-strategy.md`](docs/system/design-reviews/DR-001-cost-strategy.md)
for full rationale.

## Design Documents

- [`claude.md`](claude.md) — full design rationale and decision history
- [`docs/system/design-log.md`](docs/system/design-log.md) — running design log
- [`docs/system/design-reviews/`](docs/system/design-reviews/) — formal decision records

## Building the Firmware

Requires [PlatformIO](https://platformio.org/).

```bash
cd firmware
pio run          # Compile
pio test         # Run unit tests
pio run -t upload  # Flash to ESP32
```

## License

This is a personal engineering project. No license specified yet.
