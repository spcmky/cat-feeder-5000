// ============================================================
// hinge_v4.scad — print-in-place barrel, no gap (single combined print)
// ============================================================
include <params_v4.scad>

module pin_barrel(len) {
    rotate([0, 90, 0])
        cylinder(d = PIN_D, h = len, $fn = 28);
}

// Outer shell and bore are kept SEPARATE (not pre-hollowed) so the caller
// can union all the outer-shell material (including the part embedded in
// the base block) first, then subtract the bore as one final step. If the
// bore is cut locally inside this module, unioning the resulting tube onto
// the base block does NOT drill through the base's own solid material
// where they overlap — union never retroactively removes material.
module socket_outer(len) {
    rotate([0, 90, 0])
        cylinder(d = SOCKET_OD, h = len, $fn = 40);
}

module socket_bore(len) {
    rotate([0, 90, 0])
        cylinder(d = SOCKET_ID, h = len, $fn = 28);
}

// convenience wrapper for standalone use/testing (properly hollowed)
module socket_barrel(len) {
    difference() {
        socket_outer(len);
        socket_bore(len);
    }
}
