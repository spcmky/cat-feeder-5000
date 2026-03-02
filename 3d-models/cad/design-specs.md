# Cat Feeder 5000 — CAD Design Specifications
All dimensions in **millimeters**. Design in Fusion 360 or FreeCAD.
Coordinate system: X = width (left-right), Y = depth (front-back), Z = height (up-down).

---

## Overall Unit Envelope

| Dimension | Value | Notes |
|-----------|-------|-------|
| Width (X) | 160 mm | |
| Depth (Y) | 220 mm | Including bowl overhang |
| Height (Z) | 320 mm | Including hopper lid |
| Bowl approach clearance | ≥ 200 mm wide × 150 mm tall | Open front zone for cat access |

---

## Part 1 — Main Body / Base

**Function**: Structural core that all other parts mount into.

| Feature | Dimension |
|---------|-----------|
| Outer width | 160 mm |
| Outer depth | 200 mm |
| Outer height | 200 mm |
| Wall thickness | 3 mm |
| Floor thickness | 4 mm |
| Front opening (bowl zone) | 120 mm wide × 100 mm tall |
| Electronics bay (rear lower) | 80 mm × 60 mm × 50 mm |
| Auger tube hole (center) | 40 mm dia pass-through |
| M3 heat-set insert bosses | Ø5.5 mm × 6 mm deep, ×12 locations |
| Rear cable pass-through | 15 mm dia, lower rear wall |
| Bottom feet pockets | 4× Ø10 mm × 3 mm deep, 10 mm from corners |

**Notes**: Front face has large opening for bowl approach. Electronics bay accessible from removable bottom cover. All internal corners at R2mm to reduce stress.

---

## Part 2 — Food Hopper

**Function**: Food reservoir. Sits on top of main body, funnels food into auger tube.

| Feature | Dimension |
|---------|-----------|
| Top opening (square) | 130 mm × 130 mm |
| Bottom outlet (round) | Ø38 mm (matches auger tube OD) |
| Height | 130 mm |
| Wall thickness | 2.5 mm |
| Funnel angle | 50° from vertical (exceeds 45° min) |
| Capacity (approx) | ~500 mL / ~400 g dry kibble |
| Lip for lid | 3 mm ledge, 2 mm tall, around perimeter |
| Mount tabs | 4× M3 inserts on bottom flange |

**Notes**: No sharp interior corners at funnel transition — use R5mm fillet to prevent kibble bridging.

---

## Part 3 — Hopper Lid

**Function**: Snap/screw-on cover to keep food fresh and prevent pests.

| Feature | Dimension |
|---------|-----------|
| Outer footprint | 136 mm × 136 mm |
| Height | 20 mm |
| Wall thickness | 2 mm |
| Inner lip (snap fit) | 2 mm wide × 3 mm tall, 0.4 mm interference fit |
| Filling port option | Optional 40 mm dia flip-door in center |

**Notes**: Add 4× small vent slots (1 mm × 10 mm) under lip to prevent vacuum seal. Center filling port is optional for top-up without full lid removal.

---

## Part 4 — Auger Tube

**Function**: Channel that auger screw rotates inside to move food from hopper to bowl drop point.

| Feature | Dimension |
|---------|-----------|
| Inner diameter | 32 mm |
| Outer diameter | 38 mm |
| Length | 120 mm |
| Wall thickness | 3 mm |
| Angle from vertical | 30° (food flows toward front/bowl) |
| Top flange (hopper join) | Ø50 mm × 5 mm, M3 holes ×3 |
| Bottom exit port | Ø28 mm, angled 90° to tube axis |

**Notes**: Inner bore must be smooth — 0.15mm layer height, 3 perimeters, food-safe lubricant. Slight taper (0.5°) at bottom helps food exit cleanly.

---

## Part 5 — Auger Screw

**Function**: Rotates inside auger tube to move kibble. Motor-driven.

| Feature | Dimension |
|---------|-----------|
| Outer diameter | 30 mm (1 mm clearance to tube ID) |
| Pitch (thread spacing) | 20 mm |
| Thread depth | 12 mm |
| Length | 115 mm |
| Motor shaft coupler bore | Ø5 mm (N20) or Ø5 mm flat (stepper) |
| Coupler length | 15 mm |

**Notes**: Print vertically for best thread layer adhesion. Each full rotation = ~8–12g kibble (calibrate `STEPS_PER_GRAM` in firmware after printing). Add M3 set screw hole through coupler section for shaft grip.

---

## Part 6 — Motor Mount

**Function**: Mounts the auger drive motor to the main body, aligned with auger tube.

