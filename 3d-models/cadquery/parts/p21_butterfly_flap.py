# Cat Feeder 5000 — Part 21: Butterfly Flap
# One of two flaps that cover the bowl. Hinged at outer edge, swings up.
# Has hinge knuckles along the hinge edge and a servo linkage hole.
# Print: PETG, 0.2mm layers, 30% infill, no supports.

import cadquery as cq
import sys; sys.path.insert(0, "..")
from params import BOWL_FLOOR_W, GATE_ROD_D


# Flap dimensions (from detail_bowl_flaps.scad)
FLAP_W = 52              # Each flap = half the bowl span
FLAP_D = 95              # Covers bowl length
FLAP_T = 3               # Flap thickness
HINGE_D = GATE_ROD_D     # 3.2mm hinge pin diameter
HINGE_BOSS_D = 8         # Hinge boss outer diameter

# Knuckle positions along hinge edge (Y offsets from flap origin)
KNUCKLE_POSITIONS = [10, FLAP_D / 2, FLAP_D - 10]
KNUCKLE_LEN = 12


def butterfly_flap() -> cq.Workplane:
    """Single butterfly flap panel with hinge knuckles.

    Origin at min corner (0,0,0). Hinge edge at X=0.
    """
    # Main panel
    panel = (
        cq.Workplane("XY")
        .box(FLAP_W, FLAP_D, FLAP_T, centered=False)
    )

    # Hinge knuckles along hinge edge (X=0), cylinders along +Y
    for y_off in KNUCKLE_POSITIONS:
        knuckle = (
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(0, y_off, FLAP_T / 2),
                         rotate=cq.Vector(-90, 0, 0))
            .circle((HINGE_BOSS_D - 1) / 2)
            .extrude(KNUCKLE_LEN)
        )
        panel = panel.union(knuckle)

    # Hinge pin holes through all knuckles
    for y_off in KNUCKLE_POSITIONS:
        pin_hole = (
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(0, y_off - 1, FLAP_T / 2),
                         rotate=cq.Vector(-90, 0, 0))
            .circle((HINGE_D + 0.3) / 2)
            .extrude(KNUCKLE_LEN + 2)
        )
        panel = panel.cut(pin_hole)

    # Servo linkage hole
    linkage = (
        cq.Workplane("XY")
        .center(FLAP_W * 0.7, FLAP_D - 15)
        .circle(2.5 / 2)
        .extrude(FLAP_T + 2)
        .translate((0, 0, -1))
    )
    panel = panel.cut(linkage)

    return panel


if __name__ == "__main__":
    result = butterfly_flap()
    bb = result.val().BoundingBox()
    print(f"Butterfly flap: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p21_butterfly_flap.step")
    cq.exporters.export(result, "p21_butterfly_flap.stl")
    print("Exported p21_butterfly_flap.step and p21_butterfly_flap.stl")
