// Cat Feeder 5000 — Part 15: Antenna Arch (Round Halo, Tilted)
//
// A thin-walled semicircular arch the cat walks through. Tilted
// forward ~18° so the coil peak sits directly over the cat's
// shoulders when its head is down eating from the bowl.
//
// SIDE VIEW (tilted):
//
//            ╭─╮   ← arch peak (coil over shoulders)
//           │   │
//          │     │     16mm OD tube, 2mm wall
//         │       │    12mm coil channel inside
//        │    18°  │
//       ┴─┬        │── body front Y=0
//      feet        │
//       ──┴────────┘
//
// FRONT VIEW:
//
//          ╭──────────╮
//         ╱  130 clear  ╲     ← thin round arch
//        │               │
//        │               │
//        ┴─┬─┘         └─┬─┴
//       foot              foot
//
// The entire ring (legs + arch) is tilted as one rigid piece.
// Feet are flattened at the base so it sits flat on the floor
// despite the tilt. Cable exits through the left foot.
//
// Print: PETG, 0.2mm layers, 25% infill, supports for arch overhang.

include <params.scad>

// ── Halo geometry ───────────────────────────────────────────────────────────
HALO_CLEAR_W   = 130;          // Inner clear width between legs
HALO_TUBE_OD   = 16;           // Tube outer diameter (wide axis)
HALO_TUBE_WALL = 2;            // Tube wall thickness
HALO_TUBE_ID   = HALO_TUBE_OD - 2*HALO_TUBE_WALL;  // 12mm coil channel
HALO_FLAT      = 0.55;         // Oval ratio: height/width (flat top+bottom)

// Leg geometry (pre-tilt, in local vertical frame)
HALO_LEG_H     = 77;           // Leg height before tilt

// Arch geometry
HALO_ARCH_R    = HALO_CLEAR_W / 2;  // 65mm, center-to-center of tube

// Forward tilt
HALO_TILT      = 18;           // Degrees forward (top leans away from bowl)

// Total width
HALO_TOTAL_W   = HALO_CLEAR_W + HALO_TUBE_OD;  // 146mm

// Mounting feet (flattened base pads, independent of tilt)
FOOT_W         = 30;           // Foot width (X)
FOOT_D         = 30;           // Foot depth (Y)
FOOT_H         = 5;            // Foot thickness (Z)

// Cable exit
CABLE_CH_D     = 6;            // Cable channel diameter

color(COL_RFID) antenna_arch();

module antenna_arch() {
    // The arch is built upright in local coords, then tilted as a unit.
    // Feet are added AFTER the tilt so they sit flat on the floor.

    // ── Tilted arch (legs + semicircle) ─────────────────────────────────
    // Tilt around X axis at Z=0: top of arch leans in -Y direction
    rotate([-HALO_TILT, 0, 0])
        difference() {
            _halo_solid();
            _halo_hollow();
        }

    // ── Mounting feet (flat on floor, not tilted) ───────────────────────
    // Left foot — centered under left leg base
    translate([HALO_TUBE_OD/2 - FOOT_W/2, -FOOT_D + HALO_TUBE_OD/2, 0])
        _foot();

    // Right foot — centered under right leg base
    translate([HALO_TOTAL_W - HALO_TUBE_OD/2 - FOOT_W/2, -FOOT_D + HALO_TUBE_OD/2, 0])
        _foot();
}

// Solid outer shape of the halo (legs + arch)
module _halo_solid() {
    // Left leg (flat oval: wide in X, thin in Y)
    translate([HALO_TUBE_OD/2, 0, 0])
        scale([HALO_FLAT, 1, 1])
            cylinder(d=HALO_TUBE_OD, h=HALO_LEG_H);

    // Right leg
    translate([HALO_TOTAL_W - HALO_TUBE_OD/2, 0, 0])
        scale([HALO_FLAT, 1, 1])
            cylinder(d=HALO_TUBE_OD, h=HALO_LEG_H);

    // Semicircular arch connecting leg tops (arches UPWARD over the cat)
    // Cross-section: scale Y to flatten (Y becomes front-back after rotate)
    translate([HALO_TOTAL_W/2, 0, HALO_LEG_H])
        rotate([90, 0, 0])
            rotate_extrude(angle=180, $fn=96)
                translate([HALO_ARCH_R, 0])
                    scale([HALO_FLAT, 1])
                        circle(d=HALO_TUBE_OD);
}

// Hollow interior (coil channel through entire path)
module _halo_hollow() {
    // Left leg channel (matching oval)
    translate([HALO_TUBE_OD/2, 0, -0.1])
        scale([HALO_FLAT, 1, 1])
            cylinder(d=HALO_TUBE_ID, h=HALO_LEG_H + 0.2);

    // Right leg channel
    translate([HALO_TOTAL_W - HALO_TUBE_OD/2, 0, -0.1])
        scale([HALO_FLAT, 1, 1])
            cylinder(d=HALO_TUBE_ID, h=HALO_LEG_H + 0.2);

    // Arch channel (matching oval cross-section)
    translate([HALO_TOTAL_W/2, 0, HALO_LEG_H])
        rotate([90, 0, 0])
            rotate_extrude(angle=180, $fn=96)
                translate([HALO_ARCH_R, 0])
                    scale([HALO_FLAT, 1])
                        circle(d=HALO_TUBE_ID);

    // Cable exit through left leg base
    translate([HALO_TUBE_OD/2, 0, -0.1])
        scale([HALO_FLAT, 1, 1])
            cylinder(d=CABLE_CH_D, h=1);
}

// Flat mounting foot with bolt holes
module _foot() {
    difference() {
        fillet_box(FOOT_W, FOOT_D, FOOT_H, r=3);

        // Two M3 bolt holes per foot
        for (dx = [FOOT_W/2 - 8, FOOT_W/2 + 8])
            translate([dx, FOOT_D/2, -0.1])
                m3_clear(h=FOOT_H + 0.2);
    }
}
