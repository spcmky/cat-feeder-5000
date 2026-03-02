# Cat Feeder 5000 — Master Plan
**Project**: Automated Multi-Cat Feeder System
**Units**: 2 identical feeders
**Date**: 2026-03-02
**Version**: 1.2 (implanted microchip RFID + swing-up gate)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Bill of Materials](#3-bill-of-materials)
4. [3D-Printed Parts](#4-3d-printed-parts)
5. [Wiring & Electronics](#5-wiring--electronics)
6. [Arduino Firmware](#6-arduino-firmware)
7. [Raspberry Pi Software](#7-raspberry-pi-software)
8. [Web Interface & API](#8-web-interface--api)
9. [Design Rationale](#9-design-rationale)
10. [Risk Mitigation](#10-risk-mitigation)
11. [Project Phases & Deliverables](#11-project-phases--deliverables)

---

## 1. Project Overview

### Goal
Build two identical automated cat feeders that:
- Dispense precise food portions on a schedule
- Enforce per-cat access by reading the cat's **implanted microchip** (no collar required)
- Use a camera to visually verify which cat is present (cross-check)
- Allow full remote monitoring and control via a web app
- Are housed in professional-looking, fully 3D-printed enclosures

### Key Design Decisions
- **Open-front bowl**: Bowl has no walls at the cat's face side — low 25mm side walls, forward-extending floor. Whisker-friendly, comfortable eating position.
- **Implanted chip RFID**: Uses each cat's existing ISO 11784/11785 FDX-B microchip (134.2 kHz, implanted between the shoulders). No collar or tag required. Reader uses an EM4095 analog front end with a custom flat coil antenna mounted overhead.
- **Overhead antenna arch**: The antenna coil is positioned in a horizontal arch above and just behind the bowl opening, so the chip passes directly under it as the cat lowers its head to eat. The antenna never contacts the cat.
- **Swing-up gate**: The bowl gate flap is hinged at the top and swings up into the feeder body when open. The cat's head and back are never in the path of the gate — it cannot hit them.
- **Dual-layer cat ID**: RFID handles physical enforcement (gate open/close); camera handles visual verification and smart alerts. Cross-verification catches edge cases.
- **Two-board design**: Pi handles compute-heavy tasks (camera, web server, RFID logic). Arduino handles real-time 5V peripherals (motors, servos, sensors).

---

## 2. System Architecture

### Hardware Architecture

```
┌─────────────────────────────────────────────────────┐
│              Raspberry Pi (per feeder)               │
│  - Web server (Flask/FastAPI)                        │
│  - Camera + cat ID (OpenCV)                          │
│  - RFID access logic                                 │
│  - Schedule manager                                  │
│  - Database (SQLite)                                 │
│  - Serial comms to Arduino                           │
└──────────────────────┬──────────────────────────────┘
                       │ USB Serial (115200 baud)
┌──────────────────────▼──────────────────────────────┐
│              Arduino Nano (per feeder)               │
│  - Auger/dispense motor (stepper or DC)              │
│  - Bowl gate servo (SG90, pin D8)                    │
│  - EM4095 RFID AFE (SPI, pins D10-D13) + coil antenna│
│  - Buzzer (pin A2)                                   │
│  - Weight/load sensor (optional)                     │
│  - Status LED                                        │
└──────────────────────────────────────────────────────┘
```

### Network Architecture

```
[Cat Feeder Unit 1] ──┐
                       ├── Local WiFi ── [Router] ── [Internet]
[Cat Feeder Unit 2] ──┘                     │
                                            │
                                    [Web App / Mobile]
                                    (remote monitoring)
```

### Serial Protocol (Pi ↔ Arduino)

| Direction | Command | Description |
|-----------|---------|-------------|
| Pi → Arduino | `FEED:<grams>` | Dispense specified portion |
| Pi → Arduino | `GATE:OPEN` | Open bowl gate |
| Pi → Arduino | `GATE:CLOSE` | Close bowl gate |
| Arduino → Pi | `EVENT:RFID:<uid>` | RFID tag detected (UID string) |
| Arduino → Pi | `EVENT:WEIGHT:<grams>` | Current bowl weight |
| Arduino → Pi | `STATUS:READY` | Arduino boot complete |

---

## 3. Bill of Materials

**Estimated cost: ~$170 per feeder** (×2 = ~$340 total)

### Core Electronics

| Qty | Component | Est. Cost | Notes |
|-----|-----------|-----------|-------|
| 1 | Raspberry Pi Zero 2 W | $15 | Or Pi 4 for more headroom |
| 1 | Arduino Nano | $5 | Clone acceptable |
| 1 | EM4095 RFID analog front end (AFE) | $3 | 125 kHz AFE, tune LC tank to 134.2 kHz for FDX-B; SPI; 5V native — no level shifter needed. Alt: TMS3705 (TI, dedicated 134.2 kHz animal ID IC, harder to source) |
| 1 | Antenna coil (custom wound or pre-made) | $3 | Flat spiral coil, ~10–15cm diameter, tuned to 134.2 kHz with capacitor. Mounted overhead in arch housing above cat's shoulders |
| 1 | Tuning capacitor for antenna | $1 | LC tank cap, value calculated for 134.2 kHz resonance with chosen coil |
| 1 | Pi Camera Module 3 (or V2) | $25 | Wide angle preferred |
| 1 | SG90 micro servo (gate) | $3 | Swing-up gate actuation |
| 1 | N20 gear motor or NEMA 14 stepper | $8 | Auger drive |
| 1 | Motor driver (L298N or A4988) | $3 | |
| 1 | Active buzzer 5V | $1 | Feeding alert |
| 1 | 5V 3A power supply (USB-C) | $10 | Powers Pi + Arduino |
| 1 | Micro SD card 32GB | $8 | Pi OS + data |

### Mechanical & Hardware

| Qty | Component | Est. Cost | Notes |
|-----|-----------|-----------|-------|
| 1 | Food-grade PETG filament (1kg) | $25 | Main body, hopper, bowl |
| 1 | TPU filament (200g) | $8 | Gate bumper, feet |
| 1 | M3 heat-set inserts (50 pack) | $6 | Assembly fasteners |
| 1 | M3 screws assorted (100 pack) | $5 | |
| 1 | Silicone food bowl liner (optional) | $5 | Hygiene, replaceable |
| — | Misc: wire, connectors, JST | $10 | |

**Total per feeder: ~$140–170 depending on sourcing**

---

## 4. 3D-Printed Parts

All parts printed on LulzBot Taz or Pro. Primary material: PETG (food-safe, durable). Gate bumper: TPU (flexible, quiet).

### Complete Parts List (18 parts)

| # | Part Name | Material | Layer Height | Infill | Supports | Notes |
|---|-----------|----------|--------------|--------|----------|-------|
| 1 | Main body / base | PETG | 0.25mm | 40% | No | Structural core, fits all internals |
| 2 | Food hopper | PETG | 0.25mm | 25% | No | 1–2 cup capacity, funnel angle ≥45° |
| 3 | Hopper lid | PETG | 0.2mm | 20% | No | Snap or screw-on, keeps food fresh |
| 4 | Auger tube | PETG | 0.2mm | 30% | No | Food-grade, smooth inner bore |
| 5 | Auger screw | PETG | 0.15mm | 60% | Yes | Precision thread, calibrate for portion accuracy |
| 6 | Motor mount | PETG | 0.25mm | 40% | No | Mounts auger drive motor |
| 7 | Electronics tray | PETG | 0.25mm | 30% | No | Holds Pi, Arduino, wiring; snap-in |
| 8 | Electronics cover | PETG | 0.2mm | 20% | No | Ventilation slots, removable |
| 9 | Bowl — open-front design | PETG | 0.15mm | 30% | No | No face-side wall; low 25mm side walls; floor extends forward; whisker-friendly |
| 10 | Bowl mounting bracket | PETG | 0.25mm | 40% | No | Secures bowl to main body |
| 11 | Camera mount / arm | PETG | 0.2mm | 35% | Yes | Angled for top-down cat face view |
| 12 | Camera cover / bezel | PETG | 0.2mm | 20% | No | Cosmetic, protects lens |
| 13 | **Bowl gate / flap — swing-up** *(RFID)* | PETG | 0.15mm | 40% | No | Hinged at top of bowl opening; swings up into feeder body when open. Cat's head and back are never in the path of travel. Servo-actuated |
| 14 | **Gate top hinge mount** *(RFID)* | PETG | 0.2mm | 40% | No | Mounts gate flap pivot at top of bowl opening; keeps gate travel path above the cat |
| 15 | **Antenna arch housing** *(RFID)* | PETG | 0.2mm | 25% | No | Overhead arch that positions the flat coil antenna horizontally above the approach zone, ~5–8cm above where the cat's shoulders sit while eating. Coil slots into a recessed channel inside the arch. Sized so gate flap retracts into the feeder body above it |
| 16 | **Gate servo bracket** *(RFID)* | PETG | 0.2mm | 40% | No | Mounts SG90 servo inside feeder body; linkage arm connects to top of gate flap |
| 17 | **TPU gate bumper** *(RFID)* | TPU | 0.2mm | 30% | No | Soft stop at top of gate travel (fully open position); prevents servo overrun and rattle |
| 18 | Feet / non-slip pads | TPU | 0.3mm | 15% | No | 4 per unit, press-fit into base |

### LulzBot Print Notes

- **PETG settings (Taz/Pro)**: 240°C nozzle / 70–80°C bed. 0.5mm nozzle recommended for structural parts. Dry filament before printing (PETG is hygroscopic).
- **TPU settings**: 220°C nozzle / 45°C bed. Disable retraction or minimize. Print slow (25–30mm/s).
- **Food contact parts** (auger, bowl): Use food-safe PETG, 3+ perimeters, 40%+ infill, food-safe lubricant only on auger.
- **Orientation**: Print auger screw vertically for thread integrity. Print gate flap flat (face down). Print antenna arch upright — thin walls need orientation parallel to print direction for layer bonding strength.
- **Antenna coil channel**: Leave a 2–3mm recessed groove inside the arch for the coil wire. Print without top-surface perimeters over the channel so coil can be seated and epoxied in place.

---

## 5. Wiring & Electronics

### Arduino Pin Map

| Pin | Function | Component |
|-----|----------|-----------|
| D2 | Stepper STEP or motor PWM | Motor driver |
| D3 | Stepper DIR or motor IN2 | Motor driver |
| D4 | Motor driver enable | L298N/A4988 EN |
| D5 | RFID modulation (MOD) | EM4095 |
| D6 | RFID RF off (RF_OFF) | EM4095 |
| D8 | Gate servo PWM | SG90 servo (swing-up gate) |
| D9 | Status LED | LED + resistor |
| **D10** | **RFID chip select (CS)** | **EM4095** |
| **D11** | **SPI MOSI** | **EM4095** |
| **D12** | **SPI MISO / DEMOD_OUT** | **EM4095** |
| **D13** | **SPI SCK** | **EM4095** |
| A2 | Buzzer | Active buzzer |
| A4 | I2C SDA (optional) | Load cell amp |
| A5 | I2C SCL (optional) | Load cell amp |

> **NOTE**: EM4095 is a **5V device** — no level converter needed. Power directly from Arduino 5V. The antenna coil connects to the COIL1/COIL2 pins on the EM4095 via the LC tank circuit (coil + tuning cap resonant at 134.2 kHz).

### Antenna Coil Design

The read range and reliability of the implanted chip detection depends entirely on the antenna coil. Key parameters:

| Parameter | Target value |
|-----------|-------------|
| Coil diameter | 10–15 cm flat spiral |
| Number of turns | 10–20 (tune for resonance) |
| Resonant frequency | 134.2 kHz (FDX-B) |
| Target read range | 5–8 cm (sufficient for chip ~2–4 cm below skin) |
| Coil position | Horizontal, centered in arch housing, ~5–8 cm above cat shoulder level |
| Coil orientation | Flat/horizontal — maximizes flux through chip (chip axis is vertical when cat's back is level) |

**LC tank resonance formula**: `f = 1 / (2π√(LC))` — choose L (coil inductance), solve for C. Wind coil, measure inductance with LCR meter or Arduino LC meter, then calculate exact cap value.

### Power Architecture

```
USB-C 5V 3A PSU
    ├── Raspberry Pi (5V via USB-C)
    └── Arduino Nano (5V via USB or Vin)
            ├── SG90 servo (5V, ~250mA peak)
            ├── Motor driver (5V logic, motor on separate 5-12V if needed)
            ├── Buzzer (5V)
            └── EM4095 + coil antenna (5V, ~50–100mA during read)
```

### RFID Wiring (EM4095 ↔ Arduino Nano)

| EM4095 Pin | Arduino Pin | Notes |
|-----------|-------------|-------|
| VCC | 5V | 5V native — no level shifter |
| GND | GND | |
| COIL1 | — | To LC tank coil (one end) |
| COIL2 | — | To LC tank coil (other end) |
| DEMOD_OUT | D12 (MISO) | Demodulated data out |
| MOD | D5 | Modulation input (for write capability) |
| RF_OFF | D6 | Pull high to disable RF field |
| SHD | GND | Pull low to enable (or use D-pin for software control) |

---

## 6. Arduino Firmware

### Responsibilities
- Drive the EM4095 antenna coil to read FDX-B implanted microchip UIDs; report to Pi over serial
- Actuate swing-up gate servo (open = flap retracts into body above bowl; close = flap blocks bowl opening)
- Drive auger motor for food dispensing (on Pi command)
- Sound buzzer for feeding alerts
- Optionally read load cell for bowl weight

### Key Serial Commands

```
Pi → Arduino:
  FEED:<grams>        — dispense specified grams
  GATE:OPEN           — open bowl gate flap
  GATE:CLOSE          — close bowl gate flap
  BUZZ:<pattern>      — trigger buzzer (1=short, 2=long, 3=error)

Arduino → Pi:
  EVENT:RFID:<uid>    — RFID tag detected with UID
  EVENT:WEIGHT:<g>    — bowl weight reading
  STATUS:READY        — boot complete
  STATUS:GATE:OPEN    — gate opened confirmation
  STATUS:GATE:CLOSED  — gate closed confirmation
```

### Gate State Machine

```
[CLOSED] → RFID detected → Pi validates → GATE:OPEN → [OPEN]
[OPEN] → 30s timeout → GATE:CLOSE → [CLOSED]
[OPEN] → cat leaves (weight sensor) → GATE:CLOSE → [CLOSED]
```

### Source Files
- `firmware/cat-feeder-arduino/cat-feeder-arduino.ino` — main sketch
- Libraries: `Servo`, `AccelStepper`
- RFID decoding: custom Manchester decoder for FDX-B bit stream from EM4095 DEMOD_OUT. No off-the-shelf Arduino library covers EM4095 + FDX-B directly — implementation uses timer interrupt to sample DEMOD_OUT at 2× bit rate and decode Manchester encoding.

---

## 7. Raspberry Pi Software

### Python Modules

| Module | File | Purpose |
|--------|------|---------|
| Main daemon | `main.py` | Orchestrates all services |
| Schedule manager | `scheduler.py` | Feeding schedule, cron-like |
| Serial bridge | `serial_bridge.py` | Pi ↔ Arduino serial comms |
| RFID access control | `rfid_access.py` | Tag registration, access decisions |
| Gate controller | `gate_controller.py` | Gate open/close logic, timeout |
| Camera / cat ID | `camera.py` | OpenCV, cat face detection |
| Database | `db.py` | SQLite ORM layer |
| API server | `api/app.py` | Flask/FastAPI REST API |

### Database Schema (SQLite)

```sql
-- Cats
CREATE TABLE cats (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  rfid_uid TEXT,           -- RFID collar tag UID
  photo_embedding BLOB,    -- Camera ID feature vector
  daily_portion_g INTEGER DEFAULT 80,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RFID tags
CREATE TABLE rfid_tags (
  id INTEGER PRIMARY KEY,
  uid TEXT UNIQUE NOT NULL,
  cat_id INTEGER REFERENCES cats(id),
  active BOOLEAN DEFAULT 1,
  registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Feeding events
CREATE TABLE feeding_log (
  id INTEGER PRIMARY KEY,
  cat_id INTEGER REFERENCES cats(id),
  feeder_id INTEGER,
  trigger TEXT,            -- 'schedule', 'manual', 'rfid'
  portion_g INTEGER,
  dispensed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RFID access events
CREATE TABLE access_log (
  id INTEGER PRIMARY KEY,
  rfid_uid TEXT,
  cat_id INTEGER REFERENCES cats(id),
  feeder_id INTEGER,
  result TEXT,             -- 'granted', 'denied', 'unknown_tag'
  camera_verify TEXT,      -- 'match', 'mismatch', 'skipped'
  accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Feeding schedules
CREATE TABLE schedules (
  id INTEGER PRIMARY KEY,
  feeder_id INTEGER,
  cat_id INTEGER REFERENCES cats(id),
  time TEXT NOT NULL,      -- 'HH:MM' format
  portion_g INTEGER,
  enabled BOOLEAN DEFAULT 1
);
```

### Cat Identification Pipeline

```
1. RFID tag detected (Arduino → Pi)
2. Pi looks up tag in rfid_tags table → gets cat_id
3. Pi sends GATE:OPEN to Arduino (physical access granted)
4. Camera captures frame, runs face detection (OpenCV)
5. Compare detected cat against registered cat embeddings
6. If RFID cat ≠ camera cat → log alert, optionally close gate
7. Log event to access_log with both RFID and camera results
```

---

## 8. Web Interface & API

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Feeder status, last event |
| GET | `/api/cats` | List registered cats |
| POST | `/api/cats` | Register new cat |
| GET | `/api/feeding-log` | Recent feeding history |
| POST | `/api/feed` | Manual feed trigger |
| GET | `/api/schedule` | Get feeding schedule |
| PUT | `/api/schedule` | Update schedule |
| GET | `/api/rfid/tags` | List registered RFID tags |
| POST | `/api/rfid/pair` | Pair new RFID tag to cat |
| DELETE | `/api/rfid/tags/:id` | Remove RFID tag |
| POST | `/api/gate/open` | Manual gate open |
| POST | `/api/gate/close` | Manual gate close |
| GET | `/api/access-log` | RFID access event log |
| GET | `/api/camera/snapshot` | Live camera frame |

### Web UI Features
- Dashboard: live status for both feeders
- Feeding history chart (per cat, per day)
- Schedule editor (drag-and-drop time slots)
- Cat profile management (photo, name, portion size)
- RFID tag management (pair, disable, re-pair)
- Access log with camera snapshots
- Manual feed button
- Gate control (override open/close)

---

## 9. Design Rationale

### Why Pi + Arduino (not Pi alone)?
The Pi GPIO is not well-suited for real-time PWM servo/stepper control, and 5V peripherals require level shifting. The Arduino handles time-critical 5V tasks reliably, while the Pi focuses on compute: camera inference, web serving, and RFID logic. USB serial provides a clean, reliable bridge.

### Why Implanted Chip (Not Collar Tag)?
The cat's ISO 11784/11785 FDX-B microchip is already implanted between the shoulders — it's permanent, can't be removed, lost, or swapped between cats. Collar tags require the cat to always be wearing the collar, and cats are notorious for losing them. Using the implanted chip eliminates an entire class of failure modes and means no new hardware needs to be attached to the cat.

### Why EM4095 + Custom Coil (Not RC522/MFRC522)?
The MFRC522 operates at 13.56 MHz (ISO 14443 / ISO 15693) — it physically cannot read implanted pet microchips, which operate at 134.2 kHz (FDX-B). The EM4095 is a 5V-native LF analog front end designed for exactly this frequency range. A custom-wound flat coil tuned to 134.2 kHz via an LC tank gives precise control over read range and antenna geometry.

### Why Overhead Antenna Arch (Not Front-Mounted)?
The microchip is between the cat's shoulder blades. As the cat lowers its head to the bowl, the shoulders are roughly level with the bowl rim. A front-mounted antenna would require the chip to pass horizontally through the read field — awkward geometry, poor coupling. An overhead flat coil positioned above the shoulder zone reads the chip at nearly optimal angle (coil plane parallel to the cat's back, flux perpendicular to chip axis) as the cat settles into eating position.

### Why RFID + Camera (dual-layer)?
RFID alone can't catch the edge case of one cat crouching right behind another. Camera alone is compute-heavy and can fail in low light. Together they provide reliable access: RFID opens the gate physically, camera confirms visually and catches anomalies.

### Why Open-Front Bowl?
Cats have sensitive whiskers. Deep or walled bowls cause "whisker fatigue" — discomfort when whiskers touch bowl sides during eating. The open-front design with low 25mm side walls and a forward-extending floor allows cats to eat comfortably without whisker contact, while still containing food adequately.

### Why RFID Gate Instead of Camera-Gated Gate?
Camera inference adds latency (100–500ms) on a Pi Zero. An RFID reader responds in <50ms and requires no compute. Using RFID for the physical gate and camera only for cross-verification gives fast, reliable physical access control with the smart verification layer as a safety net.

### Why Swing-Up Gate?
A downward-swinging or forward-opening gate creates a collision risk as the cat approaches or backs away. A swing-up gate retracts fully into the feeder body above the bowl — it is physically impossible for it to contact the cat's head or back during normal operation. The servo travel path is internal to the unit.

### Why Full 3D-Print?
Full 3D printing means every dimension can be tuned, iterated, and upgraded without new tooling. PETG is food-safe, durable, and easy to clean. Custom prints also enable purpose-fit cable routing, snap-fit assembly, and aesthetics not possible with off-the-shelf parts.

---

## 10. Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Wrong cat eats from open feeder | Medium | High | RFID gate physically blocks access; camera cross-checks |
| Chip not read as cat approaches | Low | Medium | Antenna coil sized and positioned for optimal coupling; cat must be in position to eat before gate opens anyway; retry logic in firmware polls at ~10 Hz |
| Chip read angle poor (cat tilts/crouches oddly) | Low | Low | Flat coil with 10–15cm diameter gives generous field volume; minor angle variation (<30°) has negligible effect on FDX-B coupling |
| Gate hits cat | Very Low | Medium | Swing-up design: gate retracts into body above the bowl — physically cannot contact the cat. TPU bumper stops servo at top of travel |
| Gate servo jam | Low | Medium | 30s auto-close timeout; manual override in web UI; swing-up means gravity assists closing |
| Two cats approach simultaneously | Low | Medium | Gate only opens for one UID at a time; coil read range limited to ~8cm so second cat is too far to trigger |
| Antenna LC tank drifts off resonance (temperature) | Low | Low | PETG housing insulates coil; resonance measured at room temp; minor drift at 134.2 kHz is tolerable given FDX-B chip sensitivity |
| Pi Zero underpowered for camera + web | Medium | Low | Optimize OpenCV pipeline; or upgrade to Pi 4 Model B |
| Auger clog | Medium | Medium | Food-grade PETG smooth bore; minimum 45° hopper angle; jam-detection via stall sensing |
| Food spoilage in hopper | Low | Medium | Hopper lid keeps food fresh; programmable max daily portion limits |
| Cat ignores feeder | Low | Low | Schedule-based buzz alert; treat-dispensing mode as incentive |

---

## 11. Project Phases & Deliverables

### Phase 1 — Hardware & Prototyping (Weeks 1–3)
- [ ] Source all components (BOM)
- [ ] Wind test coil, calculate LC tank cap for 134.2 kHz, verify resonance with LCR meter
- [ ] Breadboard test: Arduino + EM4095 + test coil → successfully read cat's implanted chip
- [ ] Verify read range with coil at different heights above cat's shoulders
- [ ] Breadboard test: swing-up gate servo travel and clearance geometry
- [ ] Validate serial protocol between Pi and Arduino
- [ ] Test camera with basic OpenCV cat detection

### Phase 2 — 3D Design & Printing (Weeks 2–5, parallel)
- [ ] CAD all 18 parts in Fusion 360 / FreeCAD
- [ ] Print and test-fit main body, hopper, auger
- [ ] Print and test bowl (open-front design) + gate mechanism
- [ ] Print RFID housing, gate servo bracket, TPU bumper
- [ ] Full assembly dry-run, iterate as needed

### Phase 3 — Firmware (Weeks 3–4)
- [ ] Arduino sketch: RFID reading, serial commands
- [ ] Gate state machine (open/close/timeout)
- [ ] Auger/motor control, portion calibration
- [ ] Buzzer patterns

### Phase 4 — Pi Software (Weeks 4–6)
- [ ] Serial bridge + scheduler
- [ ] SQLite schema + db.py
- [ ] rfid_access.py + gate_controller.py
- [ ] Camera pipeline + cat ID embeddings
- [ ] Flask API (all endpoints)
- [ ] Web UI

### Phase 5 — Integration & Testing (Weeks 6–8)
- [ ] Full system integration test (both units)
- [ ] RFID pairing for all cats
- [ ] Schedule setup + feeding calibration
- [ ] Edge case testing (simultaneous approach, lost tag, jams)
- [ ] Final assembly and cable management

### Final Deliverables
- [ ] 2× fully assembled Cat Feeder 5000 units
- [ ] Arduino firmware (`firmware/`)
- [ ] Pi Python software (`software/`)
- [ ] Web UI (`software/web/`)
- [ ] All 3D-print files (`3d-models/`)
- [ ] Wiring schematics (`hardware/wiring/`)
- [ ] Bill of materials (`hardware/bom/`)
- [ ] This master plan document (`docs/`)
