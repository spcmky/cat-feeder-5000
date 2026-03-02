"""
Cat Feeder 5000 — Database Layer
SQLite via sqlite3. Call init_db() once at startup.
"""
import sqlite3
import os
import logging
from config import DB_PATH

log = logging.getLogger(__name__)


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Create tables if they don't exist."""
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS cats (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                rfid_uid    TEXT,
                daily_g     INTEGER DEFAULT 80,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS rfid_tags (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                uid             TEXT UNIQUE NOT NULL,
                cat_id          INTEGER REFERENCES cats(id) ON DELETE SET NULL,
                active          INTEGER DEFAULT 1,
                registered_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS feeding_log (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                cat_id          INTEGER REFERENCES cats(id) ON DELETE SET NULL,
                feeder_id       INTEGER,
                trigger         TEXT,   -- 'schedule', 'manual', 'rfid'
                portion_g       INTEGER,
                dispensed_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS access_log (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                rfid_uid        TEXT,
                cat_id          INTEGER REFERENCES cats(id) ON DELETE SET NULL,
                feeder_id       INTEGER,
                result          TEXT,   -- 'granted', 'denied', 'unknown_tag'
                camera_verify   TEXT,   -- 'match', 'mismatch', 'skipped'
                accessed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS schedules (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                feeder_id   INTEGER,
                cat_id      INTEGER REFERENCES cats(id) ON DELETE CASCADE,
                time        TEXT NOT NULL,   -- 'HH:MM'
                portion_g   INTEGER DEFAULT 80,
                enabled     INTEGER DEFAULT 1
            );
        """)
    log.info("Database initialised at %s", DB_PATH)


# ── Cat helpers ───────────────────────────────────────────────────────────────

def get_all_cats():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM cats ORDER BY name")]

def get_cat(cat_id):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM cats WHERE id=?", (cat_id,)).fetchone()
        return dict(row) if row else None

def create_cat(name, daily_g=80):
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO cats (name, daily_g) VALUES (?,?)", (name, daily_g))
        return cur.lastrowid

def update_cat(cat_id, **kwargs):
    allowed = {"name", "daily_g"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    set_clause = ", ".join(f"{k}=?" for k in fields)
    with get_conn() as conn:
        conn.execute(f"UPDATE cats SET {set_clause} WHERE id=?",
                     list(fields.values()) + [cat_id])


# ── RFID tag helpers ──────────────────────────────────────────────────────────

def get_cat_by_uid(uid):
    """Return cat dict if uid is registered and active, else None."""
    with get_conn() as conn:
        row = conn.execute("""
            SELECT c.* FROM cats c
            JOIN rfid_tags t ON t.cat_id = c.id
            WHERE t.uid=? AND t.active=1
        """, (uid,)).fetchone()
        return dict(row) if row else None

def register_tag(uid, cat_id):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO rfid_tags (uid, cat_id) VALUES (?,?)
            ON CONFLICT(uid) DO UPDATE SET cat_id=excluded.cat_id, active=1
        """, (uid, cat_id))

def deactivate_tag(uid):
    with get_conn() as conn:
        conn.execute("UPDATE rfid_tags SET active=0 WHERE uid=?", (uid,))

def get_all_tags():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT t.*, c.name as cat_name
            FROM rfid_tags t LEFT JOIN cats c ON c.id=t.cat_id
            ORDER BY t.registered_at DESC
        """)]


# ── Log helpers ───────────────────────────────────────────────────────────────

def log_access(rfid_uid, cat_id, feeder_id, result, camera_verify="skipped"):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO access_log (rfid_uid, cat_id, feeder_id, result, camera_verify)
            VALUES (?,?,?,?,?)
        """, (rfid_uid, cat_id, feeder_id, result, camera_verify))

def log_feeding(cat_id, feeder_id, trigger, portion_g):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO feeding_log (cat_id, feeder_id, trigger, portion_g)
            VALUES (?,?,?,?)
        """, (cat_id, feeder_id, trigger, portion_g))
    log.info("Feeding logged: cat=%s feeder=%s trigger=%s grams=%s",
             cat_id, feeder_id, trigger, portion_g)

def get_feeding_log(limit=50):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT f.*, c.name as cat_name
            FROM feeding_log f LEFT JOIN cats c ON c.id=f.cat_id
            ORDER BY f.dispensed_at DESC LIMIT ?
        """, (limit,))]

def get_access_log(limit=50):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT a.*, c.name as cat_name
            FROM access_log a LEFT JOIN cats c ON c.id=a.cat_id
            ORDER BY a.accessed_at DESC LIMIT ?
        """, (limit,))]


# ── Schedule helpers ──────────────────────────────────────────────────────────

def get_schedules(feeder_id):
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT s.*, c.name as cat_name
            FROM schedules s LEFT JOIN cats c ON c.id=s.cat_id
            WHERE s.feeder_id=? AND s.enabled=1
            ORDER BY s.time
        """, (feeder_id,))]

def upsert_schedule(feeder_id, cat_id, time_str, portion_g):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO schedules (feeder_id, cat_id, time, portion_g)
            VALUES (?,?,?,?)
        """, (feeder_id, cat_id, time_str, portion_g))

def delete_schedule(schedule_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM schedules WHERE id=?", (schedule_id,))
