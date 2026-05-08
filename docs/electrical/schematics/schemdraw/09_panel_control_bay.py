"""Panel-wiring pictorial: CONTROL BAY zone (low-voltage side).

Modules:
    PSU-001     5 V / 2 A USB charger (mains in, USB out)
    ESP-001     ESP32-DevKitC (powered via USB-A from PSU-001)
    MAX31855 #1 / #2 / #3   K-type TC amplifiers, share SPI bus

Cables out to other zones:
    -> HEATER  (C-CT-1..3)  GPIO 22 + 5 V + GND  for SSR drive
    -> BLOWER  (C-BL-1..5)  PWM, ZC, +5 V, GND, CT-out + GND
    <- BLOWER  CT secondary (analog, shielded twisted pair)

PSU-001 PE pin internally bonds to its own 0 V output (earth tie).
"""
import schemdraw
import schemdraw.elements as elm

from common import (C_3V3, C_5V, C_GND, C_L, C_N, C_PE, C_SIG,
                    cable_schedule, module, save, stem_from_argv0, term, wire,
                    zone)


def build() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.0, fontsize=9)

    Z_X0, Z_Y0, Z_X1, Z_Y1 = 0, 0, 32, 22
    zone(d, Z_X0, Z_Y0, Z_X1, Z_Y1, "CONTROL BAY  (low-voltage side)")

    # ---- Incoming pigtails from MAINS ENTRY (top edge, far left) ----
    in_l = (3, 21.4)
    in_n = (5, 21.4)
    in_pe = (7, 21.4)
    d.add(elm.Dot(open=True).at(in_l).label("L (C-MN-6)", "top", fontsize=7))
    d.add(elm.Dot(open=True).at(in_n).label("N (C-MN-7)", "top", fontsize=7))
    d.add(elm.Dot(open=True).at(in_pe).label("PE (C-PE-3)", "top", fontsize=7))

    # ---- PSU-001 (5 V/2 A USB charger) ----
    psu_x0, psu_y0, psu_x1, psu_y1 = 4, 17.5, 11, 20.5
    module(d, psu_x0, psu_y0, psu_x1, psu_y1, "PSU-001  5 V / 2 A USB charger")
    psu_l = term(d, (psu_x0, 19.5), "L", "left")
    psu_n = term(d, (psu_x0, 18.5), "N", "left")
    psu_pe = term(d, ((psu_x0 + psu_x1) / 2, psu_y0), "PE\n(internal earth bond)", "bottom")
    psu_5v = term(d, (psu_x1, 19.5), "+5 V (USB-A)", "right")
    psu_gnd = term(d, (psu_x1, 18.5), "0 V (USB-A)", "right")

    wire(d, in_l, psu_l, C_L, "BLK 14 AWG")
    wire(d, in_n, psu_n, C_N, "WHT 14 AWG")

    # ---- ESP-001 (ESP32-DevKitC) ----
    esp_x0, esp_y0, esp_x1, esp_y1 = 4, 7, 13, 16
    module(d, esp_x0, esp_y0, esp_x1, esp_y1, "ESP-001  ESP32-DevKitC")
    esp_usb = term(d, ((esp_x0 + esp_x1) / 2, esp_y1), "USB-micro\n(power + serial)", "top")
    # Right-side pins (logic outputs / SPI)
    pins = [
        ("GPIO 18  SCK",  15.5),
        ("GPIO 19  MISO", 15.0),
        ("GPIO  5  CS1",  14.5),
        ("GPIO 16  CS2",  14.0),
        ("GPIO 17  CS3",  13.5),
        ("GPIO 22  -> SSR (D1)",       12.5),
        ("GPIO 23  -> TRIAC PWM (D2)", 12.0),
        ("GPIO  4  <- TRIAC ZC  (D2)", 11.5),
        ("GPIO 34  <- CT  ADC   (D2)", 11.0),
        ("3V3 out", 10.0),
        ("GND",     9.5),
    ]
    pin_pts = {}
    for label, y in pins:
        pin_pts[label] = term(d, (esp_x1, y), label, "right")
    # USB cable from PSU to ESP
    wire(d, psu_5v, (12, 19.5), C_5V)
    wire(d, (12, 19.5), (12, esp_y1 + 0.5), C_5V)
    wire(d, (12, esp_y1 + 0.5), (esp_usb[0], esp_y1 + 0.5), C_5V)
    wire(d, (esp_usb[0], esp_y1 + 0.5), esp_usb, C_5V, "USB-A -> USB-micro\n(power + serial)",
         label_at=(11.5, 17.0))
    # Add USB host PC stub
    d.add(elm.Dot(open=True).at((esp_usb[0], esp_y1 + 1.5)).label(
        "to host PC\n(Artisan, 115200 bps)", "top", fontsize=7))
    wire(d, (esp_usb[0], esp_y1 + 0.5), (esp_usb[0], esp_y1 + 1.5), C_5V)

    # ---- 3x MAX31855 (right of ESP, stacked vertically) ----
    max_specs = [
        ("MAX31855 #1\nTC1: Process Air", "GPIO  5  CS1",  20.0),
        ("MAX31855 #2\nTC2: Bean Bed",    "GPIO 16  CS2",  16.5),
        ("MAX31855 #3\nTC3: Exhaust",     "GPIO 17  CS3",  13.0),
    ]
    max_pins = []  # list of (vcc, gnd, sck, do, cs, tcp, tcm)
    for label, cs_pin_name, mx0_y_top in max_specs:
        mx_x0, mx_y1 = 18, mx0_y_top
        mx_x1, mx_y0 = 24, mx0_y_top - 3.0
        module(d, mx_x0, mx_y0, mx_x1, mx_y1, label)
        m_vcc = term(d, (mx_x0, mx_y1 - 0.4), "VCC", "left")
        m_gnd = term(d, (mx_x0, mx_y1 - 0.9), "GND", "left")
        m_sck = term(d, (mx_x0, mx_y1 - 1.5), "SCK", "left")
        m_do = term(d, (mx_x0, mx_y1 - 2.0), "DO", "left")
        m_cs = term(d, (mx_x0, mx_y1 - 2.5), "CS", "left")
        m_tcp = term(d, (mx_x1, mx_y1 - 0.6), "T+", "right")
        m_tcm = term(d, (mx_x1, mx_y1 - 1.2), "T-", "right")
        max_pins.append({
            "vcc": m_vcc, "gnd": m_gnd, "sck": m_sck, "do": m_do, "cs": m_cs,
            "tcp": m_tcp, "tcm": m_tcm, "cs_name": cs_pin_name,
        })

    # ---- SPI fan-out: SCK and MISO from ESP to all 3 MAX, CS individual ----
    sck_pin = pin_pts["GPIO 18  SCK"]
    miso_pin = pin_pts["GPIO 19  MISO"]
    # Routing: take SCK and MISO over to a vertical riser at x=15.5, then drop down
    # and tap into each MAX SCK / DO pin.
    riser_sck_x = 15.5
    riser_miso_x = 16.0
    wire(d, sck_pin, (riser_sck_x, sck_pin[1]), C_3V3)
    wire(d, miso_pin, (riser_miso_x, miso_pin[1]), C_3V3)
    # SCK riser: from sck_pin.y down to lowest MAX sck.y
    bottom_sck_y = max_pins[-1]["sck"][1]
    top_sck_y = sck_pin[1]
    wire(d, (riser_sck_x, top_sck_y), (riser_sck_x, bottom_sck_y), C_3V3)
    bottom_miso_y = max_pins[-1]["do"][1]
    wire(d, (riser_miso_x, miso_pin[1]), (riser_miso_x, bottom_miso_y), C_3V3)
    for mp in max_pins:
        # tap from SCK riser to MAX SCK
        wire(d, (riser_sck_x, mp["sck"][1]), mp["sck"], C_3V3)
        d.add(elm.Dot().at((riser_sck_x, mp["sck"][1])))
        # tap from MISO riser to MAX DO
        wire(d, (riser_miso_x, mp["do"][1]), mp["do"], C_3V3)
        d.add(elm.Dot().at((riser_miso_x, mp["do"][1])))
        # CS lines: individual from ESP CS pin to MAX CS
        cs_pin = pin_pts[mp["cs_name"]]
        # Each CS gets its own riser slot
        cs_x = 16.5 + 0.4 * max_pins.index(mp)
        wire(d, cs_pin, (cs_x, cs_pin[1]), C_3V3)
        wire(d, (cs_x, cs_pin[1]), (cs_x, mp["cs"][1]), C_3V3)
        wire(d, (cs_x, mp["cs"][1]), mp["cs"], C_3V3)

    # ---- VCC / GND for each MAX (tap from ESP 3V3 out + GND pins) ----
    esp_3v3 = pin_pts["3V3 out"]
    esp_gnd = pin_pts["GND"]
    # Combined power rail along x=14.5 going down
    rail_3v3_x = 14.5
    rail_gnd_x = 14.0
    bottom_vcc_y = max_pins[-1]["vcc"][1]
    bottom_gnd_y = max_pins[-1]["gnd"][1]
    wire(d, esp_3v3, (rail_3v3_x, esp_3v3[1]), C_3V3)
    wire(d, (rail_3v3_x, esp_3v3[1]), (rail_3v3_x, max(bottom_vcc_y, bottom_gnd_y)), C_3V3)
    wire(d, esp_gnd, (rail_gnd_x, esp_gnd[1]), C_GND)
    wire(d, (rail_gnd_x, esp_gnd[1]), (rail_gnd_x, max(bottom_vcc_y, bottom_gnd_y)), C_GND)
    for mp in max_pins:
        wire(d, (rail_3v3_x, mp["vcc"][1]), mp["vcc"], C_3V3)
        d.add(elm.Dot().at((rail_3v3_x, mp["vcc"][1])))
        wire(d, (rail_gnd_x, mp["gnd"][1]), mp["gnd"], C_GND)
        d.add(elm.Dot().at((rail_gnd_x, mp["gnd"][1])))

    # ---- Thermocouple stubs out the right of each MAX ----
    for i, mp in enumerate(max_pins):
        # Yellow + Red K-type TC pair
        d.add(elm.Line().at(mp["tcp"]).right().length(0.7).color("#cca000"))  # K+ yellow
        d.add(elm.Dot(open=True).at((mp["tcp"][0] + 0.7, mp["tcp"][1])))
        d.add(elm.Line().at(mp["tcm"]).right().length(0.7).color("#c8262a"))  # K- red
        d.add(elm.Dot(open=True).at((mp["tcm"][0] + 0.7, mp["tcm"][1])))
        d.add(elm.Label().at((mp["tcp"][0] + 1.0, (mp["tcp"][1] + mp["tcm"][1]) / 2)).label(
            "K-type TC\nYEL=+  RED=-\n(K-cable)", "right", fontsize=7))

    # ---- PSU PE bond from PSU to bay PE bus ----
    wire(d, psu_pe, ((psu_x0 + psu_x1) / 2, 16.0), C_PE)
    wire(d, ((psu_x0 + psu_x1) / 2, 16.0), (in_pe[0], 16.0), C_PE)
    wire(d, in_pe, (in_pe[0], 1.5), C_PE, "GRN 14 AWG", label_at=(in_pe[0] + 0.5, 13.5))

    # PE bus
    d.add(elm.Line().at((1, 1.5)).to((30, 1.5)).color(C_PE))
    d.add(elm.Label().at((15, 0.9)).label(
        "Chassis earth bus  (GRN 14 AWG)  -  PSU-001 PE, ESP/MAX board mounting screws (if metal)",
        fontsize=8, color=C_PE))

    # ---- Outgoing cables to HEATER BAY (left edge, mid) ----
    out_g22 = (1, 7.5)
    out_5v = (1, 6.7)
    out_gnd = (1, 5.9)
    d.add(elm.Dot(open=True).at(out_g22).label("GPIO 22\n(C-CT-1)", "left", fontsize=7))
    d.add(elm.Dot(open=True).at(out_5v).label("+5 V\n(C-CT-2)", "left", fontsize=7))
    d.add(elm.Dot(open=True).at(out_gnd).label("sig GND\n(C-CT-3)", "left", fontsize=7))
    # ESP GPIO 22 -> out_g22
    g22 = pin_pts["GPIO 22  -> SSR (D1)"]
    wire(d, g22, (g22[0] + 0.5, g22[1]), C_3V3)
    wire(d, (g22[0] + 0.5, g22[1]), (g22[0] + 0.5, 7.5), C_3V3)
    wire(d, (g22[0] + 0.5, 7.5), out_g22, C_3V3, "PUR 22 AWG", label_at=(7.5, 7.7))
    # +5 V tap (from PSU-001 +5V output)
    wire(d, psu_5v, (12.5, 19.5), C_5V)  # extra tap point already drawn above
    wire(d, (12.5, 19.5), (12.5, 6.7), C_5V)
    wire(d, (12.5, 6.7), out_5v, C_5V, "RED 22 AWG", label_at=(7.5, 6.9))
    # signal GND tap (from ESP GND pin / PSU 0V)
    wire(d, esp_gnd, (esp_gnd[0] + 0.7, esp_gnd[1]), C_GND)
    wire(d, (esp_gnd[0] + 0.7, esp_gnd[1]), (esp_gnd[0] + 0.7, 5.9), C_GND)
    wire(d, (esp_gnd[0] + 0.7, 5.9), out_gnd, C_GND, "BLK 22 AWG", label_at=(7.5, 6.1))

    # ---- Outgoing cables to BLOWER BAY (left edge, lower) ----
    out_pwm = (1, 4.5)
    out_zc = (1, 3.9)
    out_vccb = (1, 3.3)
    out_gndb = (1, 2.7)
    out_ct = (1, 4.5 - 3.6 + 0.2)
    out_ct_gnd = out_ct
    # Use the same dot-style stubs at left edge
    d.add(elm.Dot(open=True).at(out_pwm).label("GPIO 23 (PWM)\n(C-BL-1)", "left", fontsize=7))
    d.add(elm.Dot(open=True).at(out_zc).label("GPIO 4 (ZC)\n(C-BL-2)", "left", fontsize=7))
    d.add(elm.Dot(open=True).at(out_vccb).label("+5 V\n(C-BL-3)", "left", fontsize=7))
    d.add(elm.Dot(open=True).at(out_gndb).label("sig GND\n(C-BL-4)", "left", fontsize=7))

    # PWM
    g23 = pin_pts["GPIO 23  -> TRIAC PWM (D2)"]
    wire(d, g23, (g23[0] + 0.8, g23[1]), C_3V3)
    wire(d, (g23[0] + 0.8, g23[1]), (g23[0] + 0.8, 4.5), C_3V3)
    wire(d, (g23[0] + 0.8, 4.5), out_pwm, C_3V3, "PUR 22 AWG")
    # ZC
    g4 = pin_pts["GPIO  4  <- TRIAC ZC  (D2)"]
    wire(d, g4, (g4[0] + 1.0, g4[1]), C_3V3)
    wire(d, (g4[0] + 1.0, g4[1]), (g4[0] + 1.0, 3.9), C_3V3)
    wire(d, (g4[0] + 1.0, 3.9), out_zc, C_3V3, "PUR 22 AWG")
    # +5V to blower
    wire(d, (12.7, 19.5), (12.7, 3.3), C_5V)
    wire(d, (12.7, 3.3), out_vccb, C_5V, "RED 22 AWG")
    # GND to blower
    wire(d, (esp_gnd[0] + 0.9, esp_gnd[1]), (esp_gnd[0] + 0.9, 2.7), C_GND)
    wire(d, esp_gnd, (esp_gnd[0] + 0.9, esp_gnd[1]), C_GND)
    wire(d, (esp_gnd[0] + 0.9, 2.7), out_gndb, C_GND, "BLK 22 AWG")

    # CT input from blower (incoming cable, at very bottom-left)
    in_ct = (1, 4.0)
    # Note: this overlaps with out_pwm visually; place it deeper down
    in_ct = (1, 5.1)
    g34 = pin_pts["GPIO 34  <- CT  ADC   (D2)"]
    d.add(elm.Dot(open=True).at(in_ct).label("CT in\n(C-BL-5)", "left", fontsize=7))
    wire(d, in_ct, (g34[0] + 1.2, in_ct[1]), C_SIG)
    wire(d, (g34[0] + 1.2, in_ct[1]), (g34[0] + 1.2, g34[1]), C_SIG)
    wire(d, (g34[0] + 1.2, g34[1]), g34, C_SIG, "BLU 22 AWG shielded")

    # ---- Title and cable schedule (below zone) ----
    d.add(elm.Label().at((16, -1.0)).label(
        "Panel Wiring  -  Zone 4 of 4: CONTROL BAY  (low-voltage side)\n"
        "PSU-001 internal earth bond is the SINGLE PE <-> signal-GND tie - do not add another.\n"
        "All TC cables shielded, drained at the panel end only. SCK / MISO are shared SPI; CS individual.",
        fontsize=10))

    cable_schedule(d, 2, -5.0, [
        ("CABLE",  "FROM",                  "TO",                          "COND", "WIRE"),
        ("---",    "---",                   "---",                         "---",  "---"),
        ("C-MN-6", "MAINS L bus 4",         "PSU-001 L",                   "1",    "BLK 14 AWG"),
        ("C-MN-7", "MAINS N bus 4",         "PSU-001 N",                   "1",    "WHT 14 AWG"),
        ("C-PE-3", "MAINS chassis stud",    "Bay PE bus + PSU-001 PE",     "1",    "GRN 14 AWG"),
        ("(int)",  "PSU-001 USB-A out",     "ESP-001 USB-micro",           "n/a",  "USB-A to USB-uB"),
        ("(int)",  "ESP-001 SCK / MISO",    "MAX31855 #1/#2/#3 SCK / DO",  "2",    "PUR 22 AWG"),
        ("(int)",  "ESP-001 CS1 / 2 / 3",   "MAX31855 #1 / #2 / #3 CS",    "1 ea", "PUR 22 AWG"),
        ("(int)",  "ESP-001 3V3 / GND",     "MAX31855 #1/#2/#3 VCC / GND", "2",    "RED + BLK 22 AWG"),
        ("(TC)",   "MAX31855 #1 T+ / T-",   "TC-001 (process air)",        "2",    "K-cable YEL+RED"),
        ("(TC)",   "MAX31855 #2 T+ / T-",   "TC-002 (bean bed)",           "2",    "K-cable YEL+RED"),
        ("(TC)",   "MAX31855 #3 T+ / T-",   "TC-003 (exhaust)",            "2",    "K-cable YEL+RED"),
        ("C-CT-1", "ESP GPIO 22",           "HEATER DRV-BD-001 in",        "1",    "PUR 22 AWG"),
        ("C-CT-2", "PSU-001 +5 V tap",      "HEATER DRV-BD-001 +5 V",      "1",    "RED 22 AWG"),
        ("C-CT-3", "ESP GND",               "HEATER DRV-BD-001 GND",       "1",    "BLK 22 AWG"),
        ("C-BL-1", "ESP GPIO 23",           "BLOWER BLW-CTRL PWM",         "1",    "PUR 22 AWG"),
        ("C-BL-2", "BLOWER BLW-CTRL ZC",    "ESP GPIO 4",                  "1",    "PUR 22 AWG"),
        ("C-BL-3", "PSU-001 +5 V tap",      "BLOWER BLW-CTRL VCC",         "1",    "RED 22 AWG"),
        ("C-BL-4", "ESP GND",               "BLOWER BLW-CTRL GND",         "1",    "BLK 22 AWG"),
        ("C-BL-5", "BLOWER BN-001 out",     "ESP GPIO 34 + GND",           "2+S",  "BLU+BLK 22 AWG shielded"),
    ], col_widths=(2.5, 6.5, 6.5, 1.2, 6.0))

    return d


if __name__ == "__main__":
    save(build(), stem_from_argv0())
