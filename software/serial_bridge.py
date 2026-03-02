"""
Cat Feeder 5000 — Serial Bridge
Manages the serial connection to the Arduino Nano.
Runs a background reader thread; exposes send() and on_event callbacks.
"""
import serial
import threading
import logging
import time
from config import SERIAL_PORT, SERIAL_BAUD, SERIAL_TIMEOUT

log = logging.getLogger(__name__)


class SerialBridge:
    def __init__(self):
        self._ser = None
        self._thread = None
        self._running = False
        self._lock = threading.Lock()
        self._callbacks = {}      # event_prefix -> callable(line)
        self.connected = False

    # ── Connection ────────────────────────────────────────────────────────────

    def connect(self):
        try:
            self._ser = serial.Serial(
                port=SERIAL_PORT,
                baudrate=SERIAL_BAUD,
                timeout=SERIAL_TIMEOUT
            )
            time.sleep(2)  # Allow Arduino to reset after serial open
            self.connected = True
            self._running = True
            self._thread = threading.Thread(target=self._reader, daemon=True)
            self._thread.start()
            log.info("Serial bridge connected on %s", SERIAL_PORT)
        except serial.SerialException as e:
            log.error("Failed to open serial port %s: %s", SERIAL_PORT, e)
            self.connected = False

    def disconnect(self):
        self._running = False
        if self._ser and self._ser.is_open:
            self._ser.close()
        self.connected = False
        log.info("Serial bridge disconnected")

    # ── Send ──────────────────────────────────────────────────────────────────

    def send(self, command: str):
        """Send a command string to the Arduino (newline appended)."""
        if not self.connected or not self._ser:
            log.warning("Serial not connected, cannot send: %s", command)
            return False
        with self._lock:
            try:
                self._ser.write((command + "\n").encode())
                log.debug("Serial TX: %s", command)
                return True
            except serial.SerialException as e:
                log.error("Serial write error: %s", e)
                self.connected = False
                return False

    # ── Event registration ────────────────────────────────────────────────────

    def on(self, prefix: str, callback):
        """Register a callback for lines starting with prefix."""
        self._callbacks[prefix] = callback

    # ── Reader thread ─────────────────────────────────────────────────────────

    def _reader(self):
        log.debug("Serial reader thread started")
        while self._running:
            try:
                if self._ser and self._ser.in_waiting:
                    line = self._ser.readline().decode(errors="replace").strip()
                    if line:
                        log.debug("Serial RX: %s", line)
                        self._dispatch(line)
                else:
                    time.sleep(0.01)
            except serial.SerialException as e:
                log.error("Serial read error: %s", e)
                self.connected = False
                break
            except Exception as e:
                log.exception("Unexpected serial error: %s", e)

    def _dispatch(self, line: str):
        for prefix, cb in self._callbacks.items():
            if line.startswith(prefix):
                try:
                    cb(line)
                except Exception as e:
                    log.exception("Callback error for '%s': %s", prefix, e)
                return
        log.debug("Unhandled serial line: %s", line)
