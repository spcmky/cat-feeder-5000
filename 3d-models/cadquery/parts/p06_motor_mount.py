# Cat Feeder 5000 — Part 06: Motor Mount
# Mounts auger drive motor (N20 or NEMA14 stepper) aligned to auger tube.
# Print: PETG, 0.25mm layers, 40% infill, no supports.

import cadquery as cq
import sys; sys.path.insert(0, "..")
from params import M3_CLEAR
from common import fillet_box


# Mount dimensions
MW = 30
MD = 30
MH = 20
SHAFT_H = 10   # Height of shaft bore from base


def motor_mount(motor_type: str = "N20") -> cq.Workplane:
    """Motor mount block. Origin at min corner (0,0,0)."""
    result = fillet_box(MW, MD, MH, r=3)

    if motor_type == "N20":
        # N20 motor pocket: 13mm dia x 25mm deep (round, from top)
        result = (
            result
            .faces(">Z").workplane()
            .center(MW / 2, MD / 2)
            .circle(13 / 2)
            .cutBlind(-25)
        )
        # Gearbox pocket (rectangular, top of motor)
        gearbox = (
            cq.Workplane("XY")
            .workplane(offset=MH - 10)
            .box(13, 11, 11, centered=False)
            .translate((MW / 2 - 6.5, MD / 2 - 5.5, 0))
        )
        result = result.cut(gearbox)
        # Shaft bore through bottom
        result = (
            result
            .faces("<Z").workplane()
            .center(MW / 2, MD / 2)
            .circle(6 / 2)
            .cutBlind(-SHAFT_H - 1)
        )
    else:
        # NEMA14 pocket: 28mm sq from top
        nema_pocket = (
            cq.Workplane("XY")
            .workplane(offset=MH - 20)
            .box(28, 28, 21, centered=False)
            .translate((MW / 2 - 14, MD / 2 - 14, 0))
        )
        result = result.cut(nema_pocket)
        # NEMA14 shaft bore
        result = (
            result
            .faces("<Z").workplane()
            .center(MW / 2, MD / 2)
            .circle(8 / 2)
            .cutBlind(-SHAFT_H - 1)
        )
        # NEMA14 mount holes (M3, 26mm bolt circle)
        for dx in [-13, 13]:
            for dy in [-13, 13]:
                result = (
                    result
                    .faces("<Z").workplane()
                    .center(MW / 2 + dx, MD / 2 + dy)
                    .circle(M3_CLEAR / 2)
                    .cutThruAll()
                )

    # Body mount holes (M3 clearance, 4 corners)
    for x in [6, MW - 6]:
        for y in [6, MD - 6]:
            result = (
                result
                .faces("<Z").workplane()
                .center(x, y)
                .circle(M3_CLEAR / 2)
                .cutBlind(-6)
            )

    return result


if __name__ == "__main__":
    result = motor_mount("N20")
    bb = result.val().BoundingBox()
    print(f"Motor mount (N20): {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p06_motor_mount.step")
    cq.exporters.export(result, "p06_motor_mount.stl")
    print("Exported p06_motor_mount.step and p06_motor_mount.stl")
