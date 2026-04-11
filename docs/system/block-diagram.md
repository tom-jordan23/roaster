# System Block Diagram

## Overview

This document defines the system-level architecture for the v1 fluid-bed coffee roaster.
All subsystem boundaries and interfaces are defined here. Downstream design work
(mechanical, electrical, firmware) must be consistent with these diagrams.

---

## Air Path

The process airflow is the core physical system. Everything else exists to support,
control, and measure this flow.

```mermaid
flowchart LR
    A[Ambient Air] --> B[Blower]
    B --> C[Heater Can]
    C -->|Side Entry| D[Box Plenum]
    D --> E[Baffles / Flow Conditioning]
    E --> F[Distributor Plate]
    F --> G[Roast Chamber]
    G --> H[Expansion Chamber\n~4in OD x 5in tall SS]
    H --> J[30x30 SS Mesh Screen]
    J --> I[Exhaust Out]

    style F fill:#f96,stroke:#333
    style D fill:#69f,stroke:#333
    style H fill:#f9f,stroke:#333
```

### Air Path Notes

| Segment | Key Parameter | Design Concern |
|---------|--------------|----------------|
| Blower → Heater Can | Airflow rate (CFM), static pressure | Hose clamp joint (not welded) to preserve future bypass option (DR-005) |
| Heater Can | Air temperature rise | Element must fit the can; air must contact element long enough for heat transfer |
| Heater Can → Plenum | Side-entry velocity | High inlet velocity must be tamed by plenum + baffles |
| Plenum + Baffles | Pressure equalization | Convert directional jet to uniform pressure field |
| Distributor Plate | Velocity uniformity | Critical tuning component — must be swappable for iteration |
| Roast Chamber | Fluidization quality | Even bed motion, no dead zones, no geysering |
| Expansion Chamber | Chaff separation by velocity drop | Step-up from chamber dia to ~4" OD drops velocity to 2-4 ft/sec; chaff settles (DR-006) |
| Mesh Screen | Secondary chaff capture | 30×30 SS mesh; removable for cleaning between roasts |
| Exhaust | Backpressure budget | Expansion chamber + mesh must not restrict flow enough to impede fluidization |

### Cooling Mode (DR-005)

During cooling: SSR off (heater 0%), blower 100%. Air path remains serial
(Blower → Heater Can → Plenum → Chamber). Residual heater thermal mass
(~13-23 kJ) dissipates in ~15-30 seconds at 10-15 CFM forced convection.
Target: beans from ~200°C to <50°C within 140 seconds.

The blower-to-heater-can joint is a hose clamp connection, not welded. If
TP-002 data shows thermal lag is unacceptable, the heater can can be physically
disconnected for bypass cooling, or a diverter added later.

---

## Power Path

```mermaid
flowchart TD
    MAINS["120V AC Mains"] --> DISC["Hard Disconnect\n(switch or plug)"]
    DISC --> FUSE["Fuse / Breaker\n(15A)"]
    FUSE --> BUS["AC Power Bus"]

    subgraph DOMAIN1["Domain 1: 120V AC (Mains)"]
        BUS --> SSR["Zero-Cross SSR"]
        SSR --> HTR["Heater Element\n(Warrior 1500W nichrome)"]
    end

    subgraph DOMAIN2["Domain 2: 12V DC"]
        BUS --> PSU12["12V AC-DC PSU\n(switching, 3A+)"]
        PSU12 --> MOSFET["Logic-Level MOSFET\n(e.g. IRLZ44N)"]
        MOSFET --> BLWR["12V Brushless\nCentrifugal Blower"]
    end

    subgraph DOMAIN3["Domain 3: 3.3V DC"]
        BUS --> PSU3["3.3V PSU\n(USB or regulator)"]
        PSU3 --> ESP["ESP32 + Control Board"]
    end

    ESP -->|"GPIO (PWM)"| MOSFET
    ESP -->|"GPIO"| SSR

    style SSR fill:#f66,stroke:#333
    style DISC fill:#ff9,stroke:#333
    style DOMAIN1 fill:#fee,stroke:#c33
    style DOMAIN2 fill:#eef,stroke:#33c
    style DOMAIN3 fill:#efe,stroke:#3c3
```

### Power Path Notes

- **Three power domains:** 120V AC (heater), 12V DC (blower), 3.3V DC (controls)
- Hard disconnect is **mandatory** — must be reachable during operation
- Fuse sized for total load: heater + 12V PSU + 3.3V PSU (~13A max at 120V)
- SSR is controlled by ESP32 via zero-cross switching for burst-fire duty control
- Blower driven by MOSFET with PWM from ESP32 — no AC motor control needed
- 12V PSU: switching wall wart or enclosed supply, 3A minimum
- Both low-voltage PSUs must be isolated from mains; ESP32 side is entirely low-voltage
- Flyback diode required across blower motor leads
- **All metal chassis components must be grounded to mains earth**

