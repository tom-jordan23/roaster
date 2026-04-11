# Sourcing Notes

## Cost Strategy

Per DR-001: thrift and adapt where we can. Design around available cheap parts
rather than specifying ideal parts and paying catalog prices. See
`docs/system/design-reviews/DR-001-cost-strategy.md` for full rationale.

**Target v1 BOM: $50-80**

## Status Key
- **Needs selection** — specification not yet finalized
- **Needs sourcing** — spec known, vendor/part number needed
- **Thrift hunt** — go find one at a thrift store / junk drawer
- **Ordered** — part ordered, awaiting delivery
- **In hand** — part received and verified
- **Installed** — part built into the machine

## Sourcing Priority Order

Source parts in this order because downstream geometry depends on upstream finds:

1. **Hair dryer or heat gun** (thrift store) — determines heater element geometry,
   heater power, and possibly blower. Get this first, measure everything, then
   design around it.
2. **Chamber tubes** (auto parts store or online) — 2.5" and 3.0" OD SS exhaust
   pipe. Standard sizes, easy to find.
3. **Plenum container** (thrift store or restaurant supply) — SS steam table pan,
   steel junction box, or similar. Measure it, then design baffles to fit.
4. **Electronics** (Amazon) — ESP32, MAX31855 x3, SSR, TCs, wiring. These are
   spec-driven and can be ordered in parallel with steps 1-3.
5. **Hardware store run** — fuse, disconnect switch, strain reliefs, wire, connectors,
   fasteners.

## Vendor Shortlist

### Thrift / Salvage
- Goodwill, Salvation Army, Habitat ReStore — hair dryers, heat guns, SS thermoses,
  steel containers, stainless cookware
- Junk drawer — USB phone chargers (5V PSU), laptop bricks (12V PSU), USB cables

### Online (cheap)
- Amazon — generic ESP32, MAX31855 breakouts, SSR, K-type TCs, perforated SS sheet,
  wire assortment kits
- eBay — same as Amazon, sometimes cheaper for bulk/salvage electronics

### Auto Parts
- AutoZone, O'Reilly, Amazon — 2.5" and 3.0" stainless exhaust pipe straight sections

### Hardware / Electrical
- Home Depot, Lowes, Ace — 14 AWG wire, fuses, disconnect switch, strain reliefs,
  ring terminals, junction boxes, fasteners
- Restaurant supply store — stainless steam table pans (plenum body candidates)

## Substitution Policy

For v1, exact part numbers are less important than meeting the functional requirement
at minimum cost. Document any substitutions in the BOM Notes column.

**Exception:** Safety-critical items (fuse, mains wiring, grounding hardware) must
meet rated specifications. Do not substitute with lower-rated parts to save money.

## What to measure when you find parts

### Hair dryer / heat gun teardown
- Element resistance (calculate wattage: P = V²/R at 120V)
- Element physical dimensions (length, diameter, frame shape)
- Fan/blower type (DC motor? Universal AC? What voltage?)
- Fan airflow (qualitative: hold tissue at outlet)
- Whether the blower is usable independently of the element

### Plenum container
- Internal dimensions (L × W × H or diameter × H)
- Wall material and thickness
- Whether it can tolerate process air temperatures (~200°C+ on entry side)
- Where to cut the side-entry hole
