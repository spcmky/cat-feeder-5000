# Cat Feeder 5000 — LulzBot Print Settings
LulzBot Taz 6 / Pro. Slicer: Cura LulzBot Edition or PrusaSlicer with LulzBot profile.

## Filament Prep
- **PETG**: Dry at 65°C for 4–6 hours before printing. PETG is hygroscopic — wet filament causes stringing and weak layers.
- **TPU**: Dry at 50°C for 2–4 hours. Load slowly; use direct drive (LulzBot Taz is direct drive — good for TPU).

---

## PETG Profile (Structural Parts)

| Setting | Value |
|---------|-------|
| Nozzle temp | 240°C |
| Bed temp | 75°C (PEI sheet) |
| Nozzle size | 0.5mm |
| Layer height | 0.25mm (standard) / 0.2mm (detail) / 0.15mm (fine/food-contact) |
| First layer height | 0.35mm |
| Print speed | 45 mm/s |
| First layer speed | 20 mm/s |
| Perimeters | 3 (food-contact parts: use 4) |
| Top/bottom layers | 4 |
| Cooling | 30–50% fan (PETG needs some cooling but not too much) |
| Retraction | 1.5mm @ 25mm/s (direct drive) |
| Z-hop | 0.2mm |
| Seam | Rear or aligned |

## TPU Profile (Flexible Parts: bumper, feet)

| Setting | Value |
|---------|-------|
| Nozzle temp | 220°C |
| Bed temp | 45°C |
| Nozzle size | 0.5mm |
| Layer height | 0.2mm (feet) / 0.3mm (bumper) |
| Print speed | 25 mm/s max |
| Retraction | DISABLED (TPU does not retract well — causes jams) |
| Perimeters | 3 |
| Infill | 15% (feet) / 30% (bumper) |
| Cooling | 50% |
| Combing | ON (avoids travel moves over infill, reduces stringing) |

---

## Per-Part Settings

| # | Part | Material | Layer H | Infill | Supports | Orientation | Notes |
|---|------|----------|---------|--------|----------|-------------|-------|
| 01 | Main body | PETG | 0.25mm | 40% | No | Upright (Z+) | Largest print ~6h |
| 02 | Hopper | PETG | 0.25mm | 25% | No | Upright | Funnel thin walls |
| 03 | Hopper lid | PETG | 0.2mm | 20% | No | Upright | Snap lip down |
| 04 | Auger tube | PETG | 0.2mm | 30% | No | Upright | Smooth bore critical |
| 05 | Auger screw | PETG | 0.15mm | 60% | Yes | VERTICAL (thread integrity) | Supports on thread underside |
| 06 | Motor mount | PETG | 0.25mm | 40% | No | Flat | N20 or NEMA14 variant |
| 07 | Electronics tray | PETG | 0.25mm | 30% | No | Flat | Open side up |
| 08 | Electronics cover | PETG | 0.2mm | 20% | No | Flat | Vent slots up |
| 09 | Bowl | PETG | 0.15mm | 30% | No | Upright | 4 perimeters, food-safe |
| 10 | Bowl bracket | PETG | 0.25mm | 40% | No | Flat | |
| 11 | Camera mount | PETG | 0.2mm | 35% | Yes | Upright | Supports under camera head |
| 12 | Camera bezel | PETG | 0.2mm | 20% | No | Flat | |
| 13 | Gate flap | PETG | 0.15mm | 40% | No | Flat (face down) | Smooth cat-facing surface |
| 14 | Gate hinge mount | PETG | 0.2mm | 40% | No | Flat | |
| 15 | Antenna arch | PETG | 0.2mm | 25% | No | UPRIGHT | Thin walls need upright orientation; NO top perimeters over coil channel |
| 16 | Servo bracket | PETG | 0.2mm | 40% | No | Flat | |
| 17 | Gate bumper | TPU | 0.2mm | 30% | No | Flat | TPU profile, slow |
| 18 | Feet ×4 | TPU | 0.3mm | 15% | No | Peg up | Print all 4 at once |

---

## Antenna Arch Special Notes (Part 15)

The coil channel in the arch top bridge must be open on the top surface — no bridging perimeters over it. In Cura/PrusaSlicer:
- Use "Surface mode: Normal" 
- The channel is a blind slot from the top — the slicer will naturally leave it open since it's open geometry
- After printing, seat the wound coil in the channel and fix with food-safe 2-part epoxy
- Route cable through the 5mm channel in the left leg to the electronics bay

## Food-Contact Parts: Post-Processing

Parts 02 (hopper), 04 (auger tube), 05 (auger screw), 09 (bowl):
1. Wash with warm soapy water, rinse well
2. Inspect for layer gaps or rough areas — sand smooth with 400 grit if needed
3. Apply thin coat of food-safe mineral oil or food-grade PTFE lubricant to auger screw/tube interface only
4. Do NOT use acetone or other solvents (degrades PETG surface)

## Heat-Set Insert Installation

All M3 inserts: use soldering iron at 200–220°C. Press insert flush with surface, perpendicular. Allow 60s to cool before stressing.
Insert bore diameter in all parts: **4.7mm** (M3 insert OD = 4.5mm + 0.2mm print tolerance).

## Print Order (Recommended)

Print larger/longer parts first to catch any issues before committing to smaller detail prints:
1. Main body (01) — longest, catches any bed leveling issues
2. Hopper (02) + Auger tube (04) in same session if bed space allows
3. Auger screw (05) — most precision-sensitive, print alone
4. Bowl (09) — food-contact, inspect carefully
5. Gate assembly: flap (13) + hinge mount (14) + servo bracket (16) + bumper (17)
6. Antenna arch (15) — inspect coil channel carefully before continuing
7. Remaining parts in any order
