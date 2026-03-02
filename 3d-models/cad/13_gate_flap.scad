// Cat Feeder 5000 — Part 13: Bowl Gate Flap (Swing-Up)
// Hinged at top, swings up into feeder body when open. Servo-actuated.
// CRITICAL: Swings UPWARD — cat's head/back cannot contact it.
// Print: PETG, 0.15mm layers, 40% infill, no supports. Print flat (face down).

include <params.scad>

color(COL_GATE) gate_flap();

module gate_flap() {
    GW = GATE_W;    // 118mm
    GH = GATE_H;    // 90mm
    GT = GATE_T;    // 3mm

    difference() {
        // Main flap body
        fillet_box(GW, GT, GH, r=2);

        // Hinge rod holes (×2, top edge, 3.2mm dia)
        for (x = [20, GW - 20])
            translate([x, -0.1, GH - 8])
                rotate([-90, 0, 0])
                    cylinder(d=GATE_ROD_D, h=GT + 0.2);

        // Servo linkage hole (top center, Ø3mm)
        translate([GW/2, -0.1, GH - 10])
            rotate([-90, 0, 0])
                cylinder(d=3, h=GT + 0.2);

        // Bottom edge chamfer (R5, cat-facing side — no sharp edge)
        translate([0, -0.1, 0])
            rotate([-90, 0, 0])
                difference() {
                    cube([GW, 6, GT + 0.2]);
                    translate([0, 0, 0]) fillet_box(GW, 6, GT + 0.2, r=5);
                }
    }
}
