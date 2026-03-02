"""
Cat Feeder 5000 — Main Daemon
Entry point. Wires together all subsystems and runs forever.

Usage:
    python main.py

Environment variables (see config.py):
    FEEDER_ID, SERIAL_PORT, DB_PATH, CAMERA_ENABLED, API_PORT
"""
import logging
import signal
import sys
import threading

import db
from config import FEEDER_ID, API_HOST, API_PORT
from serial_bridge import SerialBridge
from rfid.gate_controller import GateController
from rfid.rfid_access import RFIDAccessController
from scheduler import FeedingScheduler
from camera.camera import CameraModule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/var/log/catfeeder.log"),
    ]
)
log = logging.getLogger(__name__)


def main():
    log.info("Cat Feeder 5000 starting — Feeder ID %d", FEEDER_ID)

    # ── Database ──────────────────────────────────────────────────────────────
    db.init_db()

    # ── Serial bridge ─────────────────────────────────────────────────────────
    serial = SerialBridge()
    serial.connect()

    # ── Gate controller ───────────────────────────────────────────────────────
    gate = GateController(serial)

    # ── RFID access controller ────────────────────────────────────────────────
    rfid = RFIDAccessController(serial, gate)

    # ── Feeding scheduler ─────────────────────────────────────────────────────
    scheduler = FeedingScheduler(serial)
    scheduler.start()

    # ── Camera ────────────────────────────────────────────────────────────────
    camera = CameraModule()
    camera.start()

    # ── Flask API ─────────────────────────────────────────────────────────────
    from api.app import create_app
    app = create_app(serial=serial, gate=gate, scheduler=scheduler, camera=camera)
    api_thread = threading.Thread(
        target=lambda: app.run(host=API_HOST, port=API_PORT, debug=False),
        daemon=True
    )
    api_thread.start()
    log.info("API server running on %s:%d", API_HOST, API_PORT)

    # ── Graceful shutdown ─────────────────────────────────────────────────────
    def shutdown(sig, frame):
        log.info("Shutdown signal received")
        scheduler.stop()
        camera.stop()
        gate.close(reason="shutdown")
        serial.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    log.info("Cat Feeder 5000 running. Press Ctrl+C to stop.")
    signal.pause()


if __name__ == "__main__":
    main()
