"""Domain 2 - 120 V AC blower circuit (DR-011, supersedes DR-003).

Power path:
    L bus -> FILT-001 (X+Y line filter)
          -> CT-001 (ZMCT103C clamped on L lead, primary mains-isolated)
          -> BLW-CTRL-001 (RobotDyn-style TRIAC dimmer with on-board ZC detect)
          -> BLW-001 (salvaged universal-AC bypass-cooled vacuum motor)
          -> N bus
    BOND-001 bonds the motor frame to chassis earth (universal motor leakage).

Logic side (3.3 V from ESP32):
    GPIO 23 (PWM out)  -> dimmer PWM in (gate trigger, phase-fired)
    GPIO 4  (ZC IRQ)   <- dimmer ZC out (one pulse per AC zero-cross)
    GPIO 34 (ADC)      <- CT-001 burden + bias network (RMS for airflow interlock)

Ferrite chokes (FERR-001) are clamped on the motor leads between TRIAC and
motor; not a schematic component but called out below.
"""
import schemdraw
import schemdraw.elements as elm

from common import WIRE_3V3, WIRE_L, WIRE_N, WIRE_PE, box, save, stem_from_argv0


def build() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.5, fontsize=10)

    # ===================================================================
    # AC power path (top): L bus -> FILT -> CT -> TRIAC -> motor -> N bus
    # ===================================================================
    Y_AC = 0
    X_LBUS = 0
    X_NBUS = 30

    d += elm.Dot().at((X_LBUS, Y_AC)).label("L bus", "left")
    d += elm.Line().at((X_LBUS, Y_AC)).to((2, Y_AC)).color(WIRE_L)

    # FILT-001 - drawn as a labeled rectangle
    box(d, 2, Y_AC - 1, 5, Y_AC + 1)
    d += elm.Line().at((2, Y_AC)).to((5, Y_AC)).color(WIRE_L)
    d += elm.Label().at((3.5, Y_AC + 1.6)).label("FILT-001\nAC line filter\n(X + Y caps)", fontsize=9)

    # CT-001 (current transformer, drawn as inductor passing through the L line)
    d += elm.Line().at((5, Y_AC)).to((6.5, Y_AC)).color(WIRE_L)
    # Primary: just the L wire passing under/through; we show CT body as a box around it
    box(d, 6.5, Y_AC - 1, 9, Y_AC + 1)
    d += elm.Line().at((6.5, Y_AC)).to((9, Y_AC)).color(WIRE_L)
    d += elm.Label().at((7.75, Y_AC + 1.6)).label("CT-001\nZMCT103C 5A\n(split-core)", fontsize=9)

    # CT secondary tap to logic (drawn coming out the bottom)
    ct_sec = (7.75, Y_AC - 1)
    d += elm.Dot().at(ct_sec)
    d += elm.Line().at(ct_sec).down().length(2)

    # TRIAC dimmer module
    d += elm.Line().at((9, Y_AC)).to((11, Y_AC)).color(WIRE_L)
    box(d, 11, Y_AC - 2, 17, Y_AC + 2)
    d += elm.Line().at((11, Y_AC)).to((17, Y_AC)).color(WIRE_L)
    d += elm.Label().at((14, Y_AC + 1.4)).label(
        "BLW-CTRL-001\nTRIAC Dimmer  (RobotDyn-style 8 A)", fontsize=9)
    # Logic pins inside the dimmer box (PWM in, ZC out)
    pwm_pin = (12.5, Y_AC - 2)
    zc_pin = (15.5, Y_AC - 2)
    d += elm.Dot().at(pwm_pin).label("PWM in", "right", fontsize=8)
    d += elm.Dot().at(zc_pin).label("ZC out", "right", fontsize=8)

    # Ferrite choke + line out to motor
    d += elm.Line().at((17, Y_AC)).to((19, Y_AC)).color(WIRE_L)
    d += elm.Label().at((18, Y_AC + 0.7)).label("FERR-001\n(snap-on)", fontsize=8, color="#888888")

    # Motor (universal AC, drawn as an AC source / motor symbol)
    motor = d.add(elm.Motor().at((19, Y_AC)).right().label(
        "BLW-001\nUniversal AC\nbypass-cooled\nvacuum motor", "top"))
    d += elm.Line().at(motor.end).to((X_NBUS, Y_AC)).color(WIRE_N)
    d += elm.Dot().at((X_NBUS, Y_AC)).label("N bus", "right")

    # Earth bond (BOND-001) from motor frame to chassis ground stub
    d += elm.Line().at((motor.center.x, motor.center.y - 1.5)).down().length(2.5).color(WIRE_PE)
    d += elm.Ground().at((motor.center.x, motor.center.y - 4.0)).color(WIRE_PE)
    d += elm.Label().at((motor.center.x + 2.3, motor.center.y - 3.0)).label(
        "BOND-001\nframe -> chassis earth", fontsize=8, color=WIRE_PE)

    # ===================================================================
    # Logic side (bottom): ESP32 PWM/ZC/ADC connections
    # ===================================================================
    Y_ESP = -10
    X_ESP = 5

    # ESP32 stub
    box(d, X_ESP, Y_ESP - 2, X_ESP + 4, Y_ESP + 2)
    d += elm.Label().at((X_ESP + 2, Y_ESP)).label(
        "ESP32\nGPIO 23 (PWM)\nGPIO  4 (ZC IRQ)\nGPIO 34 (ADC)", fontsize=9)
    pin_pwm = (X_ESP + 4, Y_ESP + 1.2)
    pin_zc = (X_ESP + 4, Y_ESP + 0)
    pin_adc = (X_ESP + 4, Y_ESP - 1.2)
    d += elm.Dot().at(pin_pwm)
    d += elm.Dot().at(pin_zc)
    d += elm.Dot().at(pin_adc)

    # PWM out -> dimmer PWM in (purple = 3.3V logic)
    d += elm.Line().at(pin_pwm).to((11, Y_ESP + 1.2)).color(WIRE_3V3)
    d += elm.Line().at((11, Y_ESP + 1.2)).to((11, pwm_pin[1] - 0.001)).color(WIRE_3V3)
    d += elm.Line().at((11, Y_ESP + 1.2)).to((pwm_pin[0], Y_ESP + 1.2)).color(WIRE_3V3)
    d += elm.Line().at((pwm_pin[0], Y_ESP + 1.2)).to(pwm_pin).color(WIRE_3V3)

    # ZC out <- dimmer ZC out
    d += elm.Line().at(zc_pin).to((zc_pin[0], Y_ESP + 0)).color(WIRE_3V3)
    d += elm.Line().at((zc_pin[0], Y_ESP + 0)).to(pin_zc).color(WIRE_3V3)

    # CT secondary -> burden + bias network -> ADC
    # The CT secondary already drops down 2 units; carry it further to a small burden network
    # Burden: 62 ohm shunt (ZMCT103C typical)
    burden_top = (ct_sec[0], Y_AC - 3)
    burden_bot = (ct_sec[0], Y_AC - 5)
    d += elm.Resistor().at(burden_top).to(burden_bot).label("R-BURDEN\n62 ohm")
    # Bias divider: tap at midpoint up to ADC line
    bias_node = (ct_sec[0], Y_AC - 4)
    d += elm.Dot().at(bias_node)
    # Run a horizontal trace from bias_node down/right to the ADC pin
    d += elm.Line().at(burden_bot).down().length(0.8)
    d += elm.Ground().at((ct_sec[0], Y_AC - 5.8))
    # Bias net to ADC
    d += elm.Line().at(bias_node).to((pin_adc[0] + 4, bias_node[1])).color(WIRE_3V3)
    d += elm.Line().at((pin_adc[0] + 4, bias_node[1])).to((pin_adc[0] + 4, pin_adc[1])).color(WIRE_3V3)
    d += elm.Line().at((pin_adc[0] + 4, pin_adc[1])).to(pin_adc).color(WIRE_3V3)
    d += elm.Label().at((pin_adc[0] + 5.5, bias_node[1] + 0.6)).label(
        "(burden + bias\n to ADC mid-rail)", fontsize=8)

    # Title
    d += (elm.Label().at((15, Y_ESP - 5))
          .label("Domain 2 - Blower Circuit (120 V AC, DR-011)\n"
                 "Phase-angle TRIAC control with hardware ZC detect.\n"
                 "ZMCT103C airflow interlock: RMS sensed on GPIO 34 (replaces DR-003 PWM>0 check).\n"
                 "FERR-001 ferrite chokes on motor leads + every TC SPI cable. FILT-001 mandatory for SPI integrity.",
                 fontsize=9))

    return d


if __name__ == "__main__":
    save(build(), stem_from_argv0())