---

## Signal Path

```mermaid
flowchart TD
    subgraph Sensors
        TC1["TC1: Process Air\n(K-type)"]
        TC2["TC2: Bean Bed\n(K-type)"]
        TC3["TC3: Exhaust\n(K-type)"]
    end

    subgraph TC_Interface["TC Amplifiers"]
        AMP1["MAX31855 #1"]
        AMP2["MAX31855 #2"]
        AMP3["MAX31855 #3"]
    end

    TC1 --> AMP1
    TC2 --> AMP2
    TC3 --> AMP3

    subgraph MCU["ESP32"]
        SPI["SPI Bus"]
        GPIO_SSR["GPIO → SSR Control"]
        GPIO_BLWR["GPIO → Blower Control"]
        SAFETY["Safety Layer"]
        CTRL["Control Layer"]
        LOG["Logging Layer"]
    end

    AMP1 -->|SPI + CS1| SPI
    AMP2 -->|SPI + CS2| SPI
    AMP3 -->|SPI + CS3| SPI

    SPI --> SAFETY
    SPI --> CTRL
    SPI --> LOG

    SAFETY -->|Override| GPIO_SSR
    CTRL --> GPIO_SSR
    CTRL --> GPIO_BLWR

    GPIO_SSR --> SSR["SSR Gate"]
    GPIO_BLWR --> BDRV["Blower Driver Gate"]

    style SAFETY fill:#f66,stroke:#333
    style CTRL fill:#6f6,stroke:#333
    style LOG fill:#69f,stroke:#333
```

### Signal Path Notes

- Three MAX31855 breakout boards share a single SPI bus with individual chip-select lines
- SSR control is a single GPIO (logic-level, active high assumed until schematic finalized)
- Blower control GPIO drives a logic-level MOSFET gate via PWM
- **Safety layer has hardware-priority override on SSR GPIO** — it can force heater off regardless of control layer state
- All signal wiring must be physically separated from mains wiring

---

## Data Path

```mermaid
flowchart LR
    ESP32["ESP32"] -->|Serial / USB| PC["Host PC"]
    PC --> ARTISAN["Artisan\nRoast Logger"]

    ESP32 -.->|"Future: WiFi/TCP"| PC

    subgraph Data_Stream["Data Stream (2+ Hz)"]
        direction TB
        D1["TC1 (°C)"]
        D2["TC2 (°C)"]
        D3["TC3 (°C)"]
        D4["Heater Cmd (%)"]
        D5["Blower Cmd (%)"]
        D6["State / Faults"]
        D7["Timestamp (ms)"]
    end

    ESP32 --- Data_Stream
```

### Data Path Notes

- v1 primary interface: **USB serial** at 115200 baud (or as Artisan requires)
- Protocol: Modbus TCP or Artisan serial protocol (to be specified in `docs/software/artisan-integration.md`)
- Minimum sample rate: **2 Hz** per channel (Artisan expects 1-3 second intervals)
- Future option: ESP32 WiFi for wireless logging (same data format, TCP transport)
- All data fields are logged even in manual mode — this is the characterization dataset

---

## Subsystem Boundary Summary

| Subsystem | Inputs | Outputs | Interface Owner |
|-----------|--------|---------|-----------------|
| Blower | 12V DC via MOSFET, PWM speed command | Airflow + pressure | Electrical → Mechanical |
| Heater Can | Airflow, AC power via SSR | Heated airflow | Electrical → Mechanical |
| Plenum + Plate | Heated airflow (side entry) | Uniform upward velocity | Mechanical |
| Roast Chamber | Uniform hot air, green beans | Roasted beans, hot exhaust + chaff | Mechanical |
| Expansion Chamber | Hot air + chaff | Separated chaff, slower air | Mechanical |
| Mesh Screen + Exhaust | Slow air with residual chaff | Clean exhaust out | Mechanical |
| TC Sensors (x3) | Physical temperature | SPI digital readings | Electrical → Firmware |
| ESP32 Control | Sensor data, operator commands | SSR duty, blower command, data stream | Firmware |
| Safety System | Sensor data, fault signals | Override commands, fault latch | Firmware (authoritative) |
| Artisan Interface | Serial data stream | Roast logs, visualization | Firmware → Host PC |

---

## Cross-Reference

- Mechanical details: `docs/mechanical/`
- Electrical schematic: `docs/electrical/`
- Firmware architecture: `docs/software/firmware-architecture.md`
- Safety logic: `docs/software/safety-logic.md`
- Artisan protocol: `docs/software/artisan-integration.md`
