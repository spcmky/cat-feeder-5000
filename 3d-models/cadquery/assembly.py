# Cat Feeder 5000 — CadQuery Assembly
# Full assembly with all parts positioned and colored.
# Mirrors the layout from assembly_preview.scad.

import cadquery as cq
from params import (
    UNIT_W, UNIT_D, UNIT_H,
    AUGER_TUBE_OD, AUGER_TUBE_L,
    BOWL_FLOOR_W, BOWL_FLOOR_D, BOWL_OVERHANG, BOWL_SIDE_H,
    GATE_SETBACK, FLOOR, SERVO_D, SERVO_W, SERVO_H,
    COL_BODY, COL_FOOD, COL_RFID, COL_TPU, COL_GATE,
)

# Import all part modules
from parts.p01_main_body import main_body
from parts.p02_hopper import hopper
from parts.p03_hopper_lid import hopper_lid
from parts.p04_auger_tube import auger_tube
from parts.p05_auger_screw import auger_screw
from parts.p06_motor_mount import motor_mount
from parts.p07_electronics_tray import electronics_tray
from parts.p11_camera_mount import camera_mount
from parts.p15_antenna_arch import antenna_arch
from parts.p18_feet import foot
from parts.p20_bowl_housing import bowl_housing
from parts.p21_butterfly_flap import butterfly_flap


def _color_tuple(rgba):
    """Convert RGBA tuple to CadQuery color."""
    return cq.Color(*rgba)


def build_assembly() -> cq.Assembly:
    """Build the complete feeder assembly with all parts positioned."""
    assy = cq.Assembly(name="CatFeeder5000")

    # Main body
    assy.add(
        main_body(),
        name="main_body",
        color=_color_tuple(COL_BODY),
    )

    # Hopper — sits on top of main body
    assy.add(
        hopper(),
        name="hopper",
        loc=cq.Location(cq.Vector(15, 100, UNIT_H + 10)),
        color=_color_tuple(COL_FOOD),
    )

    # Hopper lid
    assy.add(
        hopper_lid(),
        name="hopper_lid",
        loc=cq.Location(cq.Vector(15, 100, UNIT_H + 10 + 130)),
        color=_color_tuple(COL_FOOD),
    )

    # Auger position (matching assembly_preview.scad)
    auger_x = UNIT_W / 2
    auger_y = 100 + 130 / 2     # Hopper center Y
    auger_top = UNIT_H + 10
    auger_bot = auger_top - AUGER_TUBE_L

    # Auger tube
    assy.add(
        auger_tube(),
        name="auger_tube",
        loc=cq.Location(cq.Vector(auger_x, auger_y, auger_bot)),
        color=_color_tuple(COL_FOOD),
    )

    # Auger screw
    assy.add(
        auger_screw(),
        name="auger_screw",
        loc=cq.Location(cq.Vector(auger_x, auger_y, auger_bot)),
        color=_color_tuple(COL_FOOD),
    )

    # Motor mount
    assy.add(
        motor_mount(),
        name="motor_mount",
        loc=cq.Location(cq.Vector(auger_x - 15, auger_y - 15, auger_bot - 20)),
        color=_color_tuple(COL_BODY),
    )

    # Antenna arch (halo)
    assy.add(
        antenna_arch(),
        name="antenna_arch",
        loc=cq.Location(cq.Vector((UNIT_W - 146) / 2, 11, 0)),
        color=_color_tuple(COL_RFID),
    )

    # Bowl housing
    bowl_ox = (UNIT_W - BOWL_FLOOR_W) / 2
    bowl_oy = GATE_SETBACK + 15
    bowl_oz = FLOOR

    assy.add(
        bowl_housing(),
        name="bowl_housing",
        loc=cq.Location(cq.Vector(bowl_ox, bowl_oy, bowl_oz)),
        color=_color_tuple(COL_FOOD),
    )

    # Butterfly flaps (left and right)
    bh_w = BOWL_FLOOR_W
    bh_d = BOWL_FLOOR_D + BOWL_OVERHANG
    bh_h = BOWL_SIDE_H + 3
    flap_w = BOWL_FLOOR_W / 2
    flap_z = bowl_oz + bh_h + 1

    assy.add(
        butterfly_flap(),
        name="left_flap",
        loc=cq.Location(cq.Vector(bowl_ox, bowl_oy + bh_d / 2 - 95 / 2, flap_z)),
        color=_color_tuple(COL_GATE),
    )

    # Right flap (mirrored)
    right_flap = butterfly_flap().mirror("YZ")
    assy.add(
        right_flap,
        name="right_flap",
        loc=cq.Location(cq.Vector(
            bowl_ox + bh_w, bowl_oy + bh_d / 2 - 95 / 2, flap_z
        )),
        color=_color_tuple(COL_GATE),
    )

    # Camera mount
    assy.add(
        camera_mount(),
        name="camera_mount",
        loc=cq.Location(cq.Vector(UNIT_W - 20, 105, UNIT_H - 30)),
        color=_color_tuple(COL_BODY),
    )

    # Electronics tray
    assy.add(
        electronics_tray(),
        name="electronics_tray",
        loc=cq.Location(cq.Vector(UNIT_W / 2 - 39, UNIT_D - 68, FLOOR)),
        color=_color_tuple(COL_BODY),
    )

    # Feet (4 corners)
    for i, (x, y) in enumerate([
        (15, 15), (UNIT_W - 15, 15),
        (15, UNIT_D - 15), (UNIT_W - 15, UNIT_D - 15),
    ]):
        assy.add(
            foot(),
            name=f"foot_{i}",
            loc=cq.Location(cq.Vector(x, y, -4)),
            color=_color_tuple(COL_TPU),
        )

    return assy


if __name__ == "__main__":
    print("Building assembly...")
    assy = build_assembly()
    print("Exporting assembly STEP...")
    assy.export("assembly.step")
    print("Exported assembly.step")
