/**
 * Cat Feeder 5000 — Arduino Firmware
 * v1.0 (first iteration)
 *
 * Hardware:
 *   - Arduino Nano
 *   - EM4095 RFID AFE + custom flat coil (134.2 kHz, FDX-B)
 *   - SG90 servo (swing-up gate)
 *   - Motor driver (auger)
 *   - Active buzzer
 *   - Optional: status LED
 *
 * Serial protocol (115200 baud) with Raspberry Pi:
 *   Pi → Arduino:  FEED:<grams>, GATE:OPEN, GATE:CLOSE, BUZZ:<pattern>
 *   Arduino → Pi:  EVENT:RFID:<uid>, STATUS:READY, STATUS:GATE:OPEN,
 *                  STATUS:GATE:CLOSED, STATUS:FEED:DONE, ERROR:<msg>
 */

#include <Servo.h>

// ─── Pin Definitions ─────────────────────────────────────────────────────────
#define PIN_MOTOR_STEP   2    // Auger stepper STEP (or DC motor PWM)
#define PIN_MOTOR_DIR    3    // Auger stepper DIR (or DC motor IN2)
#define PIN_MOTOR_EN     4    // Motor driver enable (active LOW for A4988)
#define PIN_RFID_MOD     5    // EM4095 MOD (modulation)
#define PIN_RFID_RF_OFF  6    // EM4095 RF_OFF (pull HIGH to disable RF field)
#define PIN_GATE_SERVO   8    // SG90 servo PWM
#define PIN_LED          9    // Status LED
#define PIN_RFID_CS      10   // EM4095 CS / SHD (active LOW to enable)
#define PIN_RFID_DEMOD   12   // EM4095 DEMOD_OUT — Manchester encoded FDX-B data
#define PIN_BUZZER       A2   // Active buzzer

// ─── Gate Servo Angles ────────────────────────────────────────────────────────
#define GATE_CLOSED_ANGLE  10   // Servo angle when gate is closed (blocking bowl)
#define GATE_OPEN_ANGLE    95   // Servo angle when gate is open (retracted upward)

// ─── Feeding Constants ────────────────────────────────────────────────────────
#define STEPS_PER_GRAM     45   // Calibrate: stepper steps per gram of food
#define MOTOR_STEP_DELAY   800  // Microseconds between steps (lower = faster)

// ─── Gate Auto-Close ─────────────────────────────────────────────────────────
#define GATE_TIMEOUT_MS    30000  // Auto-close gate after 30 seconds

// ─── FDX-B / EM4095 RFID ─────────────────────────────────────────────────────
// FDX-B (ISO 11784/11785) bit rate = 134200 / 32 = ~4194 bps
// Manchester half-period = ~119 µs
// We sample DEMOD_OUT via Timer2 interrupt at ~2× bit rate (~238 µs period)
#define FDXB_BIT_PERIOD_US  238   // Full bit period in µs
#define FDXB_HALF_PERIOD_US 119   // Half bit period
#define FDXB_FRAME_BITS     128   // Full FDX-B frame length
#define FDXB_HEADER_BITS    11    // 11 leading '1' bits + stop '0'
#define FDXB_POLL_INTERVAL  100   // ms between read attempts

// ─── State ───────────────────────────────────────────────────────────────────
Servo gateServo;
bool  gateOpen         = false;
unsigned long gateOpenTime = 0;

// RFID sampling state (used in pollRFID)
uint8_t  rfidBuf[16];   // 128 bits = 16 bytes
uint8_t  rfidBitCount   = 0;
bool     rfidFrameReady = false;

// Serial command buffer
#define CMD_BUF_SIZE 32
char     cmdBuf[CMD_BUF_SIZE];
uint8_t  cmdLen = 0;

// ─── Setup ───────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);

  // Gate servo
  gateServo.attach(PIN_GATE_SERVO);
  gateServo.write(GATE_CLOSED_ANGLE);

  // Motor pins
  pinMode(PIN_MOTOR_STEP, OUTPUT);
  pinMode(PIN_MOTOR_DIR,  OUTPUT);
  pinMode(PIN_MOTOR_EN,   OUTPUT);
  digitalWrite(PIN_MOTOR_EN, HIGH);  // Disable motor at startup

  // RFID pins
  pinMode(PIN_RFID_DEMOD,  INPUT);
  pinMode(PIN_RFID_RF_OFF, OUTPUT);
  pinMode(PIN_RFID_MOD,    OUTPUT);
  pinMode(PIN_RFID_CS,     OUTPUT);
  digitalWrite(PIN_RFID_RF_OFF, LOW);   // RF field ON
  digitalWrite(PIN_RFID_CS,    LOW);    // Enable EM4095
  digitalWrite(PIN_RFID_MOD,   LOW);

  // Misc
  pinMode(PIN_LED,     OUTPUT);
  pinMode(PIN_BUZZER,  OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);
  digitalWrite(PIN_LED, HIGH);

  delay(200);
  Serial.println("STATUS:READY");
  blinkLed(3, 100);
}

