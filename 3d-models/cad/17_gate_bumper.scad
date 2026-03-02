// Cat Feeder 5000 — Part 17: TPU Gate Bumper
// Soft end-stop for gate flap at fully-open position. Prevents servo overrun.
// Print: TPU 95A, 0.2mm layers, 30% infill. Print SLOW (25mm/s), no retraction.

include <params.scad>

color(COL_TPU) gate_bumper();

module gate_bumper() {
    BL = 30; BW = 15; BH = 8;
    PEG_D = 4; PEG_H = 4; // Press-fit peg into body wall

    union() {
        // Main bumper body
        fillet_box(BL, BW, BH, r=2);
        // Press-fit mounting pegs (×2)
        for (x = [8, BL - 8])
            translate([x, BW/2, BH])
                cylinder(d=PEG_D, h=PEG_H);
    }
}
