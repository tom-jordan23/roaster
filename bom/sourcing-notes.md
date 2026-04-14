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

2. **12V blower** (Amazon) — 12V brushless DC centrifugal, 120mm x 32mm form factor
   (e.g. WDERAIR or Wathai). **T1 CRITICAL: Measure actual P-Q curve before
   committing to any other sizing.** Also source a 12V/3A+ switching PSU if not
   in the junk drawer. See DR-003.

3. **Chamber tubes** (auto parts store or online) — 2.5" and 3.0" OD SS exhaust
   pipe. Standard sizes, easy to find. Also source a 3.0" OD borosilicate glass
   tube (A3) from Amazon or lab supply (~$5-10) for visual fluidization testing.

4. **Plenum pan** (restaurant supply or thrift store) — 1/6 size SS steam table
   pan, 4" deep. ~$4-8 new from WebstaurantStore, Chef's Deal, or local
   restaurant supply. At thrift stores look for any small rectangular SS pan
   with straight walls and at least 3" depth. M7: Burn off outdoors at full
   temp for 10 min before first use. See DR-007.

5. **Electronics** (Amazon) — ESP32, MAX31855 x3, SSR, MOSFET (IRLZ44N), TCs,
   compression fittings (M9), plus DR-010 additions:
   - NPN transistor 2N2222 + 1k base resistor (E7: SSR drive buffer)
   - SS34 Schottky diode (E9: upgraded flyback)
   - 47Ω 2W resistor + 0.01µF/400V X2 film cap (E10: RC snubber)
   - Second thermal fuse 192-216°C (E6: airstream backup)
   - Shielded cable for SPI bus runs near heater (E13)
   These are spec-driven and can be ordered in parallel with steps 1-4.

6. **Hardware store run** — fuse, DPST disconnect switch (E8: double-pole, not
   single-pole), strain reliefs, wire (14 AWG; 12 AWG if using 20A circuit per
   E5), connectors, fasteners (including fender washers and backing strips per
   M3), all-stainless hose clamps (M11).

7. **Baseplate materials** (hardware store or salvage) — M1: 20"×12" plywood or
   sheet metal. L-brackets for lateral bracing. Ballast weight (steel plate,
   bricks, or sand bag).

## Vendor Shortlist

### Thrift / Salvage
- Goodwill, Salvation Army, Habitat ReStore — popcorn poppers (A4), SS containers,
  stainless cookware
- Junk drawer — USB phone chargers (5V PSU), laptop bricks (12V PSU), USB cables,
  small electronics components

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
- Note: the heat gun's built-in axial fan is not being used (DR-003)
- Note: the heat gun housing is not being retained (A1 rejected)

### 12V blower P-Q verification (T1 — CRITICAL)
- Measure actual airflow at several static pressure points:
  - Free air (0" WC)
  - 1.0" WC
  - 1.5" WC
  - 2.0" WC
  - 2.5" WC (if achievable)
- Method: use a manometer and a restriction plate to vary backpressure
- Must confirm the blower can deliver at least 12 CFM at 2" WC for the
  2.5" chamber, or 18 CFM at 2" WC for the 3.0" chamber
- If it cannot, source a larger blower before proceeding

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
