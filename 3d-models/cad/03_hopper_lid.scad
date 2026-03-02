// Cat Feeder 5000 — Part 03: Hopper Lid
// Snap-on lid to keep food fresh.
// Print: PETG, 0.2mm layers, 20% infill, no supports

include <params.scad>

color(COL_BODY) hopper_lid();

module hopper_lid() {
    LID_W = 136; LID_D = 136; LID_H = 20;
    LIP_W = 130; LIP_D = 130;
    SNAP_T = 2; SNAP_H = 3;
    PORT_D = 40;

    difference() {
        union() {
            // Top plate
            fillet_box(LID_W, LID_D, 4, r=5);
            // Skirt with snap lip
            translate([0, 0, -LID_H + 4])
                difference() {
                    fillet_box(LID_W, LID_D, LID_H - 4, r=5);
                    translate([SNAP_T, SNAP_T, -0.1])
                        fillet_box(LID_W - 2*SNAP_T, LID_D - 2*SNAP_T, LID_H, r=4);
                }
            // Snap bead (inner lip, 0.4mm interference at snap point)
            translate([SNAP_T, SNAP_T, -3])
                difference() {
                    fillet_box(LID_W - 2*SNAP_T, LID_D - 2*SNAP_T, SNAP_H, r=4);
                    translate([SNAP_T + 0.4, SNAP_T + 0.4, -0.1])
                        fillet_box(LID_W - 4*SNAP_T - 0.8, LID_D - 4*SNAP_T - 0.8, SNAP_H + 0.2, r=3);
                }
        }
        // Optional center fill port
        translate([LID_W/2, LID_D/2, -0.1])
            cylinder(d=PORT_D, h=5);
        // Vent slots under rim
        for (i = [0:3])
            rotate([0, 0, i*90])
                translate([LID_W/2 - 0.5, LID_D/4, -LID_H + 3])
                    cube([1, 10, 4]);
    }

    // Fill port plug (print separately, optional)
    // translate([LID_W/2, LID_D/2, 5]) port_plug(PORT_D);
}
