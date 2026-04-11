# CLAUDE.md

## Project: Small Electric Fluid-Bed Coffee Roaster

### Purpose
This project is a ground-up design for a small, instrumented, electrically heated fluid-bed coffee roaster intended to be developed iteratively.

The immediate goal is a reliable **v1 prototype** that can roast in **manual/open-loop mode** while collecting high-quality data. The longer-term goal is to transition the same hardware platform into **closed-loop / partially automated roasting control** without needing to redesign the system architecture.

This project should be treated as an **engineering instrument first** and a polished appliance later. Serviceability, measurement quality, airflow behavior, and safe control matter more than cosmetics in early versions.

---

## Current Design Decision Summary

### Selected Direction
We are **not** building around a hot-air popcorn popper, heat gun, or gas burner.

We are building around a **purpose-built electric fluid-bed architecture** with:
- a **stainless steel roast chamber**
- a **box plenum** under the chamber
- **side-entry heated air** into the plenum
- **internal baffles / flow conditioning** in the plenum
- a **diffusion / distributor plate** above the plenum
- **three thermocouples**
- **ESP32-based logging and control**
- **manual-first operation with future closed-loop capability**

### Batch Size Direction
The project discussion considered 1 lb, 1/2 lb, and 1/4 lb batch sizes.

The current preferred starting point is **1/4 lb (approximately 113 g green coffee)** because it:
- is much more realistic on **120 V power**
- allows a compact and efficient heater/blower system
- reduces thermal and airflow scaling problems
- supports more frequent roasting if the workflow is good
- is an easier first platform to dial in before scaling up

This smaller machine should be treated as a **learning platform and reference architecture** that can later be scaled if desired.

---

## System Architecture

### Functional Air Path
The intended process flow is:

1. **Blower** generates pressure and process airflow.
2. **Heater can** adds energy into the moving airstream.
3. **Heated air enters the plenum from the side**.
4. **Internal baffles / flow conditioning** inside the plenum reduce inlet jetting and promote more even pressure distribution.
5. **Distributor plate** converts plenum pressure into more even upward air velocity.
6. **Roast chamber** sits above the plate, where beans fluidize in the hot upward airstream.
7. **Exhaust / chaff path** removes air and chaff from the top of the roast chamber.

### Important Design Principle
The plenum is a **pressure equalization chamber**, not just a void under the chamber.

Its job is to convert a fast, uneven side-entry flow into a more uniform pressure field so the distributor plate can produce a stable, even bean bed motion.

The roaster should avoid:
- direct center jetting into the chamber
- dead zones at chamber walls
- violent geysering in the center
- poorly mixed air entering the bean bed

---

## Mechanical Decisions Settled So Far

### Roast Chamber
- **Material:** stainless steel for v1
- **Glass chamber:** discussed and rejected for v1
- Reason for stainless selection:
  - simpler fabrication
  - avoids thermal shock concerns
  - easier to mount probes and fixtures
  - better for iterative prototyping

### Plenum
- **Type:** box plenum, HVAC-inspired concept
- **Air entry:** side-entry, not bottom-center
- **Internals:** include baffles or flow-conditioning features to reduce direct inlet jetting
- **Upper interface:** distributor/diffusion plate between plenum and roast chamber

### Distributor Plate
- The plate is a critical tuning component.
- It should be treated as an interchangeable/testable part.
- The design should allow iteration on:
  - hole size
  - hole count
  - open area
  - zoning if needed

### Finish Philosophy
Do **not** prioritize paint or decorative finishing at this stage.

Treat the machine as a prototype and instrument:
- bare stainless in hot zones
- mechanical assembly prioritized
- easy disassembly and rework
- insulation and outer shell can be addressed later

---

## Controls Philosophy

### High-Level Approach
The machine should be built from the start to support **future closed-loop control**, but initial operation should be **manual/open-loop** so the physical system can be understood and tuned first.