| Feature | Dimension |
|---------|-----------|
| Overall size | 60 mm × 50 mm × 30 mm |
| Motor pocket (N20) | 12 mm × 10 mm × 25 mm deep |
| Motor pocket (stepper) | 28 mm sq × 20 mm deep |
| Shaft center offset | Matches auger tube center axis |
| Mount holes | 4× M3, matches main body bosses |

**Notes**: Design for either N20 or NEMA14 stepper (separate variants or universal with insert). Motor pocket should have 0.2 mm clearance on all sides.

---

## Part 7 — Electronics Tray

**Function**: Snap-in tray holding Pi, Arduino Nano, wiring, and power components.

| Feature | Dimension |
|---------|-----------|
| Outer size | 78 mm × 58 mm × 20 mm |
| Pi Zero 2 W pocket | 65 mm × 30 mm × 6 mm deep |
| Arduino Nano pocket | 45 mm × 18 mm × 8 mm deep |
| Wire channel width | 8 mm |
| Snap clips | 2× 2 mm wide × 4 mm tall, 0.5 mm interference |
| Standoff height (Pi) | 3 mm (M2.5 or snap-peg style) |

**Notes**: Include cable tie slots (3 mm × 1.5 mm) every 30 mm along perimeter. Tray slides into main body from rear. Ventilation holes (Ø3 mm, 6× min) above Pi.

---

## Part 8 — Electronics Cover

**Function**: Covers electronics bay. Ventilated, removable.

| Feature | Dimension |
|---------|-----------|
| Outer size | 84 mm × 64 mm × 5 mm |
| Vent slots | 20× slotted 2 mm × 15 mm, 3 mm spacing |
| Retention clip | 1× snap clip center, or 2× M3 screws |

---

## Part 9 — Bowl (Open-Front Design)

**Function**: Food bowl. Whisker-friendly open-front design.

| Feature | Dimension |
|---------|-----------|
| Internal floor width | 100 mm |
| Internal floor depth | 90 mm (front-to-back) |
| Side wall height | 25 mm |
| Back wall height | 30 mm |
| Front wall | **NONE** — fully open face |
| Floor thickness | 3 mm |
| Side wall thickness | 2.5 mm |
| Floor front overhang past opening | 15 mm |
| Mounting tabs (rear) | 2× M3 insert, 10 mm from sides |
| Corner radius (internal) | R10 mm — easy cleaning |
| Drain holes (optional) | 4× Ø3 mm in floor corners |

**Notes**: The open front means no wall on the cat-facing side. Side walls taper from 25 mm at front to 30 mm at back to loosely guide food. Floor extends 15 mm past the gate opening plane so food doesn't fall out when gate opens. All interior surfaces smooth (0.15 mm layer height).

---

## Part 10 — Bowl Mounting Bracket

**Function**: Attaches bowl to main body front opening at correct height.

| Feature | Dimension |
|---------|-----------|
| Overall size | 110 mm × 30 mm × 20 mm |
| Bowl attachment | 2× M3 holes, 90 mm apart |
| Body attachment | 4× M3 holes, countersunk |
| Bowl height from floor | Sets bowl floor at 40 mm above base |
| Tilt angle | 2° downward-front (prevents food sliding back) |

---

## Part 11 — Camera Mount / Arm

**Function**: Positions Pi Camera above and behind the bowl opening for top-down cat face view.

| Feature | Dimension |
|---------|-----------|
| Arm length | 80 mm |
| Camera face angle | 45° downward from horizontal |
| Camera pocket | 25 mm × 25 mm × 5 mm, M2 mounts × 4 |
| Body attachment (swivel base) | M3 × 2, 15 mm apart |
| Horizontal swivel range | ±20° (slot + clamp bolt) |

**Notes**: Print with supports under the angled camera head. Camera should face down-forward to capture cat's face from ~150–200 mm distance as cat eats.

---

## Part 12 — Camera Cover / Bezel

**Function**: Cosmetic trim ring around camera lens. Protects from food dust.

| Feature | Dimension |
|---------|-----------|
| Lens opening | Ø10 mm (Pi Camera lens is ~7.5 mm dia) |
| Outer footprint | 30 mm × 30 mm |
| Depth | 8 mm |
| Snap clips | 4× small 1 mm clips to camera mount |

---

## Part 13 — Bowl Gate / Flap (Swing-Up)

**Function**: Blocks bowl opening when closed. Swings up into feeder body when open. Servo-actuated.

