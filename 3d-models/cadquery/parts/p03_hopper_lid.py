# Cat Feeder 5000 — Part 03: Hopper Lid
# Snap-on lid to keep food fresh.
# Print: PETG, 0.2mm layers, 20% infill, no supports.

import cadquery as cq
import sys; sys.path.insert(0, "..")
from common import fillet_box


# Lid dimensions
LID_W = 136
LID_D = 136
LID_H = 20
LIP_W = 130
LIP_D = 130
SNAP_T = 2
SNAP_H = 3
PORT_D = 40


def hopper_lid() -> cq.Workplane:
    """Snap-on hopper lid. Origin at min corner of top plate (0,0,0).

    Skirt hangs below (negative Z).
    """
    # Top plate
    top = fillet_box(LID_W, LID_D, 4, r=5)

    # Skirt (below top plate)
    skirt_outer = fillet_box(LID_W, LID_D, LID_H - 4, r=5).translate(
        (0, 0, -(LID_H - 4))
    )
    skirt_inner = fillet_box(
        LID_W - 2 * SNAP_T, LID_D - 2 * SNAP_T, LID_H, r=4
    ).translate((SNAP_T, SNAP_T, -(LID_H - 4) - 0.1))
    skirt = skirt_outer.cut(skirt_inner)

    result = top.union(skirt)

    # Snap bead (inner lip for interference fit)
    bead_outer = fillet_box(
        LID_W - 2 * SNAP_T, LID_D - 2 * SNAP_T, SNAP_H, r=4
    ).translate((SNAP_T, SNAP_T, -3))
    bead_inner = fillet_box(
        LID_W - 4 * SNAP_T - 0.8,
        LID_D - 4 * SNAP_T - 0.8,
        SNAP_H + 0.2,
        r=3,
    ).translate((2 * SNAP_T + 0.4, 2 * SNAP_T + 0.4, -3 - 0.1))
    bead = bead_outer.cut(bead_inner)
    result = result.union(bead)

    # Center fill port
    port = (
        cq.Workplane("XY")
        .center(LID_W / 2, LID_D / 2)
        .circle(PORT_D / 2)
        .extrude(5)
        .translate((0, 0, -0.1))
    )
    result = result.cut(port)

    return result


if __name__ == "__main__":
    result = hopper_lid()
    bb = result.val().BoundingBox()
    print(f"Hopper lid: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p03_hopper_lid.step")
    cq.exporters.export(result, "p03_hopper_lid.stl")
    print("Exported p03_hopper_lid.step and p03_hopper_lid.stl")
