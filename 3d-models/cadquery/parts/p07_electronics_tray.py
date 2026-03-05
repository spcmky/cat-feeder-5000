# Cat Feeder 5000 — Part 07: Electronics Tray
# Snap-in tray holding Pi Zero 2W, Arduino Nano, and wiring.
# Print: PETG, 0.25mm layers, 30% infill, no supports.

import cadquery as cq
import sys; sys.path.insert(0, "..")
from params import WALL, FLOOR
from common import fillet_box


# Tray dimensions
TW = 78
TD = 58
TH = 20

# Board pockets
PI_W = 65; PI_D = 30; PI_H = 6
ARD_W = 45; ARD_D = 18; ARD_H = 8

# Snap clips
SNAP_T = 2
SNAP_H = 4


def electronics_tray() -> cq.Workplane:
    """Electronics tray with board pockets, wire channels, and vent holes.

    Origin at min corner (0,0,0).
    """
    # Base tray shell
    result = fillet_box(TW, TD, TH, r=3)

    # Snap clips (2x, on front face center)
    for x in [TW / 2 - 5, TW / 2 + 3]:
        clip = (
            cq.Workplane("XY")
            .workplane(offset=TH - 1)
            .box(SNAP_T, SNAP_T + 2, SNAP_H, centered=False)
            .translate((x, -SNAP_T, 0))
        )
        result = result.union(clip)

    # Hollow tray interior
    interior = fillet_box(TW - 2 * WALL, TD - 2 * WALL, TH, r=2).translate(
        (WALL, WALL, FLOOR)
    )
    result = result.cut(interior)

    # Pi Zero 2W pocket
    pi_pocket = (
        cq.Workplane("XY")
        .workplane(offset=FLOOR)
        .box(PI_W, PI_D, PI_H, centered=False)
        .translate((WALL + 2, WALL + 2, 0))
    )
    result = result.cut(pi_pocket)

    # Pi mounting peg recesses (4x M2.5 holes, 58x23mm bolt pattern)
    for x in [WALL + 3, WALL + 3 + 58]:
        for y in [WALL + 3, WALL + 3 + 23]:
            hole = (
                cq.Workplane("XY")
                .workplane(offset=FLOOR - 0.1)
                .center(x, y)
                .circle(2.7 / 2)
                .extrude(4)
            )
            result = result.cut(hole)

    # Arduino Nano pocket
    ard_pocket = (
        cq.Workplane("XY")
        .workplane(offset=FLOOR)
        .box(ARD_W, ARD_D, ARD_H, centered=False)
        .translate((TW - WALL - ARD_W - 2, WALL + 2, 0))
    )
    result = result.cut(ard_pocket)

    # Wire channel slots (3mm x 8mm, along front face)
    for i in range(4):
        slot = (
            cq.Workplane("XY")
            .workplane(offset=FLOOR + 2)
            .box(3, WALL + 0.2, 8, centered=False)
            .translate((10 + i * 18, -0.1, 0))
        )
        result = result.cut(slot)

    # Ventilation holes above Pi (3mm dia, 6x)
    for x in [15, 30, 45]:
        for y in [15, 25]:
            vent = (
                cq.Workplane("XY")
                .workplane(offset=TH - FLOOR - 0.1)
                .center(x, y)
                .circle(3 / 2)
                .extrude(FLOOR + 0.2)
            )
            result = result.cut(vent)

    return result


if __name__ == "__main__":
    result = electronics_tray()
    bb = result.val().BoundingBox()
    print(f"Electronics tray: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p07_electronics_tray.step")
    cq.exporters.export(result, "p07_electronics_tray.stl")
    print("Exported p07_electronics_tray.step and p07_electronics_tray.stl")