// ─── Main Loop ────────────────────────────────────────────────────────────────
void loop() {
  readSerial();
  pollRFID();
  checkGateTimeout();
}

// ─── Serial Input ─────────────────────────────────────────────────────────────
void readSerial() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (cmdLen > 0) {
        cmdBuf[cmdLen] = '\0';
        handleCommand(cmdBuf);
        cmdLen = 0;
      }
    } else if (cmdLen < CMD_BUF_SIZE - 1) {
      cmdBuf[cmdLen++] = c;
    }
  }
}

void handleCommand(const char* cmd) {
  if (strcmp(cmd, "GATE:OPEN") == 0) {
    openGate();
  } else if (strcmp(cmd, "GATE:CLOSE") == 0) {
    closeGate();
  } else if (strncmp(cmd, "FEED:", 5) == 0) {
    int grams = atoi(cmd + 5);
    if (grams > 0 && grams <= 500) {
      dispenseFood(grams);
    } else {
      Serial.println("ERROR:INVALID_FEED_AMOUNT");
    }
  } else if (strncmp(cmd, "BUZZ:", 5) == 0) {
    int pattern = atoi(cmd + 5);
    buzzerPattern(pattern);
  } else {
    Serial.print("ERROR:UNKNOWN_CMD:");
    Serial.println(cmd);
  }
}

// ─── Gate Control ─────────────────────────────────────────────────────────────
void openGate() {
  gateServo.write(GATE_OPEN_ANGLE);
  gateOpen = true;
  gateOpenTime = millis();
  delay(300);  // Allow servo to reach position
  Serial.println("STATUS:GATE:OPEN");
  digitalWrite(PIN_LED, LOW);   // LED off when gate open = eating
}

void closeGate() {
  gateServo.write(GATE_CLOSED_ANGLE);
  gateOpen = false;
  delay(300);
  Serial.println("STATUS:GATE:CLOSED");
  digitalWrite(PIN_LED, HIGH);
}

void checkGateTimeout() {
  if (gateOpen && (millis() - gateOpenTime >= GATE_TIMEOUT_MS)) {
    closeGate();
  }
}

// ─── Food Dispensing ──────────────────────────────────────────────────────────
void dispenseFood(int grams) {
  long steps = (long)grams * STEPS_PER_GRAM;
  digitalWrite(PIN_MOTOR_DIR, HIGH);
  digitalWrite(PIN_MOTOR_EN,  LOW);   // Enable motor

  for (long i = 0; i < steps; i++) {
    digitalWrite(PIN_MOTOR_STEP, HIGH);
    delayMicroseconds(MOTOR_STEP_DELAY);
    digitalWrite(PIN_MOTOR_STEP, LOW);
    delayMicroseconds(MOTOR_STEP_DELAY);
  }

  digitalWrite(PIN_MOTOR_EN, HIGH);  // Disable motor
  Serial.println("STATUS:FEED:DONE");
  buzzerPattern(1);  // Short confirmation beep
}

// ─── RFID — FDX-B Manchester Decode ──────────────────────────────────────────
//
// EM4095 outputs a demodulated Manchester stream on DEMOD_OUT.
// FDX-B Manchester encoding:
//   '0' = LOW→HIGH transition at bit midpoint
//   '1' = HIGH→LOW transition at bit midpoint
// Full bit period = ~238 µs at 134.2 kHz / 32
//
// Strategy: poll DEMOD_OUT, detect transitions, measure timing,
// accumulate bits into a 128-bit buffer, validate and report UID.

#define DEMOD_SAMPLE_TIMEOUT_US 600   // Max time to wait for a transition
#define FDXB_SYNC_ONES          10    // Need 10 consecutive '1' bits for sync

