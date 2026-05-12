#!/usr/bin/env bash
# Render every NN_*.py SchemDraw script in this directory to out/NN_*.svg
# (and out/NN_*.png if cairosvg is available - it's installed via requirements.txt).
#
# Run from repo root:
#     ./docs/electrical/schematics/schemdraw/render_all.sh
# or from this directory.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
VENV="$REPO_ROOT/.venv-diagrams"
PY="$VENV/bin/python"

if [[ ! -x "$PY" ]]; then
    echo "venv not found at $VENV - bootstrapping..."
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install --quiet --upgrade pip
    "$VENV/bin/pip" install --quiet -r "$SCRIPT_DIR/requirements.txt"
fi

# cairosvg looks for libcairo.2.dylib via ctypes; on macOS Homebrew installs
# it under $(brew --prefix)/lib, which isn't on the default dyld search path.
# Export it so the SVG -> PNG step finds it.
if command -v brew >/dev/null 2>&1; then
    BREW_LIB="$(brew --prefix 2>/dev/null)/lib"
    if [[ -d "$BREW_LIB" ]]; then
        export DYLD_FALLBACK_LIBRARY_PATH="$BREW_LIB${DYLD_FALLBACK_LIBRARY_PATH:+:$DYLD_FALLBACK_LIBRARY_PATH}"
    fi
fi

cd "$SCRIPT_DIR"
mkdir -p out

shopt -s nullglob
scripts=(*.py)
shopt -u nullglob

for f in "${scripts[@]}"; do
    [[ "$f" == "common.py" ]] && continue
    [[ "$f" == "_*" ]] && continue
    echo "==> $f"
    "$PY" "$f"
done

# Convert SVG -> PNG via cairosvg (already installed in venv).
echo "==> converting SVG to PNG"
"$PY" - <<'PY'
import os, glob
import cairosvg
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else ".", "out")
out_dir = "out"
for svg in sorted(glob.glob(os.path.join(out_dir, "*.svg"))):
    png = svg[:-4] + ".png"
    cairosvg.svg2png(url=svg, write_to=png, output_width=2400)
    print(f"  {png}")
PY
echo "done."
