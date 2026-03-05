// Cat Feeder 5000 — Assembly Preview
// Shows all parts in approximate assembled position.
// Set EXPLODE > 0 to separate parts for inspection.
// Not for printing — visualization only.
//
// COORDINATE SYSTEM:
//   X = left-right (width)
//   Y = front-back (depth) — Y=0 is the body FRONT FACE (cat approach side)
//   Z = up-down (height) — Z=0 is the floor
//
// SPATIAL SEQUENCE (side view, front→back):
//
//               body top ────────────────────── Z=160
//              │                               │
//              │   hopper + auger              │
//              │                               │
//   arch peak─╮│                               │── Z=142 (77+65)
//            │ │   gate hinge ──── Z=125       │
//            │ │   (at Y=40)                   │
//            │ │                               │
//   ╭────────╯ │              electronics      │
//   │ round    │                               │
//   │ halo     │   gate flap                   │
//   │          │   (at Y=40)                   │
//   │          │          bowl                 │
//   ┴──feet────┴───shelf──────────────────────┴── Z=0
//   Y=-24      Y=0        Y=40   Y=60   Y=100   Y=240
//   (halo)   (body front) (gate) (bowl)  (shelf end)

include <params.scad>
use <01_main_body.scad>
use <02_hopper.scad>
use <03_hopper_lid.scad>
use <04_auger_tube.scad>
use <05_auger_screw.scad>
use <06_motor_mount.scad>
use <07_electronics_tray.scad>
use <11_camera_mount.scad>
use <15_antenna_arch.scad>
use <18_feet.scad>

EXPLODE = 0;    // Set to 10–30 to explode parts apart for inspection

// ═══════════════════════════════════════════════════════════════════════════
// MAIN BODY — the box that sits on the floor
// ═══════════════════════════════════════════════════════════════════════════
color(COL_BODY) main_body();

// ═══════════════════════════════════════════════════════════════════════════
// HOPPER — sits on top of main body
// ═══════════════════════════════════════════════════════════════════════════
translate([15, 100, UNIT_H + 5 + EXPLODE * 2])
    color(COL_FOOD) hopper();

// HOPPER LID — sits on hopper lip (sleeve + funnel height)
translate([15, 100, UNIT_H + 5 + AUGER_COUPLING_H + 130 + EXPLODE * 4])
    color(COL_FOOD) hopper_lid();

// ═══════════════════════════════════════════════════════════════════════════
// AUGER — vertical tube + screw, centered under hopper
// Food exits side port, chute angles it forward toward bowl
// ═══════════════════════════════════════════════════════════════════════════
_auger_x = UNIT_W/2;
_auger_y = 100 + 130/2;         // Hopper center Y (shifted back)
// Flange bottom sits on roof at Z=UNIT_H
// Flange is at local Z=(AUGER_TUBE_L-5)..AUGER_TUBE_L → global Z=160..165
// Coupling stub: global Z=165..180
_auger_bot = UNIT_H - (AUGER_TUBE_L - 5);  // = 80

translate([_auger_x, _auger_y, _auger_bot]) {
    color(COL_FOOD) auger_tube();
    color(COL_FOOD) auger_screw();
}

// MOTOR MOUNT — at bottom of vertical auger tube
translate([_auger_x - 15, _auger_y - 15, _auger_bot - 20 - EXPLODE * 2])
    color(COL_BODY) motor_mount();

// CHUTE — short downward spout from auger exit port
// Food drops from here into the bowl below. Kept short to clear the flaps.
_chute_exit_y = _auger_y - AUGER_TUBE_OD/2;
_chute_exit_z = _auger_bot + 10;

translate([_auger_x, _chute_exit_y, _chute_exit_z])
    rotate([135, 0, 0])  // Angled 45° forward+down
        color(COL_FOOD, 0.6)
        difference() {
            cylinder(d=AUGER_TUBE_ID, h=35);
            translate([0, 0, -1])
                cylinder(d=AUGER_TUBE_ID - 5, h=37);
        }

// ═══════════════════════════════════════════════════════════════════════════
// ROUND HALO — RFID antenna arch (semicircular ring)
// Sits inside the body, arch peak over front of bowl.
// Halo total_w = 146mm, centered on body (UNIT_W=160).
// With 18° tilt, arch peak at Y_base + ~44mm.
// Bowl front at Y=55, so base at Y≈11 puts peak over bowl front.
// ═══════════════════════════════════════════════════════════════════════════
translate([(UNIT_W - 146)/2, 11 - EXPLODE, 0])
    color(COL_RFID) antenna_arch();

