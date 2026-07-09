// ============================================================
// 23_assembly_v2.scad — full assembly, animated open/close
// Render animation:
//   openscad -o out.png --animate 24 --imgsize=800,600 23_assembly_v2.scad
// $t goes 0..1 automatically when using --animate; OPEN_ANGLE below
// maps that to a 0..MAX_OPEN sweep. For a static preview set T_OVERRIDE.
// ============================================================
include <params_v2.scad>
include <hinge_v2.scad>
use <20_base_v2.scad>
use <21_flap_v2.scad>
use <22_servo_mount_v2.scad>

MAX_OPEN = 105;             // degrees, matches the GIF's past-vertical open pose
T_OVERRIDE = 1.0;
t_val = (T_OVERRIDE >= 0) ? T_OVERRIDE : $t;
// ping-pong 0->1->0 over the animation loop so it opens then closes
t_pingpong = (t_val < 0.5) ? (t_val * 2) : (2 - t_val * 2);
ANGLE = t_pingpong * MAX_OPEN;

color("SteelBlue") base_assembly();

// ---- Front flap (hinge at Y=0) ----
color("CornflowerBlue")
translate([0, -KNUCKLE_OD / 2, ROD_AXIS_Z])
    rotate([ANGLE, 0, 0])
    translate([0, KNUCKLE_OD / 2, -FLAP_T / 2])
        flap_assembly();

// ---- Back flap (hinge at Y=BASE_SIZE), mirrored ----
color("CornflowerBlue")
translate([0, BASE_SIZE + KNUCKLE_OD / 2, ROD_AXIS_Z])
    rotate([-ANGLE, 0, 0])
    mirror([0, 1, 0])
    translate([0, KNUCKLE_OD / 2, -FLAP_T / 2])
        flap_assembly();

// ---- Servo mounts, one per hinge line ----
// Bracket's local shaft point is (BX, BY/2, ROD_AXIS_Z) [see echo in 22_servo_mount_v2.scad].
// Local Z already equals world Z (both brackets sit on the same ground plane as the base),
// so only X/Y need translating to land the shaft at the rod end.
SB_BX = 3 + SERVO_H + 0.5;               // = BX in 22_servo_mount_v2.scad
SB_BY = (SERVO_D + 0.5) + 2 * 3;         // = BY in 22_servo_mount_v2.scad

TARGET_SHAFT_X = -ROD_END_PROTRUDE;      // where the rod end / horn coupler sits
TARGET_SHAFT_Y = -KNUCKLE_OD / 2;        // same rod centerline as the knuckles

color("DarkSlateBlue")
translate([TARGET_SHAFT_X - SB_BX, TARGET_SHAFT_Y - SB_BY / 2, 0])
    servo_bracket();
