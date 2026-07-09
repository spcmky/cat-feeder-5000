// ============================================================
// Cat Bowl v1 — Round Bowl + Dual Trapdoor Flaps (piano-hinge)
// params_v2.scad — all key dimensions live here
// ============================================================
// NOTE: Independent of the old params.scad (rectangular body /
// halo antenna / hopper design). This is a clean start for the
// current hardware: round 108mm bowl + 2x MG996R servos.
// ============================================================

$fn = 64;

// ---- Bowl (as given: 108mm diameter, 40mm deep) ----
BOWL_DIA      = 108;
BOWL_DEPTH    = 40;
BOWL_RADIUS   = BOWL_DIA / 2;

// ---- Base block (square footprint, round pocket inside) ----
WALL          = 6;                       // wall thickness around bowl pocket
FLOOR_T       = 4;                       // floor thickness under bowl
BASE_SIZE     = BOWL_DIA + 2 * WALL;     // 120mm square
BASE_HEIGHT   = BOWL_DEPTH + FLOOR_T;    // 44mm — top of base = hinge rod height

// ---- Flap (two rectangular flaps, each covers half the top) ----
FLAP_LEN      = BASE_SIZE;               // runs full width along hinge edge (120mm)
FLAP_OVERLAP  = 4;                       // extra reach past centerline for sealing
FLAP_DEPTH    = BASE_SIZE / 2 + FLAP_OVERLAP;  // 64mm
FLAP_T        = 3;                       // flap panel thickness

// ---- Piano hinge (rod + knuckles) ----
ROD_D         = 4;                       // steel/brass rod diameter (verify what you have)
ROD_CLEARANCE = 0.4;                     // bearing clearance for knuckles that spin freely
KNUCKLE_OD    = ROD_D + 6;               // 10mm knuckle outer diameter
KNUCKLE_LEN   = 18;                      // length of each knuckle segment
KNUCKLE_GAP   = 4;                       // gap between knuckle segments
// Alternating pattern along the FLAP_LEN edge: base-flap-base-flap-base (5 segments)
// 3 fixed (base) knuckles + 2 rotating (flap) knuckles, interleaved
ROD_END_PROTRUDE = 12;                   // rod extends past the base footprint for servo coupling
ROD_LENGTH    = FLAP_LEN + 2 * ROD_END_PROTRUDE;
// Rod axis sits at the flap's mid-thickness height when the flap is closed
// and resting on top of the base — NOT at the bare top surface.
ROD_AXIS_Z    = BASE_HEIGHT + FLAP_T / 2;

// ---- MG996R servo (verify with calipers once yours arrive) ----
SERVO_W       = 40.7;   // body length
SERVO_D       = 19.7;   // body width/depth
SERVO_H       = 42.9;   // body height (shaft side up)
SERVO_SHAFT_OFFSET = 30.9; // distance from back edge to shaft, along SERVO_W
SERVO_TAB_SPAN = 54.5;  // outer tab-to-tab width
SERVO_TAB_HOLE_SPACING = 10; // hole spacing within each tab
SERVO_HORN_OD = 24;     // round disc horn diameter (verify)
SERVO_HORN_BOLT_CIRCLE = 19; // horn screw hole circle diameter (verify)

// ---- Mounting hardware ----
M3_CLEAR      = 3.4;    // M3 clearance hole
M3_HEAD       = 6.2;    // M3 pan head clearance
