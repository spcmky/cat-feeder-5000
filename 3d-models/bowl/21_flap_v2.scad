// ============================================================
// 21_flap_v2.scad — one trapdoor flap (print x2)
// Local frame: hinge edge at Y=0, panel extends to Y=+FLAP_DEPTH,
// thickness Z=0..FLAP_T. Knuckles protrude to Y<0, centered on
// mid-thickness (Z=FLAP_T/2) so they line up with the base's
// knuckle row when the flap sits closed on top of the base.
// Print orientation: lay flat, panel face down, knuckles up —
// or print on its long edge to avoid overhangs on the knuckles;
// test one first.
// ============================================================
include <params_v2.scad>
include <hinge_v2.scad>

module flap_panel() {
    // slight taper/chamfer on the leading (free) edge could be added later;
    // v1 keeps it a simple flat panel for print simplicity.
    cube([FLAP_LEN, FLAP_DEPTH, FLAP_T]);
}

module flap_hinge_knuckles() {
    hole_d = ROD_D + 0.1; // tight fit — glue or press-fit onto the rod
    overlap = 0.3; // ensure solid union with panel, not just a tangent touch
    translate([0, -KNUCKLE_OD / 2 + overlap, FLAP_T / 2])
        knuckle_row(FLAP_KNUCKLE_INDICES, hole_d);
}

module flap_assembly() {
    flap_panel();
    flap_hinge_knuckles();
}

flap_assembly();
