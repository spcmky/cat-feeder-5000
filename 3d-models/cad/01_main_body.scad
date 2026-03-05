// Cat Feeder 5000 — Part 01: Main Body / Base
// Open-front design: the front section (approach zone, gate, bowl) is OPEN —
// no side walls, no top. Only the rear section is an enclosed box for
// electronics, auger motor, and hopper mounting.
//
// Layout (front to back, Y axis):
//   Y < 0        Round halo (separate part, outside body)
//   Y = 0..100   OPEN front zone: floor + bowl shelf + gate rails only
//   Y = 100..240  ENCLOSED rear box: full walls + top, holds electronics/hopper
//
// Print: PETG, 0.25mm layers, 40% infill, no supports

include <params.scad>

// ── Approach opening ─────────────────────────────────────────────────────────
APPROACH_W = 130;           // Width of front approach (cat shoulder width)
APPROACH_H = 130;           // Height of front approach opening (on rear box face)
APPROACH_ARCH_R = 30;       // Top corner radius

// ── Gate position ────────────────────────────────────────────────────────────
GATE_Y = 40;                // Y position of gate plane

// ── Bowl recess ──────────────────────────────────────────────────────────────
BOWL_SHELF_D = 100;         // Depth where open front zone ends / rear box starts
BOWL_SHELF_H = 40;          // Height of bowl shelf

// ── Rear box ─────────────────────────────────────────────────────────────────
REAR_Y = BOWL_SHELF_D;      // Where the enclosed rear box starts
REAR_D = UNIT_D - REAR_Y;   // Depth of the rear box (140mm)

color(COL_BODY) main_body();

module main_body() {
    difference() {
        union() {
            // ── Floor / base plate ─────────────────────────────────────────
            // Full-depth floor that everything sits on
            fillet_box(UNIT_W, UNIT_D, FLOOR, r=4);

            // ── Bowl shelf ─────────────────────────────────────────────────
            // Low platform in the open front zone for the bowl to sit on
            fillet_box(UNIT_W, BOWL_SHELF_D, BOWL_SHELF_H, r=4);

            // ── Gate side rails ────────────────────────────────────────────
            // Two short vertical walls at the gate position to guide the gate flap.
            // Only as wide as needed for the gate track, not full side walls.
            rail_h = APPROACH_H;
            rail_w = 8;
            for (x = [(UNIT_W - APPROACH_W)/2 - rail_w, (UNIT_W + APPROACH_W)/2])
                translate([x, GATE_Y - 5, 0])
                    cube([rail_w, 10, rail_h]);

            // ── Enclosed rear box ──────────────────────────────────────────
            // Full walls and top — houses electronics, auger motor, wiring
            translate([0, REAR_Y, 0])
                fillet_box(UNIT_W, REAR_D, UNIT_H, r=4);
        }

        // ── Hollow out the rear box interior ───────────────────────────────
        translate([WALL, REAR_Y + WALL, FLOOR])
            fillet_box(UNIT_W - 2*WALL, REAR_D - 2*WALL, UNIT_H, r=2);

        // ── Hollow out the bowl shelf interior ─────────────────────────────
        translate([WALL, WALL, FLOOR])
            fillet_box(UNIT_W - 2*WALL, BOWL_SHELF_D - WALL, BOWL_SHELF_H, r=2);

        // ── Front face opening on rear box ─────────────────────────────────
        // Large opening in the front face of the rear box so the open front
        // zone connects to the interior
        translate([(UNIT_W - APPROACH_W)/2, REAR_Y - 1, FLOOR])
            cube([APPROACH_W, WALL + 2, APPROACH_H]);

        // ── Auger exit hole ────────────────────────────────────────────────
        translate([UNIT_W/2, BOWL_SHELF_D/2 + WALL, BOWL_SHELF_H - 1])
            cylinder(d=AUGER_TUBE_OD + 1, h=WALL + 2);

        // ── Auger tube channel ─────────────────────────────────────────────
        translate([UNIT_W/2, BOWL_SHELF_D + 20, UNIT_H - 30])
            rotate([AUGER_ANGLE, 0, 0])
                cylinder(d=AUGER_TUBE_OD + 1, h=UNIT_H);

        // ── Electronics bay (rear interior) ────────────────────────────────
        translate([UNIT_W/2 - 45, UNIT_D - 100, FLOOR])
            cube([90, 100 - WALL, 80]);

        // ── Rear cable pass-through ────────────────────────────────────────
        translate([UNIT_W/2, UNIT_D - WALL/2, 25])
            rotate([90, 0, 0])
                cylinder(d=15, h=WALL + 2);

        // ── Gate rail slots ────────────────────────────────────────────────
        for (x = [(UNIT_W - APPROACH_W)/2 + WALL,
                  (UNIT_W + APPROACH_W)/2 - WALL - GATE_T])
            translate([x, GATE_Y - GATE_T/2, FLOOR])
                cube([GATE_T + TOLERANCE, GATE_T + TOLERANCE, APPROACH_H]);

        // ── Halo floor mount holes ─────────────────────────────────────────
        halo_offset_x = (UNIT_W - 154) / 2;
        for (x_local = [12, 142])
            for (dy = [-10, 10])
                translate([halo_offset_x + x_local, dy, -0.1])
                    m3_insert(h=FLOOR + 0.2);

        // ── Halo cable pass-through ────────────────────────────────────────
        translate([halo_offset_x + 12, 0, -0.1])
            cylinder(d=8, h=FLOOR + 0.2);

        // ── Gate hinge mount holes ─────────────────────────────────────────
        for (x = [(UNIT_W - 120)/2 + 15, (UNIT_W + 120)/2 - 15])
            translate([x, GATE_Y, APPROACH_H - 5])
                rotate([-90, 0, 0]) m3_insert(h=8);

        // ── Hopper mount holes (top of rear box) ──────────────────────────
        for (x = [30, UNIT_W - 30]) for (y = [REAR_Y + 30, UNIT_D - 30])
            translate([x, y, UNIT_H - 6])
                m3_insert(h=6.2);
    }

    // ── Interior bosses ────────────────────────────────────────────────────────

    // Bowl bracket bosses (on bowl shelf, behind gate)
    for (x = [(UNIT_W - APPROACH_W)/2 + 10, (UNIT_W + APPROACH_W)/2 - 10])
        translate([x, BOWL_SHELF_D - 15, 0])
            boss(d=10, h=BOWL_SHELF_H);

    // Electronics tray bosses (rear interior floor)
    for (x = [UNIT_W/2 - 35, UNIT_W/2 + 35])
        translate([x, UNIT_D - 40, FLOOR])
            boss(d=10, h=10);

    // Gate servo bracket bosses (inside rear box, above approach opening)
    translate([UNIT_W/2, REAR_Y + 10, APPROACH_H + 10])
        boss(d=10, h=8);

    // ── Bottom feet pockets ────────────────────────────────────────────────────
    for (x = [15, UNIT_W - 15]) for (y = [15, UNIT_D - 15])
        difference() {
            translate([x - 8, y - 8, 0]) cube([16, 16, FLOOR]);
            translate([x, y, -0.1]) cylinder(d=10, h=FLOOR + 0.2);
        }
}
