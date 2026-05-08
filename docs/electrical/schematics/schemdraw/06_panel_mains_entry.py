"""Panel-wiring pictorial: MAINS ENTRY zone.

Cord -> strain relief -> SW-001 (DPST) -> FUSE-001 -> distribution buses.
G is unswitched, straight to chassis ground stud. Both poles of SW-001 are
ganged so flipping the switch breaks BOTH L and N (E8).
"""
import schemdraw
import schemdraw.elements as elm

from common import (C_GND, C_L, C_N, C_PE, cable_schedule, module, save,
                    stem_from_argv0, term, wire, zone)


def build() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.0, fontsize=9)

    # Zone outline
    Z_X0, Z_Y0, Z_X1, Z_Y1 = 0, 2, 28, 14
    zone(d, Z_X0, Z_Y0, Z_X1, Z_Y1, "MAINS ENTRY")

    # ---- Cord pigtail (left) ----
    cord_l = (1, 11.5)
    cord_n = (1, 9.5)
    cord_g = (1, 7.5)
    d.add(elm.Dot(open=True).at(cord_l).label("L  (BLK)", "left", fontsize=9))
    d.add(elm.Dot(open=True).at(cord_n).label("N  (WHT)", "left", fontsize=9))
    d.add(elm.Dot(open=True).at(cord_g).label("G  (GRN)", "left", fontsize=9))
    d.add(elm.Label().at((1, 6)).label(
        "120 V cord pigtail\n14 AWG SJOOW 3-conductor\nstrain-relief bushing on enclosure", fontsize=8))

    # ---- SW-001 disconnect ----
    sw_x0, sw_y0, sw_x1, sw_y1 = 5, 8.5, 9, 12.5
    module(d, sw_x0, sw_y0, sw_x1, sw_y1, "SW-001  DPST disconnect")
    sw_l_in = term(d, (sw_x0, 11.5), "1\nL in", "left")
    sw_l_out = term(d, (sw_x1, 11.5), "2\nL out", "right")
    sw_n_in = term(d, (sw_x0, 9.5), "3\nN in", "left")
    sw_n_out = term(d, (sw_x1, 9.5), "4\nN out", "right")
    d.add(elm.Label().at((7, 10.5)).label("(poles ganged - one\nlever breaks both)", fontsize=7))

    # ---- FUSE-001 inline fuse holder ----
    fuse_x0, fuse_x1 = 11, 14.5
    module(d, fuse_x0, 10.7, fuse_x1, 12.3, "FUSE-001  15 A inline")
    fuse_in = term(d, (fuse_x0, 11.5), "in", "left")
    fuse_out = term(d, (fuse_x1, 11.5), "out", "right")

    # ---- Distribution buses ----
    # Three-bundle drop points: x=18 (heater), x=21 (blower), x=24 (control).
    # Each bus is wide enough to space them clearly; terminals on the bottom edge.
    BUS_X0, BUS_X1 = 17, 26
    DROP_X = {"heater": 18.5, "blower": 21.0, "control": 24.0}

    # L bus
    module(d, BUS_X0, 11.0, BUS_X1, 12.0, "L bus  (4-position TB)")
    l_bus_in = term(d, (BUS_X0, 11.5), "in", "left")
    l_bus_h = term(d, (DROP_X["heater"], 11.0), "to heater", "bottom")
    l_bus_b = term(d, (DROP_X["blower"], 11.0), "to blower", "bottom")
    l_bus_c = term(d, (DROP_X["control"], 11.0), "to control", "bottom")

    # N bus
    module(d, BUS_X0, 9.0, BUS_X1, 10.0, "N bus  (4-position TB)")
    n_bus_in = term(d, (BUS_X0, 9.5), "in", "left")
    n_bus_h = term(d, (DROP_X["heater"], 9.0), "to heater", "bottom")
    n_bus_b = term(d, (DROP_X["blower"], 9.0), "to blower", "bottom")
    n_bus_c = term(d, (DROP_X["control"], 9.0), "to control", "bottom")

    # Chassis ground stud
    module(d, BUS_X0, 7.0, BUS_X1, 8.0, "Chassis GND stud  (M5, green-painted)")
    g_stud = term(d, (BUS_X0, 7.5), "in", "left")
    g_h = term(d, (DROP_X["heater"], 7.0), "to heater", "bottom")
    g_b = term(d, (DROP_X["blower"], 7.0), "to blower", "bottom")
    g_c = term(d, (DROP_X["control"], 7.0), "to control", "bottom")

    # ---- Wires ----
    wire(d, cord_l, sw_l_in, C_L, "BLK 14 AWG")
    wire(d, sw_l_out, fuse_in, C_L, "BLK 14 AWG")
    wire(d, fuse_out, l_bus_in, C_L, "BLK 14 AWG")

    wire(d, cord_n, sw_n_in, C_N, "WHT 14 AWG")
    wire(d, sw_n_out, n_bus_in, C_N, "WHT 14 AWG", route="h-then-v")

    wire(d, cord_g, (4, 7.5), C_PE, "GRN 14 AWG")
    wire(d, (4, 7.5), g_stud, C_PE)

    # Outgoing pigtails: each destination bundle drops cleanly out the bottom of the zone.
    bottom_y = 4.0
    for dest, x_center in DROP_X.items():
        # L drop
        d.add(elm.Line().at((x_center, 11.0)).to((x_center, bottom_y)).color(C_L))
        # N drop (offset slightly for visual separation)
        d.add(elm.Line().at((x_center, 9.0)).to((x_center, bottom_y)).color(C_N))
        # PE drop
        d.add(elm.Line().at((x_center, 7.0)).to((x_center, bottom_y)).color(C_PE))
        # Open dot at the bottom for "leaves the zone"
        d.add(elm.Dot(open=True).at((x_center, bottom_y)))
        d.add(elm.Label().at((x_center, bottom_y - 0.6)).label(
            f"to {dest.upper()} BAY\nL + N + PE\n14 AWG each",
            fontsize=8))

    # ---- Title and cable schedule (below zone) ----
    d.add(elm.Label().at((14, 1.0)).label(
        "Panel Wiring  -  Zone 1 of 4: MAINS ENTRY\n"
        "DPST switch breaks BOTH L and N (E8). 15 A fuse on L only. PE unswitched.\n"
        "All distribution via terminal blocks - no daisy-chain.",
        fontsize=10))

    cable_schedule(d, 2, -2.0, [
        ("CABLE",  "FROM",                       "TO",                      "COND", "WIRE"),
        ("---",    "---",                        "---",                     "---",  "---"),
        ("C-MN-1", "Cord (wall plug)",           "SW-001 1 / 3 / chassis",  "3",    "14 AWG SJOOW"),
        ("C-MN-2", "L bus 2",                    "Heater bay THFUSE-001",   "1",    "BLK 14 AWG"),
        ("C-MN-3", "N bus 2",                    "Heater bay HTR-001 N",    "1",    "WHT 14 AWG"),
        ("C-MN-4", "L bus 3",                    "Blower bay FILT-001 L-in","1",    "BLK 14 AWG"),
        ("C-MN-5", "N bus 3",                    "Blower bay FILT-001 N-in","1",    "WHT 14 AWG"),
        ("C-MN-6", "L bus 4",                    "Control bay PSU-001 L",   "1",    "BLK 14 AWG"),
        ("C-MN-7", "N bus 4",                    "Control bay PSU-001 N",   "1",    "WHT 14 AWG"),
        ("C-PE-1", "Chassis stud (heater out)",  "Heater bay PE rail",      "1",    "GRN 14 AWG"),
        ("C-PE-2", "Chassis stud (blower out)",  "Blower bay PE rail",      "1",    "GRN 14 AWG"),
        ("C-PE-3", "Chassis stud (control out)", "Control bay PE rail",     "1",    "GRN 14 AWG"),
    ], col_widths=(2.5, 6.5, 6.5, 1.2, 4.0))

    return d


if __name__ == "__main__":
    save(build(), stem_from_argv0())
