# Cat Feeder 5000 — Part 15: Antenna Arch (Round Halo, Tilted)
# Semicircular arch the cat walks through. Tilted forward ~18 deg.
# Flat oval cross-section (wide in X, thin in Y). Hollow for coil wire.
# Print: PETG, 0.2mm layers, 25% infill, supports for arch overhang.

import cadquery as cq
import math
import sys; sys.path.insert(0, "..")
from params import M3_CLEAR
from common import fillet_box


# Halo geometry
HALO_CLEAR_W = 130         # Inner clear width between legs
HALO_TUBE_OD = 16          # Tube outer diameter
HALO_TUBE_WALL = 2         # Tube wall thickness
HALO_TUBE_ID = HALO_TUBE_OD - 2 * HALO_TUBE_WALL  # 12mm coil channel
HALO_FLAT = 0.55           # Oval ratio: X/Y flattening
HALO_LEG_H = 77            # Leg height before tilt
HALO_ARCH_R = HALO_CLEAR_W / 2  # 65mm center-to-center
HALO_TILT = 18             # Degrees forward tilt
HALO_TOTAL_W = HALO_CLEAR_W + HALO_TUBE_OD  # 146mm

# Cross-section ellipse: narrow in X, full in Y (thin when viewed from front)
LEG_RX = HALO_TUBE_OD / 2 * HALO_FLAT   # 4.4mm (X half-axis)
LEG_RY = HALO_TUBE_OD / 2               # 8mm   (Y half-axis)
CH_RX = HALO_TUBE_ID / 2 * HALO_FLAT    # 3.3mm (inner X)
CH_RY = HALO_TUBE_ID / 2                # 6mm   (inner Y)

# Key X positions
LEFT_X = HALO_TUBE_OD / 2                      # 8
RIGHT_X = HALO_TOTAL_W - HALO_TUBE_OD / 2      # 138
CENTER_X = HALO_TOTAL_W / 2                     # 73
PEAK_Z = HALO_LEG_H + HALO_ARCH_R              # 142

# Mounting feet
FOOT_W = 30
FOOT_D = 30
FOOT_H = 5

# Cable exit
CABLE_CH_D = 6


def _build_arch(rx: float, ry: float) -> cq.Workplane:
    """Sweep an elliptical profile along a semicircular arc path.

    Profile: ellipse with half-axes rx (X) and ry (Y).
    Path: semicircle from right leg top to left leg top, arching upward.
    """
    # Semicircular arc: right → peak → left
    arc = cq.Edge.makeThreePointArc(
        cq.Vector(RIGHT_X, 0, HALO_LEG_H),
        cq.Vector(CENTER_X, 0, PEAK_Z),
        cq.Vector(LEFT_X, 0, HALO_LEG_H),
    )
    path_wire = cq.Wire.assembleEdges([arc])

    # Profile at start of path (right leg top)
    # At the start, path tangent is +Z, so profile is in XY plane
    profile = (
        cq.Workplane("XY")
        .workplane(offset=HALO_LEG_H)
        .center(RIGHT_X, 0)
        .ellipse(rx, ry)
    )

    return profile.sweep(cq.Workplane().add(path_wire), isFrenet=True)


def _build_leg(cx: float, rx: float, ry: float, h: float) -> cq.Workplane:
    """Extrude an elliptical leg at center position cx."""
    return (
        cq.Workplane("XY")
        .center(cx, 0)
        .ellipse(rx, ry)
        .extrude(h)
    )


def _mounting_foot() -> cq.Workplane:
    """Flat mounting foot with 2x M3 bolt holes. Origin at min corner."""
    foot = fillet_box(FOOT_W, FOOT_D, FOOT_H, r=3)
    for dx in [FOOT_W / 2 - 8, FOOT_W / 2 + 8]:
        hole = (
            cq.Workplane("XY")
            .center(dx, FOOT_D / 2)
            .circle(M3_CLEAR / 2)
            .extrude(FOOT_H + 0.2)
            .translate((0, 0, -0.1))
        )
        foot = foot.cut(hole)
    return foot


def antenna_arch() -> cq.Workplane:
    """Complete antenna arch: tilted halo + flat mounting feet.

    Origin matches OpenSCAD convention for assembly positioning.
    """
    # Outer shell: legs + arch
    left_leg_o = _build_leg(LEFT_X, LEG_RX, LEG_RY, HALO_LEG_H)
    right_leg_o = _build_leg(RIGHT_X, LEG_RX, LEG_RY, HALO_LEG_H)
    arch_o = _build_arch(LEG_RX, LEG_RY)
    outer = left_leg_o.union(right_leg_o).union(arch_o)

    # Inner channel: legs + arch (slightly longer legs for clean subtraction)
    left_leg_i = _build_leg(LEFT_X, CH_RX, CH_RY, HALO_LEG_H + 0.2).translate(
        (0, 0, -0.1)
    )
    right_leg_i = _build_leg(RIGHT_X, CH_RX, CH_RY, HALO_LEG_H + 0.2).translate(
        (0, 0, -0.1)
    )
    arch_i = _build_arch(CH_RX, CH_RY)
    inner = left_leg_i.union(right_leg_i).union(arch_i)

    halo = outer.cut(inner)

    # Apply forward tilt (rotate around X axis at Z=0)
    halo = halo.rotateAboutCenter((1, 0, 0), -HALO_TILT)

    # Mounting feet (flat on floor, NOT tilted)
    left_foot = _mounting_foot().translate(
        (HALO_TUBE_OD / 2 - FOOT_W / 2, -FOOT_D + HALO_TUBE_OD / 2, 0)
    )
    right_foot = _mounting_foot().translate(
        (HALO_TOTAL_W - HALO_TUBE_OD / 2 - FOOT_W / 2,
         -FOOT_D + HALO_TUBE_OD / 2, 0)
    )

    result = halo.union(left_foot).union(right_foot)
    return result


if __name__ == "__main__":
    result = antenna_arch()
    bb = result.val().BoundingBox()
    print(f"Antenna arch: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p15_antenna_arch.step")
    cq.exporters.export(result, "p15_antenna_arch.stl")
    print("Exported p15_antenna_arch.step and p15_antenna_arch.stl")