This means:
- the hardware architecture must already support automation
- the software should already be structured around future control loops
- the user interface for v1 should still allow direct manual control of heat and blower

### Initial Operating Mode
**Open-loop / manual roasting** with:
- user-set **heater %**
- user-set **blower %**
- live temperature logging
- roast observation and manual response

### Later Operating Mode
**Closed-loop or semi-closed-loop roasting**, likely phased in as:
1. stabilize process air using **TC1**
2. keep blower logic under manual or bounded control initially
3. later experiment with more advanced automated roasting behavior

### Important Principle
Do **not** jump straight to full automation.

Use open-loop roasting to learn:
- heater response
- chamber lag
- airflow sensitivity
- probe behavior
- relationship between process air, bean mass, and exhaust temperatures

Then automate from evidence.

---

## Sensors

### Thermocouple Count
The design has settled on **three thermocouples**.

### TC1 — Process Air / Inlet Control Sensor
**Placement:** in the hot air stream after the heater and before the plenum, where it sees mixed process air but is not touching the heater element or duct wall.

**Role:**
- fastest process temperature signal
- best candidate for first closed-loop control variable
- good anchor for heater modulation

### TC2 — Lower Bean Bed / Roast Development Sensor
**Placement:** low in the roast chamber, just above the distributor plate, slightly off-center, where it sees the lower moving bean mass.

**Role:**
- main roast-development reference
- should reflect bean-environment behavior more than free air alone

**Current preference:** side-entry probe for v1.

A bottom-entry / through-plate vertical probe is considered **possible but not preferred for v1**, because it may disturb distributor-plate airflow and complicate the most sensitive fluidization region.

### TC3 — Exhaust Sensor
**Placement:** in the exhaust stream above the bean bed and before major dilution or ambient air mixing.

**Role:**
- helps interpret system energy balance
- useful for observing heat storage and shedding
- supports later automation and profiling analysis

---

## Motor / Blower Control Strategy

### Preferred v1 Strategy
Use a blower system that can be controlled in a way that is compatible with later automation, but keep the operator workflow simple at first.

### Control Requirement
The blower is not just moving air; it is creating the pressure that makes fluidization possible.

Because of that, airflow control is a first-class system parameter.

### Current Approach
The exact final motor type may still vary depending on sourced hardware, but the architecture should support:
- **manual blower control in v1**
- **microcontroller-governed blower control later**

If using an AC universal-motor-style blower, a **TRIAC-based control stage** is the expected direction.

If using a DC blower, use a controller architecture appropriate to that motor type.

### Safety Priority
The blower is a prerequisite for heater operation.

The control system should be designed so that:
- heater cannot operate without airflow
- loss of airflow shuts off heat
- blower status is treated as a safety-critical input

---

## Heat Control Strategy

### Preferred v1 Strategy
Use an **ESP32-controlled zero-cross SSR** to switch a resistive heater using **time-proportional / burst-fire control**.

### Why
This gives a clean path from:
- manual heater percentage control now
- to automated process-air temperature control later

### Heat Control Requirements
The design should support:
- manual settable heater percentage
- repeatable software-driven heater duty control
- future closed-loop control using TC1
- hard safety override independent of normal roasting logic

### Control Path
Planned basic architecture:
- ESP32 computes heater command
- SSR applies duty-cycled power to heater
- TC1 provides process-air feedback
- TC2 and TC3 support interpretation and later advanced control

---

## Software Architecture

### Required Software Layers
The control software should be structured in three logical layers from the beginning.

#### 1. Safety Layer
Must always remain authoritative.

Responsibilities:
- heater off on over-temperature
- heater off on airflow failure / blower fault
- startup interlocks
- fault state handling
- safe shutdown behavior

#### 2. Manual Control Layer
This is the primary v1 operating mode.

Responsibilities:
- accept operator blower command
- accept operator heater command
- stream temperatures and state
- log to Artisan or compatible tooling

