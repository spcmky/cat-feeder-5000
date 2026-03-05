# Cat Feeder 5000 — Part 18: Non-Slip Feet
# Press-fit into base pockets. Print x4 per unit (x8 total for 2 feeders).
# Print: TPU 95A, 0.3mm layers, 15% infill, 25mm/s.

import cadquery as cq
import sys; sys.path.insert(0, "..")
from params import TOLERANCE


# Foot dimensions
STUD_D = 9.8     # 0.2mm interference with 10mm pocket
STUD_H = 6
PAD_D = 16
PAD_H = 4


def foot() -> cq.Workplane:
    """Single non-slip foot. Origin at pad bottom center."""
    # Pad base (sits on floor)
    pad = cq.Workplane("XY").circle(PAD_D / 2).extrude(PAD_H)
    # Press-fit stud on top
    stud = (
        cq.Workplane("XY")
        .workplane(offset=PAD_H)
        .circle(STUD_D / 2)
        .extrude(STUD_H)
    )
    return pad.union(stud)


if __name__ == "__main__":
    result = foot()
    bb = result.val().BoundingBox()
    print(f"Foot: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p18_feet.step")
    cq.exporters.export(result, "p18_feet.stl")
    print("Exported p18_feet.step and p18_feet.stl")
