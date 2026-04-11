# Design Log

Running record of design decisions, findings, and rationale. Newest entries first.

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

- Heater element: need to find and tear down a hair dryer to get real dimensions
  and measured wattage
- Blower: is the hair dryer fan independently usable and speed-controllable?
  If not, a $10-15 12V brushless from Amazon is the fallback
- Plenum: need to find a suitable SS container and check thermal tolerance
- Plenum adapter: how to mount both 2.5" and 3.0" chamber tubes on the same
  plenum (adapter ring is the likely approach)
- Touchscreen UI: user has a 5x7" touchscreen LCD available. May add a
  Raspberry Pi as a UI tier above the ESP32 control layer. Interface type
  (HDMI, SPI, DSI) needs to be determined.

### Next actions

1. Go thrift store shopping: hair dryer/heat gun, SS containers, SS thermoses
2. Tear down the hair dryer and document the element and blower
3. Order electronics (ESP32, MAX31855 x3, SSR, TCs, perforated SS sheet)
4. Source 2.5" and 3.0" SS exhaust pipe
5. Once parts are in hand: mechanical integration design
