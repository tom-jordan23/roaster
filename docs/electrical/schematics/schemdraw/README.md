# SchemDraw schematics

Source-of-truth schematics for the roaster, generated from Python via
[SchemDraw](https://schemdraw.readthedocs.io/). SVGs are checked in;
PNGs are regenerated alongside.

## Diagrams

| Source                  | Output                              | Domain |
|-------------------------|-------------------------------------|--------|
| `01_mains_entry.py`     | `out/01_mains_entry.svg`            | Mains entry, DPST disconnect, fuse |
| `02_heater_circuit.py`  | `out/02_heater_circuit.svg`         | Domain 1 - SSR, heater, thermal fuses, snubber, NPN buffer |
| `03_blower_circuit.py`  | `out/03_blower_circuit.svg`         | Domain 2 - TRIAC dimmer, vacuum motor, CT, line filter, BOND-001 (DR-011) |
| `04_control_circuit.py` | `out/04_control_circuit.svg`        | Domain 3 - ESP32 + 3x MAX31855 SPI bus + cross-domain stubs |
| `05_grounding.py`       | `out/05_grounding.svg`              | Star grounding plan (chassis vs. signal) |
| `06_panel_mains_entry.py` | `out/06_panel_mains_entry.svg`    | Panel-wiring zone 1/4: mains entry (cord, switch, fuse, buses) |
| `07_panel_heater_bay.py`  | `out/07_panel_heater_bay.svg`     | Panel-wiring zone 2/4: heater bay (thermal fuses, SSR, drive buffer) |
| `08_panel_blower_bay.py`  | `out/08_panel_blower_bay.svg`     | Panel-wiring zone 3/4: blower bay (filter, CT, dimmer, motor) |
| `09_panel_control_bay.py` | `out/09_panel_control_bay.svg`    | Panel-wiring zone 4/4: control bay (PSU, ESP32, MAX31855 ×3) |

## Regenerate

```bash
./docs/electrical/schematics/schemdraw/render_all.sh
```

The script bootstraps a venv at `<repo>/.venv-diagrams/` on first run
(requires `python3` and `python3-venv`). Subsequent runs reuse it.

## Conventions

- **Wire colors**: red = mains hot (L), grey = mains neutral (N),
  green = protective earth (PE), orange = +5 V logic supply,
  purple = 3.3 V logic, black = signal.
- **Boxes**: drawn with the `box(d, x0, y0, x1, y1)` helper in `common.py`.
  Always pass absolute drawing coordinates - the helper handles the
  element-relative-corner and element-direction footguns.
- **Em-dashes break the SVG backend**. Use `-` in labels.

## Editing

Each script is small and self-contained. Open one of the existing files to
see the coordinate-grid pattern: declare a few `Y_*` and `X_*` constants,
then place every element with `.at((x, y))` in absolute coordinates. Avoid
relying on cursor position after the first element - schemdraw inherits
direction from the previous element, which has bitten us already.

After editing a `.py`, run `render_all.sh` (or `python <name>.py` for one).
