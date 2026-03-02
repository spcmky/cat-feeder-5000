// Cat Feeder 5000 — Part 02: Food Hopper
// Funnel reservoir. Sits on top of main body. ~500mL / ~400g kibble.
// Print: PETG, 0.25mm layers, 25% infill, no supports

include <params.scad>

color(COL_FOOD) hopper();

module hopper() {
    TOP_W = 130; TOP_D = 130; HOPPER_H = 130;
    OUTLET_D = AUGER_TUBE_OD;
    LIP_H = 2; LIP_T = 3;

    difference() {
        union() {
            // Outer funnel shell (hull between top square and bottom circle)
            hull() {
                translate([0, 0, HOPPER_H - 1])
                    fillet_box(TOP_W, TOP_D, 1, r=4);
                translate([TOP_W/2, TOP_D/2, 0])
                    cylinder(d=OUTLET_D + 2*THIN_WALL, h=1);
            }
            // Lip for lid at top
            translate([-LIP_T, -LIP_T, HOPPER_H - LIP_H])
                fillet_box(TOP_W + 2*LIP_T, TOP_D + 2*LIP_T, LIP_H, r=5);
        }

        // Hollow interior (thinner walls)
        hull() {
            translate([THIN_WALL, THIN_WALL, HOPPER_H])
                fillet_box(TOP_W - 2*THIN_WALL, TOP_D - 2*THIN_WALL, 1, r=3);
            translate([TOP_W/2, TOP_D/2, -0.1])
                cylinder(d=OUTLET_D, h=1);
        }

        // Vent slots under top lip
        for (i = [0:3])
            rotate([0, 0, i*90])
                translate([TOP_W/2 + LIP_T/2, -5, HOPPER_H - LIP_H - 1])
                    cube([1, 10, LIP_H + 2]);
    }

    // Mount flange at bottom with M3 insert bosses
    translate([TOP_W/2, TOP_D/2, 0])
    difference() {
        cylinder(d=OUTLET_D + 2*THIN_WALL + 20, h=5);
        cylinder(d=OUTLET_D, h=6);
        for (a = [0, 120, 240])
            rotate([0, 0, a])
                translate([OUTLET_D/2 + 8, 0, -0.1])
                    m3_insert(h=5.2);
    }
}
