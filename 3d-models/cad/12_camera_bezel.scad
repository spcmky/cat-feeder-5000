// Cat Feeder 5000 — Part 12: Camera Cover / Bezel
// Cosmetic trim and lens protection.
// Print: PETG, 0.2mm layers, 20% infill, no supports

include <params.scad>

color(COL_BODY) camera_bezel();

module camera_bezel() {
    BW = 30; BD = 30; BH = 8;

    difference() {
        fillet_box(BW, BD, BH, r=3);
        // Lens opening (Ø10mm)
        translate([BW/2, BD/2, -0.1])
            cylinder(d=10, h=BH + 0.2);
        // Snap clip recesses (4× corners)
        for (x=[3, BW-5]) for (y=[3, BD-5])
            translate([x, y, -0.1])
                cube([2, 2, 3]);
    }
}
