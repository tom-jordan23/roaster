# Power Circuit Schematic

## Mains Entry and Protection

```mermaid
graph LR
    subgraph MAINS_ENTRY["Mains Entry"]
        L_IN["L (Hot)"] --- CORD["14 AWG\nw/ strain relief"]
        N_IN["N (Neutral)"] --- CORD
        G_IN["G (Ground)"] --- CORD
    end

    CORD --- DISC["SW-001\n120V 15A\nDisconnect Switch"]
    DISC --- FUSE["FUSE-001\n15A Inline Fuse"]

    FUSE --- L_BUS["L Bus"]
    N_IN --- N_BUS["N Bus"]
    G_IN --- GND_BUS["Chassis Ground Bus"]

    style DISC fill:#ff9,stroke:#333
    style FUSE fill:#f96,stroke:#333
    style GND_BUS fill:#0f0,stroke:#333
```

## Domain 1: 120V AC Heater Circuit

```mermaid
graph TD
    L_BUS["L Bus"] --> SSR_L["SSR-001\nZero-Cross SSR\n25A / 120V AC\nInput: 3-5V DC"]
    SSR_L --> HTR_L["HTR-001\nWarrior 1500W\nNichrome Element\n~9.6 ohm"]
    HTR_L --> N_BUS["N Bus"]

    THFUSE["THFUSE-001\n228°C Thermal Fuse\n(one-shot)"] -.-|"In series\nwith heater"| HTR_L

    ESP_SSR["ESP32 GPIO 22\n(PIN_SSR)"] -->|"3.3V logic\nactive high"| SSR_CTRL["SSR DC Input\n(+ and -)"]
    SSR_CTRL --> SSR_L

    style SSR_L fill:#f66,stroke:#333
    style THFUSE fill:#f96,stroke:#333
```

### Heater Circuit Notes

- SSR switches L (hot) side only — N is continuous to element
- Thermal fuse (THFUSE-001) in series with heater element, mounted on heater can body
- Thermal fuse is independent backup — if SSR fails shorted and safety firmware fails,
  the thermal fuse is the last-resort cutoff
- SSR control: ESP32 GPIO 22 drives SSR DC input (3.3V sufficient for most SSRs)
- Zero-cross switching for burst-fire duty cycle control (1s period, HEATER_PERIOD_MS)
- **Heater draws ~12.5A at 120V** (P = V²/R = 14400/9.6 ≈ 1500W)

## Domain 2: 12V DC Blower Circuit

```mermaid
graph TD
    L_BUS["L Bus"] --> PSU12_L["PSU-002\n12V / 3A+\nSwitching PSU"]
    N_BUS["N Bus"] --> PSU12_N["PSU-002"]
    PSU12_L --> V12_PLUS["+12V Rail"]
    PSU12_N --> V12_GND["12V GND"]

    V12_PLUS --> BLWR_PLUS["BLW-001\n12V Brushless\nCentrifugal Blower\n(+ lead)"]

    BLWR_MINUS["BLW-001\n(- lead)"] --> Q1_DRAIN["Q1 Drain\nIRLZ44N\nLogic-Level\nN-CH MOSFET"]

    Q1_SOURCE["Q1 Source"] --> V12_GND

    ESP_BLWR["ESP32 GPIO 23\n(PIN_BLOWER)"] -->|"PWM\n~25 kHz"| R1["R1\n100 ohm\nGate Resistor"]
    R1 --> Q1_GATE["Q1 Gate"]

    R2["R2\n10k ohm\nGate Pulldown"] --- Q1_GATE
    R2 --- V12_GND

    D1["D1\nFlyback Diode\n1N5819 or similar\nSchottky"] -.-|"Cathode to +12V\nAnode to drain"| BLWR_PLUS

    style Q1_DRAIN fill:#69f,stroke:#333
    style D1 fill:#f9f,stroke:#333
```

### Blower Circuit Notes

- **Q1 (IRLZ44N):** Logic-level N-channel MOSFET. Vgs(th) ~1-2V, fully on at 3.3V gate drive.
  RDS(on) ~0.022 ohm — negligible heat at blower current (~1-2A)
- **R1 (100 ohm):** Gate resistor limits inrush current to gate capacitance, reduces ringing
- **R2 (10k ohm):** Gate-source pulldown ensures MOSFET is OFF when ESP32 pin is floating
  (during boot, reset, or fault)
- **D1 (flyback diode):** Schottky across blower leads (cathode to +12V, anode to drain).
  Clamps inductive kickback when MOSFET switches off. 1N5819 rated 40V/1A is sufficient.
- **PWM frequency:** ~25 kHz (above audible range, within MOSFET switching capability)
- **Speed range:** 0-100% duty cycle maps to 0-100% blower speed

## Domain 3: 3.3V DC Control Circuit

