// Cat Feeder 5000 — Part 01: Main Body / Base
// Structural core. All other parts mount into this.
// The FRONT face (Y=0) is the cat approach side — it has a large
// open arch at ground level where the cat walks in to reach the bowl.
// The REAR (Y=UNIT_D) holds electronics and cable pass-throughs.
// Print: PETG, 0.25mm layers, 40% infill, no supports

include <params.scad>

// ── Approach opening ─────────────────────────────────────────────────────────
// The front arch opening the cat walks through. Must be wide enough for
// cat shoulders (~140mm) and tall enough so the cat doesn't hunch (~130mm).
APPROACH_W = 130;           // Width of front approach arch (cat shoulder width)
APPROACH_H = 130;           // Height of front approach arch
APPROACH_ARCH_R = 30;       // Top corner radius (cosmetic arch shape)

// ── Bowl recess ──────────────────────────────────────────────────────────────
// The bowl sits in a lowered shelf at the front of the body, at floor level.
BOWL_SHELF_D = 100;         // How deep the bowl shelf extends into the body
BOWL_SHELF_H = 40;          // Height of bowl shelf above base (bowl rim height)

color(COL_BODY) main_body();

module main_body() {
    difference() {
        // Outer shell
        fillet_box(UNIT_W, UNIT_D, UNIT_H, r=4);

        // Hollow interior (above bowl shelf height)
        translate([WALL, WALL, BOWL_SHELF_H])
            fillet_box(UNIT_W - 2*WALL, UNIT_D - 2*WALL, UNIT_H, r=2);

        // ── Front approach opening ───────────────────────────────────────
        // Large arch at the front face, starting at floor level.
        // The cat walks into this to reach the bowl.
        translate([(UNIT_W - APPROACH_W)/2, -1, 0])
            cube([APPROACH_W, WALL + 2, APPROACH_H]);
        // Arch top corners (round the top of the opening)
        // (cosmetic — softens the rectangular opening into an arch shape)

        // ── Bowl shelf cavity ────────────────────────────────────────────
        // Recessed area inside the front of the body where the bowl sits.
        // Open at the front (continuous with the approach opening).
        translate([(UNIT_W - APPROACH_W)/2, -1, 0])
            cube([APPROACH_W, BOWL_SHELF_D + 1, BOWL_SHELF_H]);

        // ── Auger exit hole ──────────────────────────────────────────────
        // Where the auger tube drops food down into the bowl area.
        // Centered left-right, positioned above the bowl shelf.
        translate([UNIT_W/2, BOWL_SHELF_D/2 + WALL, BOWL_SHELF_H - 1])
            cylinder(d=AUGER_TUBE_OD + 1, h=WALL + 2);

        // ── Auger tube channel ───────────────────────────────────────────
        // Angled channel from hopper area down to bowl shelf.
        translate([UNIT_W/2, BOWL_SHELF_D + 20, UNIT_H - 30])
            rotate([AUGER_ANGLE, 0, 0])
                cylinder(d=AUGER_TUBE_OD + 1, h=UNIT_H);

        // ── Electronics bay (rear) ───────────────────────────────────────
        // Accessible from rear. Holds Pi, Arduino, wiring.
        translate([UNIT_W/2 - 45, UNIT_D - 100, FLOOR])
            cube([90, 100 - WALL, 80]);

        // ── Rear cable pass-through ──────────────────────────────────────
        translate([UNIT_W/2, UNIT_D - WALL/2, 25])
            rotate([90, 0, 0])
                cylinder(d=15, h=WALL + 2);

        // ── Antenna arch mount holes ─────────────────────────────────────
        // Two M3 inserts on each side of the front face, near the top
        // of the approach opening. The arch legs bolt to these.
        for (x = [(UNIT_W - APPROACH_W)/2 - 12,
                  (UNIT_W + APPROACH_W)/2 + 4]) {
            translate([x, -0.1, APPROACH_H - 20])
                rotate([-90, 0, 0]) m3_insert(h=WALL + 0.2);
            translate([x, -0.1, APPROACH_H - 40])
                rotate([-90, 0, 0]) m3_insert(h=WALL + 0.2);
        }

        // ── Gate hinge mount holes ───────────────────────────────────────
        // M3 inserts at top of the approach opening, front face interior.
        for (x = [(UNIT_W - 120)/2 + 15, (UNIT_W + 120)/2 - 15])
            translate([x, WALL - 0.1, APPROACH_H - 5])
                rotate([-90, 0, 0]) m3_insert(h=8);

        // ── Hopper mount holes (top rim) ─────────────────────────────────
        for (x = [30, UNIT_W - 30]) for (y = [BOWL_SHELF_D + 30, UNIT_D - 30])
            translate([x, y, UNIT_H - 6])
                m3_insert(h=6.2);
    }

    // ── Interior bosses ──────────────────────────────────────────────────────

    // Bowl bracket bosses (inside front, on bowl shelf)
    for (x = [(UNIT_W - APPROACH_W)/2 + 10, (UNIT_W + APPROACH_W)/2 - 10])
        translate([x, BOWL_SHELF_D - 15, 0])
            boss(d=10, h=BOWL_SHELF_H);

    // Electronics tray bosses (rear interior floor)
    for (x = [UNIT_W/2 - 35, UNIT_W/2 + 35])
        translate([x, UNIT_D - 40, FLOOR])
            boss(d=10, h=10);

    // Gate servo bracket bosses (interior, above approach opening)
    translate([UNIT_W/2, WALL + 10, APPROACH_H + 10])
        boss(d=10, h=8);

    // ── Bottom feet pockets ──────────────────────────────────────────────────
    for (x = [15, UNIT_W - 15]) for (y = [15, UNIT_D - 15])
        difference() {
            translate([x - 8, y - 8, 0]) cube([16, 16, FLOOR]);
            translate([x, y, -0.1]) cylinder(d=10, h=FLOOR + 0.2);
        }
}
