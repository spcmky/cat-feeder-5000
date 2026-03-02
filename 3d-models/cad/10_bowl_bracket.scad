// Cat Feeder 5000 — Part 10: Bowl Mounting Bracket
// Attaches bowl to front of main body at correct height. 2° forward tilt.
// Print: PETG, 0.25mm layers, 40% infill, no supports

include <params.scad>

color(COL_BODY) bowl_bracket();

module bowl_bracket() {
    BRW = 110; BRD = 30; BRH = 20;
    TILT = 2; // degrees downward-front

    difference() {
        rotate([-TILT, 0, 0])
            fillet_box(BRW, BRD, BRH, r=3);
        // Bowl attach holes (M3 clearance, 2×, 90mm apart)
        translate([10, BRD/2, -0.1])     m3_clear(h=BRH + 0.2);
        translate([100, BRD/2, -0.1])    m3_clear(h=BRH + 0.2);
        // Body attach holes (M3 clearance, 4×, countersunk)
        for (x=[15, 45, 65, 95])
            translate([x, BRD/2, BRH - 3])
                cylinder(d1=6.5, d2=M3_CLEAR, h=3.5);
        translate([15, BRD/2, -0.1])    m3_clear(h=BRH);
        translate([95, BRD/2, -0.1])    m3_clear(h=BRH);
    }
}