#### 3. Control / Automation Layer
Initially present but disabled or limited.

Responsibilities later:
- closed-loop TC1 control
- bounded or guided blower control
- profile assistance
- repeatable batch logic

### Development Principle
Do not tightly couple UI, roast logic, and hardware abstraction.

Maintain clean separation between:
- sensor acquisition
- actuator output
- safety logic
- logging
- operator interface
- control algorithms

---

## Data and Logging

### Logging Goal
This machine should produce usable roast data from the first real test sessions.

### Current Direction
Use **ESP32-based sensing and control** with a path to **Artisan logging**.

### Data to Log
At minimum log:
- TC1
- TC2
- TC3
- heater command %
- blower command %
- event markers if possible

### Why This Matters
The open-loop phase is not just operational—it is how the machine will be characterized.

The recorded data will later inform:
- control tuning
- process understanding
- airflow changes
- distributor-plate redesign
- repeatability improvements

---

## Safety Expectations

This is a mains-powered, high-temperature air-handling system. Safety is not optional.

### Required Electrical and System Safety Principles
- physically separate mains and low-voltage control wiring
- ground all metal chassis components
- protect heater circuit appropriately
- include a hard power disconnect
- include heater disable on fault
- use strain relief and proper terminals
- assume SSR failure modes are real
- assume airflow failure can cause dangerous overheating

### Safety Control Behavior
The heater must never be allowed to run as an independent free agent.

The safety system should always be able to force:
- heater off
- fault latch
- operator reset requirement if needed

---

## v1 Build Intent

### What v1 Must Achieve
v1 does **not** need to be visually finished or fully automated.

v1 **does** need to:
- fluidize beans reliably
- heat the air stream effectively
- maintain safe operation
- provide meaningful temperature data
- allow manual blower and heat adjustment
- support later automation without rewiring the entire system

### What v1 Is Not Trying To Do
- be a commercial product
- be optimized cosmetically
- solve every control problem immediately
- jump straight to full PID roast automation

---

## Open Questions / Remaining Design Work

The following areas still need detailed engineering and should be treated as active work items.

### Mechanical
- final roast chamber dimensions
- exact plenum dimensions
- baffle geometry inside plenum
- distributor plate hole pattern and open area
- exhaust / cyclone / chaff management layout
- service access and assembly method

### Electrical / Controls
- final heater specification
- final blower model and motor type
- exact control board stack
- power distribution layout
- interlock implementation
- Artisan communications method

### Software
- sensor polling architecture
- command interface
- logging format
- manual control UI
- future PID / closed-loop implementation plan

---

## Working Assumptions for Claude Code

When assisting on this project, assume the following unless explicitly changed:

- The project is currently centered on a **1/4 lb electric fluid-bed roaster**.
- Power target is **120 V** for the first machine.
- The chamber is **stainless**, not glass.
- The plenum is a **box plenum with side-entry heated air**.
- The plenum contains **baffles or flow-conditioning features**.
- The chamber sits above a **distributor plate**.
- The control stack is **ESP32-centric**.
- The design includes **three thermocouples**.
- The system is built to support **closed-loop control later**, but **manual/open-loop operation first**.
- The project values **truthfulness, engineering clarity, and testability over polish**.

---

## Suggested Immediate Next Deliverables

Claude Code should be ready to help produce the following artifacts next:

1. **System block diagram**
2. **Dimensioned mechanical concept sketch**
3. **Electrical architecture diagram**
4. **ESP32 firmware scaffold**
5. **Sensor/actuator interface definitions**
6. **Safety interlock logic**
7. **Artisan integration plan**
8. **Test plan for first airflow and heat trials**

---

## One-Sentence Project Summary

Build a small stainless electric fluid-bed coffee roaster with a side-entry box plenum, three thermocouples, and ESP32-based controls that roasts manually first, logs everything well, and is architected from day one for later closed-loop automation.

