// ============================================================
// 10_combined_v4.scad — ONE PIECE: base + both flaps, flat/open
// Print exactly as modeled (flat, pocket up) — hinges are already
// assembled by the print itself. Fold each flap closed by hand
// after printing (PETG flexes enough at this pin diameter; do a
// few slow open/close cycles right off the bed while it's still
// slightly warm to work the joint in).
//
// Each flap's pin extends past one end of the base to meet a
// servo horn directly — see SERVO_EXT_LEN in params_v4.scad.
// ============================================================
include <params_v4.scad>
include <hinge_v4.scad>

// ---------------- Base ----------------
module base_block() {
    difference() {
        cube([BASE_SIZE, BASE_SIZE, BASE_HEIGHT]);
        translate([BASE_SIZE / 2, BASE_SIZE / 2, FLOOR_T])
            cylinder(r = BOWL_RADIUS, h = BOWL_DEPTH + 1, $fn = 96);
    }
}

module base_socket_shell(edge) {
    if (edge == "front")
        translate([END_MARGIN, 0, HINGE_Z])
            socket_outer(BARREL_LEN);
    else
        translate([END_MARGIN, BASE_SIZE, HINGE_Z])
            socket_outer(BARREL_LEN);
}

module base_socket_bore(edge) {
    // extended slightly past both ends for a clean cut
    if (edge == "front")
        translate([END_MARGIN - 1, 0, HINGE_Z])
            socket_bore(BARREL_LEN + 2);
    else
        translate([END_MARGIN - 1, BASE_SIZE, HINGE_Z])
            socket_bore(BARREL_LEN + 2);
}

// base_block + both socket shells, unioned, THEN both bores cut through
// everything at once — this is what gives the pin real clearance even in
// the region where the socket is embedded inside the base block.
module base_assembly() {
    difference() {
        union() {
            base_block();
            base_socket_shell("front");
            base_socket_shell("back");
        }
        base_socket_bore("front");
        base_socket_bore("back");
    }
}

// ---------------- Flap (flat/open pose) ----------------
// front flap occupies Y: -FLAP_DEPTH..0 ; back flap occupies Y: BASE_SIZE..BASE_SIZE+FLAP_DEPTH
module flap_panel(edge) {
    if (edge == "front")
        translate([0, -FLAP_DEPTH, BASE_HEIGHT])
            cube([FLAP_LEN, FLAP_DEPTH - HINGE_GAP, FLAP_T]);
    else
        translate([0, BASE_SIZE + HINGE_GAP, BASE_HEIGHT])
            cube([FLAP_LEN, FLAP_DEPTH - HINGE_GAP, FLAP_T]);
}

// pin extends SERVO_EXT_LEN past the low-X end to reach the servo horn
module flap_pin(edge) {
    total_len = BARREL_LEN + SERVO_EXT_LEN;
    start_x = END_MARGIN - SERVO_EXT_LEN;
    if (edge == "front")
        translate([start_x, 0, HINGE_Z])
            pin_barrel(total_len);
    else
        translate([start_x, BASE_SIZE, HINGE_Z])
            pin_barrel(total_len);
}

module horn_boss(edge) {
    x = END_MARGIN - SERVO_EXT_LEN;
    y = (edge == "front") ? 0 : BASE_SIZE;
    translate([x, y, HINGE_Z])
        rotate([0, 90, 0])
        difference() {
            cylinder(d = SERVO_BOSS_D, h = SERVO_BOSS_T, $fn = 40);
            for (a = [0, 180])
                rotate([0, 0, a])
                    translate([SERVO_HORN_BOLT_CIRCLE / 2, 0, -0.1])
                        cylinder(d = 2.2, h = SERVO_BOSS_T + 0.2, $fn = 16); // horn screw holes, verify size
        }
}

module flap_assembly(edge) {
    flap_panel(edge);
    flap_pin(edge);
    horn_boss(edge);
}

// ---------------- Full combined piece ----------------
module combined_assembly() {
    base_assembly();
    flap_assembly("front");
    flap_assembly("back");
}

combined_assembly();
