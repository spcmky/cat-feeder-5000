# Cat Feeder 5000 — Part 02: Food Hopper
# Funnel reservoir. Sits on top of main body. ~500mL / ~400g kibble.
# Print: PETG, 0.25mm layers, 25% infill, no supports.

import cadquery as cq
import math
import sys; sys.path.insert(0, "..")
from params import AUGER_TUBE_OD, THIN_WALL, INSERT_BORE
from common import fillet_box


# Hopper dimensions
TOP_W = 130
TOP_D = 130
HOPPER_H = 130
OUTLET_D = AUGER_TUBE_OD
LIP_H = 2
LIP_T = 3


def hopper() -> cq.Workplane:
    """Funnel hopper: square top tapering to circular bottom outlet.

    Origin at min corner of the top-projected square (0,0,0 = bottom outlet level).
    """
    # Outer funnel shell: loft from square top to circular bottom
    # Top face: rounded rectangle at z=HOPPER_H
    top_wire = (
        cq.Workplane("XY")
        .workplane(offset=HOPPER_H - 1)
        .move(4, 0).hLine(TOP_W - 8)
        .tangentArcPoint((TOP_W, 4), relative=False)
        .vLine(TOP_D - 8)
        .tangentArcPoint((TOP_W - 4, TOP_D), relative=False)
        .hLine(-(TOP_W - 8))
        .tangentArcPoint((0, TOP_D - 4), relative=False)
        .vLine(-(TOP_D - 8))
        .tangentArcPoint((4, 0), relative=False)
        .close()
    )
    # Bottom face: circle at z=0 centered on hopper
    bottom_wire = (
        cq.Workplane("XY")
        .center(TOP_W / 2, TOP_D / 2)
        .circle((OUTLET_D + 2 * THIN_WALL) / 2)
    )

    # Build as hull: top rect + bottom circle
    # CadQuery loft approach
    outer = (
        cq.Workplane("XY")
        .center(TOP_W / 2, TOP_D / 2)
        .circle((OUTLET_D + 2 * THIN_WALL) / 2)
        .workplane(offset=HOPPER_H - 1)
        .rect(TOP_W, TOP_D)
        .loft()
    )
    # Top 1mm cap at full rect size
    top_cap = fillet_box(TOP_W, TOP_D, 1, r=4).translate((0, 0, HOPPER_H - 1))
    outer = outer.union(top_cap)

    # Lip at top for lid
    lip = fillet_box(TOP_W + 2 * LIP_T, TOP_D + 2 * LIP_T, LIP_H, r=5).translate(
        (-LIP_T, -LIP_T, HOPPER_H - LIP_H)
    )
    outer = outer.union(lip)

    # Inner funnel (hollow)
    inner = (
        cq.Workplane("XY")
        .center(TOP_W / 2, TOP_D / 2)
        .circle(OUTLET_D / 2)
        .workplane(offset=HOPPER_H)
        .rect(TOP_W - 2 * THIN_WALL, TOP_D - 2 * THIN_WALL)
        .loft()
    )
    result = outer.cut(inner)

    # Mount flange at bottom with M3 insert bosses
    flange_od = OUTLET_D + 2 * THIN_WALL + 20
    flange = (
        cq.Workplane("XY")
        .center(TOP_W / 2, TOP_D / 2)
        .circle(flange_od / 2)
        .circle(OUTLET_D / 2)
        .extrude(5)
    )
    result = result.union(flange)

    # M3 insert holes in flange (x3, 120 deg apart)
    for a in [0, 120, 240]:
        rad = math.radians(a)
        hx = TOP_W / 2 + (OUTLET_D / 2 + 8) * math.cos(rad)
        hy = TOP_D / 2 + (OUTLET_D / 2 + 8) * math.sin(rad)
        hole = (
            cq.Workplane("XY")
            .center(hx, hy)
            .circle(INSERT_BORE / 2)
            .extrude(5.2)
        )
        result = result.cut(hole)

    return result


if __name__ == "__main__":
    result = hopper()
    bb = result.val().BoundingBox()
    print(f"Hopper: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p02_hopper.step")
    cq.exporters.export(result, "p02_hopper.stl")
    print("Exported p02_hopper.step and p02_hopper.stl")
