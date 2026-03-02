// Cat Feeder 5000 — Part 14: Gate Top Hinge Mount
// Fixed to top of bowl opening. Holds hinge rod for swing-up gate flap.
// Print: PETG, 0.2mm layers, 40% infill, no supports

include <params.scad>

color(COL_GATE) gate_hinge_mount();

module gate_hinge_mount() {
    HW = 120; HH = 20; HD = 15;
    ROD_H = 8;  // Rod center height from top of mount (measured from top face)

    difference() {
        fillet_box(HW, HD, HH, r=2);
        // Hinge rod bores (×2, matching gate flap rod holes at x=20 and x=100)
        for (x = [20, HW - 20])
            translate([x, -0.1, HH - ROD_H])
                rotate([-90, 0, 0])
                    cylinder(d=GATE_ROD_D, h=HD + 0.2);
        // Body attachment holes (M3 clearance, ×4 evenly spaced)
        for (x = [15, 45, 75, 105])
            translate([x, HD/2, -0.1])
                m3_clear(h=HH + 0.2);
    }
}