void pollRFID() {
  static unsigned long lastPoll = 0;
  if (millis() - lastPoll < FDXB_POLL_INTERVAL) return;
  lastPoll = millis();

  uint8_t bits[FDXB_FRAME_BITS];
  int     bitCount = 0;
  int     syncCount = 0;
  bool    synced = false;

  // Sample the bit stream for up to ~50ms (enough for 1–2 frames)
  unsigned long deadline = micros() + 50000UL;

  while (micros() < deadline && bitCount < FDXB_FRAME_BITS) {
    int bit = readManchesterBit();
    if (bit < 0) break;  // Timeout reading bit

    if (!synced) {
      if (bit == 1) {
        syncCount++;
        if (syncCount >= FDXB_SYNC_ONES) synced = true;
      } else {
        // '0' after enough '1' bits = start of data
        if (syncCount >= FDXB_SYNC_ONES) {
          synced = true;
          bitCount = 0;  // Start collecting data bits
        } else {
          syncCount = 0;
        }
      }
    } else {
      bits[bitCount++] = (uint8_t)bit;
    }
  }

  if (bitCount >= 64) {
    // Attempt to extract UID from the frame
    char uid[24];
    if (parseFDXBFrame(bits, bitCount, uid)) {
      Serial.print("EVENT:RFID:");
      Serial.println(uid);
      buzzerPattern(1);
      blinkLed(2, 80);
    }
  }
}

// Read one Manchester-encoded bit from DEMOD_OUT.
// Returns 0 or 1, or -1 on timeout.
int readManchesterBit() {
  // Wait for line to settle, then sample at mid-bit
  // We measure the pulse width to determine bit value.

  unsigned long t0;
  int startLevel = digitalRead(PIN_RFID_DEMOD);

  // Wait for transition (start of bit period)
  t0 = micros();
  while (digitalRead(PIN_RFID_DEMOD) == startLevel) {
    if (micros() - t0 > DEMOD_SAMPLE_TIMEOUT_US) return -1;
  }

  // We are now at a transition — wait half a bit period to sample mid-bit
  delayMicroseconds(FDXB_HALF_PERIOD_US / 2);
  int midSample = digitalRead(PIN_RFID_DEMOD);

  // Skip rest of bit period
  delayMicroseconds(FDXB_HALF_PERIOD_US / 2);

  // In Manchester: LOW→HIGH = '0', HIGH→LOW = '1'
  // midSample after a rising edge is HIGH → was LOW before = '0'
  // midSample after a falling edge is LOW → was HIGH before = '1'
  return (startLevel == LOW) ? 0 : 1;
}

// Parse a FDX-B bit stream and extract the 64-bit UID as hex string.
// FDX-B frame (after header): 38-bit national ID + 10-bit country code
// + status bits + CRC. We extract national+country as the UID.
bool parseFDXBFrame(uint8_t* bits, int count, char* uidOut) {
  if (count < 64) return false;

  // Extract 38-bit national ID (bits 0–37)
  unsigned long long nationalID = 0;
  for (int i = 0; i < 38; i++) {
    nationalID = (nationalID << 1) | bits[i];
  }

  // Extract 10-bit country code (bits 38–47)
  uint16_t countryCode = 0;
  for (int i = 38; i < 48; i++) {
    countryCode = (countryCode << 1) | bits[i];
  }

  // Format as "CCC-NNNNNNNNNNNN" (country-national in decimal)
  // Or as hex for simplicity in first iteration
  unsigned long high = (unsigned long)(nationalID >> 16);
  unsigned long low  = (unsigned long)(nationalID & 0xFFFF);
  snprintf(uidOut, 24, "%03u-%05lu%04lu", countryCode, high, low);

  return (nationalID > 0 || countryCode > 0);
}

// ─── Buzzer Patterns ──────────────────────────────────────────────────────────
// Pattern 1 = short beep (access granted)
// Pattern 2 = two beeps (feeding complete)
// Pattern 3 = long error tone
void buzzerPattern(int pattern) {
  switch (pattern) {
    case 1:
      tone(PIN_BUZZER, 2000, 80);
      break;
    case 2:
      tone(PIN_BUZZER, 2000, 80);
      delay(150);
      tone(PIN_BUZZER, 2000, 80);
      break;
    case 3:
      tone(PIN_BUZZER, 800, 400);
      break;
    default:
      break;
  }
}

// ─── LED Helper ───────────────────────────────────────────────────────────────
void blinkLed(int times, int ms) {
  for (int i = 0; i < times; i++) {
    digitalWrite(PIN_LED, LOW);
    delay(ms);
    digitalWrite(PIN_LED, HIGH);
    delay(ms);
  }
}