| Feature | Dimension |
|---------|-----------|
| Flap width | 118 mm (2 mm clearance each side in 120 mm opening) |
| Flap height | 90 mm (covers full bowl approach opening) |
| Thickness | 3 mm |
| Hinge rod holes (top edge) | 2× Ø3.2 mm, 20 mm from each end |
| Servo linkage hole (top center) | Ø3 mm, 10 mm from top edge |
| Bottom edge profile | R5 mm radius — no sharp edge facing cat |
| Closed position overlap | 5 mm overlap with bowl bracket each side |

**Notes**: When open (servo pulls top rearward and up), flap pivots 95–100° and rests against internal stop inside feeder body. Cat's head position during eating is ~80 mm below the hinge line — no contact possible. Print flat (face down). No texture on cat-facing side.

---

## Part 14 — Gate Top Hinge Mount

**Function**: Holds the gate flap hinge rod. Fixed to top of bowl opening frame.

| Feature | Dimension |
|---------|-----------|
| Width | 120 mm (spans full opening) |
| Height | 20 mm |
| Depth | 15 mm |
| Hinge rod bore | 2× Ø3.2 mm, press-fit M3 shaft or use Ø3mm rod |
| Rod center height from top | 8 mm |
| Body attachment holes | 4× M3, evenly spaced |

**Notes**: Rod sits just inside the feeder body plane so gate can swing inward (upward) cleanly.

---

## Part 15 — Antenna Arch Housing

**Function**: Overhead arch that cradles the flat RFID antenna coil above the bowl approach zone.

| Feature | Dimension |
|---------|-----------|
| Arch inner span (X) | 160 mm (full feeder width) |
| Arch inner height (Z above bowl rim) | 70 mm at peak |
| Arch depth (Y, front-to-back) | 40 mm |
| Coil channel width | 16 mm |
| Coil channel depth | 5 mm (recessed, no top perimeters over channel) |
| Coil center height above bowl floor | ~90–110 mm (adjust: want 50–80 mm above cat shoulder level) |
| Wall thickness | 2.5 mm |
| Body mount tabs | 2× M3 each side, into main body top |
| Coil channel position | Centered horizontally, centered front-to-back in arch |

**Notes**: Arch must not restrict the cat's head/neck access to the bowl. Profile: semi-elliptical arch, widest at base. Internal coil channel is open-top (no perimeter bridging over it) — coil wire is seated and fixed with food-safe epoxy. Route antenna cable through a 5 mm dia channel in the arch wall to the electronics bay.

---

## Part 16 — Gate Servo Bracket

**Function**: Mounts SG90 servo inside feeder body, connects via linkage arm to gate flap top.

| Feature | Dimension |
|---------|-----------|
| Servo pocket | 23 mm × 12.5 mm × 30 mm deep (SG90 body) |
| Servo ear mounting holes | M2 × 2, 28 mm apart (SG90 spec) |
| Body attachment | M3 × 2 |
| Linkage arm pivot hole | Ø2 mm, 15 mm from servo shaft center |
| Position in body | Above gate hinge, ~20 mm from top wall |

**Notes**: Orient servo so horn rotates in vertical plane parallel to gate travel. With horn at 0° gate is closed; at ~95° gate is fully open (flap resting on bumper).

---

## Part 17 — TPU Gate Bumper

**Function**: Soft end-stop for gate flap in fully-open position. Absorbs servo overrun.

| Feature | Dimension |
|---------|-----------|
| Overall size | 30 mm × 15 mm × 8 mm |
| Shore hardness | TPU 95A preferred |
| Mounting | Press-fit or M2 screw into feeder body rear wall |
| Contact face | Full 30 mm × 8 mm surface (spread impact) |
| Position | Where gate flap top edge rests when fully open |

---

## Part 18 — Feet / Non-Slip Pads

**Function**: Press-fit rubber feet, one at each corner of base. Prevents sliding.

| Feature | Dimension |
|---------|-----------|
| Body (press-fit stud) | Ø9.8 mm dia × 6 mm tall (0.2 mm interference with Ø10 mm pocket) |
| Pad base | Ø16 mm × 4 mm |
| Material | TPU 95A |
| Quantity | 4 per unit |

---

## General Design Notes

- All M3 heat-set insert bores: **Ø4.7 mm** (M3 insert OD = 4.5 mm, +0.2 mm for print tolerance)
- All M3 clearance holes (screws pass through): **Ø3.4 mm**
- All M3 captive/tapped holes: **Ø2.5 mm** (tap M3 after printing, or use insert)
- Standard print tolerance: **±0.2 mm** — design snap fits with 0.3–0.5 mm interference
- PETG shrinkage: **~0.3–0.5%** — negligible at these scales, no compensation needed for LulzBot
- All food-contact surfaces: smooth finish (0.15 mm layer height), no sharp interior corners < R3 mm
