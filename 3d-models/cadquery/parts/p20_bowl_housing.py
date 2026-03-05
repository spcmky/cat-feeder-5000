# Cat Feeder 5000 — Part 20: Bowl Housing
# Solid block with round tapered cavity for removable bowl.
# Sits on the body shelf behind the gate.
# Print: PETG, 0.25mm layers, 40% infill, no supports.

import cadquery as cq
import sys; sys.path.insert(0, "..")
from params import (
    BOWL_FLOOR_W, BOWL_FLOOR_D, BOWL_SIDE_H, BOWL_OVERHANG,
    FLOOR, GATE_SETBACK,
)
from common import fillet_box


# Derived dimensions (from assembly_preview.scad)
BH_W = BOWL_FLOOR_W                      # 100
BH_D = BOWL_FLOOR_D + BOWL_OVERHANG      # 105
BH_H = BOWL_SIDE_H + 3                   # 28
BOWL_R_TOP = min(BH_W, BH_D) / 2 - 6    # 44
BOWL_R_BOT = BOWL_R_TOP - 10             # 34
CAVITY_DEPTH = BH_H - 4                  # 24


def bowl_housing() -> cq.Workplane:
    """Bowl housing block with tapered round cavity.

    Origin at min corner (0,0,0).
    """
    # Solid block
    result = fillet_box(BH_W, BH_D, BH_H, r=4)

    # Tapered round bowl cavity scooped from top
    # Loft from smaller circle at bottom to larger circle at top
    cavity = (
        cq.Workplane("XY")
        .workplane(offset=BH_H - CAVITY_DEPTH)
        .center(BH_W / 2, BH_D / 2)
        .circle(BOWL_R_BOT)
        .workplane(offset=CAVITY_DEPTH - 1)
        .circle(BOWL_R_TOP)
        .loft()
    )
    # Add top 2mm cylinder at full radius to match hull approach
    cavity_top = (
        cq.Workplane("XY")
        .workplane(offset=BH_H - 1)
        .center(BH_W / 2, BH_D / 2)
        .circle(BOWL_R_TOP)
        .extrude(2)
    )
    cavity = cavity.union(cavity_top)

    result = result.cut(cavity)
    return result


if __name__ == "__main__":
    result = bowl_housing()
    bb = result.val().BoundingBox()
    print(f"Bowl housing: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p20_bowl_housing.step")
    cq.exporters.export(result, "p20_bowl_housing.stl")
    print("Exported p20_bowl_housing.step and p20_bowl_housing.stl")
