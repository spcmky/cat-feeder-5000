#!/usr/bin/env python3
# Cat Feeder 5000 — Batch Export
# Exports every part to STEP + STL, plus the full assembly STEP.
#
# Usage:
#   python export_all.py              # Export all to ./exports/
#   python export_all.py --outdir /tmp/parts  # Custom output directory

import argparse
import os
import time
import cadquery as cq

from parts.p01_main_body import main_body
from parts.p02_hopper import hopper
from parts.p03_hopper_lid import hopper_lid
from parts.p04_auger_tube import auger_tube
from parts.p05_auger_screw import auger_screw
from parts.p06_motor_mount import motor_mount
from parts.p07_electronics_tray import electronics_tray
from parts.p11_camera_mount import camera_mount
from parts.p15_antenna_arch import antenna_arch
from parts.p18_feet import foot
from parts.p20_bowl_housing import bowl_housing
from parts.p21_butterfly_flap import butterfly_flap
from assembly import build_assembly


PARTS = [
    ("p01_main_body", main_body),
    ("p02_hopper", hopper),
    ("p03_hopper_lid", hopper_lid),
    ("p04_auger_tube", auger_tube),
    ("p05_auger_screw", auger_screw),
    ("p06_motor_mount", motor_mount),
    ("p07_electronics_tray", electronics_tray),
    ("p11_camera_mount", camera_mount),
    ("p15_antenna_arch", antenna_arch),
    ("p18_feet", foot),
    ("p20_bowl_housing", bowl_housing),
    ("p21_butterfly_flap", butterfly_flap),
]


def export_all(outdir: str) -> None:
    os.makedirs(outdir, exist_ok=True)

    total_start = time.time()

    for name, builder in PARTS:
        t0 = time.time()
        print(f"  Building {name}...", end="", flush=True)
        result = builder()
        bb = result.val().BoundingBox()

        step_path = os.path.join(outdir, f"{name}.step")
        stl_path = os.path.join(outdir, f"{name}.stl")
        cq.exporters.export(result, step_path)
        cq.exporters.export(result, stl_path)

        dt = time.time() - t0
        print(f" {bb.xlen:.0f}x{bb.ylen:.0f}x{bb.zlen:.0f}mm"
              f"  vol={result.val().Volume():.0f}mm3"
              f"  ({dt:.1f}s)")

    # Assembly
    print("  Building assembly...", end="", flush=True)
    t0 = time.time()
    assy = build_assembly()
    assy_path = os.path.join(outdir, "assembly.step")
    assy.export(assy_path)
    dt = time.time() - t0
    print(f" ({dt:.1f}s)")

    total_dt = time.time() - total_start
    print(f"\nDone. {len(PARTS)} parts + assembly exported to {outdir}/ ({total_dt:.1f}s total)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export all Cat Feeder 5000 parts")
    parser.add_argument("--outdir", default="exports", help="Output directory")
    args = parser.parse_args()
    export_all(args.outdir)
