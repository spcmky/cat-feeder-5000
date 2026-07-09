// ============================================================
// params_v4.scad — print-in-place hinge, single continuous barrel
// Base + both flaps print together as ONE piece, flat/open (like
// the reference box), then fold closed by hand after printing.
// No rod, no pins, no hardware, no snap-assembly step.
// ============================================================
$fn = 64;

// ---- Bowl ----
BOWL_DIA      = 108;
BOWL_DEPTH    = 40;
BOWL_RADIUS   = BOWL_DIA / 2;

// ---- Base block ----
WALL          = 6;
FLOOR_T       = 4;
BASE_SIZE     = BOWL_DIA + 2 * WALL;     // 120mm square
BASE_HEIGHT   = BOWL_DEPTH + FLOOR_T;    // 44mm

// ---- Flap ----
FLAP_LEN      = BASE_SIZE;
FLAP_OVERLAP  = 4;
FLAP_DEPTH    = BASE_SIZE / 2 + FLAP_OVERLAP;
FLAP_T        = 3;

// ---- Print-in-place barrel hinge ----
PIN_D         = 8;                  // pin diameter
SOCKET_CLEAR  = 0.5;                // total diametral clearance (tune per printer/material)
SOCKET_ID     = PIN_D + SOCKET_CLEAR;
SOCKET_SHELL  = 3;
SOCKET_OD     = SOCKET_ID + 2 * SOCKET_SHELL;
END_MARGIN    = 4;                  // inset from each end of the edge
BARREL_LEN    = FLAP_LEN - 2 * END_MARGIN;   // socket length (both hinges)

// reinforcement ridge so the thin panel/base have enough material to embed the pin
PAD_DEPTH     = 10;
FLAP_PAD_H    = PIN_D + 2;
// HINGE_Z is set so the pin/socket genuinely overlaps into both the base
// block and the flap panel (a few mm of real volumetric overlap) rather
// than sitting exactly tangent to a flat face — exact tangency between
// separate solids is a classic non-manifold CSG trap.
HINGE_EMBED   = 2;  // how far the joint dips below the base's top surface
HINGE_Z       = BASE_HEIGHT + HINGE_EMBED;

// small relief gap so the flap panel doesn't touch the base along a bare
// edge (that kind of zero-area contact causes non-manifold CSG results,
// and physically the panel doesn't need to touch — only the pin/socket
// joint should connect the two pieces).
HINGE_GAP     = 0.4;
BASE_PAD_H    = (HINGE_Z - BASE_HEIGHT) + SOCKET_OD / 2 + 2;

// ---- Servo drive extension (flap's pin extends past the base to meet the horn) ----
SERVO_EXT_LEN = 22;                 // how far the pin extends past the base edge
SERVO_HORN_OD = 24;                 // verify with calipers
SERVO_HORN_BOLT_CIRCLE = 19;        // verify with calipers
SERVO_BOSS_D  = SERVO_HORN_OD + 4;
SERVO_BOSS_T  = 4;
M3_CLEAR      = 3.4;

// ---- MG996R servo body (for the separate bracket — still a physical part) ----
SERVO_W       = 40.7;
SERVO_D       = 19.7;
SERVO_H       = 42.9;
SERVO_SHAFT_OFFSET = 30.9;
