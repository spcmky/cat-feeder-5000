// Cat Feeder 5000 — Part 09: Bowl (Open-Front Design)
// Whisker-friendly. NO front wall. Low 25mm side walls.
// Print: PETG, 0.15mm layers, 30% infill, no supports. Food-safe PETG, 3+ perimeters.

include <params.scad>

color(COL_FOOD) bowl();

module bowl() {
    BW = BOWL_FLOOR_W;
    BD = BOWL_FLOOR_D + BOWL_OVERHANG;  // Total depth including front overhang
    BFT = BOWL_FLOOR_T;
    BWT = BOWL_WALL_T;
    BSH = BOWL_SIDE_H;
    BBH = BOWL_BACK_H;
    R   = 10;           // Corner radius (internal, for easy cleaning)

    difference() {
        union() {
            // Floor
            translate([0, 0, 0])
                fillet_box(BW, BD, BFT, r=R);
            // Back wall (full height)
            translate([0, BOWL_OVERHANG, BFT])
                cube([BW, BWT, BBH]);
            // Left side wall (tapered: BSH at front, BBH at back)
            translate([0, 0, BFT])
                linear_extrude(height=1, scale=[1,1])
                hull() {
                    cube([BWT, BOWL_OVERHANG, BSH]);
                    translate([0, BOWL_OVERHANG, 0])
                        cube([BWT, BWT, BBH]);
                }
            // Right side wall (mirror)
            translate([BW - BWT, 0, BFT])
                hull() {
                    cube([BWT, BOWL_OVERHANG, BSH]);
                    translate([0, BOWL_OVERHANG, 0])
                        cube([BWT, BWT, BBH]);
                }
        }
        // Round off all internal corners with fillet
        // (subtract sharp edge from interior back corners)
        for (x=[BWT, BW - BWT - R*2])
            translate([x, BOWL_OVERHANG + BWT, BFT - 0.1])
                difference() {
                    cube([R, R, BBH + 0.2]);
                    cylinder(r=R, h=BBH + 0.2);
                }
        // Optional drain holes in floor corners
        for (x=[15, BW - 15]) for (y=[5, BD - 15])
            translate([x, y, -0.1])
                cylinder(d=3, h=BFT + 0.2);
    }

    // Rear mounting tabs (2× M3 insert bosses)
    for (x = [20, BW - 20])
        translate([x, BOWL_OVERHANG, 0])
            boss(d_outer=8, h=BFT + 6);
}
