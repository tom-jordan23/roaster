"""Mains entry and protection.

Cord -> SW-001 (DPST disconnect, breaks BOTH L and N) -> FUSE-001 on L -> L bus.
N goes through pole 2 of SW-001, then straight to N bus.
G is unswitched, straight to chassis ground stud.
"""
import schemdraw
import schemdraw.elements as elm

from common import WIRE_L, WIRE_N, WIRE_PE, save, stem_from_argv0


def build() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.5, fontsize=11)

    # Three horizontal rails: L, N, G — left to right.
    Y_L, Y_N, Y_G = 0, -2, -4
    X_CORD = 0
    X_BUS = 14

    # Cord entry terminals
    d += elm.Dot(open=True).at((X_CORD, Y_L)).label("L\n(black)", "left")
    d += elm.Dot(open=True).at((X_CORD, Y_N)).label("N\n(white)", "left")
    d += elm.Dot(open=True).at((X_CORD, Y_G)).label("G\n(green)", "left")

    # ---- L rail: cord -> SW pole 1 -> FUSE -> L bus ----
    d += elm.Line().at((X_CORD, Y_L)).to((2, Y_L)).color(WIRE_L)
    sw_l = d.add(elm.Switch(action="close").at((2, Y_L)).to((5, Y_L)).color(WIRE_L)
                 .label("SW-001 / 1\nDPST disconnect"))
    d += elm.Line().at((5, Y_L)).to((7, Y_L)).color(WIRE_L)
    d += elm.Fuse().at((7, Y_L)).to((10, Y_L)).color(WIRE_L).label("FUSE-001\n15 A")
    d += elm.Line().at((10, Y_L)).to((X_BUS, Y_L)).color(WIRE_L)
    d += elm.Dot().at((X_BUS, Y_L)).label("L bus", "right")

    # ---- N rail: cord -> SW pole 2 -> N bus ----
    d += elm.Line().at((X_CORD, Y_N)).to((2, Y_N)).color(WIRE_N)
    sw_n = d.add(elm.Switch(action="close").at((2, Y_N)).to((5, Y_N)).color(WIRE_N)
                 .label("SW-001 / 2", "bottom"))
    d += elm.Line().at((5, Y_N)).to((X_BUS, Y_N)).color(WIRE_N)
    d += elm.Dot().at((X_BUS, Y_N)).label("N bus", "right")

    # Mechanical ganging between the two SW poles (dotted)
    d += (elm.Line().at(sw_l.center).to(sw_n.center)
          .linestyle(":").color("#888888"))

    # ---- G rail: cord straight through to chassis ground bus ----
    d += elm.Line().at((X_CORD, Y_G)).to((X_BUS, Y_G)).color(WIRE_PE)
    d += elm.Dot().at((X_BUS, Y_G)).label("Chassis GND bus\n(green stud)", "right").color(WIRE_PE)

    # ---- Title block ----
    d += (elm.Label()
          .at((X_BUS / 2, Y_G - 2.0))
          .label("Mains Entry and Protection - 120 V / 15 A branch\n"
                 "DPST switch breaks BOTH L and N (E8). 15 A fuse on L only.\n"
                 "Strain relief on cord. PE unswitched, bonded to chassis.",
                 fontsize=9))

    return d


if __name__ == "__main__":
    save(build(), stem_from_argv0())
