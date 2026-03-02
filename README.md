# Cat Feeder 5000

An automated multi-cat feeder system with RFID-gated bowl access, camera-based cat identification, scheduled feeding, and remote web control. Built on Raspberry Pi + Arduino with fully 3D-printed enclosures.

## Project Overview

- **Units**: 2 identical feeders
- **Platform**: Raspberry Pi (main brain) + Arduino Nano (motor/servo/sensor control)
- **Access Control**: RFID collar tags + camera visual verification (dual-layer)
- **Features**: Scheduled feeding, portion control, remote web control, per-cat access gating
- **Fabrication**: All structural parts 3D-printed on LulzBot Taz / Pro
- **BOM**: ~$170/feeder

## Repository Structure

```
cat-feeder-5000/
├── docs/                        # Planning documents and specs
│   ├── master-plan.md           # Full project master plan
│   └── master-plan.docx         # Word version
├── hardware/
│   ├── bom/                     # Bill of materials (CSV + spreadsheet)
│   ├── wiring/                  # Wiring diagrams and pin maps
│   └── schematics/              # Circuit schematics
├── firmware/
│   └── cat-feeder-arduino/      # Arduino sketch
├── software/
│   ├── api/                     # Flask/FastAPI backend (Pi)
│   ├── camera/                  # Camera + cat ID module
│   ├── rfid/                    # RFID access control
│   └── web/                     # Web UI
├── 3d-models/
│   ├── stl/                     # Print-ready STL files
│   ├── cad/                     # Source CAD files
│   └── print-settings/          # LulzBot slicer profiles
└── assets/                      # Images, diagrams, visuals
```

## Quick Links

- [Master Plan](docs/master-plan.md)
- [Bill of Materials](hardware/bom/)
- [Wiring Diagrams](hardware/wiring/)
- [Arduino Firmware](firmware/cat-feeder-arduino/)
- [3D Print Files](3d-models/)

## Status

🟡 **Planning Phase** — master plan complete, fabrication and coding next.
