// ============================================================
// 22_servo_mount_v2.scad — MG996R bracket, shaft aligned to rod
// The servo is rotated 90° from its usual orientation so the
// output shaft points sideways (along +X) into the rod/coupler,
// instead of the usual "shaft points up" mounting.
//
// Pocket is open on TOP (drop the servo in) and open on the
// FRONT/+X face (shaft + horn protrude toward the base). Servo
// is held with zip-tie slots rather than modeled ear-mount holes,
// since exact ear spacing varies by MG996R clone — verify yours
// with calipers; zip ties are forgiving of small errors for v1.
//
// Print orientation: as-is, flat on the bed.
// ============================================================
include <params_v2.scad>

WALL2   = 3;
TOL     = 0.5;   // pocket clearance around servo body

// after 90° remap: X-extent(depth into bracket)=SERVO_H, Y-extent=SERVO_D, Z-extent=SERVO_W
POCKET_X = SERVO_H + TOL;
POCKET_Y = SERVO_D + TOL;
POCKET_Z = SERVO_W + TOL;

// shaft sits 30.9mm up from the pocket's "bottom" (see params_v2 SERVO_SHAFT_OFFSET)
POCKET_BOTTOM_Z = ROD_AXIS_Z - SERVO_SHAFT_OFFSET;

BX = WALL2 + POCKET_X;              // back wall + pocket depth (front left open)
BY = POCKET_Y + 2 * WALL2;          // side walls both sides
BZ = POCKET_BOTTOM_Z + POCKET_Z;    // pedestal + pocket height (top left open)

module servo_pocket() {
    translate([WALL2, WALL2, POCKET_BOTTOM_Z])
        cube([POCKET_X + 5, POCKET_Y, POCKET_Z + 5]); // +5 extends through front & top (open)
}

module ziptie_slots() {
    // two slot pairs (through both side walls), one near pocket bottom, one near top
    for (z = [POCKET_BOTTOM_Z + 6, POCKET_BOTTOM_Z + POCKET_Z - 6]) {
        translate([WALL2 + 6, -1, z - 1.5])
            cube([3, BY + 2, 3]);
    }
}

module mount_holes() {
    // 2x M3 through the pedestal, for screwing bracket to a shared platform/board
    for (x = [6, BX - 6])
        translate([x, BY / 2, -0.1])
            cylinder(d = M3_CLEAR, h = POCKET_BOTTOM_Z + 0.2, $fn = 24);
}

module servo_bracket() {
    difference() {
        cube([BX, BY, BZ]);
        servo_pocket();
        ziptie_slots();
        mount_holes();
    }
}

servo_bracket();

// ---- reference: where the shaft/horn ends up in world coords (for the assembly) ----
echo("Servo shaft center (local bracket coords): X =", BX, " Y =", BY/2, " Z =", ROD_AXIS_Z);
