# Sourcing Notes

## Cost Strategy

Per DR-001: thrift and adapt where we can. Design around available cheap parts
rather than specifying ideal parts and paying catalog prices. See
`docs/system/design-reviews/DR-001-cost-strategy.md` for full rationale.

**Target v1 BOM: $75-125** (revised upward from $50-80 after DR-010 additions)

## Status Key
- **Needs selection** — specification not yet finalized
- **Needs sourcing** — spec known, vendor/part number needed
- **Thrift hunt** — go find one at a thrift store / junk drawer
- **Ordered** — part ordered, awaiting delivery
- **In hand** — part received and verified
- **Installed** — part built into the machine

## Sourcing Priority Order

Source parts in this order because downstream geometry depends on upstream finds:

0. **Popcorn popper** (thrift store, ~$2-5) — A4: Roast on a popper first to
   calibrate operator senses before building. Do this while sourcing other parts.
   Any hot-air popcorn popper works (West Bend Poppery, Presto PopLite, etc.).

1. **Warrior heat gun** (Harbor Freight, SKU 56434, ~$10) — heater element donor.
   Nichrome on mica former, 1500W, dual-temp. Get this first, tear down, measure
   element resistance and geometry, then design heater can around it. The heat
   gun housing is NOT retained (A1 rejected) — extract element and thermal cutout.
   See DR-002.

2. **Blower — bypass-cooled vacuum motor (salvage)** — DR-011 supersedes DR-003.
   Hunt at Habitat ReStore, Goodwill, or curb pickup for a dead/cheap shop vac
   with a **bypass / two-stage** motor (separate cooling impeller from working
   impeller — flow-through motors shed brush carbon into the bean airstream).
   Inspect dual-airpath separation before committing. Pair with these new
   line items, all on the AC side:
   - **BLW-CTRL-001** TRIAC dimmer module (RobotDyn-style 8A with on-board
     zero-cross detector), Amazon ~$5–10
   - **CT-001** ZMCT103C 5A split-core CT module for the airflow interlock,
     Amazon ~$3–8
   - **FILT-001** AC line filter (X+Y caps inline), Amazon or salvaged from
     a dead PC PSU input stage
   - **FERR-001** snap-on ferrite chokes (mixed-bore set), Amazon ~$5
   - **BOND-001** earth bonding lug for motor frame, hardware store ~$1

   The 12V/3A switching PSU (PSU-002), MOSFET (Q1-001), gate resistors
   (R1/R2-001), and flyback diode (D1-001) are no longer required and have
   been deleted from the BOM.

3. **Chamber tubes** (auto parts store or online) — 2.5" and 3.0" OD SS exhaust
   pipe. Standard sizes, easy to find. Also source a 3.0" OD borosilicate glass
   tube (A3) from Amazon or lab supply (~$5-10) for visual fluidization testing.

4. **Plenum pan** (restaurant supply or thrift store) — 1/6 size SS steam table
   pan, 4" deep. ~$4-8 new from WebstaurantStore, Chef's Deal, or local
   restaurant supply. At thrift stores look for any small rectangular SS pan
   with straight walls and at least 3" depth. M7: Burn off outdoors at full
   temp for 10 min before first use. See DR-007.

5. **Electronics** (Amazon) — ESP32, MAX31855 x3, SSR, TCs, compression
   fittings (M9), plus DR-010 + DR-011 additions:
   - NPN transistor 2N2222 + 1k base resistor (E7: SSR drive buffer)
   - 47Ω 2W resistor + 0.01µF/400V X2 film cap (E10: RC snubber)
   - Second thermal fuse 192-216°C (E6: airstream backup)
   - Shielded cable for SPI bus runs near heater (E13)
   - **DR-011 blower-control kit:** TRIAC dimmer (BLW-CTRL-001), ZMCT103C
     current sensor (CT-001), AC line filter (FILT-001), snap-on ferrite
     chokes (FERR-001), motor frame bonding lug (BOND-001)
   These are spec-driven and can be ordered in parallel with steps 1-4.

6. **Hardware store run** — fuse, DPST disconnect switch (E8: double-pole, not
   single-pole), strain reliefs, wire (14 AWG; 12 AWG if using 20A circuit per
   E5), connectors, fasteners (including fender washers and backing strips per
   M3), all-stainless hose clamps (M11).

