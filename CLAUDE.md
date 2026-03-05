# Cat Feeder 5000

Automated multi-cat feeder with RFID-gated bowl access, camera-based cat ID, scheduled feeding, and remote web control. Two identical units, 3D-printed enclosures, Raspberry Pi + Arduino.

## Architecture

- **Raspberry Pi** (per feeder): Flask web server, OpenCV camera, RFID access logic, SQLite DB, schedule manager
- **Arduino Nano** (per feeder): stepper motor (auger), servo (gate), EM4095 RFID reader, buzzer
- **Communication**: USB serial at 115200 baud with a simple text protocol (`FEED:<grams>`, `GATE:OPEN`, `EVENT:RFID:<uid>`, etc.)

## RFID System

The cats have **implanted ISO 11784/11785 FDX-B microchips** (134.2 kHz) between their shoulders. The reader is an **EM4095** analog front end with a custom wound flat coil antenna. The antenna is housed in a **round halo** (semicircular arch) at the front of the feeder — the cat walks through it, placing the chip directly in the coil's field. Manchester-encoded FDX-B data is decoded via timer interrupt on the Arduino.

## Mechanical Design

The feeder uses a **swing-up gate** (hinged at top, swings upward into the body) that physically cannot contact the cat. The gate sits **40mm inside the body** (behind the halo reading zone). Spatial sequence front-to-back: round halo → approach zone → gate → bowl.

The bowl is open-front (no wall at the cat's face), with low 25mm side walls and a 15mm floor overhang. Whisker-friendly.

## Repository Layout

```
firmware/cat-feeder-arduino/   Arduino sketch (EM4095 FDX-B decoder, gate servo, auger stepper, serial protocol)
software/                      Python backend for Raspberry Pi
  config.py                    Environment-driven configuration
  db.py                        SQLite schema + CRUD (cats, rfid_tags, feeding_log, schedules)
  serial_bridge.py             Threaded serial reader with event dispatch
  rfid/rfid_access.py          RFID access controller (debounce, access decisions)
  rfid/gate_controller.py      Gate state machine (30s auto-close)
  scheduler.py                 Feeding scheduler (polls DB every 30s)
  camera/camera.py             OpenCV capture + placeholder cat detection
  main.py                      Daemon entry point, wires subsystems, signal handlers
  api/app.py                   Flask REST API (17 endpoints: cats, feeding, schedule, RFID, gate, camera)
hardware/
  bom/bom.csv                  Full bill of materials (~$170/feeder)
  wiring/wiring-notes.md       Pin map, EM4095 wiring, LC tank antenna design
3d-models/
  cad/params.scad              Shared parameters and common modules — ALL .scad files include this
  cad/01-18_*.scad             Individual 3D-printed parts (OpenSCAD, parametric)
  cad/assembly_preview.scad    Full assembly visualization (not for printing)
  print-settings/              LulzBot PETG + TPU slicer profiles
docs/master-plan.md            Full project master plan (v1.2)
```

## 3D Models (OpenSCAD)

All parts are parametric. `params.scad` is the single source of truth for dimensions, tolerances, and colors. Key conventions:

- **Coordinate system**: X = width, Y = depth (Y=0 is front/cat side), Z = height (Z=0 is floor)
- **Units**: millimeters throughout
- **Materials**: PETG for structural and food-contact parts, TPU for bumper and feet
- **Printers**: LulzBot Taz and LulzBot Pro
- All parts use `include <params.scad>` and the shared modules (`fillet_box`, `boss`, `m3_insert`, `m3_clear`)
- The user edits `params.scad` directly — respect their changes, don't overwrite without asking
- `assembly_preview.scad` uses `use <part.scad>` (not `include`) to pull in modules without auto-rendering

### Key dimensions (from params.scad)

- Body: 160 W × 240 D × 160 H mm, 3mm walls, 4mm floor
- Halo: 130mm inner clear width, 24mm tube OD, 77mm leg height
- Gate: 118 W × 90 H × 3mm, setback 40mm from front face
- Tolerance: 0.1mm, M3 hardware (4.7mm insert bore, 3.4mm clearance)

## Code Style

- **Python**: Standard library + Flask, pyserial, opencv-python-headless. Config via environment variables. SQLite with WAL mode.
- **Arduino**: Single .ino file, ISR-based FDX-B decoding, non-blocking serial protocol handler.
- **OpenSCAD**: One file per part, numbered 01-18. Shared params in params.scad. Comments explain geometry intent.

## Important Notes

- No Word docs — all documentation is markdown (.md)
- The master plan is at v1.2 (reflects implanted chip RFID, EM4095, swing-up gate, round halo)
- Camera-based cat ID (ML model) is a TODO placeholder — currently just captures snapshots
- The web UI (`software/web/`) is scaffolded but not yet implemented