// ═══════════════════════════════════════════════════════════════════════════
// BOWL HOUSING — solid block with round bowl cavity, sits on shelf
// ═══════════════════════════════════════════════════════════════════════════
_bowl_ox = (UNIT_W - BOWL_FLOOR_W) / 2;  // Center bowl on body
_bowl_oy = GATE_SETBACK + 15;             // Behind gate
_bowl_oz = FLOOR + EXPLODE;

_bh_w = BOWL_FLOOR_W;
_bh_d = BOWL_FLOOR_D + BOWL_OVERHANG;
_bh_h = BOWL_SIDE_H + 3;                  // Up to just below flap level
_bowl_r_top = min(_bh_w, _bh_d) / 2 - 6;
_bowl_r_bot = _bowl_r_top - 10;
_cavity_depth = _bh_h - 4;

translate([_bowl_ox, _bowl_oy, _bowl_oz])
    color(COL_FOOD)
    difference() {
        fillet_box(_bh_w, _bh_d, _bh_h, r=4);
        translate([_bh_w/2, _bh_d/2, _bh_h - _cavity_depth])
            hull() {
                translate([0, 0, _cavity_depth - 1])
                    cylinder(r=_bowl_r_top, h=2);
                cylinder(r=_bowl_r_bot, h=1);
            }
    }

// ═══════════════════════════════════════════════════════════════════════════
// BOWL COVER — two butterfly flaps with direct-drive servos
// Hinged at outer bowl edges. Shown CLOSED (covering the bowl).
// ═══════════════════════════════════════════════════════════════════════════

_flap_w = BOWL_FLOOR_W / 2;     // Each flap = half the bowl width
_flap_d = 95;                    // Covers bowl length
_flap_t = 3;
_flap_z = _bowl_oz + _bh_h + 1; // Just above bowl housing
_bowl_cx = _bowl_ox + _bh_w / 2;
_bowl_cy = _bowl_oy + _bh_d / 2;

// Left flap (hinged at left edge, closed = flat)
translate([_bowl_ox, _bowl_cy - _flap_d/2, _flap_z])
    color(COL_GATE) cube([_flap_w, _flap_d, _flap_t]);

// Right flap (hinged at right edge, closed = flat)
translate([_bowl_ox + _bh_w - _flap_w, _bowl_cy - _flap_d/2, _flap_z])
    color(COL_GATE) cube([_flap_w, _flap_d, _flap_t]);

// Hinge pins (at outer edges of bowl housing)
for (x = [_bowl_ox, _bowl_ox + _bh_w])
    translate([x, _bowl_cy - _flap_d/2, _flap_z + _flap_t/2])
        rotate([-90, 0, 0])
            color([0.5, 0.5, 0.5]) cylinder(d=3.2, h=_flap_d);

// Direct-drive servos (one per flap, behind the hinge line)
_servo_y = _bowl_cy + _flap_d/2 + 3;
for (x = [_bowl_ox, _bowl_ox + _bh_w - SERVO_D])
    translate([x - SERVO_D/2 + SERVO_D/2, _servo_y, _flap_z - SERVO_H/2])
        color(COL_GATE) cube([SERVO_D, SERVO_W, SERVO_H]);

// ═══════════════════════════════════════════════════════════════════════════
// CAMERA — mounted on rear box front face, just below hopper, looking down
// toward the approach zone and bowl
// ═══════════════════════════════════════════════════════════════════════════
translate([UNIT_W - 20, 105, UNIT_H - 30 + EXPLODE])
    color(COL_BODY) camera_mount();

// ═══════════════════════════════════════════════════════════════════════════
// ELECTRONICS — rear interior of body
// ═══════════════════════════════════════════════════════════════════════════
translate([UNIT_W/2 - 39, UNIT_D - 68, FLOOR + EXPLODE])
    color(COL_BODY) electronics_tray();

// ═══════════════════════════════════════════════════════════════════════════
// FEET — 4 corners of base
// ═══════════════════════════════════════════════════════════════════════════
for (x = [15, UNIT_W - 15]) for (y = [15, UNIT_D - 15])
    translate([x, y, -4 - EXPLODE])
        color(COL_TPU) foot();

// ═══════════════════════════════════════════════════════════════════════════
// REFERENCE: Cat silhouette (approximate, for scale check)
// Uncomment to see a cat-sized block approaching through the halo.
// ═══════════════════════════════════════════════════════════════════════════
// Cat shoulder width ~120mm, height when eating ~150mm
// Positioned in front of the halo, about to walk through.
// %translate([UNIT_W/2 - 60, -80, 0])
//     color([1, 0.8, 0.5, 0.3]) cube([120, 50, 150]);
