// Cat Feeder 5000 — Part 15: Antenna Arch (Round Halo)
//
// A semicircular arch the cat walks through — the RFID coil follows
// the round shape, creating an ideal field pattern for reading the
// implanted chip between the cat's shoulders.
//
// Front view:
//
//          ╭───────────────╮        ← round arch (coil inside tube)
//         ╱                 ╲
//        │                   │
//        │    CAT WALKS HERE  │     ← 130mm clear width
//        │                   │
//        ┴─┬─┘             └─┬─┴   ← mounting feet (bolt to floor)
//
// The halo stands at the front face of the body. Its back surface
// is flush with Y=0 (body front face). The gate is further INSIDE
// the body (~40mm deep) — well behind the halo reading zone.
//
// The coil channel runs through the entire arch (both legs and the
// semicircular top). Cable exits through the left foot.
//
// Print: PETG, 0.2mm layers, 25% infill, supports for arch overhang.
// Print upright (feet on bed) — the arch overhang needs support.

include <params.scad>

// ── Halo geometry ───────────────────────────────────────────────────────────
HALO_CLEAR_W  = 130;           // Inner clear width between legs (for cat)
HALO_TUBE_OD  = 24;            // Outer diameter of the tube cross-section
HALO_TUBE_WALL = 4;            // Tube wall thickness
HALO_TUBE_ID  = HALO_TUBE_OD - 2*HALO_TUBE_WALL;  // 16mm coil channel

// Leg geometry
HALO_LEG_H    = 77;            // Straight leg height (floor to arch start)

// Arch geometry (semicircular, connects leg tops)
// Radius measured center-of-arch to center-of-tube-cross-section.
// This equals half the distance between leg tube centers.
HALO_ARCH_R   = HALO_CLEAR_W / 2;  // 65mm

// Total width = HALO_CLEAR_W + HALO_TUBE_OD = 154mm (fits inside UNIT_W=160)
HALO_TOTAL_W  = HALO_CLEAR_W + HALO_TUBE_OD;

// Mounting feet
FOOT_W        = 30;            // Foot width (X)
FOOT_D        = 35;            // Foot depth (Y, extends forward from body face)
FOOT_H        = 5;             // Foot thickness (Z)

// Cable exit
CABLE_CH_D    = 6;             // Cable channel diameter

color(COL_RFID) antenna_arch();

module antenna_arch() {
    difference() {
        union() {
            // ── Left leg (vertical tube) ─────────────────────────────────
            translate([HALO_TUBE_OD/2, 0, 0])
                cylinder(d=HALO_TUBE_OD, h=HALO_LEG_H);

            // ── Right leg (vertical tube) ────────────────────────────────
            translate([HALO_TOTAL_W - HALO_TUBE_OD/2, 0, 0])
                cylinder(d=HALO_TUBE_OD, h=HALO_LEG_H);

            // ── Semicircular arch (top half, connecting leg tops) ────────
            // rotate_extrude makes a half-torus in XY plane.
            // rotate([-90,0,0]) stands it up in XZ plane (arching upward).
            // Center at midpoint between legs, at Z = LEG_H.
            translate([HALO_TOTAL_W/2, 0, HALO_LEG_H])
                rotate([-90, 0, 0])
                    rotate_extrude(angle=180, $fn=96)
                        translate([HALO_ARCH_R, 0])
                            circle(d=HALO_TUBE_OD);

            // ── Left mounting foot ──────────────────────────────────────
            translate([HALO_TUBE_OD/2 - FOOT_W/2, -FOOT_D/2, 0])
                fillet_box(FOOT_W, FOOT_D, FOOT_H, r=3);

            // ── Right mounting foot ─────────────────────────────────────
            translate([HALO_TOTAL_W - HALO_TUBE_OD/2 - FOOT_W/2, -FOOT_D/2, 0])
                fillet_box(FOOT_W, FOOT_D, FOOT_H, r=3);
        }

        // ── Hollow left leg (coil channel) ──────────────────────────────
        translate([HALO_TUBE_OD/2, 0, -0.1])
            cylinder(d=HALO_TUBE_ID, h=HALO_LEG_H + 0.2);

        // ── Hollow right leg (coil channel) ─────────────────────────────
        translate([HALO_TOTAL_W - HALO_TUBE_OD/2, 0, -0.1])
            cylinder(d=HALO_TUBE_ID, h=HALO_LEG_H + 0.2);

        // ── Hollow arch (coil channel through semicircle) ───────────────
        translate([HALO_TOTAL_W/2, 0, HALO_LEG_H])
            rotate([-90, 0, 0])
                rotate_extrude(angle=180, $fn=96)
                    translate([HALO_ARCH_R, 0])
                        circle(d=HALO_TUBE_ID);

        // ── Cable exit (through left foot, out the bottom) ──────────────
        translate([HALO_TUBE_OD/2, 0, -0.1])
            cylinder(d=CABLE_CH_D, h=FOOT_H + 0.2);

        // ── Mounting bolt holes (vertical, through each foot) ───────────
        // Two M3 bolts per foot, going into inserts in the body floor.
        for (x = [HALO_TUBE_OD/2, HALO_TOTAL_W - HALO_TUBE_OD/2])
            for (dy = [-10, 10])
                translate([x, dy, -0.1])
                    m3_clear(h=FOOT_H + 0.2);
    }
}
