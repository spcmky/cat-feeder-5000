// Cat Feeder 5000 — Part 11: Camera Mount / Arm
// Positions Pi Camera above bowl. 45° downward angle. Print with supports.
// Print: PETG, 0.2mm layers, 35% infill, supports YES

include <params.scad>

color(COL_BODY) camera_mount();

module camera_mount() {
    ARM_L = 80; ARM_W = 20; ARM_T = 5;
    CAM_W = 25; CAM_D = 25; CAM_H = 5;
    CAM_ANGLE = 45;
    SWIVEL_D = 20; SWIVEL_H = 15;

    union() {
        // Swivel base (attaches to body side)
        difference() {
            cylinder(d=SWIVEL_D, h=SWIVEL_H);
            // Swivel slot (±20° arc)
            translate([0, 0, SWIVEL_H/2])
                rotate([0, 90, 0])
                    cylinder(d=4, h=SWIVEL_D + 2, center=true);
            // Body mount holes
            for (y=[-6, 6])
                translate([0, y, -0.1]) m3_clear(h=SWIVEL_H + 0.2);
        }
        // Arm
        translate([-ARM_W/2, 0, SWIVEL_H])
            cube([ARM_W, ARM_T, ARM_L]);
        // Camera head (angled)
        translate([0, 0, SWIVEL_H + ARM_L])
            rotate([CAM_ANGLE, 0, 0])
                difference() {
                    translate([-CAM_W/2, -CAM_D/2, 0])
                        fillet_box(CAM_W, CAM_D, CAM_H, r=2);
                    // Lens opening
                    cylinder(d=10, h=CAM_H + 0.2, center=false);
                    // M2 mount holes (4× Pi Camera pattern, 21×21mm)
                    for (x=[-10.5,10.5]) for (y=[-10.5,10.5])
                        translate([x, y, -0.1])
                            cylinder(d=2.2, h=CAM_H + 0.2);
                }
    }
}
