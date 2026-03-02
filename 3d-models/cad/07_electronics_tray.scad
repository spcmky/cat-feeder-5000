// Cat Feeder 5000 — Part 07: Electronics Tray
// Snap-in tray holding Pi Zero 2W, Arduino Nano, and wiring.
// Print: PETG, 0.25mm layers, 30% infill, no supports

include <params.scad>

color(COL_BODY) electronics_tray();

module electronics_tray() {
    TW = 78; TD = 58; TH = 20;
    PI_W = 65; PI_D = 30; PI_H = 6;
    ARD_W = 45; ARD_D = 18; ARD_H = 8;
    SNAP_T = 2; SNAP_H = 4;

    difference() {
        union() {
            // Base tray
            fillet_box(TW, TD, TH, r=3);
            // Snap clips (2×, short sides center)
            for (x = [TW/2 - 5, TW/2 + 3])
                translate([x, -SNAP_T, TH - 1])
                    cube([SNAP_T, SNAP_T + 2, SNAP_H]);
        }
        // Hollow tray interior
        translate([WALL, WALL, FLOOR])
            fillet_box(TW - 2*WALL, TD - 2*WALL, TH, r=2);

        // Pi Zero 2W pocket (left side)
        translate([WALL + 2, WALL + 2, FLOOR])
            cube([PI_W, PI_D, PI_H]);
        // Pi mounting pegs recesses (4× M2.5 holes, 58×23mm bolt pattern)
        for (x=[WALL+3, WALL+3+58]) for (y=[WALL+3, WALL+3+23])
            translate([x, y, FLOOR - 0.1]) cylinder(d=2.7, h=4);

        // Arduino Nano pocket (right lower)
        translate([TW - WALL - ARD_W - 2, WALL + 2, FLOOR])
            cube([ARD_W, ARD_D, ARD_H]);

        // Wire channel slots (3mm × 1.5mm every 25mm along long sides)
        for (i=[0:3])
            translate([10 + i*18, -0.1, FLOOR + 2])
                cube([3, WALL + 0.2, 8]);

        // Ventilation holes above Pi (Ø3mm, 6×)
        for (x=[15,30,45]) for (y=[15,25])
            translate([x, y, TH - FLOOR - 0.1])
                cylinder(d=3, h=FLOOR + 0.2);
    }
}
