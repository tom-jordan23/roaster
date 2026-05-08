"""Shared helpers for roaster SchemDraw schematics.

Conventions:
- Mains hot (L)       red
- Mains neutral (N)   white (drawn as light grey on white bg, so we use dark grey)
- Mains earth (PE)    green
- Logic 5V            orange
- Logic 3.3V          purple
- Signal              black (default)
- Signal ground       black dashed when separate from chassis

Render:
    python <name>.py
produces out/<name>.svg and out/<name>.png next to this file.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import schemdraw

OUT_DIR = Path(__file__).parent / "out"

WIRE_L = "#c8262a"      # red — mains hot
WIRE_N = "#404040"      # dark grey — mains neutral (white IRL)
WIRE_PE = "#1f9d3a"     # green — protective earth
WIRE_5V = "#e07a1a"     # orange — 5V logic supply
WIRE_3V3 = "#7b3fbf"    # purple — 3.3V logic
SIG_GND = "#000000"     # black — signal ground

TITLE_KW = dict(loc="top", fontsize=11)


# ----- Panel-wiring shared palette (used by 06-09 zone diagrams) -----
# Mirrors common wire colors so the per-zone diagrams stay consistent.
C_L = "#c8262a"      # mains hot (BLK in real life)
C_N = "#404040"      # mains neutral (WHT)
C_PE = "#1f9d3a"     # protective earth (GRN)
C_5V = "#e07a1a"     # +5 V logic
C_3V3 = "#7b3fbf"    # 3.3 V logic
C_SIG = "#1c5fa8"    # logic signal in/out (blue)
C_GND = "#000000"    # signal ground


def box(d: schemdraw.Drawing, x0: float, y0: float, x1: float, y1: float, **kw):
    """Draw a rectangle in absolute drawing coordinates.

    Avoids two schemdraw footguns:
    - Rect corners are element-relative, so we anchor at (x0, y0) and pass
      (0, 0) to (x1-x0, y1-y0) as the local corners.
    - Element direction is inherited from the previous element, so a Rect
      placed after a downward Resistor would rotate. .right() forces
      element-x to point along drawing-x.
    """
    import schemdraw.elements as elm
    return d.add(
        elm.Rect(corner1=(0, 0), corner2=(x1 - x0, y1 - y0), **kw)
        .right()
        .at((x0, y0))
    )


def zone(d: schemdraw.Drawing, x0: float, y0: float, x1: float, y1: float, title: str):
    """Dashed-outline zone box with a centered top-of-box title."""
    import schemdraw.elements as elm
    d.add(
        elm.Rect(corner1=(0, 0), corner2=(x1 - x0, y1 - y0), ls="--", lw=1.0)
        .right().at((x0, y0))
    )
    d.add(elm.Label().at(((x0 + x1) / 2, y1 - 0.4)).label(title, fontsize=11))


def module(d: schemdraw.Drawing, x0: float, y0: float, x1: float, y1: float,
           title: str, fill=None):
    """Solid-outline module box with a centered title near the top."""
    import schemdraw.elements as elm
    box(d, x0, y0, x1, y1, fill=fill)
    d.add(elm.Label().at(((x0 + x1) / 2, y1 - 0.45)).label(title, fontsize=10))


def term(d: schemdraw.Drawing, xy, label: str, side: str = "bottom"):
    """A labeled screw-terminal dot. Returns the (x, y) tuple."""
    import schemdraw.elements as elm
    d.add(elm.Dot().at(xy))
    d.add(elm.Label().at(xy).label(label, side, fontsize=8))
    return xy


def wire(d: schemdraw.Drawing, p0, p1, color, gauge_label=None, label_at=None,
         route: str = "h-then-v"):
    """Manhattan two-segment wire from p0 to p1.

    route='h-then-v' (default): horizontal leg first, then vertical.
    route='v-then-h':            vertical leg first, then horizontal.
    Single straight segment if collinear.
    """
    import schemdraw.elements as elm
    x0, y0 = p0
    x1, y1 = p1
    if x0 != x1 and y0 != y1:
        mid = (x1, y0) if route == "h-then-v" else (x0, y1)
        d.add(elm.Line().at(p0).to(mid).color(color))
        d.add(elm.Line().at(mid).to(p1).color(color))
    else:
        d.add(elm.Line().at(p0).to(p1).color(color))
    if gauge_label:
        if label_at is None:
            label_at = ((x0 + x1) / 2, (y0 + y1) / 2 + 0.3)
        d.add(elm.Label().at(label_at).label(gauge_label, fontsize=7, color=color))


def cable_schedule(d: schemdraw.Drawing, x0: float, y0: float, rows,
                   col_widths=(1.5, 5.5, 5.5, 1.0, 4.0)):
    """Render a cable-schedule table with proper column alignment.

    Place top-left corner at (x0, y0). Each row is rendered as 5 individual
    labels positioned at column-start x-coordinates so the columns align even
    when SchemDraw's SVG backend renders text proportionally.

    rows is a list of 5-tuples: (cable_id, from_label, to_label, conductors, wire).
    The first row is treated as a header.
    """
    import schemdraw.elements as elm
    d.add(elm.Label().at((x0, y0)).label(
        "Cable schedule  (cables entering / leaving this zone)",
        "right", fontsize=10))
    # Compute column x-positions
    xs = [x0]
    for w in col_widths[:-1]:
        xs.append(xs[-1] + w)
    for i, row in enumerate(rows):
        y = y0 - 0.6 - i * 0.45
        bold = (i == 0)
        size = 8 if bold else 7
        for x, cell in zip(xs, row):
            d.add(elm.Label().at((x, y)).label(str(cell), "right", fontsize=size))


def save(d: schemdraw.Drawing, stem: str) -> None:
    """Save the drawing as out/<stem>.svg.

    SVG is the source of truth: text-based, diffable in git, and renders inline
    in GitHub Markdown and browsers. render_all.sh converts to PNG via rsvg-convert
    if installed.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg = OUT_DIR / f"{stem}.svg"
    d.save(str(svg))
    print(f"wrote {svg}")


def stem_from_argv0() -> str:
    return Path(sys.argv[0]).stem
