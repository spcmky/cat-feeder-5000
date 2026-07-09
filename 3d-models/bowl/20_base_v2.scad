// ============================================================
// 20_base_v2.scad — square base, round bowl pocket, hinge mounts
// Print orientation: as-is, flat on the bed (pocket facing up).
// ============================================================
include <params_v2.scad>
include <hinge_v2.scad>

SUPPORT_RIDGE_H = 6;   // height of the gusset ridge under each knuckle row
SUPPORT_RIDGE_D = 6;   // how far it projects out from the wall

module base_block() {
    difference() {
        // outer square block
        cube([BASE_SIZE, BASE_SIZE, BASE_HEIGHT]);

        // round bowl pocket, open at top, floor = FLOOR_T thick
        translate([BASE_SIZE / 2, BASE_SIZE / 2, FLOOR_T])
            cylinder(r = BOWL_RADIUS, h = BOWL_DEPTH + 1, $fn = 96);
    }
}

module support_ridge(edge = "front") {
    if (edge == "front") {
        translate([0, -SUPPORT_RIDGE_D, BASE_HEIGHT - SUPPORT_RIDGE_H])
            cube([FLAP_LEN, SUPPORT_RIDGE_D, SUPPORT_RIDGE_H]);
    } else {
        translate([0, BASE_SIZE, BASE_HEIGHT - SUPPORT_RIDGE_H])
            cube([FLAP_LEN, SUPPORT_RIDGE_D, SUPPORT_RIDGE_H]);
    }
}

module base_hinge_knuckles(edge = "front") {
    hole_d = ROD_D + ROD_CLEARANCE;
    overlap = 0.3;
    if (edge == "front") {
        translate([0, -KNUCKLE_OD / 2 + overlap, ROD_AXIS_Z])
            knuckle_row(BASE_KNUCKLE_INDICES, hole_d);
    } else {
        translate([0, BASE_SIZE + KNUCKLE_OD / 2 - overlap, ROD_AXIS_Z])
            knuckle_row(BASE_KNUCKLE_INDICES, hole_d);
    }
}

module base_assembly() {
    base_block();
    support_ridge("front");
    support_ridge("back");
    base_hinge_knuckles("front");
    base_hinge_knuckles("back");
}

base_assembly();
