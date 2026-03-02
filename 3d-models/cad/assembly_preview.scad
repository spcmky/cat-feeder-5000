// Cat Feeder 5000 — Assembly Preview
// Shows all parts in approximate assembled position.
// Use this to check fit and clearances. Set EXPLODE > 0 to separate parts.
// Not for printing.

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

EXPLODE = 0;   // Set to 1–30 to explode parts apart for inspection

// Main body
main_body();

// Hopper (on top of body)
translate([15, 35, UNIT_H + EXPLODE*2])
    hopper();

// Hopper lid
translate([15, 35, UNIT_H + 130 + EXPLODE*4])
    hopper_lid();

// Bowl bracket (front, bottom)
translate([(UNIT_W - 110)/2, -5, 40 + EXPLODE])
    bowl_bracket();

// Bowl (on bracket, front)
translate([(UNIT_W - 100)/2, -BOWL_OVERHANG - 5, 43 + EXPLODE])
    bowl();

// Gate hinge mount (top of bowl opening)
translate([(UNIT_W - 120)/2, -5, 40 + BOWL_OPENING_H + EXPLODE*2])
    gate_hinge_mount();

// Gate flap (closed position — covers bowl opening)
translate([(UNIT_W - GATE_W)/2, -GATE_T - 3, 40 + EXPLODE])
    gate_flap();

// Antenna arch (top, centered)
translate([0, 20, UNIT_H - 10 + EXPLODE*3])
    antenna_arch();

// Electronics tray (rear interior)
translate([UNIT_W/2 - 39, UNIT_D - 68, FLOOR + EXPLODE])
    electronics_tray();

// Gate servo bracket (inside, above gate)
translate([UNIT_W/2 - 20, 5, 120 + EXPLODE])
    gate_servo_bracket();

// Gate bumper (inside top, gate fully-open stop)
translate([UNIT_W/2 - 15, 8, UNIT_H - 20 + EXPLODE])
    gate_bumper();

// Feet (4 corners of base)
for (x=[10, UNIT_W-10]) for (y=[10, UNIT_D-10])
    translate([x, y, -4 - EXPLODE])
        foot();
