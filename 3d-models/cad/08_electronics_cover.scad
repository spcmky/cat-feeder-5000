// Cat Feeder 5000 — Part 08: Electronics Cover
// Ventilated removable cover over electronics bay.
// Print: PETG, 0.2mm layers, 20% infill, no supports

include <params.scad>

color(COL_BODY) electronics_cover();

module electronics_cover() {
    CW = 84; CD = 64; CH = 5;

    difference() {
        fillet_box(CW, CD, CH, r=4);
        // Vent slots (2mm × 15mm, 3mm spacing)
        for (row=[0:1]) for (col=[0:9])
            translate([8 + col*7, 12 + row*22, -0.1])
                cube([2, 15, CH + 0.2]);
        // Retention screw holes (M3 clearance, 2× center sides)
        translate([CW/2, 5,  -0.1]) m3_clear(h=CH + 0.2);
        translate([CW/2, CD-5, -0.1]) m3_clear(h=CH + 0.2);
    }
}
