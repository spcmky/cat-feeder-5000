# Cat Feeder 5000 — Master Plan
**Project**: Automated Multi-Cat Feeder System
**Units**: 2 identical feeders
**Date**: 2026-03-02
**Version**: 1.1 (RFID-gated bowl update)

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
- Enforce per-cat access using RFID collar tags (physical gate)
- Use a camera to visually verify which cat is present (cross-check)
- Allow full remote monitoring and control via a web app
- Are housed in professional-looking, fully 3D-printed enclosures

### Key Design Decisions
- **Open-front bowl**: Bowl has no walls at the cat's face side — low 25mm side walls, forward-extending floor. Whisker-friendly, comfortable eating position.
- **RFID-gated access**: A servo-actuated gate/flap physically blocks bowl access until the correct RFID collar tag is detected. Gate auto-closes after 30 seconds.
- **Dual-layer cat ID**: RFID handles physical enforcement; camera handles visual verification and smart alerts. Cross-verification catches edge cases (lost tags, tag swaps).
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
│  - MFRC522 RFID reader (SPI, pins D7/D10-D13)        │
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
| 1 | MFRC522 RFID reader module | $4 | RC522, SPI interface |
| 2 | RFID collar tags (13.56 MHz) | $2 | One per cat |
| 1 | Pi Camera Module 3 (or V2) | $25 | Wide angle preferred |
| 1 | SG90 micro servo (gate) | $3 | Bowl gate actuation |
| 1 | N20 gear motor or NEMA 14 stepper | $8 | Auger drive |
| 1 | Motor driver (L298N or A4988) | $3 | |
| 1 | Active buzzer 5V | $1 | Feeding alert |
| 1 | 5V 3A power supply (USB-C) | $10 | Powers Pi + Arduino |
| 1 | Micro SD card 32GB | $8 | Pi OS + data |
| 1 | Logic level converter (3.3V↔5V) | $2 | RFID on 3.3V |

### Mechanical & Hardware

| Qty | Component | Est. Cost | Notes |
|-----|-----------|-----------|-------|
| 1 | Food-grade PETG filament (1kg) | $25 | Main body, hopper, bowl |
| 1 | TPU filament (200g) | $8 | Gate bumper, feet |
| 1 | M3 heat-set inserts (50 pack) | $6 | Assembly fasteners |
| 1 | M3 screws assorted (100 pack) | $5 | |
| 1 | Silicone food bowl liner (optional) | $5 | Hygiene, replaceable |
| — | Misc: wire, connectors, JST | $10 | |

**Total per feeder: ~$145–175 depending on sourcing**

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
| 13 | **Bowl gate / flap** *(RFID)* | PETG | 0.15mm | 40% | No | Pivoting flap that blocks bowl opening; driven by gate servo |
| 14 | **Gate hinge mount** *(RFID)* | PETG | 0.2mm | 40% | No | Mounts gate flap pivot point to main body |
| 15 | **RFID reader housing** *(RFID)* | PETG | 0.2mm | 30% | No | Positions RC522 antenna flush at approach zone |
| 16 | **Gate servo bracket** *(RFID)* | PETG | 0.2mm | 40% | No | Mounts SG90 servo to gate hinge assembly |
| 17 | **TPU gate bumper** *(RFID)* | TPU | 0.2mm | 30% | No | Soft stop for gate flap; quiet, no rattle |
| 18 | Feet / non-slip pads | TPU | 0.3mm | 15% | No | 4 per unit, press-fit into base |

### LulzBot Print Notes

- **PETG settings (Taz/Pro)**: 240°C nozzle / 70–80°C bed. 0.5mm nozzle recommended for structural parts. Dry filament before printing (PETG is hygroscopic).
- **TPU settings**: 220°C nozzle / 45°C bed. Disable retraction or minimize. Print slow (25–30mm/s).
- **Food contact parts** (auger, bowl): Use food-safe PETG, 3+ perimeters, 40%+ infill, food-safe lubricant only on auger.
- **Orientation**: Print auger screw vertically for thread integrity. Print gate flap flat.

---

## 5. Wiring & Electronics

### Arduino Pin Map

