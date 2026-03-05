# Cat Feeder 5000 — Part 11: Camera Mount / Arm
# Positions Pi Camera above bowl. 45 deg downward angle.
# Print: PETG, 0.2mm layers, 35% infill, supports YES.

import cadquery as cq
import sys; sys.path.insert(0, "..")
from params import M3_CLEAR
from common import fillet_box


# Dimensions
ARM_L = 80
ARM_W = 20
ARM_T = 5
CAM_W = 25
CAM_D = 25
CAM_H = 5
CAM_ANGLE = 45
SWIVEL_D = 20
SWIVEL_H = 15


def camera_mount() -> cq.Workplane:
    """Camera mount: swivel base + arm + angled camera head.

    Origin at swivel base center bottom.
    """
    # Swivel base (attaches to body side)
    base = cq.Workplane("XY").circle(SWIVEL_D / 2).extrude(SWIVEL_H)

    # Swivel slot (through-hole at mid-height, along X axis)
    slot = (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .center(0, SWIVEL_H / 2)
        .circle(4 / 2)
        .extrude(SWIVEL_D + 2, both=True)
    )
    base = base.cut(slot)

    # Body mount holes (2x M3, along Y)
    for y in [-6, 6]:
        hole = (
            cq.Workplane("XY")
            .center(0, y)
            .circle(M3_CLEAR / 2)
            .extrude(SWIVEL_H + 0.2)
            .translate((0, 0, -0.1))
        )
        base = base.cut(hole)

    # Arm (extends upward from swivel top)
    arm = (
        cq.Workplane("XY")
        .workplane(offset=SWIVEL_H)
        .box(ARM_W, ARM_T, ARM_L, centered=False)
        .translate((-ARM_W / 2, 0, 0))
    )
    result = base.union(arm)

    # Camera head (angled 45 deg forward)
    # Build camera head at origin, then position it
    cam_head = fillet_box(CAM_W, CAM_D, CAM_H, r=2).translate(
        (-CAM_W / 2, -CAM_D / 2, 0)
    )

    # Lens opening
    lens = cq.Workplane("XY").circle(10 / 2).extrude(CAM_H + 0.2)
    cam_head = cam_head.cut(lens)

    # M2 mount holes (4x Pi Camera pattern, 21x21mm)
    for x in [-10.5, 10.5]:
        for y in [-10.5, 10.5]:
            m2_hole = (
                cq.Workplane("XY")
                .center(x, y)
                .circle(2.2 / 2)
                .extrude(CAM_H + 0.2)
                .translate((0, 0, -0.1))
            )
            cam_head = cam_head.cut(m2_hole)

    # Rotate and position camera head
    cam_head = (
        cam_head
        .rotateAboutCenter((1, 0, 0), CAM_ANGLE)
        .translate((0, 0, SWIVEL_H + ARM_L))
    )
    result = result.union(cam_head)

    return result


if __name__ == "__main__":
    result = camera_mount()
    bb = result.val().BoundingBox()
    print(f"Camera mount: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p11_camera_mount.step")
    cq.exporters.export(result, "p11_camera_mount.stl")
    print("Exported p11_camera_mount.step and p11_camera_mount.stl")
