"""Grounding plan: chassis (PE) star ground vs. signal star ground.

Two separate stars. They are tied together at exactly one point: inside the
isolated 5 V PSU (PSU-001), via its Y-cap or earth-bond. Do NOT add a second
chassis-to-signal-GND tie - it creates a ground loop.

Chassis ground star (mains earth, green):
    Mains Earth (cord G) -> Chassis GND bus / stud
        +-> Metal baseplate
        +-> Plenum pan (ground lug)
        +-> Heater can (ground lug)
        +-> SSR-001 heatsink (if metal)
        +-> Blower motor frame (BOND-001) - DR-011

Signal ground star (5 V PSU 0 V output):
    +-> ESP32 GND
    +-> TRIAC dimmer logic GND
    +-> CT-001 burden / bias return
    (tied to chassis only via PSU's internal earth bond)
"""
import schemdraw
import schemdraw.elements as elm

from common import SIG_GND, WIRE_PE, box, save, stem_from_argv0


def build() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.5, fontsize=10)

    # ===================================================================
    # Left half - Chassis (PE) ground star
    # ===================================================================
    X_PE = 0
    Y_TOP = 0
    # Mains earth source
    d += elm.Dot(open=True).at((X_PE, Y_TOP)).label("Mains Earth\n(cord G, green)", "left")
    d += elm.Line().at((X_PE, Y_TOP)).down().length(2).color(WIRE_PE)
    pe_bus = (X_PE, Y_TOP - 2)
    # Chassis GND bus / stud
    box(d, X_PE - 1.5, Y_TOP - 3, X_PE + 1.5, Y_TOP - 2)
    d += elm.Label().at((X_PE, Y_TOP - 2.5)).label("Chassis GND bus\n(green-painted stud)", fontsize=9)
    pe_star = (X_PE, Y_TOP - 3)
    d += elm.Dot().at(pe_star)

    # Star branches: each goes down + right to a labeled load
    pe_loads = [
        "Metal baseplate",
        "Plenum pan\n(ground lug)",
        "Heater can\n(ground lug)",
        "SSR-001 heatsink\n(if metal)",
        "Blower motor frame\n(BOND-001 - DR-011)",
    ]
    for i, name in enumerate(pe_loads):
        y_branch = pe_star[1] - 1.5 - i * 1.6
        d += elm.Line().at(pe_star).to((pe_star[0], y_branch)).color(WIRE_PE)
        d += elm.Line().at((pe_star[0], y_branch)).to((pe_star[0] + 3, y_branch)).color(WIRE_PE)
        d += elm.Dot().at((pe_star[0] + 3, y_branch)).color(WIRE_PE)
        d += elm.Label().at((pe_star[0] + 3.2, y_branch)).label(name, "right", fontsize=9)

    # Vertical line down for the chassis ground rail (visual)
    d += elm.Line().at(pe_star).to((pe_star[0], pe_star[1] - 1.5 - (len(pe_loads) - 1) * 1.6)).color(WIRE_PE)

    d += elm.Label().at((pe_star[0] - 1.5, pe_star[1] - 5)).label(
        "Star ground:\nall PE returns\nbond at the stud,\nnot daisy-chained",
        "left", fontsize=8, color="#666666")

    # ===================================================================
    # Right half - Signal (0 V) ground star
    # ===================================================================
    X_SIG = 14
    # 5 V PSU at top of signal column
    box(d, X_SIG - 2, Y_TOP - 3, X_SIG + 2, Y_TOP - 0.5)
    d += elm.Label().at((X_SIG, Y_TOP - 1.7)).label(
        "PSU-001\n5 V / 2 A USB charger\n(isolated SMPS)", fontsize=9)
    sig_psu_gnd = (X_SIG, Y_TOP - 3)
    d += elm.Dot().at(sig_psu_gnd).label("0 V out", "left", fontsize=8)

    # Signal ground star branches
    sig_loads = [
        "ESP32 GND",
        "TRIAC dimmer\nlogic GND",
        "CT-001 burden\n+ bias return",
        "MAX31855 GND\n(via SPI cable shield drain - one end)",
    ]
    for i, name in enumerate(sig_loads):
        y_branch = sig_psu_gnd[1] - 1.5 - i * 1.6
        d += elm.Line().at(sig_psu_gnd).to((sig_psu_gnd[0], y_branch)).color(SIG_GND)
        d += elm.Line().at((sig_psu_gnd[0], y_branch)).to((sig_psu_gnd[0] + 3, y_branch)).color(SIG_GND)
        d += elm.Dot().at((sig_psu_gnd[0] + 3, y_branch)).color(SIG_GND)
        d += elm.Label().at((sig_psu_gnd[0] + 3.2, y_branch)).label(name, "right", fontsize=9)

    d += elm.Line().at(sig_psu_gnd).to(
        (sig_psu_gnd[0], sig_psu_gnd[1] - 1.5 - (len(sig_loads) - 1) * 1.6)
    ).color(SIG_GND)

    # ===================================================================
    # The single PE <-> signal GND tie inside the PSU (drawn as a Y-cap symbol)
    # ===================================================================
    # PSU PE input (left side of PSU box) -> internal Y-cap -> 0V output node
    psu_pe_in = (X_SIG - 2, Y_TOP - 1.7)  # left edge of PSU box
    # Tie line from PE bus over to PSU
    d += elm.Line().at((pe_star[0] + 3, pe_star[1] - 1.5)).to((X_SIG - 5, pe_star[1] - 1.5)).color(WIRE_PE)
    d += elm.Line().at((X_SIG - 5, pe_star[1] - 1.5)).to((X_SIG - 5, psu_pe_in[1])).color(WIRE_PE)
    d += elm.Line().at((X_SIG - 5, psu_pe_in[1])).to(psu_pe_in).color(WIRE_PE)
    d += elm.Label().at((X_SIG - 5.2, (pe_star[1] - 1.5 + psu_pe_in[1]) / 2)).label(
        "PE in\n(green wire\nto PSU\nchassis pin)", "left", fontsize=8, color=WIRE_PE)

    # Note about the single tie point
    d += elm.Label().at((X_SIG, Y_TOP - 11)).label(
        "Single PE <-> signal-GND tie inside PSU-001\n"
        "(internal Y-cap or earth-bond resistor).\n"
        "Do NOT add a second chassis-to-signal-GND wire\n"
        "anywhere else - that would create a ground loop\n"
        "and inject motor/SSR noise into the SPI bus.",
        fontsize=8, color="#666666")

    # ===================================================================
    # Title and isolation note at bottom
    # ===================================================================
    d += elm.Label().at((X_SIG / 2 - 1, Y_TOP - 14)).label(
        "Grounding Plan - Two Stars, One Tie\n"
        "Left: chassis (PE) star at the ground stud, all metal parts bond here.\n"
        "Right: signal (0 V) star at PSU-001 0 V output, all logic returns bond here.\n"
        "The two stars are tied at exactly one point - inside PSU-001.",
        fontsize=9)

    # Mid-divider note
    d += elm.Label().at(((X_PE + X_SIG) / 2, Y_TOP + 0.3)).label(
        "ISOLATION BARRIER\n(PSU-001)", fontsize=10, color="#888888")

    return d


if __name__ == "__main__":
    save(build(), stem_from_argv0())
