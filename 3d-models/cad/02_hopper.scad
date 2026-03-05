// Cat Feeder 5000 — Part 02: Food Hopper
// Funnel reservoir. Sits on auger flange via slip-fit coupling sleeve.
// ~500mL / ~400g kibble.
// Print: PETG, 0.25mm layers, 25% infill, no supports

include <params.scad>

color(COL_FOOD) hopper();

module hopper() {
    TOP_W = 130; TOP_D = 130; HOPPER_H = 130;
    LIP_H = 2; LIP_T = 3;

    // Coupling sleeve dimensions (slip fit over auger stub)
    SLEEVE_ID = AUGER_TUBE_OD + 0.4;    // 38.4mm
    SLEEVE_OD = SLEEVE_ID + 2*THIN_WALL; // 43.4mm
    SZ = AUGER_COUPLING_H;               // Sleeve height = funnel Z offset

    difference() {
        union() {
            // Coupling sleeve at bottom (slides over auger stub)
            translate([TOP_W/2, TOP_D/2, 0])
                cylinder(d=SLEEVE_OD, h=SZ);

            // Outer funnel shell (hull between top square and bottom sleeve)
            hull() {
                translate([0, 0, SZ + HOPPER_H - 1])
                    fillet_box(TOP_W, TOP_D, 1, r=4);
                translate([TOP_W/2, TOP_D/2, SZ])
                    cylinder(d=SLEEVE_OD, h=1);
            }

            // Lip for lid at top
            translate([-LIP_T, -LIP_T, SZ + HOPPER_H - LIP_H])
                fillet_box(TOP_W + 2*LIP_T, TOP_D + 2*LIP_T, LIP_H, r=5);
        }

        // Hollow interior (funnel tapers to sleeve bore)
        hull() {
            translate([THIN_WALL, THIN_WALL, SZ + HOPPER_H])
                fillet_box(TOP_W - 2*THIN_WALL, TOP_D - 2*THIN_WALL, 1, r=3);
            translate([TOP_W/2, TOP_D/2, SZ - 0.1])
                cylinder(d=SLEEVE_ID, h=1);
        }

        // Sleeve bore (through the coupling sleeve)
        translate([TOP_W/2, TOP_D/2, -0.1])
            cylinder(d=SLEEVE_ID, h=SZ + 0.2);

        // Vent slots under top lip
        for (i = [0:3])
            rotate([0, 0, i*90])
                translate([TOP_W/2 + LIP_T/2, -5, SZ + HOPPER_H - LIP_H - 1])
                    cube([1, 10, LIP_H + 2]);
    }
}
