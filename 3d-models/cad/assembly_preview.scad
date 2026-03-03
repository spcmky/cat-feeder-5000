// Cat Feeder 5000 — Assembly Preview
// Shows all parts in approximate assembled position.
// Set EXPLODE > 0 to separate parts for inspection.
// Not for printing — visualization only.
//
// COORDINATE SYSTEM:
//   X = left-right (width)
//   Y = front-back (depth) — Y=0 is the FRONT (cat approach side)
//   Z = up-down (height) — Z=0 is the floor
//
// LAYOUT (side view):
//
//   ┌─────────────────────┐  ← hopper lid
//   │      HOPPER         │
//   ├─────────────────────┤  ← top of main body (Z=UNIT_H)
//   │                     │
//   │   auger  ╲          │
//   │     tube  ╲  elec.  │
//   │            ╲  bay   │
//   │   ┌bridge──┐        │  ← antenna arch bridge (Z=LEG_H)
//   │   │ (coil) │        │
//   │  L│        │R       │  ← arch legs (outside body, at front face)
//   │  E│  CAT   │I       │
//   │  G│ walks  │G       │  ← approach opening
//   │   │ here   │        │
//   │   │ [bowl] │        │  ← bowl at floor level
//   └───┴────────┴────────┘  ← floor (Z=0)
//        ← front    rear →
//        Y=0        Y=UNIT_D

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
// ANTENNA ARCH — front-mounted halo doorway
// Bolts to the front face of the body, extending FORWARD (Y-negative).
// The cat walks through the arch to reach the bowl.
// ═══════════════════════════════════════════════════════════════════════════
// Arch legs sit at Y = -LEG_D (extending forward from the body front face).
// Arch spans the full UNIT_W, centered on the approach opening.
translate([0, -35 - EXPLODE, 0])
    antenna_arch();

// ═══════════════════════════════════════════════════════════════════════════
// BOWL — sits at floor level inside the front of the body
// The cat's head reaches in through the approach opening to eat.
// ═══════════════════════════════════════════════════════════════════════════
// Bowl is inside the body, on the bowl shelf, centered in the approach opening.
translate([(UNIT_W - 100)/2, 10, FLOOR + EXPLODE])
    bowl();

// BOWL BRACKET
translate([(UNIT_W - 110)/2, 10, FLOOR - EXPLODE])
    bowl_bracket();

// ═══════════════════════════════════════════════════════════════════════════
// GATE — blocks the approach opening. Swing-up: hinged at top.
// When closed, it covers the approach opening from the inside.
// When open, it swings up into the body above the opening.
// ═══════════════════════════════════════════════════════════════════════════
// Closed position: flat across the approach opening, just inside body front face.
translate([(UNIT_W - GATE_W)/2, WALL, FLOOR + EXPLODE])
    gate_flap();

// GATE HINGE MOUNT — bolts across the top of the approach opening, inside face.
translate([(UNIT_W - 120)/2, WALL, 130 - 20 + EXPLODE * 2])
    gate_hinge_mount();

// GATE SERVO BRACKET — inside body, above approach opening.
translate([UNIT_W/2 - 20, WALL + 5, 130 + 5 + EXPLODE * 2])
    gate_servo_bracket();

// GATE BUMPER — inside body, where gate flap rests when fully open.
translate([UNIT_W/2 - 15, WALL + 5, UNIT_H - 25 + EXPLODE])
    gate_bumper();

// ═══════════════════════════════════════════════════════════════════════════
// CAMERA — mounted inside body, looking down toward the approach zone.
// Captures cat's face from above as it eats.
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
// Uncomment to see a cat-sized block in the approach zone.
// ═══════════════════════════════════════════════════════════════════════════
// Cat shoulder width ~120mm, height when eating ~150mm, head at bowl level.
// %translate([UNIT_W/2 - 60, -80, 0])
//     color([1, 0.8, 0.5, 0.3]) cube([120, 100, 150]);
