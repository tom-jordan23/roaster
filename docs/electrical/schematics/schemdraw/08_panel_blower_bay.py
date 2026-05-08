"""Panel-wiring pictorial: BLOWER BAY zone (DR-011).

Mains side:
    L bus pigtail -> FILT-001 L-in
                  -> FILT-001 L-out -> CT-001 P1 -> CT-001 P2 -> BLW-CTRL-001 AC-In L
                  -> BLW-CTRL-001 AC-Out L -> [FERR-001] -> BLW-001 L
    N bus pigtail -> FILT-001 N-in -> FILT-001 N-out -> BLW-CTRL-001 AC-In N
                  -> BLW-CTRL-001 AC-Out N -> [FERR-001] -> BLW-001 N

Earth:
    PE pigtail -> bay PE bus
    FILT-001 PE tab -> PE bus
    BLW-001 motor frame -> PE bus  (BOND-001 - mandatory; universal motor leakage)

Logic side:
    CT-001 secondary -> burden + bias network -> C-CT-A cable to control bay GPIO 34
    BLW-CTRL-001 4-pin header (VCC, GND, ZC, PWM) -> control bay
"""
import schemdraw
import schemdraw.elements as elm

from common import (C_3V3, C_5V, C_GND, C_L, C_N, C_PE, C_SIG,
                    cable_schedule, module, save, stem_from_argv0, term, wire,
                    zone)


