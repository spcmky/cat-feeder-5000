// ============================================================
// hinge_v2.scad — shared piano-hinge knuckle geometry
// Pattern along the hinge edge: BASE-FLAP-BASE-FLAP-BASE (5 segments)
// Segment index 0,2,4 = fixed to BASE (rod spins freely inside)
// Segment index 1,3   = fixed to FLAP (rod glued/pinned, rotates with flap)
// ============================================================
include <params_v2.scad>

PATTERN_TOTAL = 5 * KNUCKLE_LEN + 4 * KNUCKLE_GAP;
PATTERN_MARGIN = (FLAP_LEN - PATTERN_TOTAL) / 2;

// Returns the x-start position of segment index i (0..4)
function knuckle_x(i) = PATTERN_MARGIN + i * (KNUCKLE_LEN + KNUCKLE_GAP);

// A single knuckle cylinder, axis along X, with a through-bore for the rod.
// hole_d: ROD_D + ROD_CLEARANCE for a bearing (base) knuckle,
//         ROD_D + 0.1 for a tight/glued (flap) knuckle.
module knuckle(hole_d) {
    difference() {
        rotate([0, 90, 0])
            cylinder(d = KNUCKLE_OD, h = KNUCKLE_LEN, $fn = 32);
        rotate([0, 90, 0])
            cylinder(d = hole_d, h = KNUCKLE_LEN + 2, center = true, $fn = 24);
    }
}

// Row of knuckles at given indices, positioned along X starting at x_offset,
// centered on Y=0 locally (caller translates to the actual hinge edge).
module knuckle_row(indices, hole_d, x_offset = 0) {
    for (i = indices) {
        translate([x_offset + knuckle_x(i), 0, 0])
            knuckle(hole_d);
    }
}

BASE_KNUCKLE_INDICES = [0, 2, 4];
FLAP_KNUCKLE_INDICES = [1, 3];
