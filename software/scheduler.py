"""
Cat Feeder 5000 — Feeding Scheduler
Polls the schedule table every minute and dispatches feedings at the right time.
"""
import threading
import logging
import time
from datetime import datetime
import db
from config import FEEDER_ID

log = logging.getLogger(__name__)


class FeedingScheduler:
    def __init__(self, serial_bridge):
        self.serial = serial_bridge
        self._running = False
        self._thread = None
        self._last_fired = {}   # schedule_id -> date string (prevent double-fire)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        log.info("Feeding scheduler started")

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            today = now.strftime("%Y-%m-%d")

            schedules = db.get_schedules(FEEDER_ID)
            for sched in schedules:
                if sched["time"] == current_time:
                    key = f"{sched['id']}:{today}"
                    if key not in self._last_fired:
                        self._last_fired[key] = True
                        self._fire(sched)

            # Clean up old keys (keep only today's)
            self._last_fired = {k: v for k, v in self._last_fired.items()
                                if k.endswith(today)}

            time.sleep(30)  # Check every 30s (precise enough for HH:MM granularity)

    def _fire(self, sched: dict):
        cat_name = sched.get("cat_name", f"cat {sched['cat_id']}")
        portion_g = sched.get("portion_g", 80)
        log.info("Schedule fire: %s -> %sg for %s", sched["time"], portion_g, cat_name)

        self.serial.send(f"FEED:{portion_g}")
        self.serial.send("BUZZ:2")
        db.log_feeding(sched["cat_id"], FEEDER_ID, "schedule", portion_g)

    def manual_feed(self, cat_id: int, portion_g: int):
        """Trigger a manual feeding immediately."""
        self.serial.send(f"FEED:{portion_g}")
        db.log_feeding(cat_id, FEEDER_ID, "manual", portion_g)
        log.info("Manual feed: cat=%s grams=%s", cat_id, portion_g)