```mermaid
graph TD
    L_BUS["L Bus"] --> PSU5_L["PSU-001\n5V / 2A\nUSB Charger"]
    N_BUS["N Bus"] --> PSU5_N["PSU-001"]
    PSU5_L --> V5_PLUS["+5V → ESP32\nOnboard 3.3V Reg"]
    PSU5_N --> V5_GND["5V GND"]

    V5_PLUS --> ESP["ESP-001\nESP32-DevKitC\n(powered via USB\nor VIN pin)"]

    ESP --> SPI["SPI Bus\nCLK: GPIO 18\nMISO: GPIO 19"]

    SPI --> AMP1["MAX31855 #1\nCS: GPIO 5\n(TC1 Process Air)"]
    SPI --> AMP2["MAX31855 #2\nCS: GPIO 16\n(TC2 Bean Bed)"]
    SPI --> AMP3["MAX31855 #3\nCS: GPIO 17\n(TC3 Exhaust)"]

    AMP1 --- TC1["TC-001\nK-Type TC\nSS Sheath"]
    AMP2 --- TC2["TC-002\nK-Type TC\nSS Sheath"]
    AMP3 --- TC3["TC-003\nK-Type TC\nSS Sheath"]

    ESP -->|"GPIO 22"| SSR_OUT["→ SSR Gate\n(Domain 1)"]
    ESP -->|"GPIO 23\n(PWM)"| MOSFET_OUT["→ MOSFET Gate\n(Domain 2)"]
    ESP -->|"USB Serial\n115200 baud"| PC["Host PC\n(Artisan)"]

    style ESP fill:#6f6,stroke:#333
```

### Control Circuit Notes

- ESP32 powered via USB (5V) — onboard regulator provides 3.3V for MCU and GPIO
- Three MAX31855 share SPI bus (CLK, MISO) with individual CS lines
- MOSI not connected — MAX31855 is read-only
- SPI clock: default ~4 MHz (MAX31855 max is 5 MHz)
- USB serial provides both power and data connection to host PC
- **All signal wiring (22-26 AWG) must be physically routed away from mains wiring (14 AWG)**

## Grounding

```mermaid
graph TD
    MAINS_GND["Mains Earth\n(green wire)"] --> GND_BUS["Chassis Ground\nBus / Stud"]

    GND_BUS --> BASE["Metal Baseplate\n(if metal)"]
    GND_BUS --> PLEN["Plenum Pan\n(ground lug)"]
    GND_BUS --> HTR_CAN["Heater Can\n(ground lug)"]
    GND_BUS --> SSR_HS["SSR Heatsink\n(if metal)"]

    V12_GND["12V PSU GND"] ---|"Star ground\nat PSU output"| SIG_GND["Signal Ground"]
    V5_GND["5V PSU GND"] --- SIG_GND
    SIG_GND --- ESP_GND["ESP32 GND"]

    style GND_BUS fill:#0f0,stroke:#333
    style MAINS_GND fill:#0f0,stroke:#333
```

### Grounding Notes

- **Chassis ground (earth):** All metal enclosure parts bonded to mains earth via
  dedicated ground wire. This is safety-critical — prevents shock if a mains wire
  contacts the chassis.
- **Signal ground:** 12V GND and 5V GND share a common return at the PSU output
  terminals (star ground). ESP32 GND connects here.
- **Do NOT connect chassis earth to signal ground** unless through the PSU's
  internal earth-ground bond (most isolated switching PSUs bond earth to output
  GND via a high-value resistor or Y-cap internally).

## Complete Pin Assignment Summary

| ESP32 GPIO | Function | Connected To | Wire Gauge |
|------------|----------|-------------|------------|
| 18 | SPI CLK | MAX31855 x3 CLK | 22-26 AWG |
| 19 | SPI MISO | MAX31855 x3 DO | 22-26 AWG |
| 5 | TC1 CS | MAX31855 #1 CS | 22-26 AWG |
| 16 | TC2 CS | MAX31855 #2 CS | 22-26 AWG |
| 17 | TC3 CS | MAX31855 #3 CS | 22-26 AWG |
| 22 | SSR Control | SSR-001 DC input (+) | 22-26 AWG |
| 23 | Blower PWM | Q1 gate via R1 (100 ohm) | 22-26 AWG |
| USB | Serial data | Host PC (Artisan) | USB cable |

## Bill of Electrical Materials (schematic-specific)

| Ref | Component | Value | Package | Notes |
|-----|-----------|-------|---------|-------|
| Q1 | N-CH MOSFET | IRLZ44N | TO-220 | Logic-level, Vgs(th) ~1-2V |
| R1 | Gate resistor | 100 ohm | 1/4W axial | Limits gate inrush |
| R2 | Gate pulldown | 10k ohm | 1/4W axial | Ensures off at boot |
| D1 | Flyback diode | 1N5819 | DO-41 | 40V 1A Schottky |
