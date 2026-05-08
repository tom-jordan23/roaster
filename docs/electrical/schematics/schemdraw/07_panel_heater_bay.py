"""Panel-wiring pictorial: HEATER BAY zone.

Mains side (top of bay, left -> right):
    L bus pigtail -> THFUSE-001 (228 C, can body)
                  -> THFUSE-002 (192-216 C, airstream)
                  -> SSR-001 T1 -> SSR-001 T2 -> HTR-001 L
    HTR-001 N -> N return rail (one row below the AC chain) -> N bus pigtail
    Snubber (R-SNB + C-SNB) across SSR T1-T2.

Logic side (bottom of bay):
    GPIO 22 (3.3 V) -> R3 (1k) -> Q2 (2N2222) base
    Q2 emitter -> signal GND (control bay)
    Q2 collector -> SSR DC- (terminal 4)
    +5 V (control bay) -> SSR DC+ (terminal 3)
DRV-BD-001 is a small protoboard mounted within ~6 in of the SSR.
"""
import schemdraw
import schemdraw.elements as elm

from common import (C_3V3, C_5V, C_GND, C_L, C_N, C_PE, cable_schedule, module,
                    save, stem_from_argv0, term, wire, zone)


def build() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.0, fontsize=9)

    Z_X0, Z_Y0, Z_X1, Z_Y1 = 0, 0, 32, 18
    zone(d, Z_X0, Z_Y0, Z_X1, Z_Y1, "HEATER BAY  (mains side)")

    # Useful row Ys for the AC chain
    Y_AC = 15.0      # main AC chain (L through everything)
    Y_NRET = 12.5    # N return rail (below AC chain, above SSR DC pins)

    # ---- Incoming pigtails from MAINS ENTRY (top edge) ----
    in_l = (3, 17.4)
    in_n = (5, 17.4)
    in_pe = (7, 17.4)
    d.add(elm.Dot(open=True).at(in_l).label("L  (C-MN-2)", "top", fontsize=7))
    d.add(elm.Dot(open=True).at(in_n).label("N  (C-MN-3)", "top", fontsize=7))
    d.add(elm.Dot(open=True).at(in_pe).label("PE  (C-PE-1)", "top", fontsize=7))

    # Drop into the bay
    wire(d, in_l, (3, Y_AC), C_L, "BLK 14 AWG", label_at=(3.5, 16.4))
    wire(d, in_n, (5, Y_NRET), C_N, "WHT 14 AWG", label_at=(5.5, 14.5))

    # ---- THFUSE-001 (heater can body) ----
    thf1_x0, thf1_x1 = 4, 7
    module(d, thf1_x0, Y_AC - 0.6, thf1_x1, Y_AC + 0.6, "THFUSE-001  228 C")
    thf1_a = term(d, (thf1_x0, Y_AC), "a", "left")
    thf1_b = term(d, (thf1_x1, Y_AC), "b", "right")

    # ---- THFUSE-002 (in airstream) ----
    thf2_x0, thf2_x1 = 9, 12
    module(d, thf2_x0, Y_AC - 0.6, thf2_x1, Y_AC + 0.6, "THFUSE-002  192-216 C")
    thf2_a = term(d, (thf2_x0, Y_AC), "a", "left")
    thf2_b = term(d, (thf2_x1, Y_AC), "b", "right")

    d.add(elm.Label().at(((thf1_x0 + thf2_x1) / 2, Y_AC - 1.1)).label(
        "axial-lead thermal fuses, crimped inline -> spade -> can stud / plenum lid",
        fontsize=7))

    # ---- SSR-001 (mid-bay) ----
    ssr_x0, ssr_y0, ssr_x1, ssr_y1 = 14, 9.5, 19, 16.0
    module(d, ssr_x0, ssr_y0, ssr_x1, ssr_y1, "SSR-001  25 A zero-cross")
    ssr_t1 = term(d, (ssr_x0, Y_AC), "1\nT1 (L in)", "left")
    ssr_t2 = term(d, (ssr_x1, Y_AC), "2\nT2 (L out)", "right")
    ssr_3 = term(d, (15.5, ssr_y0), "3\n+5 V", "bottom")
    ssr_4 = term(d, (17.5, ssr_y0), "4\nDC -", "bottom")
    d.add(elm.Label().at((20.0, 11.5)).label(
        "SSR heatsink: aluminum bar bonded to PE", fontsize=7))

    # ---- HTR-001 (heater element) ----
    htr_x0, htr_x1 = 21, 26
    module(d, htr_x0, Y_AC - 0.7, htr_x1, Y_AC + 0.7, "HTR-001  Warrior 1500 W")
    htr_l = term(d, (htr_x0, Y_AC), "L", "left")
    htr_n = term(d, (htr_x1, Y_AC), "N", "right")
    d.add(elm.Label().at(((htr_x0 + htr_x1) / 2, Y_AC - 1.2)).label(
        "nichrome element  ~9.6 ohm  ~12.5 A", fontsize=7))

    # ---- Snubber (R-SNB + C-SNB across SSR T1-T2), drawn ABOVE SSR ----
    sn_y = 17.0
    d.add(elm.Resistor().at((14, sn_y)).right().to((16, sn_y)).label("R-SNB 47R 2W", fontsize=7))
    d.add(elm.Capacitor().at((16, sn_y)).right().to((19, sn_y)).label("C-SNB 0.01uF X2", fontsize=7))
    # Snubber taps from SSR T1 and T2 (drawn going up from ssr_y1)
    wire(d, (14, sn_y), (14, ssr_y1), C_L)
    wire(d, (19, sn_y), (19, ssr_y1), C_L)

    # ---- Mains-side wires (AC chain + N return) ----
    wire(d, (3, Y_AC), thf1_a, C_L, "BLK 14 AWG")
    wire(d, thf1_b, thf2_a, C_L, "BLK 14 AWG")
    wire(d, thf2_b, ssr_t1, C_L, "BLK 14 AWG")
    wire(d, ssr_t2, htr_l, C_L, "BLK 14 AWG")

    # N return: HTR-001 N -> drops down to Y_NRET -> all the way left -> N pigtail
    wire(d, htr_n, (27, Y_AC), C_N)
    wire(d, (27, Y_AC), (27, Y_NRET), C_N)
    wire(d, (27, Y_NRET), (5, Y_NRET), C_N, "WHT 14 AWG  (N return)", label_at=(8.5, Y_NRET + 0.3))

    # ---- DRV-BD-001 (drive buffer board), bottom of bay ----
    drv_x0, drv_y0, drv_x1, drv_y1 = 12.5, 4.0, 21, 7.5
    module(d, drv_x0, drv_y0, drv_x1, drv_y1, "DRV-BD-001  SSR drive buffer")
    drv_in = term(d, (drv_x0, 6.0), "GPIO 22 in", "left")
    drv_5v_in = term(d, (drv_x0, 5.2), "+5 V in", "left")
    drv_gnd_in = term(d, (drv_x0, 4.4), "GND in", "left")
    drv_dcp = term(d, (drv_x1, 6.5), "to SSR 3", "right")
    drv_dcm = term(d, (drv_x1, 5.5), "to SSR 4", "right")
    drv_pe = term(d, (drv_x1, 4.4), "to PE", "right")
    # Internal layout note (no symbols - protoboard reality is "R3 in series, Q2 to ground")
    d.add(elm.Label().at(((drv_x0 + drv_x1) / 2, drv_y0 - 0.7)).label(
        "1 x 2 in protoboard:\n"
        "GPIO 22 in -> R3 (1 k axial) -> Q2 (2N2222) base\n"
        "Q2 emitter -> GND in;  Q2 collector -> SSR 4 out;  +5 V in -> SSR 3 out",
        fontsize=7))

    # ---- DC drive wires (SSR DC + / DC -) ----
    wire(d, drv_dcp, (drv_x1 + 0.4, 6.5), C_5V)
    wire(d, (drv_x1 + 0.4, 6.5), (ssr_3[0], 6.5), C_5V, route="v-then-h")
    wire(d, (ssr_3[0], 6.5), ssr_3, C_5V, "RED 22 AWG", label_at=(15.7, 8.0))
    wire(d, drv_dcm, (drv_x1 + 0.7, 5.5), C_3V3)
    wire(d, (drv_x1 + 0.7, 5.5), (ssr_4[0], 5.5), C_3V3, route="v-then-h")
    wire(d, (ssr_4[0], 5.5), ssr_4, C_3V3, "PUR 22 AWG", label_at=(17.7, 7.5))

    # PE chassis connection from drive board
    wire(d, drv_pe, (drv_x1 + 1, drv_pe[1]), C_PE)
    wire(d, (drv_x1 + 1, drv_pe[1]), (drv_x1 + 1, 1.5), C_PE)

    # ---- PE/chassis-earth bus along bottom of zone ----
    d.add(elm.Line().at((1, 1.5)).to((30, 1.5)).color(C_PE))
    d.add(elm.Label().at((15, 0.9)).label(
        "Chassis earth bus  (GRN 14 AWG)  -  SSR heatsink, panel chassis, can/plenum lugs",
        fontsize=8, color=C_PE))
    # Drops onto the bus
    wire(d, in_pe, (7, 1.5), C_PE, "GRN 14 AWG", label_at=(7.5, 9.0))
    for x, label in [(16.5, "SSR-001 heatsink"), (23, "HTR-001 can lug")]:
        wire(d, (x, 1.5), (x, 2.4), C_PE)
        d.add(elm.Dot().at((x, 2.4)))
        d.add(elm.Label().at((x, 2.7)).label(label, fontsize=7, color=C_PE))

    # ---- Incoming cables from CONTROL BAY (right edge) ----
    in_g22 = (31, 6.0)
    in_5v = (31, 5.2)
    in_gnd = (31, 4.4)
    d.add(elm.Dot(open=True).at(in_g22).label("GPIO 22\n(C-CT-1)", "right", fontsize=7))
    d.add(elm.Dot(open=True).at(in_5v).label("+5 V\n(C-CT-2)", "right", fontsize=7))
    d.add(elm.Dot(open=True).at(in_gnd).label("sig GND\n(C-CT-3)", "right", fontsize=7))
    # The control bay cables enter on the right and must be routed to the LEFT side of the
    # drv board (terminals are on the left of DRV-BD-001). Route along bottom edge.
    Y_CTRLBUS = 3.0
    wire(d, in_g22, (in_g22[0], Y_CTRLBUS), C_3V3)
    wire(d, in_5v, (in_5v[0] - 0.3, Y_CTRLBUS - 0.3), C_5V)
    wire(d, in_gnd, (in_gnd[0] - 0.6, Y_CTRLBUS - 0.6), C_GND)
    wire(d, (in_g22[0], Y_CTRLBUS), (drv_x0 - 0.5, Y_CTRLBUS), C_3V3)
    wire(d, (in_5v[0] - 0.3, Y_CTRLBUS - 0.3), (drv_x0 - 0.7, Y_CTRLBUS - 0.3), C_5V)
    wire(d, (in_gnd[0] - 0.6, Y_CTRLBUS - 0.6), (drv_x0 - 0.9, Y_CTRLBUS - 0.6), C_GND)
    wire(d, (drv_x0 - 0.5, Y_CTRLBUS), drv_in, C_3V3, route="v-then-h")
    wire(d, (drv_x0 - 0.7, Y_CTRLBUS - 0.3), drv_5v_in, C_5V, route="v-then-h")
    wire(d, (drv_x0 - 0.9, Y_CTRLBUS - 0.6), drv_gnd_in, C_GND, route="v-then-h")

    # ---- Title (above schedule), then cable schedule ----
    d.add(elm.Label().at((16, -1.0)).label(
        "Panel Wiring  -  Zone 2 of 4: HEATER BAY\n"
        "Both thermal fuses in series upstream of SSR (E6). RC snubber across SSR T1 / T2 (E10).\n"
        "DRV-BD-001 is a 1 x 2 in protoboard with Q2 + R3 - mounted within 6 in of SSR.",
        fontsize=10))

    cable_schedule(d, 2, -4.0, [
        ("CABLE",  "FROM",                "TO",                       "COND", "WIRE"),
        ("---",    "---",                 "---",                      "---",  "---"),
        ("C-MN-2", "MAINS L bus 2",       "THFUSE-001 a",             "1",    "BLK 14 AWG"),
        ("C-MN-3", "MAINS N bus 2",       "HTR-001 N (return)",       "1",    "WHT 14 AWG"),
        ("C-PE-1", "MAINS chassis stud",  "Bay PE bus",               "1",    "GRN 14 AWG"),
        ("C-CT-1", "CTRL ESP GPIO 22",    "DRV-BD-001 GPIO 22 in",    "1",    "PUR 22 AWG"),
        ("C-CT-2", "CTRL +5 V",           "DRV-BD-001 +5 V in",       "1",    "RED 22 AWG"),
        ("C-CT-3", "CTRL signal GND",     "DRV-BD-001 GND in",        "1",    "BLK 22 AWG"),
    ], col_widths=(2.5, 6.5, 6.5, 1.2, 4.0))

    return d


if __name__ == "__main__":
    save(build(), stem_from_argv0())
