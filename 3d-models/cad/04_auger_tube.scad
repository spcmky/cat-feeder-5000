// Cat Feeder 5000 — Part 04: Auger Tube
// Food channel. Auger screw rotates inside this.
// Coupling stub above flange accepts the hopper sleeve (slip fit).
// Print: PETG, 0.2mm layers, 30% infill, no supports. Smooth inner bore.

include <params.scad>

color(COL_FOOD) auger_tube();

module auger_tube() {
    FLANGE_D = 50; FLANGE_H = 5;
    EXIT_D = 28;

    difference() {
        union() {
            // Main tube
            cylinder(d=AUGER_TUBE_OD, h=AUGER_TUBE_L);
            // Top flange (roof mount)
            translate([0, 0, AUGER_TUBE_L - FLANGE_H])
                cylinder(d=FLANGE_D, h=FLANGE_H);
            // Coupling stub above flange (hopper slides onto this)
            translate([0, 0, AUGER_TUBE_L])
                cylinder(d=AUGER_TUBE_OD, h=AUGER_COUPLING_H);
        }
        // Bore (inner channel) — full height including coupling stub
        translate([0, 0, -0.1])
            cylinder(d=AUGER_TUBE_ID, h=AUGER_TUBE_L + AUGER_COUPLING_H + 0.2);
        // Bottom exit port (90° to tube axis)
        translate([0, -AUGER_TUBE_OD, 10])
            rotate([-90, 0, 0])
                cylinder(d=EXIT_D, h=AUGER_TUBE_OD + 2);
        // Flange M3 holes (×3, 120° apart)
        for (a = [0, 120, 240])
            rotate([0, 0, a])
                translate([FLANGE_D/2 - 8, 0, AUGER_TUBE_L - FLANGE_H - 0.1])
                    m3_clear(h=FLANGE_H + 0.2);
    }
}
