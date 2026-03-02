// Cat Feeder 5000 — Part 05: Auger Screw
// Rotates inside auger tube. Motor-driven. Calibrate STEPS_PER_GRAM in firmware.
// Print: PETG, 0.15mm layers, 60% infill, supports YES (for thread underside)
// IMPORTANT: Print vertically (coupler end down) for thread layer integrity.

include <params.scad>

color(COL_FOOD) auger_screw();

module auger_screw() {
    SCREW_OD   = 30;        // 1mm clearance to tube ID=32
    PITCH      = AUGER_PITCH;
    TURNS      = floor(AUGER_TUBE_L / PITCH) - 1;
    SCREW_L    = TURNS * PITCH;
    THREAD_D   = 12;        // Thread fin depth
    SHAFT_D    = 5;         // Motor shaft bore
    COUPLER_L  = 15;
    SET_D      = 3;         // Set screw hole diameter

    difference() {
        union() {
            // Core rod
            cylinder(d=SCREW_OD * 0.4, h=SCREW_L + COUPLER_L);
            // Helical thread fins (approximated as stacked angled discs)
            for (i = [0 : TURNS - 1])
                translate([0, 0, i * PITCH])
                    linear_extrude(height=PITCH, twist=-360, slices=24)
                        translate([SCREW_OD * 0.2, 0, 0])
                            square([THREAD_D, PITCH * 0.8], center=true);
            // Motor coupler
            translate([0, 0, -COUPLER_L])
                cylinder(d=SCREW_OD * 0.5, h=COUPLER_L);
        }
        // Shaft bore
        translate([0, 0, -COUPLER_L - 0.1])
            cylinder(d=SHAFT_D + TOLERANCE, h=COUPLER_L + 5);
        // Set screw hole (side of coupler, M3)
        translate([SCREW_OD * 0.25 + 3, 0, -COUPLER_L/2])
            rotate([0, 90, 0])
                cylinder(d=SET_D, h=SCREW_OD);
    }
}
