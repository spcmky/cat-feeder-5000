// Cat Feeder 5000 — Detail: Bowl + Butterfly Flaps + Chute
// Subcomponent view for design review and animation.
//
// Animation: $t goes 0→1
//   0.0 = flaps closed (covering bowl)
//   0.5 = flaps fully open (90° up)
//   1.0 = flaps closed again
//
// Render static:  openscad -o detail.png detail_bowl_flaps.scad
// Render anim:    openscad -o frame --animate=30 detail_bowl_flaps.scad

include <params.scad>
use <09_bowl.scad>
use <10_bowl_bracket.scad>

$fn = 64;

// ── Flap parameters ──────────────────────────────────────────────────────────
FLAP_W    = 52;          // Each flap width (half the bowl span)
FLAP_D    = 95;          // Flap depth (covers bowl length)
FLAP_T    = 3;           // Flap thickness
FLAP_GAP  = 2;           // Gap between flaps when closed
HINGE_D   = 3.2;         // Hinge pin diameter (M3 rod)
HINGE_BOSS_D = 8;        // Hinge boss outer diameter

// ── Chute parameters ─────────────────────────────────────────────────────────
CHUTE_W   = AUGER_TUBE_OD + 4;
CHUTE_R   = 60;
CHUTE_T   = 2.5;         // Chute wall thickness

// ── Bowl position ────────────────────────────────────────────────────────────
BOWL_X    = 0;
BOWL_Y    = 0;
BOWL_Z    = 0;

// ── Derived ──────────────────────────────────────────────────────────────────
FLAP_Z = BOWL_SIDE_H + FLAP_T + 1;  // Flap hinge height (above bowl rim)
BOWL_CX = BOWL_FLOOR_W / 2;
BOWL_CY = BOWL_FLOOR_D / 2;

// ── Animation ────────────────────────────────────────────────────────────────
// Use anim_t for CLI override (-D 'anim_t=0.5'), falls back to $t for GUI animation.
anim_t = is_undef(anim_t) ? $t : anim_t;  // CLI: -D 'anim_t=0.25'
flap_angle = ((anim_t <= 0.5) ? anim_t * 2 : (1 - anim_t) * 2) * 90;  // 0°→90°→0°


// ══════════════════════════════════════════════════════════════════════════════
// ASSEMBLY
// ══════════════════════════════════════════════════════════════════════════════

// ── Bowl shelf / base ────────────────────────────────────────────────────────
color([0.75, 0.75, 0.75])
    translate([-15, -15, -FLOOR])
        cube([BOWL_FLOOR_W + 30, BOWL_FLOOR_D + 50, FLOOR]);

// ── Bowl housing (solid block with round bowl cavity) ───────────────────────
// A solid cradle that a round removable bowl drops into.
_bh_w = BOWL_FLOOR_W;
_bh_d = BOWL_FLOOR_D + BOWL_OVERHANG;
_bh_h = FLAP_Z - 1;             // Fill up to just below flap level
_cavity_depth = _bh_h - 4;      // Depth of the bowl cavity
_bowl_r_top = min(_bh_w, _bh_d) / 2 - 6;  // Bowl opening radius (with wall margin)
_bowl_r_bot = _bowl_r_top - 10;             // Tapered bottom radius

color(COL_FOOD)
    difference() {
        // Solid block
        fillet_box(_bh_w, _bh_d, _bh_h, r=4);

        // Round bowl cavity scooped out of the top
        translate([_bh_w/2, _bh_d/2, _bh_h - _cavity_depth])
            hull() {
                // Wide circle at top (bowl rim)
                translate([0, 0, _cavity_depth - 1])
                    cylinder(r=_bowl_r_top, h=2);
                // Narrower circle at bottom (tapered bowl)
                cylinder(r=_bowl_r_bot, h=1);
            }
    }

// ── Left flap (hinged at left edge, swings up to the left) ───────────────────
translate([0, BOWL_CY - FLAP_D/2, FLAP_Z])
    rotate([0, -flap_angle, 0])
        translate([0, 0, 0])
            color(COL_GATE) flap_panel();

// ── Right flap (hinged at right edge, swings up to the right) ────────────────
// Mirror the panel so hinge knuckles are at the right (outer) edge, not center.
translate([BOWL_FLOOR_W, BOWL_CY - FLAP_D/2, FLAP_Z])
    rotate([0, flap_angle, 0])
        translate([-FLAP_W, 0, 0])
            color(COL_GATE) mirror([1, 0, 0]) translate([-FLAP_W, 0, 0]) flap_panel();

