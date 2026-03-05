# Cat Feeder 5000 — Part 01: Main Body / Base
# Open-front design: front section is OPEN (approach zone, gate, bowl),
# rear section is enclosed box for electronics/hopper.
#
# Layout (front to back, Y axis):
#   Y=0..100   OPEN front zone: floor + bowl shelf + gate rails
#   Y=100..240  ENCLOSED rear box: full walls + top
#
# Print: PETG, 0.25mm layers, 40% infill, no supports.

import cadquery as cq
import sys; sys.path.insert(0, "..")
from params import (
    WALL, FLOOR, UNIT_W, UNIT_D, UNIT_H,
    AUGER_TUBE_OD, AUGER_ANGLE, GATE_T, TOLERANCE,
    INSERT_BORE, M3_CLEAR,
)
from common import fillet_box, boss


# Local constants (from 01_main_body.scad)
APPROACH_W = 130
APPROACH_H = 130
APPROACH_ARCH_R = 30
GATE_Y = 40
BOWL_SHELF_D = 100
BOWL_SHELF_H = 40
REAR_Y = BOWL_SHELF_D
REAR_D = UNIT_D - REAR_Y


def main_body() -> cq.Workplane:
    """Main body with open front zone and enclosed rear box.

    Origin at min corner (0,0,0).
    """
    # ── Floor / base plate ──────────────────────────────────────────
    floor_plate = fillet_box(UNIT_W, UNIT_D, FLOOR, r=4)

    # ── Bowl shelf ──────────────────────────────────────────────────
    shelf = fillet_box(UNIT_W, BOWL_SHELF_D, BOWL_SHELF_H, r=4)

    # ── Gate side rails ─────────────────────────────────────────────
    rail_h = APPROACH_H
    rail_w = 8
    left_rail_x = (UNIT_W - APPROACH_W) / 2 - rail_w
    right_rail_x = (UNIT_W + APPROACH_W) / 2
    left_rail = (
        cq.Workplane("XY")
        .box(rail_w, 10, rail_h, centered=False)
        .translate((left_rail_x, GATE_Y - 5, 0))
    )
    right_rail = (
        cq.Workplane("XY")
        .box(rail_w, 10, rail_h, centered=False)
        .translate((right_rail_x, GATE_Y - 5, 0))
    )

    # ── Enclosed rear box ───────────────────────────────────────────
    rear_box = fillet_box(UNIT_W, REAR_D, UNIT_H, r=4).translate((0, REAR_Y, 0))

    # Union everything
    result = floor_plate.union(shelf).union(left_rail).union(right_rail).union(rear_box)

    # ── Hollow out the rear box interior ────────────────────────────
    rear_interior = fillet_box(
        UNIT_W - 2 * WALL, REAR_D - 2 * WALL, UNIT_H, r=2
    ).translate((WALL, REAR_Y + WALL, FLOOR))
    result = result.cut(rear_interior)

    # ── Hollow out the bowl shelf interior ──────────────────────────
    shelf_interior = fillet_box(
        UNIT_W - 2 * WALL, BOWL_SHELF_D - WALL, BOWL_SHELF_H, r=2
    ).translate((WALL, WALL, FLOOR))
    result = result.cut(shelf_interior)

    # ── Front face opening on rear box ──────────────────────────────
    front_opening = (
        cq.Workplane("XY")
        .box(APPROACH_W, WALL + 2, APPROACH_H, centered=False)
        .translate(((UNIT_W - APPROACH_W) / 2, REAR_Y - 1, FLOOR))
    )
    result = result.cut(front_opening)

    # ── Auger exit hole ─────────────────────────────────────────────
    auger_hole = (
        cq.Workplane("XY")
        .workplane(offset=BOWL_SHELF_H - 1)
        .center(UNIT_W / 2, BOWL_SHELF_D / 2 + WALL)
        .circle((AUGER_TUBE_OD + 1) / 2)
        .extrude(WALL + 2)
    )
    result = result.cut(auger_hole)

    # ── Electronics bay (rear interior) ─────────────────────────────
    elec_bay = (
        cq.Workplane("XY")
        .box(90, 100 - WALL, 80, centered=False)
        .translate((UNIT_W / 2 - 45, UNIT_D - 100, FLOOR))
    )
    result = result.cut(elec_bay)

    # ── Rear cable pass-through ─────────────────────────────────────
    cable_hole = (
        cq.Workplane("XZ")
        .workplane(offset=UNIT_D - WALL / 2)
        .center(UNIT_W / 2, 25)
        .circle(15 / 2)
        .extrude(-(WALL + 2))
    )
    result = result.cut(cable_hole)

    # ── Gate rail slots ─────────────────────────────────────────────
    for x in [(UNIT_W - APPROACH_W) / 2 + WALL,
              (UNIT_W + APPROACH_W) / 2 - WALL - GATE_T]:
        gate_slot = (
            cq.Workplane("XY")
            .box(GATE_T + TOLERANCE, GATE_T + TOLERANCE, APPROACH_H, centered=False)
            .translate((x, GATE_Y - GATE_T / 2, FLOOR))
        )
        result = result.cut(gate_slot)

    # ── Halo floor mount holes ──────────────────────────────────────
    halo_offset_x = (UNIT_W - 154) / 2
    for x_local in [12, 142]:
        for dy in [-10, 10]:
            halo_hole = (
                cq.Workplane("XY")
                .center(halo_offset_x + x_local, dy)
                .circle(INSERT_BORE / 2)
                .extrude(FLOOR + 0.2)
                .translate((0, 0, -0.1))
            )
            result = result.cut(halo_hole)

    # ── Halo cable pass-through ─────────────────────────────────────
    halo_cable = (
        cq.Workplane("XY")
        .center(halo_offset_x + 12, 0)
        .circle(8 / 2)
        .extrude(FLOOR + 0.2)
        .translate((0, 0, -0.1))
    )
    result = result.cut(halo_cable)

    # ── Gate hinge mount holes ──────────────────────────────────────
    for x in [(UNIT_W - 120) / 2 + 15, (UNIT_W + 120) / 2 - 15]:
        hinge_hole = (
            cq.Workplane("XZ")
            .workplane(offset=GATE_Y)
            .center(x, APPROACH_H - 5)
            .circle(INSERT_BORE / 2)
            .extrude(-8)
        )
        result = result.cut(hinge_hole)

    # ── Hopper mount holes (top of rear box) ────────────────────────
    for x in [30, UNIT_W - 30]:
        for y in [REAR_Y + 30, UNIT_D - 30]:
            hopper_hole = (
                cq.Workplane("XY")
                .workplane(offset=UNIT_H - 6)
                .center(x, y)
                .circle(INSERT_BORE / 2)
                .extrude(6.2)
            )
            result = result.cut(hopper_hole)

    # ── Interior bosses ─────────────────────────────────────────────
    # Bowl bracket bosses (on bowl shelf, behind gate)
    for x in [(UNIT_W - APPROACH_W) / 2 + 10, (UNIT_W + APPROACH_W) / 2 - 10]:
        b = boss(d=10, h=BOWL_SHELF_H).translate((x, BOWL_SHELF_D - 15, 0))
        result = result.union(b)

    # Electronics tray bosses (rear interior floor)
    for x in [UNIT_W / 2 - 35, UNIT_W / 2 + 35]:
        b = boss(d=10, h=10).translate((x, UNIT_D - 40, FLOOR))
        result = result.union(b)

    # Gate servo bracket boss (inside rear box, above approach opening)
    b = boss(d=10, h=8).translate((UNIT_W / 2, REAR_Y + 10, APPROACH_H + 10))
    result = result.union(b)

    # ── Bottom feet pockets ─────────────────────────────────────────
    for x in [15, UNIT_W - 15]:
        for y in [15, UNIT_D - 15]:
            pocket = (
                cq.Workplane("XY")
                .center(x, y)
                .circle(10 / 2)
                .extrude(FLOOR + 0.2)
                .translate((0, 0, -0.1))
            )
            result = result.cut(pocket)

    return result


if __name__ == "__main__":
    result = main_body()
    bb = result.val().BoundingBox()
    print(f"Main body: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    cq.exporters.export(result, "p01_main_body.step")
    cq.exporters.export(result, "p01_main_body.stl")
    print("Exported p01_main_body.step and p01_main_body.stl")
