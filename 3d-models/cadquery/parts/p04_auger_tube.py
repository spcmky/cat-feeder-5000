# Cat Feeder 5000 — Part 04: Auger Tube
# Food channel. Auger screw rotates inside this.
# Print: PETG, 0.2mm layers, 30% infill, no supports. Smooth inner bore.

import cadquery as cq
import sys; sys.path.insert(0, "..")
from params import AUGER_TUBE_OD, AUGER_TUBE_ID, AUGER_TUBE_L, M3_CLEAR
import math


# Tube-specific dims
FLANGE_D = 50
FLANGE_H = 5
EXIT_D = 28


def auger_tube() -> cq.Workplane:
    """Auger tube with top flange, bore, exit port, and bolt holes.

    Origin at base center, tube extends upward along Z.
    """
    # Main tube
    tube = cq.Workplane("XY").circle(AUGER_TUBE_OD / 2).extrude(AUGER_TUBE_L)

    # Top flange
    flange = (
        cq.Workplane("XY")
        .workplane(offset=AUGER_TUBE_L - FLANGE_H)
        .circle(FLANGE_D / 2)
        .extrude(FLANGE_H)
    )
    result = tube.union(flange)

    # Bore (inner channel, full length)
    result = (
        result
        .faces("<Z").workplane()
        .circle(AUGER_TUBE_ID / 2)
        .cutBlind(-AUGER_TUBE_L - 0.2)
    )

    # Bottom exit port (cylinder perpendicular to tube axis at Z=10)
    exit_cyl = (
        cq.Workplane("XZ")
        .workplane(offset=-AUGER_TUBE_OD - 1)
        .center(0, 10)
        .circle(EXIT_D / 2)
        .extrude(AUGER_TUBE_OD + 2)
    )
    result = result.cut(exit_cyl)

    # Flange M3 holes (x3, 120 deg apart)
    for a in [0, 120, 240]:
        rad = math.radians(a)
        hx = (FLANGE_D / 2 - 8) * math.cos(rad)
        hy = (FLANGE_D / 2 - 8) * math.sin(rad)
        hole = (
            cq.Workplane("XY")
            .workplane(offset=AUGER_TUBE_L - FLANGE_H - 0.1)
            .center(hx, hy)
            .circle(M3_CLEAR / 2)
            .extrude(FLANGE_H + 0.2)
        )
        result = result.cut(hole)

    return result


if __name__ == "__main__":
    result = auger_tube()
    bb = result.val().BoundingBox()
    print(f"Auger tube: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p04_auger_tube.step")
    cq.exporters.export(result, "p04_auger_tube.stl")
    print("Exported p04_auger_tube.step and p04_auger_tube.stl")
