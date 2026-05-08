"""Domain 1 - 120 V AC heater circuit.

Power path:
    L bus -> THFUSE-001 (228 C, can body) -> THFUSE-002 (192-216 C, airstream)
          -> SSR-001 (zero-cross SSR, switches L only)
          -> HTR-001 (Warrior 1500 W nichrome element, ~9.6 ohm)
          -> N bus

Both thermal fuses are in series with the heater, on the L side, upstream of
the SSR. If the SSR fails shorted, opening either thermal fuse still kills
the element.

Snubber: 47 ohm + 0.01 uF X2 across the SSR output (E10).

Drive:
    ESP32 GPIO 22 -> R3 (1k) -> Q2 base (NPN, 2N2222)
    Q2 emitter -> SSR DC IN(-)
    +5V -> SSR DC IN(+) (high-side); Q2 sinks the input to enable.
    NPN buffer (E7) lifts the 3.3 V GPIO drive to a clean 5 V level.
"""
import schemdraw
import schemdraw.elements as elm

from common import WIRE_3V3, WIRE_5V, WIRE_L, WIRE_N, box, save, stem_from_argv0


def build() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.5, fontsize=10)

    # ===================================================================
    # Top half - AC power path: L bus (left) -> ... -> N bus (right)
    # ===================================================================
    Y_AC = 0
    X_LBUS = 0
    X_NBUS = 26

    d += elm.Dot().at((X_LBUS, Y_AC)).label("L bus", "left")

    # Thermal fuse 1 (on heater can)
    d += elm.Line().at((X_LBUS, Y_AC)).to((2, Y_AC)).color(WIRE_L)
    d += elm.Fuse().at((2, Y_AC)).to((5, Y_AC)).color(WIRE_L).label(
        "THFUSE-001\n228 C\n(on can body)")

    # Thermal fuse 2 (in airstream)
    d += elm.Line().at((5, Y_AC)).to((6, Y_AC)).color(WIRE_L)
    d += elm.Fuse().at((6, Y_AC)).to((9, Y_AC)).color(WIRE_L).label(
        "THFUSE-002\n192-216 C\n(in airstream)")

    # SSR power side (top contacts)
    d += elm.Line().at((9, Y_AC)).to((11, Y_AC)).color(WIRE_L)
    ssr_in = (11, Y_AC)
    ssr_out = (15, Y_AC)
    # Box around SSR
    box(d, 11, Y_AC - 2.6, 15, Y_AC + 0.8)
    d += elm.Line().at(ssr_in).to(ssr_out).color(WIRE_L)
    d += elm.Dot().at(ssr_in)
    d += elm.Dot().at(ssr_out)
    d += elm.Label().at((13, Y_AC + 0.4)).label("SSR-001\n25 A zero-cross", fontsize=9)

    # RC snubber across SSR power terminals (E10)
    # Drop down from ssr_in, R then C, back up to ssr_out
    Y_SNUB = Y_AC - 1.6
    d += elm.Line().at(ssr_in).to((11, Y_SNUB))
    d += elm.Resistor().at((11, Y_SNUB)).to((12.7, Y_SNUB)).label("R-SNB\n47 ohm 2W", fontsize=8)
    d += elm.Capacitor().at((12.7, Y_SNUB)).to((15, Y_SNUB)).label("C-SNB\n0.01 uF\nX2 400V", fontsize=8)
    d += elm.Line().at((15, Y_SNUB)).to(ssr_out)

    # Heater element
    d += elm.Line().at(ssr_out).to((17, Y_AC)).color(WIRE_L)
    d += elm.Resistor().at((17, Y_AC)).to((22, Y_AC)).color(WIRE_L).label(
        "HTR-001\nWarrior 1500 W\n~9.6 ohm  (~12.5 A)")
    d += elm.Line().at((22, Y_AC)).to((X_NBUS, Y_AC)).color(WIRE_N)
    d += elm.Dot().at((X_NBUS, Y_AC)).label("N bus", "right")

    # ===================================================================
    # Bottom half - SSR DC drive: ESP32 GPIO 22 -> R3 -> Q2 -> SSR DC IN
    # ===================================================================
    Y_DRV = -8
    X_ESP = 0

    # ESP32 stub (left)
    box(d, X_ESP, Y_DRV - 1, X_ESP + 3.5, Y_DRV + 1)
    d += elm.Label().at((X_ESP + 1.75, Y_DRV)).label("ESP32\nGPIO 22\n(PIN_SSR)", fontsize=9)
    d += elm.Dot().at((X_ESP + 3.5, Y_DRV))

    # Base resistor R3
    d += elm.Line().at((X_ESP + 3.5, Y_DRV)).to((6, Y_DRV)).color(WIRE_3V3)
    d += elm.Resistor().at((6, Y_DRV)).to((9, Y_DRV)).color(WIRE_3V3).label("R3\n1 k")

    # Q2 NPN
    d += elm.Line().at((9, Y_DRV)).to((10.5, Y_DRV)).color(WIRE_3V3)
    q2 = d.add(elm.BjtNpn().at((10.5, Y_DRV)).right().anchor("base").label("Q2\n2N2222", "left"))
    # Emitter to ground (signal GND)
    d += elm.Line().at(q2.emitter).to((q2.emitter.x, Y_DRV - 2.5))
    d += elm.Ground().at((q2.emitter.x, Y_DRV - 2.5))

    # +5V rail and SSR DC IN
    Y_5V = Y_DRV + 3
    d += elm.Line().at((q2.collector.x, q2.collector.y)).to((q2.collector.x, Y_5V)).color(WIRE_5V)
    ssr_dc_minus = (q2.collector.x, Y_5V)
    ssr_dc_plus = (16, Y_5V)
    d += elm.Dot().at(ssr_dc_minus).label("SSR DC -\n(to gate)", "top", fontsize=8)
    d += elm.Line().at(ssr_dc_minus).to(ssr_dc_plus).color(WIRE_5V)
    d += elm.Dot().at(ssr_dc_plus).label("SSR DC +", "top", fontsize=8)

    # +5V supply tie-in (PSU-001 shown in control diagram)
    d += elm.Line().at(ssr_dc_plus).to((19, Y_5V)).color(WIRE_5V)
    d += elm.Dot(open=True).at((19, Y_5V)).label("+5 V\n(from PSU-001)", "right")

    # Title
    d += (elm.Label().at((13, Y_DRV - 4.5))
          .label("Domain 1 - Heater Circuit (120 V AC)\n"
                 "L-side switching only. Two thermal fuses in series upstream of SSR (E6).\n"
                 "RC snubber across SSR (E10). NPN buffer Q2 lifts 3.3 V GPIO to 5 V SSR drive (E7).",
                 fontsize=9))

    return d


if __name__ == "__main__":
    save(build(), stem_from_argv0())
