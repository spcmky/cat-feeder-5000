// Cat Feeder 5000 — Part 06: Motor Mount
// Mounts auger drive motor (N20 or NEMA14 stepper) aligned to auger tube.
// Print: PETG, 0.25mm layers, 40% infill, no supports

include <params.scad>

// Set MOTOR_TYPE to "N20" or "NEMA14"
MOTOR_TYPE = "N20";

color(COL_BODY) motor_mount();

module motor_mount() {
    MW = 30; MD = 30; MH = 20;
    SHAFT_H = 10; // Height of shaft bore from base

    difference() {
        fillet_box(MW, MD, MH, r=3);

        if (MOTOR_TYPE == "N20") {
            // N20 motor pocket: 12mm dia × 25mm deep (round)
            translate([MW/2, MD/2, MH - 25])
                cylinder(d=13, h=26);
            // Gearbox pocket (rectangular, on top of motor)
            translate([MW/2 - 6.5, MD/2 - 5.5, MH - 10])
                cube([13, 11, 11]);
            // Shaft bore (through bottom)
            translate([MW/2, MD/2, -0.1])
                cylinder(d=6, h=SHAFT_H + 1);
        } else {
            // NEMA14 pocket: 28mm sq
            translate([MW/2 - 14, MD/2 - 14, MH - 20])
                cube([28, 28, 21]);
            // NEMA14 shaft bore
            translate([MW/2, MD/2, -0.1])
                cylinder(d=8, h=SHAFT_H + 1);
            // NEMA14 mount holes (M3, 26mm bolt circle)
            for (x=[-13,13]) for (y=[-13,13])
                translate([MW/2+x, MD/2+y, -0.1])
                    m3_clear(h=MH+0.2);
        }

        // Body mount holes (M3 clearance, 4 corners)
        for (x=[6, MW-6]) for (y=[6, MD-6])
            translate([x, y, -0.1]) m3_clear(h=6);
    }
}
