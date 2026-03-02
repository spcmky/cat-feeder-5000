"""
Cat Feeder 5000 — RFID Access Controller
Handles incoming RFID events from the serial bridge,
makes access decisions, triggers gate open/close.
"""
import logging
import db
from config import FEEDER_ID

log = logging.getLogger(__name__)


class RFIDAccessController:
    def __init__(self, serial_bridge, gate_controller):
        self.serial = serial_bridge
        self.gate = gate_controller
        self._last_uid = None

        # Register for RFID events from Arduino
        self.serial.on("EVENT:RFID:", self._on_rfid_event)

    def _on_rfid_event(self, line: str):
        """Called when Arduino reports EVENT:RFID:<uid>"""
        uid = line.split(":", 2)[-1].strip()
        if not uid:
            return

        # Debounce: ignore same tag within 3 seconds
        if uid == self._last_uid:
            return
        self._last_uid = uid

        log.info("RFID event: uid=%s", uid)
        self._process(uid)

    def _process(self, uid: str):
        cat = db.get_cat_by_uid(uid)

        if cat is None:
            log.warning("Unknown RFID tag: %s", uid)
            db.log_access(uid, None, FEEDER_ID, "unknown_tag")
            self.serial.send("BUZZ:3")   # Error tone
            return

        log.info("Access granted: %s (cat: %s)", uid, cat["name"])
        db.log_access(uid, cat["id"], FEEDER_ID, "granted")
        self.gate.open(cat)

    def reset_debounce(self):
        self._last_uid = None