7. **Baseplate materials** (hardware store or salvage) — M1: 20"×12" plywood or
   sheet metal. L-brackets for lateral bracing. Ballast weight (steel plate,
   bricks, or sand bag).

## Sourced Amazon Parts (validated 2026-04-28; DR-011 additions validated 2026-04-29)

All Amazon URLs below were validated by HTTP 200 fetch on the dates noted.
Cross-referenced against search-result titles to confirm product match.
Amazon ASINs and listings change — re-validate before placing the order.

DR-011 (2026-04-29) removed BLW-001, Q1-001, D1-001, and PSU-002 from this
table — they were 12V DC blower components that are no longer needed. The
new DR-011 line items (BLW-CTRL-001, CT-001, FILT-001, FERR-001) have been
validated and added to the Electronics table below. BOND-001 is hardware
store only — no Amazon listing.

### Electronics

| BOM Item | Listing | ASIN |
|---|---|---|
| ESP-001 | HiLetgo ESP-WROOM-32 dev board (single) | [B0718T232Z](https://www.amazon.com/dp/B0718T232Z) |
| TC-AMP-001 (×3) | NOYITO MAX31855 K-type breakout | [B07K5MJ43M](https://www.amazon.com/dp/B07K5MJ43M) |
| SSR-001 | SSR-25DA 25A zero-cross 3-32VDC / 24-380VAC | [B07FVR37QN](https://www.amazon.com/dp/B07FVR37QN) |
| Q2-001 | OCR 2N2222/2N3904 etc. TO-92 transistor kit | [B071KK9B3H](https://www.amazon.com/dp/B071KK9B3H) |
| R3-001 | ELEGOO 525-pc 1/4 W 1% resistor kit (covers 1 k and many other values) | [B072BL2VX1](https://www.amazon.com/dp/B072BL2VX1) |
| R-SNB-001 | uxcell 47 Ω 2 W metal-oxide flame-proof (60-pack) | [B07V2NV3P9](https://www.amazon.com/dp/B07V2NV3P9) |
| C-SNB-001 | 0.01 µF 275 VAC X2 safety film cap | [B09JWZ5MWQ](https://www.amazon.com/dp/B09JWZ5MWQ) |
| THFUSE-001 | NEC SF240E SEFUSE 240 °C 10 A axial | [B015675DA8](https://www.amazon.com/dp/B015675DA8) |
| THFUSE-002 | AUPO BF192 192 °C 10 A axial (10-pack) | [B0FJ5WJM9Z](https://www.amazon.com/dp/B0FJ5WJM9Z) |
| WIRE-002 | TUOFENG 22 AWG silicone hookup wire (6 colors × 26 ft) | [B07G2JWYDW](https://www.amazon.com/dp/B07G2JWYDW) |
| CONN-001 | Sopoby 1200-pc insulated crimp-terminal assortment | [B01GAESOWA](https://www.amazon.com/dp/B01GAESOWA) |

### Electronics — DR-011 blower control kit (validated 2026-04-29)

| BOM Item | Listing | ASIN |
|---|---|---|
| BLW-CTRL-001 | Genuine RobotDYN PWM AC programmable light dimmer 110-220V w/ heatsink, 3.3V/5V logic | [B071X19VL1](https://www.amazon.com/dp/B071X19VL1) |
| CT-001 | HiLetgo 3-pc ZMCT103C 5A AC current sensor w/ onboard op-amp + bias (single-phase, voltage output) | [B0CDWWYLMQ](https://www.amazon.com/dp/B0CDWWYLMQ) |
| FILT-001 | uxcell CW4L2-10A-T AC EMI filter 115/250 V 10 A (chassis-mount, terminal block, X+Y caps) | [B016EISSGE](https://www.amazon.com/dp/B016EISSGE) |
| FERR-001 | IEUYO 22-pc clip-on ferrite kit, 5 sizes (3/5/7/9/13 mm bore) | [B07DPM44BV](https://www.amazon.com/dp/B07DPM44BV) |
| BOND-001 | Hardware store — M4 or #8 ring terminal + green/yellow 14 AWG pigtail | (no Amazon link) |

### Sensors

| BOM Item | Listing | ASIN |
|---|---|---|
| TC-001/002/003 (×3) | Industrial Q-K-01 K-type 6 in × 3 mm 316 SS quick-disconnect probe | [B078QS3NWP](https://www.amazon.com/dp/B078QS3NWP) |
| TC-FIT-001 (×3) | Pysrych 1/8 in OD × 1/8 in NPT 304 SS double-ferrule (2-pack — buy 2) | [B09FF7LRL6](https://www.amazon.com/dp/B09FF7LRL6) |

### Mechanical

| BOM Item | Listing | ASIN |
|---|---|---|
| CHAM-001C | SUNWO borosilicate cylinder 3 in dia × 8 in tall (open-end chimney) | [B06XJT46QL](https://www.amazon.com/dp/B06XJT46QL) |
| PLEN-001 (backup) | AmazonCommercial 1/6-size 4 in deep anti-jam SS hotel pan (2-pack) | [B083M4N3SJ](https://www.amazon.com/dp/B083M4N3SJ) |
| PLEN-004 | 1 in fiberglass woodstove gasket rope (7 ft) | [B01ETURR0M](https://www.amazon.com/dp/B01ETURR0M) |
| PLATE-001A/B | FengYoo 4 in dia round 304 SS perforated disc, 1/16 in holes (qty 2) | [B09SF15S47](https://www.amazon.com/dp/B09SF15S47) |
| EXH-002 | 30-mesh 304 SS woven wire screen 11.8 × 23.6 in | [B09VNSQGVH](https://www.amazon.com/dp/B09VNSQGVH) |

### Substitutions and decisions to flag

- **THFUSE-001 (228 °C → 240 °C).** 228 °C single-pieces are not stocked by major Amazon sellers; nearest in-stock single-piece axial is the NEC SEFUSE 240 °C. Both ratings are well below nichrome failure (~1400 °C) and cool-mass thermal runaway envelopes — 240 °C is conservative for a heater-can-body cutoff. Acceptable per the safety-critical substitution gate.
- **CHAM-001C (10–12 in target → 8 in actual).** 3 in OD × 10 in+ borosilicate at hobby price is essentially unavailable on Amazon; the SUNWO chimney glass is 8 in tall. Validate that 8 in still gives enough freeboard above the bean bed (~2 in deep when fluidized) before the chaff transition. If insufficient, alternatives are GreatGlas custom Pyrex/quartz, Wale Apparatus 5 ft tubing cut to length, or staying with the SS chamber and accepting no visual.
- **PLATE-001A/B hole size.** Pre-cut 4 in disc ships with 1/16 in (1.5 mm) holes — small. Open area is ~22 % which gives high pressure drop. Confirm fluidization at 12 CFM during T1; if dP is too high, substitute a coarser perforated sheet.
- **PLEN-001.** Restaurant-supply or thrift is still the preferred path (per DR-001). The Amazon AmazonCommercial 2-pack is listed as a backup only.
- **EXH-001.** No clean Amazon match for a 4 in × 5 in tall pure-SS cylinder at low cost. Plan to thrift a SS flatware caddy, utensil cylinder, or coffee tin.
- **CT-001 (active op-amp output vs passive burden).** Original spec language called for "burden + bias network" — the HiLetgo board ships with an onboard op-amp that converts the CT's 5 mA secondary to a buffered voltage signal already biased to mid-rail. This is *better* than a passive burden + divider for ADC sampling (lower output impedance, less susceptible to ADC sample-and-hold loading). Firmware reads voltage on GPIO 34 and computes RMS. No spec change required; flag only because the implementation differs from the literal wording.
- **FILT-001 (chassis-mount terminal block, not 2-lead inline).** Original spec language called for an "inline module." The CW4L2-10A-T is a chassis-mount filter with screw terminals — it sits in the mains path between fuse bus and TRIAC dimmer, but it is mechanically a chassis part with mounting flange and earth lug, not a 2-leaded inline component. The earth lug must be bonded to the chassis-ground bus (see baseplate-layout.md §5). Functionally equivalent; affects mounting only.

## Vendor Shortlist

### Thrift / Salvage
- Goodwill, Salvation Army, Habitat ReStore — popcorn poppers (A4), SS containers,
  stainless cookware, dead/cheap shop vacs (BLW-001 — bypass-cooled motor donor)
- Junk drawer — USB phone chargers (5V PSU), USB cables, small electronics components
- Curb / free pickup — shop vacs are common discards; verify bypass-cooled motor type

### Online (cheap)
- Amazon — generic ESP32, MAX31855 breakouts, SSR, K-type TCs, compression fittings,
  perforated SS sheet, wire assortment kits, borosilicate glass tubes, 2N2222,
  SS34, film capacitors
- eBay — same as Amazon, sometimes cheaper for bulk/salvage electronics

### Auto Parts
- AutoZone, O'Reilly, Amazon — 2.5" and 3.0" stainless exhaust pipe straight sections

### Hardware / Electrical
- Home Depot, Lowes, Ace — wire (14 or 12 AWG), fuses, DPST disconnect switch,
  strain reliefs, ring terminals, junction boxes, fasteners, fender washers,
  all-stainless hose clamps, L-brackets
- Restaurant supply store — stainless steam table pans (plenum body candidates)

### Specialty
- McMaster-Carr — 1/8" Swagelok-style compression fittings for TC probes (M9),
  if Amazon options are poor quality
- Lab supply (Amazon or eBay) — borosilicate glass tubing 3.0" OD (A3)

## Substitution Policy

For v1, exact part numbers are less important than meeting the functional requirement
at minimum cost. Document any substitutions in the BOM Notes column.

**Exception:** Safety-critical items (fuse, mains wiring, grounding hardware,
thermal fuses, SSR, disconnect switch) must meet rated specifications. Do not
substitute with lower-rated parts to save money.

## What to measure when you find parts

### Warrior heat gun teardown (SKU 56434)
- Element resistance (calculate wattage: P = V²/R at 120V; expect ~9.6Ω for 1500W)
- Element physical dimensions (length, diameter, mica former shape)
- Thermal cutout specs (temperature rating, one-shot vs resettable)
- Mica former tab locations (M5: needed for mounting in custom heater can)
- Note: the heat gun's built-in axial fan is not being used (DR-003 / DR-011)
- Note: the heat gun housing is not being retained (A1 rejected)

### Vacuum motor characterization (DR-011 — supersedes T1)

T1 changed from "verify the blower meets spec" to "find the operating duty-cycle
range for a motor that exceeds spec." The salvaged vacuum motor will have far
more pressure than the system needs at 100% conduction; the question is where
to operate the TRIAC.

What to measure once the salvaged motor is in hand:

- **Bypass-cooling confirmation (BEFORE bench testing).** Identify the cooling
  airpath and the working airpath. Run the motor briefly with a paper towel
  held over the working inlet — the working impeller stalls; the motor must
  *not* stall (cooling impeller is independent). If both stop, it's
  flow-through — reject this motor.
- **No-load draw at 120 V.** Clamp meter on one motor lead. Establishes the
  baseline for the CT-001 airflow-interlock threshold.
- **CFM vs. TRIAC conduction angle.** With the working impeller plumbed to a
  manometer + restriction plate, sweep the dimmer from minimum smooth running
  (often ~30%) to 100% in steps. Record CFM at the 2.5" and 3.0" chamber
  operating-pressure points (1.5" and 2.0" WC respectively).
- **Smooth-running floor.** Universal motors don't run cleanly at very low
  conduction — find the lowest conduction angle that still produces stable
  rotation. This sets the bottom of the operating duty-cycle range.
- **Goal:** define a TRIAC duty-cycle range that maps to the 8–18 CFM
  operating envelope across both chambers, with margin for chaff-mesh loading
  (T8) and bed-depth variation.

### Plenum pan (1/6 size steam table pan)
- Internal dimensions (L × W × H) — confirm ~6" × 6" × 4" minimum
- Wall material and thickness — should be 18/8 or 304 SS
- Rim/flange width — needed to size clamping ring bolts
- Where to drill the side-entry hole (centered on one wall, as low as practical)
- Whether rim is flat enough for gasket sealing
- M2: Assess wall thickness for stub tube installation

### Borosilicate glass tube (A3)
- Confirm 3.0" OD and wall thickness
- Check ends are fire-polished (no sharp edges)
- Handle with care — thermal shock risk during testing