def build() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.0, fontsize=9)

    Z_X0, Z_Y0, Z_X1, Z_Y1 = 0, 0, 32, 18
    zone(d, Z_X0, Z_Y0, Z_X1, Z_Y1, "BLOWER BAY  (mains side, DR-011)")

    Y_AC_L = 14.0  # AC L rail (top)
    Y_AC_N = 12.5  # AC N rail (just below L)

    # ---- Incoming pigtails from MAINS ENTRY (top edge) ----
    in_l = (3, 17.4)
    in_n = (5, 17.4)
    in_pe = (7, 17.4)
    d.add(elm.Dot(open=True).at(in_l).label("L  (C-MN-4)", "top", fontsize=7))
    d.add(elm.Dot(open=True).at(in_n).label("N  (C-MN-5)", "top", fontsize=7))
    d.add(elm.Dot(open=True).at(in_pe).label("PE  (C-PE-2)", "top", fontsize=7))

    wire(d, in_l, (3, Y_AC_L), C_L, "BLK 14 AWG", label_at=(3.5, 16.0))
    wire(d, in_n, (5, Y_AC_N), C_N, "WHT 14 AWG", label_at=(5.5, 15.5))
    wire(d, in_pe, (7, 1.5), C_PE, "GRN 14 AWG", label_at=(7.5, 9.5))

    # ---- FILT-001 (line filter) ----
    filt_x0, filt_y0, filt_x1, filt_y1 = 4, 11.5, 7.5, 14.5
    module(d, filt_x0, filt_y0, filt_x1, filt_y1, "FILT-001  EMI line filter")
    filt_l_in = term(d, (filt_x0, Y_AC_L), "L-in", "left")
    filt_n_in = term(d, (filt_x0, Y_AC_N), "N-in", "left")
    filt_l_out = term(d, (filt_x1, Y_AC_L), "L-out", "right")
    filt_n_out = term(d, (filt_x1, Y_AC_N), "N-out", "right")
    filt_pe = term(d, ((filt_x0 + filt_x1) / 2, filt_y0), "PE", "bottom")

    # ---- CT-001 (split-core current transformer, primary clamps on L wire) ----
    ct_x0, ct_x1 = 9, 11
    module(d, ct_x0, Y_AC_L - 0.7, ct_x1, Y_AC_L + 0.7, "CT-001  ZMCT103C")
    ct_p1 = term(d, (ct_x0, Y_AC_L), "P1", "left")
    ct_p2 = term(d, (ct_x1, Y_AC_L), "P2", "right")
    ct_s1 = term(d, ((ct_x0 + ct_x1) / 2 - 0.3, Y_AC_L - 0.7), "S1", "bottom")
    ct_s2 = term(d, ((ct_x0 + ct_x1) / 2 + 0.3, Y_AC_L - 0.7), "S2", "bottom")

    # ---- BLW-CTRL-001 (TRIAC dimmer) ----
    bc_x0, bc_y0, bc_x1, bc_y1 = 13, 8.5, 19, 15.0
    module(d, bc_x0, bc_y0, bc_x1, bc_y1, "BLW-CTRL-001  TRIAC dimmer")
    bc_l_in = term(d, (bc_x0, Y_AC_L), "AC-In L", "left")
    bc_n_in = term(d, (bc_x0, Y_AC_N), "AC-In N", "left")
    bc_l_out = term(d, (bc_x1, Y_AC_L), "AC-Out L", "right")
    bc_n_out = term(d, (bc_x1, Y_AC_N), "AC-Out N", "right")
    bc_vcc = term(d, (bc_x0 + 0.7, bc_y0), "VCC", "bottom")
    bc_gnd = term(d, (bc_x0 + 2.0, bc_y0), "GND", "bottom")
    bc_zc = term(d, (bc_x0 + 3.5, bc_y0), "ZC", "bottom")
    bc_pwm = term(d, (bc_x0 + 5.0, bc_y0), "PWM", "bottom")
    d.add(elm.Label().at(((bc_x0 + bc_x1) / 2, bc_y0 + 1.0)).label(
        "phase-fired TRIAC w/\non-board ZC detect", fontsize=7))

    # FERR-001 ferrite call-out (between dimmer and motor)
    d.add(elm.Label().at((20.5, Y_AC_L + 0.8)).label("FERR-001\n(snap-on)", fontsize=7, color="#888888"))

    # ---- BLW-001 (universal AC vacuum motor) ----
    blw_x0, blw_y0, blw_x1, blw_y1 = 22, 10.5, 28, 14.5
    module(d, blw_x0, blw_y0, blw_x1, blw_y1, "BLW-001  vacuum motor")
    blw_l = term(d, (blw_x0, Y_AC_L), "L", "left")
    blw_n = term(d, (blw_x0, Y_AC_N), "N", "left")
    blw_pe = term(d, ((blw_x0 + blw_x1) / 2, blw_y0), "frame", "bottom")
    d.add(elm.Label().at(((blw_x0 + blw_x1) / 2, blw_y0 + 1.0)).label(
        "salvaged universal AC,\nbypass-cooled,\n~1-4 A draw", fontsize=7))

    # ---- L rail wires ----
    wire(d, (3, Y_AC_L), filt_l_in, C_L, "BLK 14 AWG")
    wire(d, filt_l_out, ct_p1, C_L, "BLK 14 AWG")
    wire(d, ct_p2, bc_l_in, C_L, "BLK 14 AWG")
    wire(d, bc_l_out, blw_l, C_L, "BLK 14 AWG")

    # ---- N rail wires ----
    wire(d, (5, Y_AC_N), filt_n_in, C_N, "WHT 14 AWG")
    wire(d, filt_n_out, bc_n_in, C_N, "WHT 14 AWG")
    wire(d, bc_n_out, blw_n, C_N, "WHT 14 AWG")

    # ---- Burden + bias network for CT-001 secondary ----
    # Drawn just below CT-001 as two resistors (burden + bias divider). The output
    # is a single-ended AC waveform riding on +1.65 V (mid-rail), routed to GPIO 34.
    bn_x0, bn_y0, bn_x1, bn_y1 = 8.5, 6.5, 11.5, 9.0
    module(d, bn_x0, bn_y0, bn_x1, bn_y1, "BN-001  burden + bias")
    bn_in_a = term(d, (bn_x0, 8.5), "S1", "left")
    bn_in_b = term(d, (bn_x0, 7.5), "S2", "left")
    bn_out_sig = term(d, (bn_x1, 8.5), "out (AC)", "right")
    bn_out_gnd = term(d, (bn_x1, 7.0), "GND", "right")
    d.add(elm.Label().at(((bn_x0 + bn_x1) / 2, bn_y0 - 0.4)).label(
        "62 ohm burden across S1-S2;\nresistor divider biases\noutput to mid-rail (1.65 V)",
        fontsize=7))

    wire(d, ct_s1, bn_in_a, C_SIG, route="v-then-h")
    wire(d, ct_s2, bn_in_b, C_SIG, route="v-then-h")
    d.add(elm.Label().at((ct_s1[0] - 0.3, 9.5)).label(
        "twisted pair\nshielded", "left", fontsize=6, color=C_SIG))

    # ---- PE / chassis-earth bus along bottom ----
    d.add(elm.Line().at((1, 1.5)).to((30, 1.5)).color(C_PE))
    d.add(elm.Label().at((15, 0.9)).label(
        "Chassis earth bus  (GRN 14 AWG)  -  FILT PE, motor frame (BOND-001), bay panel",
        fontsize=8, color=C_PE))
    # Drops onto the bus
    wire(d, filt_pe, (filt_pe[0], 2.4), C_PE)
    d.add(elm.Dot().at((filt_pe[0], 2.4)))
    d.add(elm.Label().at((filt_pe[0], 2.7)).label("FILT-001 PE", fontsize=7, color=C_PE))
    wire(d, blw_pe, ((blw_x0 + blw_x1) / 2, 2.4), C_PE, "BOND-001  GRN 14 AWG", label_at=(25.5, 5.0))
    d.add(elm.Dot().at(((blw_x0 + blw_x1) / 2, 2.4)))
    d.add(elm.Label().at(((blw_x0 + blw_x1) / 2, 2.7)).label("BLW-001 frame", fontsize=7, color=C_PE))

    # ---- Outgoing cables to CONTROL BAY (right edge) ----
    out_y0 = 8.0
    out_pwm = (31, out_y0)
    out_zc = (31, out_y0 - 0.8)
    out_vcc = (31, out_y0 - 1.6)
    out_gnd = (31, out_y0 - 2.4)
    out_ct = (31, out_y0 - 3.6)
    out_ct_gnd = (31, out_y0 - 4.4)
    d.add(elm.Dot(open=True).at(out_pwm).label("PWM (C-BL-1)", "right", fontsize=7))
    d.add(elm.Dot(open=True).at(out_zc).label("ZC (C-BL-2)", "right", fontsize=7))
    d.add(elm.Dot(open=True).at(out_vcc).label("+5 V (C-BL-3)", "right", fontsize=7))
    d.add(elm.Dot(open=True).at(out_gnd).label("sig GND (C-BL-4)", "right", fontsize=7))
    d.add(elm.Dot(open=True).at(out_ct).label("CT out (C-BL-5)", "right", fontsize=7))
    d.add(elm.Dot(open=True).at(out_ct_gnd).label("CT GND (C-BL-5)", "right", fontsize=7))

    # Wires from dimmer 4-pin header up out of the zone
    wire(d, bc_pwm, (bc_pwm[0], 6.5), C_3V3)
    wire(d, (bc_pwm[0], 6.5), (29, 6.5), C_3V3)
    wire(d, (29, 6.5), (29, out_pwm[1]), C_3V3)
    wire(d, (29, out_pwm[1]), out_pwm, C_3V3, "PUR 22 AWG", label_at=(30.0, out_pwm[1] + 0.2))

    wire(d, bc_zc, (bc_zc[0], 6.0), C_3V3)
    wire(d, (bc_zc[0], 6.0), (29.4, 6.0), C_3V3)
    wire(d, (29.4, 6.0), (29.4, out_zc[1]), C_3V3)
    wire(d, (29.4, out_zc[1]), out_zc, C_3V3, "PUR 22 AWG", label_at=(30.0, out_zc[1] + 0.2))

    wire(d, bc_vcc, (bc_vcc[0], 5.5), C_5V)
    wire(d, (bc_vcc[0], 5.5), (29.7, 5.5), C_5V)
    wire(d, (29.7, 5.5), (29.7, out_vcc[1]), C_5V)
    wire(d, (29.7, out_vcc[1]), out_vcc, C_5V, "RED 22 AWG", label_at=(30.0, out_vcc[1] + 0.2))

    wire(d, bc_gnd, (bc_gnd[0], 5.0), C_GND)
    wire(d, (bc_gnd[0], 5.0), (28.7, 5.0), C_GND)
    wire(d, (28.7, 5.0), (28.7, out_gnd[1]), C_GND)
    wire(d, (28.7, out_gnd[1]), out_gnd, C_GND, "BLK 22 AWG", label_at=(30.0, out_gnd[1] + 0.2))

    # CT secondary out
    wire(d, bn_out_sig, (12, 8.5), C_SIG)
    wire(d, (12, 8.5), (28.4, out_ct[1]), C_SIG, route="h-then-v")
    wire(d, (28.4, out_ct[1]), out_ct, C_SIG, "BLU 22 AWG shielded", label_at=(29.7, out_ct[1] + 0.2))

    wire(d, bn_out_gnd, (12.3, 7.0), C_GND)
    wire(d, (12.3, 7.0), (28.0, out_ct_gnd[1]), C_GND, route="h-then-v")
    wire(d, (28.0, out_ct_gnd[1]), out_ct_gnd, C_GND, "BLK 22 AWG (drain at one end)",
         label_at=(29.7, out_ct_gnd[1] + 0.2))

    # ---- Title (above schedule) and cable schedule ----
    d.add(elm.Label().at((16, -1.0)).label(
        "Panel Wiring  -  Zone 3 of 4: BLOWER BAY  (DR-011)\n"
        "FILT-001 mandatory: blocks TRIAC EMI from re-entering mains and SPI bus.\n"
        "BOND-001 mandatory: universal motor frame must be earth-bonded.\n"
        "FERR-001 ferrites snap on every motor lead and TC SPI cable.",
        fontsize=10))

    cable_schedule(d, 2, -5.0, [
        ("CABLE",  "FROM",                  "TO",                          "COND", "WIRE"),
        ("---",    "---",                   "---",                         "---",  "---"),
        ("C-MN-4", "MAINS L bus 3",         "FILT-001 L-in",               "1",    "BLK 14 AWG"),
        ("C-MN-5", "MAINS N bus 3",         "FILT-001 N-in",               "1",    "WHT 14 AWG"),
        ("C-PE-2", "MAINS chassis stud",    "Bay PE bus",                  "1",    "GRN 14 AWG"),
        ("C-BL-1", "BLW-CTRL-001 PWM",      "CTRL ESP GPIO 23",            "1",    "PUR 22 AWG"),
        ("C-BL-2", "BLW-CTRL-001 ZC",       "CTRL ESP GPIO 4",             "1",    "PUR 22 AWG"),
        ("C-BL-3", "CTRL +5 V",             "BLW-CTRL-001 VCC",            "1",    "RED 22 AWG"),
        ("C-BL-4", "CTRL signal GND",       "BLW-CTRL-001 GND",            "1",    "BLK 22 AWG"),
        ("C-BL-5", "BN-001 (CT secondary)", "CTRL ESP GPIO 34 + GND",      "2+S",  "BLU+BLK 22 AWG shielded"),
    ], col_widths=(2.5, 6.5, 6.5, 1.2, 6.0))

    return d


if __name__ == "__main__":
    save(build(), stem_from_argv0())
