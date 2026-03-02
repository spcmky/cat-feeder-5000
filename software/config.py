"""
Cat Feeder 5000 — Configuration
Edit this file to match your hardware setup.
"""
import os

# ── Feeder Identity ────────────────────────────────────────────────────────────
FEEDER_ID = int(os.getenv("FEEDER_ID", "1"))   # 1 or 2
FEEDER_NAME = os.getenv("FEEDER_NAME", f"Feeder {FEEDER_ID}")

# ── Serial (Arduino) ──────────────────────────────────────────────────────────
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
SERIAL_BAUD = 115200
SERIAL_TIMEOUT = 2.0       # seconds

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = os.getenv("DB_PATH", "/var/lib/catfeeder/catfeeder.db")

# ── Camera ────────────────────────────────────────────────────────────────────
CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
CAMERA_ENABLED = os.getenv("CAMERA_ENABLED", "true").lower() == "true"
SNAPSHOT_DIR = "/var/lib/catfeeder/snapshots"

# ── Gate ──────────────────────────────────────────────────────────────────────
GATE_TIMEOUT_S = 30        # Auto-close after N seconds (also set in Arduino)

# ── API Server ────────────────────────────────────────────────────────────────
API_HOST = "0.0.0.0"
API_PORT = int(os.getenv("API_PORT", "8080"))
API_DEBUG = os.getenv("API_DEBUG", "false").lower() == "true"

# ── Feeding Defaults ──────────────────────────────────────────────────────────
DEFAULT_PORTION_G = 80     # Default grams per feeding if not per-cat configured
