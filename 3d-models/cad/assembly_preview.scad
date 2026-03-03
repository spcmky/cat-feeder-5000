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
use <09_bowl.scad>
use <10_bowl_bracket.scad>
use <11_camera_mount.scad>
use <13_gate_flap.scad>
use <14_gate_hinge_mount.scad>
use <15_antenna_arch.scad>
use <16_gate_servo_bracket.scad>
use <17_gate_bumper.scad>
use <18_feet.scad>

EXPLODE = 0;    // Set to 10–30 to explode parts apart for inspection

// ═══════════════════════════════════════════════════════════════════════════
// MAIN BODY — the box that sits on the floor
// ═══════════════════════════════════════════════════════════════════════════
main_body();

// ═══════════════════════════════════════════════════════════════════════════
// HOPPER — sits on top of main body
// ═══════════════════════════════════════════════════════════════════════════
translate([15, 80, UNIT_H + EXPLODE * 2])
    hopper();

// HOPPER LID
translate([15, 80, UNIT_H + 130 + EXPLODE * 4])
    hopper_lid();

// ═══════════════════════════════════════════════════════════════════════════
// ROUND HALO — RFID antenna arch (semicircular ring)
// Sits just outside the body front face. The cat walks through the ring.
// Halo total_w = 154mm, centered on body (UNIT_W=160).
// Halo back surface flush with Y=0 (body front face).
// Feet extend forward to Y = -FOOT_D/2 ≈ -17.
// ═══════════════════════════════════════════════════════════════════════════
// Center halo on body: offset_x = (160 - 154)/2 = 3
// Position so halo tube center is at Y = -HALO_TUBE_OD/2 = -12
// (back surface at Y=0, front surface at Y=-24)
translate([(UNIT_W - 154)/2, -HALO_TUBE_OD/2 - EXPLODE, 0])
    antenna_arch();

// ═══════════════════════════════════════════════════════════════════════════
// BOWL — sits behind the gate, on the shelf inside the body
// ═══════════════════════════════════════════════════════════════════════════
// Bowl centered in approach opening, behind gate (Y > GATE_SETBACK)
translate([(UNIT_W - 100)/2, GATE_SETBACK + 15, FLOOR + EXPLODE])
    bowl();

// BOWL BRACKET
translate([(UNIT_W - 110)/2, GATE_SETBACK + 15, FLOOR - EXPLODE])
    bowl_bracket();

// ═══════════════════════════════════════════════════════════════════════════
// GATE — blocks the approach opening. Swing-up: hinged at top.
// Sits at GATE_SETBACK (40mm) inside the body — behind the halo.
// When closed, it covers the approach from inside.
// When open, it swings up into the body above the opening.
// ═══════════════════════════════════════════════════════════════════════════
translate([(UNIT_W - GATE_W)/2, GATE_SETBACK, FLOOR + EXPLODE])
    gate_flap();

// GATE HINGE MOUNT — at top of approach opening, at GATE_SETBACK depth
translate([(UNIT_W - 120)/2, GATE_SETBACK, 130 - 20 + EXPLODE * 2])
    gate_hinge_mount();

// GATE SERVO BRACKET — inside body, above gate position
translate([UNIT_W/2 - 20, GATE_SETBACK + 15, 130 + 5 + EXPLODE * 2])
    gate_servo_bracket();

// GATE BUMPER — inside body, where gate flap rests when fully open
translate([UNIT_W/2 - 15, GATE_SETBACK + 5, UNIT_H - 25 + EXPLODE])
    gate_bumper();

// ═══════════════════════════════════════════════════════════════════════════
// CAMERA — mounted inside body, looking down toward the approach zone
// ═══════════════════════════════════════════════════════════════════════════
translate([UNIT_W - 20, 20, 130 + EXPLODE])
    camera_mount();

// ═══════════════════════════════════════════════════════════════════════════
// ELECTRONICS — rear interior of body
// ═══════════════════════════════════════════════════════════════════════════
translate([UNIT_W/2 - 39, UNIT_D - 68, FLOOR + EXPLODE])
    electronics_tray();

// ═══════════════════════════════════════════════════════════════════════════
// FEET — 4 corners of base
// ═══════════════════════════════════════════════════════════════════════════
for (x = [15, UNIT_W - 15]) for (y = [15, UNIT_D - 15])
    translate([x, y, -4 - EXPLODE])
        foot();

// ═══════════════════════════════════════════════════════════════════════════
// REFERENCE: Cat silhouette (approximate, for scale check)
// Uncomment to see a cat-sized block approaching through the halo.
// ═══════════════════════════════════════════════════════════════════════════
// Cat shoulder width ~120mm, height when eating ~150mm
// Positioned in front of the halo, about to walk through.
// %translate([UNIT_W/2 - 60, -80, 0])
//     color([1, 0.8, 0.5, 0.3]) cube([120, 50, 150]);
