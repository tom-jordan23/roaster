"""Domain 3 - 3.3 V DC control circuit.

Layout (left -> right, top -> bottom):
    [ESP32-DevKitC]          [MAX31855 #1]  [MAX31855 #2]  [MAX31855 #3]
    GPIO 18 SCK   ----+------+ SCK    DO +--+ SCK    DO +--+ SCK    DO +
    GPIO 19 MISO  ----+------+              +              +
    GPIO  5 CS1   ----+----- CS              :              :
    GPIO 16 CS2   ----+--------------------- CS             :
    GPIO 17 CS3   ----+--------------------------------- CS

    GPIO 22 -> SSR (D1)        (cross-domain stubs to the right)
    GPIO 23 -> TRIAC PWM (D2)
    GPIO  4 <- TRIAC ZC  (D2)
    GPIO 34 <- CT ADC    (D2)
    USB     <-> Host PC

Each MAX31855 -> K-type TC, SS sheath (drawn out the top).
"""
import schemdraw
import schemdraw.elements as elm

from common import WIRE_3V3, WIRE_5V, box, save, stem_from_argv0


def build() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.5, fontsize=10)

    # ===================================================================
    # ESP32 (left)
    # ===================================================================
    X_ESP, Y_ESP = 0, 0
    ESP_W, ESP_H = 5.0, 14.0
    box(d, X_ESP, Y_ESP, X_ESP + ESP_W, Y_ESP + ESP_H)
    d += elm.Label().at((X_ESP + ESP_W / 2, Y_ESP + ESP_H - 0.7)).label(
        "ESP32-DevKitC\n(ESP-001)", fontsize=11)

    def esp_pin(name_label: str, y: float):
        x_in, x_out = X_ESP + ESP_W - 0.4, X_ESP + ESP_W
        d.add(elm.Line().at((x_in, y)).to((x_out, y)))
        d.add(elm.Dot().at((x_out, y)))
        d.add(elm.Label().at((X_ESP + ESP_W - 0.6, y)).label(name_label, "left", fontsize=8))
        return (x_out, y)

    # Top group: SPI shared bus (SCK, MISO)
    p_clk = esp_pin("GPIO 18  SCK", Y_ESP + 12)
    p_miso = esp_pin("GPIO 19  MISO", Y_ESP + 11)

    # Below SPI bus: CS lines (one per chip)
    p_cs1 = esp_pin("GPIO  5  CS1  TC1", Y_ESP + 9.5)
    p_cs2 = esp_pin("GPIO 16  CS2  TC2", Y_ESP + 8.5)
    p_cs3 = esp_pin("GPIO 17  CS3  TC3", Y_ESP + 7.5)

    # Bottom group: cross-domain stubs
    p_ssr = esp_pin("GPIO 22  -> SSR (D1)", Y_ESP + 5)
    p_pwm = esp_pin("GPIO 23  -> TRIAC PWM (D2)", Y_ESP + 4)
    p_zc = esp_pin("GPIO  4  <- TRIAC ZC (D2)", Y_ESP + 3)
    p_adc = esp_pin("GPIO 34  <- CT ADC (D2)", Y_ESP + 2)
    p_usb = esp_pin("USB  <->  Host PC", Y_ESP + 0.7)

    # ===================================================================
    # SPI bus rails (horizontal) and three MAX31855 boxes (above the rails)
    # ===================================================================
    X_BUS = 7
    X_BUS_END = 24
    Y_CLK = p_clk[1]
    Y_MISO = p_miso[1]

    # Pin -> bus
    d += elm.Line().at(p_clk).to((X_BUS, Y_CLK))
    d += elm.Line().at(p_miso).to((X_BUS, Y_MISO))
    # Long bus rails
    d += elm.Line().at((X_BUS, Y_CLK)).to((X_BUS_END, Y_CLK))
    d += elm.Line().at((X_BUS, Y_MISO)).to((X_BUS_END, Y_MISO))
    d += elm.Label().at((X_BUS_END + 0.4, Y_CLK)).label("SCK", "right", fontsize=9)
    d += elm.Label().at((X_BUS_END + 0.4, Y_MISO)).label("MISO", "right", fontsize=9)

    # Three MAX31855 boxes ABOVE the bus, each 3.5 x 3, spaced apart.
    # Pin layout on each box (bottom edge): SCK, DO, CS - left to right.
    MAX_Y0 = Y_MISO + 1.5      # bottom of MAX box (above MISO rail)
    MAX_Y1 = MAX_Y0 + 2.5      # top of MAX box
    max_specs = [
        ("MAX31855 #1\nTC1: Process Air", p_cs1, 8.0),
        ("MAX31855 #2\nTC2: Bean Bed", p_cs2, 14.0),
        ("MAX31855 #3\nTC3: Exhaust", p_cs3, 20.0),
    ]
    # CS rail row (above SPI bus, below MAX boxes) - one Y per chip so lines don't overlap
    cs_rail_y = {p_cs1[1]: Y_MISO + 0.3, p_cs2[1]: Y_MISO + 0.6, p_cs3[1]: Y_MISO + 0.9}

    for label, p_cs, x_max in max_specs:
        bx0, bx1 = x_max, x_max + 3.5
        box(d, bx0, MAX_Y0, bx1, MAX_Y1)
        d += elm.Label().at(((bx0 + bx1) / 2, (MAX_Y0 + MAX_Y1) / 2)).label(
            label, fontsize=9)

        # Pins on bottom of MAX box: SCK | DO | CS - evenly spaced
        x_sck = bx0 + 0.5
        x_do = bx0 + 1.75
        x_cs = bx0 + 3.0

        # SCK pin: drop from MAX bottom to SCK rail (with tap dot)
        d += elm.Line().at((x_sck, MAX_Y0)).to((x_sck, Y_CLK))
        d += elm.Dot().at((x_sck, Y_CLK))
        d += elm.Label().at((x_sck, MAX_Y0 + 0.05)).label("SCK", "bottom", fontsize=7)

        # DO pin: drop from MAX bottom to MISO rail (with tap dot)
        d += elm.Line().at((x_do, MAX_Y0)).to((x_do, Y_MISO))
        d += elm.Dot().at((x_do, Y_MISO))
        d += elm.Label().at((x_do, MAX_Y0 + 0.05)).label("DO", "bottom", fontsize=7)

        # CS pin: trace from ESP CS pin -> CS rail (per-chip Y) -> drop to MAX CS pin
        cs_y = cs_rail_y[p_cs[1]]
        # ESP pin -> short stub right -> down to cs rail y -> right to x_cs -> down to MAX
        d += elm.Line().at(p_cs).to((p_cs[0] + 0.6, p_cs[1])).color(WIRE_3V3)
        d += elm.Line().at((p_cs[0] + 0.6, p_cs[1])).to((p_cs[0] + 0.6, cs_y)).color(WIRE_3V3)
        d += elm.Line().at((p_cs[0] + 0.6, cs_y)).to((x_cs, cs_y)).color(WIRE_3V3)
        d += elm.Line().at((x_cs, cs_y)).to((x_cs, MAX_Y0)).color(WIRE_3V3)
        d += elm.Label().at((x_cs, MAX_Y0 + 0.05)).label("CS", "bottom", fontsize=7)

        # K-type TC out the top of the MAX box
        tc_x = (bx0 + bx1) / 2
        d += elm.Line().at((tc_x, MAX_Y1)).to((tc_x, MAX_Y1 + 1.5))
        d += elm.Dot().at((tc_x, MAX_Y1))
        d += elm.Dot(open=True).at((tc_x, MAX_Y1 + 1.5))
        d += elm.Label().at((tc_x, MAX_Y1 + 1.7)).label(
            "K-type TC\n(SS sheath)", "top", fontsize=8)

    # ===================================================================
    # Cross-domain stubs (below the SPI section, going right off ESP32)
    # ===================================================================
    def stub(p, label, color=None):
        x0, y0 = p
        ln = d.add(elm.Line().at(p).to((x0 + 1.6, y0)))
        if color:
            ln.color(color)
        d.add(elm.Dot(open=True).at((x0 + 1.6, y0)))
        d.add(elm.Label().at((x0 + 1.8, y0)).label(label, "right", fontsize=8))

    stub(p_ssr, "to SSR-001 DC IN -  (Domain 1)", WIRE_3V3)
    stub(p_pwm, "to BLW-CTRL-001 PWM in  (Domain 2)", WIRE_3V3)
    stub(p_zc, "from BLW-CTRL-001 ZC out  (Domain 2)", WIRE_3V3)
    stub(p_adc, "from CT-001 burden / bias  (Domain 2 airflow interlock)", WIRE_3V3)
    stub(p_usb, "Host PC (Artisan)  115200 baud serial", WIRE_5V)

    d += elm.Label().at((p_usb[0] + 1.8, p_usb[1] - 0.8)).label(
        "USB also feeds +5 V to the SSR drive (Domain 1)",
        "right", fontsize=7, color="#666666")

    # Title
    d += (elm.Label()
          .at(((X_ESP + X_BUS_END + 4) / 2, Y_ESP - 2.5))
          .label("Domain 3 - 3.3 V DC Control Circuit\n"
                 "ESP32 with shared SPI bus to 3x MAX31855 (CS lines individual).\n"
                 "All signal wiring 22-26 AWG, routed away from mains. SPI cables shielded; FERR-001 ferrites at each end.",
                 fontsize=9))

    return d


if __name__ == "__main__":
    save(build(), stem_from_argv0())
