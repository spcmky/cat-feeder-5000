// Cat Feeder 5000 — Part 16: Gate Servo Bracket
// Mounts SG90 servo inside feeder body. Linkage arm connects to gate flap top.
// Print: PETG, 0.2mm layers, 40% infill, no supports

include <params.scad>

color(COL_GATE) gate_servo_bracket();

module gate_servo_bracket() {
    BW = 40; BD = 30; BH = 50;
    // SG90 body: 23mm × 12.5mm × 30mm
    SW = SERVO_W; SD = SERVO_D; SH = SERVO_H;
    EAR = SERVO_EAR_SPAN;   // 28mm ear spacing

    difference() {
        fillet_box(BW, BD, BH, r=3);

        // Servo pocket (centered, open top)
        translate([(BW - SW)/2, (BD - SD)/2, BH - SH - 2])
            cube([SW + TOLERANCE*2, SD + TOLERANCE*2, SH + 2.1]);

        // Servo ear mount holes (M2, ×2)
        for (y = [(BD - EAR)/2, (BD + EAR)/2])
            translate([BW/2, y, BH - 5])
                cylinder(d=2.2, h=6);

        // Body attachment holes (M3 clearance, ×2)
        for (x = [8, BW - 8])
            translate([x, BD/2, -0.1])
                m3_clear(h=BH + 0.2);

        // Linkage arm exit slot (top, for servo horn arm to pass through)
        translate([BW/2 - 4, (BD - 3)/2, BH - 3])
            cube([8, 3, 4]);
    }
}
