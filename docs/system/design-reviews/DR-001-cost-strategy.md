# DR-001: Cost Strategy — Thrift and Adapt Where We Can

**Date:** 2026-04-10
**Status:** DECIDED

## Decision

This project will prioritize low-cost, resourceful sourcing for the v1 prototype.
Consumer parts, thrift store finds, salvage, and Amazon generics are preferred over
industrial catalog parts wherever they meet the functional requirement.

Engineering specs may be flexed slightly to accommodate available cheap parts —
for example, designing the heater can geometry around a salvaged hair dryer element
rather than specifying an exact element and ordering it.

## Rationale

- This is a learning platform, not a product. Every dollar saved is a dollar
  available for iteration.
- A $5 thrift store hair dryer contains both a 1500W heater element and a blower
  motor already matched for airflow — collapsing ~$80 of separate component
  sourcing into one purchase.
- Generic ESP32 boards, MAX31855 breakouts, and K-type thermocouples from Amazon
  are functionally identical to name-brand equivalents at 1/3 the price.
- Stainless steel containers, exhaust pipe, and plumbing fittings are cheaper
  than ordering tube stock from metals suppliers and often come in useful sizes.
- The prototype will be rebuilt and modified many times. Expensive precision parts
  will be wasted if the design changes.

## Where to be resourceful

| Component | Cheap source | Est. cost |
|-----------|-------------|-----------|
| Heater element | Harbor Freight Warrior heat gun (DR-002) | $10 |
| Blower motor | Salvaged bypass-cooled vacuum motor (DR-011) | $0-10 |
| Blower control kit | TRIAC dimmer + ZMCT103C CT + line filter + ferrites (DR-011) | $15-25 |
| Chamber tube | Auto exhaust pipe (2.5"/3.0") or thrift store SS thermos | $5-15 |
| Plenum body | SS steam table pan, steel junction box, or paint can | $3-10 |
| Distributor plate | Perforated SS sheet (Amazon) cut to size, or drilled jar lid | $5-12 |
| ESP32 | Generic dev board (Amazon) | $5-7 |
| MAX31855 x3 | Generic breakouts (Amazon) | $12-18 |
| SSR | Generic 25A (Amazon) + thermal fuse backup | $6-10 |
| K-type TC x3 | SS-sheathed probes (Amazon) | $9-15 |
| 5V PSU | Old USB phone charger from junk drawer | $0 |
| Wiring + connectors | Assortment kits (Amazon) | $10-15 |
| Fuse, switch, strain reliefs | Hardware store | $5-10 |

**Estimated v1 BOM total: $50-80**

## Where NOT to cheap out

These items are either safety-critical or affect measurement quality. Buy proper parts:

- **Fuse or breaker** — real 15A rated, from a hardware or electrical store
- **Mains wiring** — 14 AWG minimum, new, rated insulation
- **Strain reliefs** — proper cord grips on every mains entry point
- **Grounding hardware** — ring terminals, star washers, proper chassis bonding
- **TC amplifier boards** — generic MAX31855 is fine, but don't skip the amplifier
  and try to read raw TC voltage on an ADC. The cold-junction compensation and
  signal conditioning matter.
- **SSR backup** — add a thermal fuse (~$1) on the heater as an independent
  last-resort cutoff in case the SSR fails shorted

## Implications for downstream design

1. **Heater can geometry** will be designed around whatever element we harvest,
   not the other way around. Get the hair dryer first, measure the element,
   then design the can.
2. **Blower characterization** happens on the bench with the actual salvaged or
   purchased unit before committing to airflow numbers. The architecture doc's
   CFM estimates are targets, but real numbers come from the real part.
3. **Chamber dimensions** are set by available tube stock (2.5" and 3.0" OD
   standard sizes), which is already aligned with cheap sourcing.
4. **Plenum dimensions** will be driven by whatever container we adapt. Design
   the baffles to fit the container, not the other way around.
5. **The BOM becomes a shopping list** — some items are "go to the thrift store
   and find one" rather than "order part number X from vendor Y."

## Design-to-cost sequence

Because several dimensions depend on what parts we actually find:

1. **Source the hair dryer / heat gun first** — this determines heater element
   size, heater power, and possibly the blower
2. **Source the chamber tubes** — standard sizes, easy to get
3. **Source the plenum container** — then design baffles to fit
4. **Order electronics** — these are spec-driven, not geometry-driven
5. **Design the mechanical assembly around what we have**

This is the opposite of traditional engineering (design first, then source).
For a cheap v1 prototype, it's the right approach. We design around available
parts rather than specifying parts to match a design.
