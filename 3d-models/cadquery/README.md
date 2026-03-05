# CadQuery Parts — STEP/STL Export

CadQuery (Python + OpenCascade) port of the OpenSCAD parts. **Design work
happens in OpenSCAD** (`../cad/`). This directory exists for two things:

1. **STEP + STL export** — machine shops, slicers, and CAD tools that don't
   read `.scad` files. Run `export_all.py` to batch-export everything.
2. **Geometry that OpenSCAD can't do well** — the auger screw uses a true
   parametric helix (`Wire.makeHelix` + `sweep`), and the antenna arch uses
   a swept elliptical profile along a 3-point arc. Both are approximations
   in OpenSCAD.

## Quick start

```bash
source .venv/bin/activate
python export_all.py                # → exports/ directory with STEP + STL
python export_all.py --outdir /tmp  # custom output path
python parts/p05_auger_screw.py     # build + export a single part
```

## Keeping in sync

If you change dimensions in `params.scad`, update `params.py` to match.
The CadQuery parts read from `params.py` only.
