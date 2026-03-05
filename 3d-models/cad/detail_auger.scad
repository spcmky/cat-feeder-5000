// Cat Feeder 5000 — Detail: Auger System
// Motor at BOTTOM, hopper open on top. Food path: hopper → tube → side exit port.
// Default view: cutaway (front half sliced) so internals are visible.
// Optional: -D 'show_full=1' to also show transparent version alongside.
//
// Render: openscad -o detail.png detail_auger.scad
// Camera: --camera=0,0,50,55,0,0,350

include <params.scad>
use <02_hopper.scad>
use <04_auger_tube.scad>
use <05_auger_screw.scad>
use <06_motor_mount.scad>

$fn = 64;

// ── Animation ───────────────────────────────────────────────────────────────
// anim_t drives screw rotation for CLI: -D 'anim_t=0.5'
anim_t = is_undef(anim_t) ? $t : anim_t;
screw_angle = -anim_t * 360;  // Clockwise (from above) to push food down

// ── Mode flags ──────────────────────────────────────────────────────────────
show_full = is_undef(show_full) ? 0 : show_full;

// ══════════════════════════════════════════════════════════════════════════════
// CUTAWAY VIEW — front half sliced off to reveal internals
// ══════════════════════════════════════════════════════════════════════════════

// Slice the housing parts (hopper, tube, motor mount) but NOT the screw/motor
difference() {
    union() {
        // Hopper — sits directly on tube flange, open path into bore
        translate([-65, -65, AUGER_TUBE_L])
            color(COL_FOOD) hopper();

        // Auger tube
        color(COL_FOOD) auger_tube();

        // Motor mount — at BOTTOM of tube, extending downward
        translate([-15, -15, -20])
            color(COL_BODY) motor_mount();
    }

    // Slice off front half (Y < 0)
    translate([-200, -200, -50])
        cube([400, 200, 400]);
}

// ── Auger screw (uncut, fully visible inside the cutaway) ─────────────────
// Screw fills the tube bore, flights rub against tube walls
translate([0, 0, 5])
    rotate([0, 0, screw_angle])
        color([0.85, 0.65, 0.2]) auger_screw();

// ── N20 Gearmotor — at BOTTOM ────────────────────────────────────────────
// Motor sits in mount pocket below the tube.
// Shaft goes UP into auger screw coupler from below.
// Set screw in coupler locks shaft to screw.
translate([0, 0, 0]) {
    // Motor shaft (silver, goes UP into coupler bore at bottom of screw)
    color([0.75, 0.75, 0.78])
        translate([0, 0, -15])
            cylinder(d=5, h=20);

    // Shaft-coupler overlap zone (red highlight, inside bottom of tube)
    color([1, 0.3, 0.3, 0.5])
        translate([0, 0, -2])
            cylinder(d=8, h=10);

    // Set screw position indicator (on the side, locks shaft to screw)
    translate([10, 0, 3])
        color([0.5, 0.5, 0.5])
            rotate([0, 90, 0]) cylinder(d=3, h=5);

    // Motor can (dark metal, below mount)
    translate([0, 0, -40])
        color([0.25, 0.25, 0.3]) {
            cylinder(d=12, h=26);
            // Motor end cap
            translate([0, 0, -2])
                cylinder(d=12, h=2);
        }

    // Gearbox (between motor can and mount)
    translate([-6, -5, -14])
        color([0.35, 0.35, 0.4])
            cube([12, 10, 10]);

    // Wires (red + black, coming off bottom of motor)
    translate([-2, 0, -62])
        color([0.9, 0.1, 0.1]) cylinder(d=1.5, h=20);
    translate([2, 0, -62])
        color([0.15, 0.15, 0.15]) cylinder(d=1.5, h=20);
}

// ── Exit port indicator (where food drops out the side) ───────────────────
translate([0, -AUGER_TUBE_OD/2 - 2, 10])
    rotate([90, 0, 0])
        color([1, 0.4, 0.2, 0.6]) cylinder(d=20, h=3);

// ── Flange bolts (at tube-hopper joint) ───────────────────────────────────
for (a = [0, 120, 240])
    rotate([0, 0, a])
        translate([50/2 - 8, 0, AUGER_TUBE_L - 5])
            color([0.5, 0.5, 0.5]) cylinder(d=3, h=8);

// ══════════════════════════════════════════════════════════════════════════════
// FULL TRANSPARENT VERSION — shown alongside cutaway
// Enable with: -D 'show_full=1'
// ══════════════════════════════════════════════════════════════════════════════
if (show_full == 1) {
    translate([-130, 0, 0]) {
        // Hopper (transparent)
        translate([-65, -65, AUGER_TUBE_L])
            color(COL_FOOD, 0.15) hopper();

        // Auger tube (transparent)
        color(COL_FOOD, 0.15) auger_tube();

        // Motor mount at bottom (transparent)
        translate([-15, -15, -20])
            color(COL_BODY, 0.15) motor_mount();

        // Screw (solid)
        translate([0, 0, 5])
            rotate([0, 0, screw_angle])
                color([0.85, 0.65, 0.2]) auger_screw();

        // Motor at bottom
        translate([0, 0, 0]) {
            color([0.75, 0.75, 0.78])
                translate([0, 0, -15])
                    cylinder(d=5, h=20);
            color([1, 0.3, 0.3, 0.5])
                translate([0, 0, -2])
                    cylinder(d=8, h=10);
            translate([0, 0, -40])
                color([0.25, 0.25, 0.3]) {
                    cylinder(d=12, h=26);
                    translate([0, 0, -2])
                        cylinder(d=12, h=2);
                }
            translate([-6, -5, -14])
                color([0.35, 0.35, 0.4])
                    cube([12, 10, 10]);
        }
    }
}
