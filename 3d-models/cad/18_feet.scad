// Cat Feeder 5000 — Part 18: Non-Slip Feet
// Press-fit into base pockets. Print ×4 per unit (×8 total for 2 feeders).
// Print: TPU 95A, 0.3mm layers, 15% infill. Print SLOW (25mm/s).

include <params.scad>

color(COL_TPU) foot();

module foot() {
    STUD_D = 9.8;    // 0.2mm interference with 10mm pocket
    STUD_H = 6;
    PAD_D  = 16;
    PAD_H  = 4;

    union() {
        // Press-fit stud (goes into base pocket)
        cylinder(d=STUD_D, h=STUD_H);
        // Pad base (contacts floor)
        translate([0, 0, -PAD_H])
            cylinder(d=PAD_D, h=PAD_H);
    }
}

// Print all 4 feet in one go
for (i = [0:3])
    translate([i * 20, 0, 0])
        foot();