// ── Hinge pins ───────────────────────────────────────────────────────────────
for (x = [0, BOWL_FLOOR_W])
    translate([x, BOWL_CY - FLAP_D/2 - 3, FLAP_Z])
        rotate([-90, 0, 0])
            color([0.5, 0.5, 0.5]) cylinder(d=HINGE_D, h=FLAP_D + 6);

// ── Hinge bosses (mounting points on bowl shelf) ─────────────────────────────
for (x = [0, BOWL_FLOOR_W])
    for (y = [BOWL_CY - FLAP_D/2, BOWL_CY + FLAP_D/2]) {
        translate([x, y, 0])
            color([0.7, 0.7, 0.7])
            difference() {
                cylinder(d=HINGE_BOSS_D, h=FLAP_Z + 2);
                translate([0, 0, -1])
                    cylinder(d=HINGE_D + 0.4, h=FLAP_Z + 4);
            }
    }


// ── Two servos — one per flap, direct drive ─────────────────────────────────
// Each servo sits BEHIND the flap hinge line, with shaft coaxial to the hinge
// pin. Servo body extends backward (+Y), out of the bowl/eating area.

_servo_y = BOWL_CY + FLAP_D/2 + 3;  // Behind the back hinge boss

// ── Left servo (shaft at X=0, coaxial with left hinge pin) ─────────────────
translate([-SERVO_D/2, _servo_y, FLAP_Z - SERVO_H/2])
    color(COL_GATE) {
        // Body (standing upright, shaft comes out the top toward flap)
        cube([SERVO_D, SERVO_W, SERVO_H]);
        // Mounting ears (on the sides)
        translate([-2.5, 0, SERVO_H/2 - 1.5])
            cube([SERVO_D + 5, 2, 3]);
    }
// Left servo horn (rotates with left flap)
translate([0, _servo_y - 1, FLAP_Z])
    rotate([0, -flap_angle, 0])
        color([0.95, 0.95, 0.95]) {
            cylinder(d=8, h=3, center=true);
            translate([0, -2, -1.5]) cube([15, 4, 3]);
        }

// ── Right servo (shaft at X=BOWL_FLOOR_W, coaxial with right hinge pin) ────
translate([BOWL_FLOOR_W - SERVO_D/2, _servo_y, FLAP_Z - SERVO_H/2])
    color(COL_GATE) {
        cube([SERVO_D, SERVO_W, SERVO_H]);
        translate([-2.5, 0, SERVO_H/2 - 1.5])
            cube([SERVO_D + 5, 2, 3]);
    }
// Right servo horn (rotates with right flap)
translate([BOWL_FLOOR_W, _servo_y - 1, FLAP_Z])
    rotate([0, flap_angle, 0])
        color([0.95, 0.95, 0.95]) {
            cylinder(d=8, h=3, center=true);
            translate([-15, -2, -1.5]) cube([15, 4, 3]);
        }


// ══════════════════════════════════════════════════════════════════════════════
// MODULES
// ══════════════════════════════════════════════════════════════════════════════

module flap_panel() {
    // Single flap with hinge knuckles and food-safe surface
    difference() {
        union() {
            // Main panel
            cube([FLAP_W, FLAP_D, FLAP_T]);

            // Hinge knuckles along the hinge edge (X=0)
            for (y_off = [10, FLAP_D/2, FLAP_D - 10])
                translate([0, y_off, FLAP_T/2])
                    rotate([-90, 0, 0])
                        cylinder(d=HINGE_BOSS_D - 1, h=12);
        }
        // Hinge pin holes through knuckles
        for (y_off = [10, FLAP_D/2, FLAP_D - 10])
            translate([0, y_off - 1, FLAP_T/2])
                rotate([-90, 0, 0])
                    cylinder(d=HINGE_D + 0.3, h=14);

        // Linkage hole (for servo pushrod connection)
        translate([FLAP_W * 0.7, FLAP_D - 15, -1])
            cylinder(d=2.5, h=FLAP_T + 2);
    }
}


module food_chute() {
    // Half-pipe curved chute, food slides from top (auger exit) down to bowl
    rotate([-90, 0, 0])
        rotate([0, 90, 0])
            difference() {
                // Outer tube quarter section
                rotate_extrude(angle=90, $fn=48)
                    translate([CHUTE_R, 0])
                        circle(d=CHUTE_W);
                // Inner cut to make half-pipe
                rotate_extrude(angle=90, $fn=48)
                    translate([CHUTE_R, 0])
                        circle(d=CHUTE_W - 2*CHUTE_T);
                // Slice off top half to make open trough
                translate([0, 0, -CHUTE_W/2 - 1])
                    cube([CHUTE_R + CHUTE_W + 1, CHUTE_R + CHUTE_W + 1, CHUTE_W/2 + 1]);
            }
}
