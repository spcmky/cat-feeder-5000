"""
Cat Feeder 5000 — Gate Controller
Manages the swing-up bowl gate state machine.
RFID controller calls open(); gate auto-closes after timeout.
"""
import threading
import logging
import time
from config import FEEDER_ID, GATE_TIMEOUT_S

log = logging.getLogger(__name__)


class GateController:
    def __init__(self, serial_bridge):
        self.serial = serial_bridge
        self.is_open = False
        self._current_cat = None
        self._timer = None
        self._lock = threading.Lock()

        # Listen for gate status from Arduino
        self.serial.on("STATUS:GATE:", self._on_gate_status)

    def open(self, cat: dict):
        with self._lock:
            if self.is_open:
                # Already open — reset timeout, maybe for same cat
                self._reset_timer()
                return

            self._current_cat = cat
            self.serial.send("GATE:OPEN")
            self.serial.send("BUZZ:1")
            log.info("Gate opened for %s", cat["name"])
            self._start_timer()

    def close(self, reason="manual"):
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
            self.serial.send("GATE:CLOSE")
            log.info("Gate closed (reason: %s)", reason)
            self._current_cat = None

    def _start_timer(self):
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(GATE_TIMEOUT_S, self._timeout_close)
        self._timer.daemon = True
        self._timer.start()

    def _reset_timer(self):
        self._start_timer()

    def _timeout_close(self):
        log.info("Gate auto-close after %ds timeout", GATE_TIMEOUT_S)
        self.close(reason="timeout")

    def _on_gate_status(self, line: str):
        if "OPEN" in line:
            self.is_open = True
        elif "CLOSED" in line:
            self.is_open = False
            self._current_cat = None

    @property
    def current_cat(self):
        return self._current_cat
