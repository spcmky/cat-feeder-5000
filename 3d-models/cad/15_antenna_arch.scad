// Cat Feeder 5000 — Part 15: Antenna Arch Housing
// Overhead arch holding flat RFID coil. Coil channel is open-top (no bridging).
// Antenna reads cat's implanted FDX-B chip as cat's shoulders pass below.
// Print: PETG, 0.2mm layers, 25% infill, no supports. Print UPRIGHT.

include <params.scad>

color(COL_RFID) antenna_arch();

module antenna_arch() {
    SPAN   = ARCH_SPAN;    // 160mm
    AH     = ARCH_H;       // 70mm height of arch above base
    AD     = ARCH_D;       // 40mm depth
    WT     = THIN_WALL;    // 2.5mm wall
    CCW    = COIL_CH_W;    // 16mm coil channel width
    CCD    = COIL_CH_D;    // 5mm coil channel depth
    CABLE_D = 5;           // Antenna cable channel diameter

    difference() {
        union() {
            // Left leg
            translate([0, 0, 0])
                fillet_box(AD, AD, AH + AD, r=4);
            // Right leg
            translate([SPAN - AD, 0, 0])
                fillet_box(AD, AD, AH + AD, r=4);
            // Top arch bridge
            translate([0, 0, AH])
                fillet_box(SPAN, AD, AD, r=4);
        }

        // Hollow legs
        translate([WT, WT, -0.1])
            cube([AD - 2*WT, AD - 2*WT, AH + AD + 0.2]);
        translate([SPAN - AD + WT, WT, -0.1])
            cube([AD - 2*WT, AD - 2*WT, AH + AD + 0.2]);

        // Hollow bridge interior
        translate([AD, WT, AH + WT])
            cube([SPAN - 2*AD, AD - 2*WT, AD]);

        // Coil channel (open top — no perimeters over this in slicer)
        // Centered horizontally and front-to-back in top bridge
        translate([SPAN/2 - CCW/2, (AD - CCW)/2, AH + AD - CCD])
            cube([CCW, CCW, CCD + 0.1]);

        // Antenna cable channel through left leg wall
        translate([-0.1, AD/2, AH/2])
            rotate([0, 90, 0])
                cylinder(d=CABLE_D, h=WT + 0.2);

        // Body mount holes — 2× M3 insert per leg base
        for (x = [AD/2 - 8, AD/2 + 8])
            translate([x, AD/2, -0.1]) m3_clear(h=8);
        for (x = [SPAN - AD/2 - 8, SPAN - AD/2 + 8])
            translate([x, AD/2, -0.1]) m3_clear(h=8);
    }
}
