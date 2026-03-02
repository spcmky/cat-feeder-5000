// Cat Feeder 5000 — Part 01: Main Body / Base
// Structural core. All other parts mount into this.
// Print: PETG, 0.25mm layers, 40% infill, no supports

include <params.scad>

color(COL_BODY) main_body();

module main_body() {
    difference() {
        // Outer shell
        fillet_box(UNIT_W, UNIT_D, UNIT_H, r=4);

        // Hollow interior
        translate([WALL, WALL, FLOOR])
            fillet_box(UNIT_W - 2*WALL, UNIT_D - 2*WALL, UNIT_H, r=2);

        // Front bowl approach opening
        translate([(UNIT_W - BOWL_OPENING_W)/2, -1, FLOOR])
            cube([BOWL_OPENING_W, WALL + 2, BOWL_OPENING_H]);

        // Auger tube hole (center, angled)
        translate([UNIT_W/2, UNIT_D/2, FLOOR + 20])
            rotate([AUGER_ANGLE, 0, 0])
                cylinder(d=AUGER_TUBE_OD + 1, h=UNIT_H);

        // Electronics bay cutout (rear lower)
        translate([UNIT_W/2 - 40, UNIT_D - WALL - 80, FLOOR])
            cube([80, 60, 50]);

        // Rear cable pass-through
        translate([UNIT_W/2, UNIT_D - WALL/2, 20])
            rotate([90, 0, 0])
                cylinder(d=15, h=WALL + 2);

        // M3 boss cutouts (top rim, for hopper mount)
        for (x = [30, UNIT_W - 30]) for (y = [30, UNIT_D - 30])
            translate([x, y, UNIT_H - 6])
                m3_insert(h=6.2);
    }

    // M3 insert bosses (interior, for mounting sub-parts)
    interior_bosses();

    // Bottom feet pockets
    for (x = [10, UNIT_W - 10]) for (y = [10, UNIT_D - 10])
        difference() {
            translate([x - 8, y - 8, 0]) cube([16, 16, FLOOR]);
            translate([x, y, -0.1]) cylinder(d=10, h=FLOOR + 0.2);
        }
}

module interior_bosses() {
    // Bowl bracket bosses (front interior, sides)
    for (x = [20, UNIT_W - 20])
        translate([x, WALL + 5, FLOOR])
            boss(d_outer=8, h=30);
    // Electronics tray bosses (rear)
    for (x = [UNIT_W/2 - 35, UNIT_W/2 + 35])
        translate([x, UNIT_D - WALL - 10, FLOOR])
            boss(d_outer=8, h=10);
    // Antenna arch mount (top sides)
    for (x = [15, UNIT_W - 15])
        translate([x, UNIT_D/2, UNIT_H - WALL])
            rotate([0, 0, 0]) boss(d_outer=8, h=8);
}
