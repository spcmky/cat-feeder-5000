// Cat Feeder 5000 — Shared Parameters & Common Modules
// Include this file first in all part files: include <params.scad>

// ===== DIMENSIONS =====
WALL = 3;                // Standard wall thickness (mm)
THIN_WALL = 2.5;         // Thin walls (antenna arch, etc.)
FLOOR = 4;               // Base floor thickness
INSERT_BORE = 4.7;       // M3 heat-set insert pocket bore
M3_CLEAR = 3.4;          // M3 clearance hole
UNIT_W = 160;            // Main body width
UNIT_D = 240;            // Main body depth
UNIT_H = 160;            // Main body height
GATE_W = 118;            // Gate flap width
GATE_H = 90;             // Gate flap height
GATE_T = 3;              // Gate flap thickness
GATE_ROD_D = 3.2;        // Gate hinge rod diameter
HALO_CLEAR_W = 130;      // Round halo inner clear width
HALO_TUBE_OD = 24;       // Halo tube outer diameter
HALO_LEG_H = 77;         // Halo leg height (floor to arch start)
GATE_SETBACK = 40;       // Gate Y position inside body (mm from front face)
SERVO_W = 23;            // SG90 servo width
SERVO_D = 12.5;          // SG90 servo depth
SERVO_H = 30;            // SG90 servo height
SERVO_EAR_SPAN = 28;     // SG90 servo ear spacing
TOLERANCE = 0.1;         // General fit tolerance

// ===== AUGER =====
AUGER_TUBE_ID = 32;         // Auger tube inner diameter
AUGER_TUBE_OD = 38;         // Auger tube outer diameter
AUGER_TUBE_L = 85;          // Auger tube length
AUGER_PITCH = 20;           // Auger screw thread pitch
AUGER_ANGLE = 30;           // Auger tube angle from vertical (degrees)

// ===== ROOF & COUPLING =====
ROOF_T = 5;                    // Roof thickness (holds M3 inserts)
AUGER_COUPLING_H = 15;        // Coupling stub above auger flange

// ===== BOWL =====
BOWL_FLOOR_W = 100;         // Bowl floor width
BOWL_FLOOR_D = 90;          // Bowl floor depth
BOWL_SIDE_H = 25;           // Bowl side wall height
BOWL_BACK_H = 30;           // Bowl back wall height
BOWL_FLOOR_T = 3;           // Bowl floor thickness
BOWL_WALL_T = 2.5;          // Bowl wall thickness
BOWL_OVERHANG = 15;         // Bowl floor extends past gate plane

// ===== FOOD =====
COL_FOOD = [0.9, 0.7, 0.3, 0.8]; // Tan — food-contact parts

// ===== RENDER QUALITY =====
$fn = 64;                // Circle resolution (smooth curves)

// ===== COLORS =====
COL_RFID = [0.8, 0.2, 0.2, 0.8];      // Red — RFID antenna arch
COL_TPU = [0.4, 0.7, 0.3, 0.8];       // Green — TPU flexible parts
COL_GATE = [0.2, 0.5, 0.8, 0.8];      // Blue — Gate mechanism
COL_BODY = [0.6, 0.6, 0.6, 0.8];      // Gray — Main body structure

// ===== COMMON MODULES =====

// M3 heat-set insert pocket (bore hole for pressed insert)
module m3_insert(h = 8) {
    cylinder(d = INSERT_BORE, h = h);
}

// M3 clearance hole (for bolt pass-through)
module m3_clear(h = 8) {
    cylinder(d = M3_CLEAR, h = h);
}

// Fillet box: rectangular box with filleted corners
// w, d, h = width, depth, height; r = corner radius
module fillet_box(w, d, h, r = 2) {
    hull() {
        translate([r, r, 0])
            cylinder(r = r, h = h);
        translate([w - r, r, 0])
            cylinder(r = r, h = h);
        translate([r, d - r, 0])
            cylinder(r = r, h = h);
        translate([w - r, d - r, 0])
            cylinder(r = r, h = h);
    }
}

// Boss: raised circular pad with M3 pocket
// Useful for internal reinforcement at bolt points
module boss(d = 10, h = 4, pocket = true) {
    difference() {
        cylinder(d = d, h = h);
        if (pocket)
            translate([0, 0, -0.1])
                m3_clear(h = h + 0.2);
    }
}
