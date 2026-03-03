// Cat Feeder 5000 — Part 15: Antenna Arch Housing (Front-Mounted Halo)
//
// This is the RFID "doorway" the cat walks through to reach the bowl.
// It bolts to the FRONT FACE of the main body, straddling the approach
// opening. The two legs sit on either side of the opening, and the bridge
// spans overhead. The flat coil sits in a channel in the bridge,
// positioned directly above the cat's shoulders as it eats.
//
// Viewed from front:
//
//     ┌──────────────── bridge (coil inside) ────────────────┐
//     │                                                       │
//     │   leg                                           leg   │
//     │   │                                             │     │
//     │   │         ← cat walks through here →          │     │
//     │   │                                             │     │
//     └───┘                                             └─────┘
//    ─────── floor ──────────────────────────────────────────────
//
// The arch extends FORWARD from the body face (into Y-negative space)
// so the cat passes under it before reaching the bowl inside.
//
// Print: PETG, 0.2mm layers, 25% infill, no supports. Print UPRIGHT.

include <params.scad>

// ── Arch geometry ─────────────────────────────────────────────────────────────
// The arch straddles the approach opening (APPROACH_W = 130 in main body).
// Legs sit outside the opening on either side.
LEG_W       = 15;           // Leg wall thickness (left-right)
LEG_D       = 35;           // Leg depth (extends forward from body face)
LEG_H       = 140;          // Leg height (floor to underside of bridge)
BRIDGE_H    = 30;           // Bridge height (thickness of overhead section)
BRIDGE_SPAN = 160;          // Full span including legs (= UNIT_W)
BRIDGE_D    = LEG_D;        // Bridge depth matches leg depth
CABLE_D     = 5;            // Cable routing channel

color(COL_RFID) antenna_arch();

module antenna_arch() {
    WT = THIN_WALL;
    CCW = COIL_CH_W;
    CCD = COIL_CH_D;
    INNER_SPAN = BRIDGE_SPAN - 2*LEG_W;  // Clear span cat walks through

    difference() {
        union() {
            // ── Left leg ─────────────────────────────────────────────────
            translate([0, 0, 0])
                fillet_box(LEG_W, LEG_D, LEG_H + BRIDGE_H, r=3);

            // ── Right leg ────────────────────────────────────────────────
            translate([BRIDGE_SPAN - LEG_W, 0, 0])
                fillet_box(LEG_W, LEG_D, LEG_H + BRIDGE_H, r=3);

            // ── Bridge (overhead, connects legs) ─────────────────────────
            translate([0, 0, LEG_H])
                fillet_box(BRIDGE_SPAN, BRIDGE_D, BRIDGE_H, r=3);
        }

        // ── Hollow legs (weight reduction, cable routing) ────────────────
        translate([WT, WT, -0.1])
            cube([LEG_W - 2*WT, LEG_D - 2*WT, LEG_H + 0.2]);
        translate([BRIDGE_SPAN - LEG_W + WT, WT, -0.1])
            cube([LEG_W - 2*WT, LEG_D - 2*WT, LEG_H + 0.2]);

        // ── Hollow bridge interior ───────────────────────────────────────
        translate([LEG_W, WT, LEG_H + WT])
            cube([INNER_SPAN, BRIDGE_D - 2*WT, BRIDGE_H - 2*WT]);

        // ── Coil channel (recessed from top of bridge) ───────────────────
        // The flat spiral coil sits in this channel. Open top for
        // coil insertion, then epoxied in place.
        // Centered horizontally, centered front-to-back in bridge.
        translate([BRIDGE_SPAN/2 - CCW/2, (BRIDGE_D - CCW)/2,
                   LEG_H + BRIDGE_H - CCD])
            cube([CCW, CCW, CCD + 0.1]);

        // ── Cable channel (through left leg, from bridge to base) ────────
        translate([-0.1, LEG_D/2, LEG_H/2])
            rotate([0, 90, 0])
                cylinder(d=CABLE_D, h=LEG_W + 0.2);
        // Vertical cable path inside left leg
        translate([LEG_W/2, LEG_D/2, 0])
            cylinder(d=CABLE_D, h=LEG_H + BRIDGE_H);

        // ── Body mount bolt holes (through leg backs, into body face) ────
        // 2 bolts per leg, through the rear face (Y = LEG_D side).
        // These go into M3 inserts in the main body front face.
        for (z = [LEG_H - 30, LEG_H - 50])
            translate([LEG_W/2, LEG_D - 0.1, z])
                rotate([-90, 0, 0]) m3_clear(h=5);
        for (z = [LEG_H - 30, LEG_H - 50])
            translate([BRIDGE_SPAN - LEG_W/2, LEG_D - 0.1, z])
                rotate([-90, 0, 0]) m3_clear(h=5);
    }
}
