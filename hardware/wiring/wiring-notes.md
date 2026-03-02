# Cat Feeder 5000 — Wiring Reference
**Version**: 1.2

---

## Arduino Nano Pin Map

| Pin | Function               | Connected To               | Notes |
|-----|------------------------|----------------------------|-------|
| D2  | Motor STEP             | A4988 STEP / L298N PWM     | |
| D3  | Motor DIR              | A4988 DIR / L298N IN2      | |
| D4  | Motor Enable           | A4988 EN / L298N ENA       | Active LOW for A4988 |
| D5  | RFID MOD               | EM4095 MOD                 | Modulation input |
| D6  | RFID RF_OFF            | EM4095 RF_OFF              | Pull HIGH to disable RF field |
| D8  | Gate Servo PWM         | SG90 signal wire           | Swing-up gate |
| D9  | Status LED             | LED + 220Ω resistor → GND  | |
| D10 | RFID CS/SHD            | EM4095 SHD                 | Pull LOW to enable chip |
| D11 | SPI MOSI               | EM4095 (if SPI mode)       | |
| D12 | DEMOD_OUT              | EM4095 DEMOD_OUT           | Manchester encoded FDX-B data |
| D13 | SPI SCK                | EM4095 (if SPI mode)       | |
| A2  | Buzzer                 | Active buzzer +            | Buzzer − to GND |
| A4  | I2C SDA (optional)     | Load cell amp SDA          | |
| A5  | I2C SCL (optional)     | Load cell amp SCL          | |
| 5V  | Power out              | EM4095 VCC, servo VCC      | |
| GND | Ground                 | All component grounds      | Common ground |

---

## EM4095 Connections

| EM4095 Pin | Connects To        | Notes |
|------------|--------------------|-------|
| VDD        | Arduino 5V         | 5V native — no level shifter needed |
| GND        | Arduino GND        | |
| COIL1      | LC tank coil end A | Series with tuning cap to COIL2 |
| COIL2      | LC tank coil end B | |
| DEMOD_OUT  | Arduino D12        | Manchester-encoded FDX-B bit stream |
| MOD        | Arduino D5         | For write; tie LOW if read-only |
| RF_OFF     | Arduino D6         | Pull HIGH to disable field between reads |
| SHD        | Arduino D10 (GND)  | Pull LOW to enable; use pin for software control |

---

## LC Tank Antenna (134.2 kHz)

The antenna coil and tuning capacitor form a resonant LC tank at 134.2 kHz.

**Resonance formula**: `f = 1 / (2π × √(L × C))`

**Target**: f = 134,200 Hz

**Procedure**:
1. Wind flat spiral coil: ~12cm diameter, 28 AWG magnet wire, ~15 turns
2. Measure coil inductance (L) with LCR meter or Arduino LC meter sketch
3. Solve for C: `C = 1 / ((2π × f)² × L)`
4. Use closest standard capacitor value; trim with small parallel cap

**Example** (15 turns, ~12cm dia): L ≈ 60–80 µH → C ≈ 17–24 nF at 134.2 kHz

**Coil placement**: Horizontal, in the overhead antenna arch housing,
centered 5–8 cm above where the cat's shoulders sit while eating.

---

## SG90 Servo (Swing-Up Gate)

| Servo wire | Connects to     |
|------------|-----------------|
| Brown/Black | GND            |
| Red         | 5V             |
| Orange/Yellow | Arduino D8   |

- **Closed angle**: 10° (gate blocks bowl opening)
- **Open angle**: 95° (gate retracts upward into feeder body)
- Adjust angles in firmware `GATE_CLOSED_ANGLE` / `GATE_OPEN_ANGLE` constants

---

## Power Architecture

```
USB-C 5V 3A PSU
├── Raspberry Pi Zero 2 W (via USB-C)
│     └── USB-A → Arduino Nano (5V via USB)
│           ├── EM4095 + antenna coil (5V, ~50–100mA)
│           ├── SG90 servo (5V, ~250mA peak)
│           ├── Motor driver (5V logic; motor on same 5V rail)
│           ├── Buzzer (5V)
│           └── Status LED (5V via 220Ω)
└── (Optional) Separate 5–12V supply for auger motor if high torque needed
```

> **Note**: SG90 peak current (250mA) + motor can exceed USB current limits.
> If brownouts occur, power Pi and Arduino from separate USB ports on the PSU,
> or use a powered USB hub.

---

## Serial Connection (Pi ↔ Arduino)

- Pi USB-A → Arduino Nano USB Mini-B
- Port on Pi: `/dev/ttyUSB0` (or `/dev/ttyACM0` — check `dmesg` after plugging in)
- Baud rate: 115200
- Set `SERIAL_PORT` env variable in software config if different
