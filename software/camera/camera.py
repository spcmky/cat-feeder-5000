"""
Cat Feeder 5000 — Camera Module
Captures frames from Pi Camera and provides cat identification.
First iteration: motion/presence detection + placeholder for ML cat ID.
"""
import logging
import os
import time
from datetime import datetime
from config import CAMERA_INDEX, CAMERA_ENABLED, SNAPSHOT_DIR

log = logging.getLogger(__name__)

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    log.warning("cv2 not available — camera disabled")


class CameraModule:
    def __init__(self):
        self.enabled = CAMERA_ENABLED and CV2_AVAILABLE
        self._cap = None
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    def start(self):
        if not self.enabled:
            log.info("Camera disabled or cv2 unavailable")
            return
        self._cap = cv2.VideoCapture(CAMERA_INDEX)
        if not self._cap.isOpened():
            log.error("Failed to open camera index %d", CAMERA_INDEX)
            self.enabled = False
            return
        # Set reasonable resolution for Pi
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        log.info("Camera started (index %d)", CAMERA_INDEX)

    def stop(self):
        if self._cap:
            self._cap.release()
            self._cap = None

    def capture_snapshot(self) -> str | None:
        """Capture a single frame and save to SNAPSHOT_DIR. Returns file path."""
        if not self.enabled or not self._cap:
            return None
        ret, frame = self._cap.read()
        if not ret:
            log.warning("Camera read failed")
            return None
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(SNAPSHOT_DIR, f"snap_{ts}.jpg")
        cv2.imwrite(path, frame)
        return path

    def identify_cat(self, known_cats: list) -> dict | None:
        """
        First iteration: presence detection only.
        Returns None (no cat detected) or {'cat_id': None, 'confidence': 0.0}
        meaning 'something is there but we can't ID it yet'.

        TODO: Replace with MobileNet/ResNet embedding comparison.
        """
        if not self.enabled or not self._cap:
            return None

        ret, frame = self._cap.read()
        if not ret:
            return None

        # Simple presence check: look for motion / large foreground blob
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Without a background model, just check mean brightness change
        # as a very rough presence detector for first iteration
        mean_val = cv2.mean(gray)[0]
        if mean_val < 10:
            return None   # Too dark, skip

        # Placeholder: return unidentified presence
        return {"cat_id": None, "confidence": 0.0, "note": "presence_detected"}

    def get_latest_snapshot_path(self) -> str | None:
        """Return path to most recent snapshot file."""
        try:
            files = sorted([
                os.path.join(SNAPSHOT_DIR, f)
                for f in os.listdir(SNAPSHOT_DIR)
                if f.endswith(".jpg")
            ])
            return files[-1] if files else None
        except Exception:
            return None