| Pin | Function | Component |
|-----|----------|-----------|
| D2 | Stepper STEP or motor PWM | Motor driver |
| D3 | Stepper DIR or motor IN2 | Motor driver |
| D4 | Motor driver enable | L298N/A4988 EN |
| **D7** | **RFID SDA (SS/CS)** | **MFRC522** |
| D8 | Gate servo PWM | SG90 servo |
| D9 | Status LED | LED + resistor |
| **D10** | **RFID SS (alt)** | **MFRC522** |
| **D11** | **RFID MOSI** | **MFRC522** |
| **D12** | **RFID MISO** | **MFRC522** |
| **D13** | **RFID SCK** | **MFRC522** |
| A2 | Buzzer | Active buzzer |
| A4 | I2C SDA (optional) | Load cell amp |
| A5 | I2C SCL (optional) | Load cell amp |

> **CRITICAL**: MFRC522 is a 3.3V device. Use logic level converter or voltage divider on MOSI/SCK/SDA lines. Power from Arduino 3.3V pin (max 50mA — sufficient for RC522).

### Power Architecture

```
USB-C 5V 3A PSU
    ├── Raspberry Pi (5V via USB-C)
    └── Arduino Nano (5V via USB or Vin)
            ├── SG90 servo (5V, ~250mA peak)
            ├── Motor driver (5V logic, motor on separate 5-12V if needed)
            ├── Buzzer (5V)
            └── MFRC522 (3.3V from Arduino 3V3 pin)
```

### RFID Wiring (RC522 ↔ Arduino Nano)

| RC522 Pin | Arduino Pin | Voltage |
|-----------|-------------|---------|
| SDA | D7 (via level converter) | 3.3V |
| SCK | D13 (via level converter) | 3.3V |
| MOSI | D11 (via level converter) | 3.3V |
| MISO | D12 | 3.3V out |
| IRQ | Not connected | — |
| GND | GND | — |
| RST | D9 (or tied high) | 3.3V |
| 3.3V | 3.3V | 3.3V |

---

## 6. Arduino Firmware

### Responsibilities
- Read RFID tags via MFRC522 and report UIDs to Pi over serial
- Actuate gate servo (open/close on Pi command)
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
- Libraries: `MFRC522`, `Servo`, `AccelStepper`

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

### Why RFID + Camera (dual-layer)?
RFID alone can't distinguish if a cat removes/loses their collar. Camera alone is compute-heavy and can fail in low light. Together they provide reliable access: RFID opens the gate physically, camera confirms visually and catches anomalies (tag swap, wrong cat sneaking in behind the correct one).

### Why Open-Front Bowl?
Cats have sensitive whiskers. Deep or walled bowls cause "whisker fatigue" — discomfort when whiskers touch bowl sides during eating. The open-front design with low 25mm side walls and a forward-extending floor allows cats to eat comfortably without whisker contact, while still containing food adequately.

### Why RFID Gate Instead of Camera-Gated Gate?
Camera inference adds latency (100–500ms) on a Pi Zero. An RFID reader responds in <50ms and requires no compute. Using RFID for the physical gate and camera only for cross-verification gives fast, reliable physical access control with the smart verification layer as a safety net.

### Why Full 3D-Print?
Full 3D printing means every dimension can be tuned, iterated, and upgraded without new tooling. PETG is food-safe, durable, and easy to clean. Custom prints also enable purpose-fit cable routing, snap-fit assembly, and aesthetics not possible with off-the-shelf parts.

---

## 10. Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Wrong cat eats from open feeder | Medium | High | RFID gate physically blocks access; camera cross-checks |
| Cat loses/removes RFID collar | Medium | Medium | Camera fallback; alert sent; schedule-based fallback feeding |
| Gate servo jam | Low | Medium | 30s auto-close timeout; manual override in web UI; TPU bumper absorbs impact |
| Two cats approach simultaneously | Low | Medium | Gate only opens for one UID at a time; second cat waits or is blocked |
| RFID range bleed (reads from too far) | Low | Low | Antenna positioned in housing flush to approach zone; minimal read range at 13.56 MHz |
| RFID tag collision (two collars near reader) | Low | Low | RC522 handles anti-collision in hardware; first UID wins |
| Pi Zero underpowered for camera + web | Medium | Low | Optimize OpenCV pipeline; or upgrade to Pi 4 Model B |
| Auger clog | Medium | Medium | Food-grade PETG smooth bore; minimum 45° hopper angle; jam-detection via stall sensing |
| Food spoilage in hopper | Low | Medium | Hopper lid keeps food fresh; programmable max daily portion limits |
| Cat ignores feeder | Low | Low | Schedule-based buzz alert; treat-dispensing mode as incentive |

---

## 11. Project Phases & Deliverables

### Phase 1 — Hardware & Prototyping (Weeks 1–3)
- [ ] Source all components (BOM)
- [ ] Breadboard test: Arduino + MFRC522 + servo + motor
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
