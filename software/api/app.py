"""
Cat Feeder 5000 — Flask REST API
All endpoints for the web UI and external control.
"""
import os
import logging
from flask import Flask, jsonify, request, send_file, abort
import db
from config import FEEDER_ID

log = logging.getLogger(__name__)


def create_app(serial=None, gate=None, scheduler=None, camera=None):
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # Inject dependencies via app context
    app.serial    = serial
    app.gate      = gate
    app.scheduler = scheduler
    app.camera    = camera

    # ── Status ────────────────────────────────────────────────────────────────

    @app.route("/api/status")
    def status():
        return jsonify({
            "feeder_id":   FEEDER_ID,
            "gate_open":   gate.is_open if gate else False,
            "gate_cat":    gate.current_cat if gate else None,
            "serial_ok":   serial.connected if serial else False,
            "camera_ok":   camera.enabled if camera else False,
        })

    # ── Cats ──────────────────────────────────────────────────────────────────

    @app.route("/api/cats", methods=["GET"])
    def list_cats():
        return jsonify(db.get_all_cats())

    @app.route("/api/cats", methods=["POST"])
    def create_cat():
        data = request.get_json(force=True)
        name = data.get("name", "").strip()
        if not name:
            return jsonify({"error": "name required"}), 400
        daily_g = int(data.get("daily_g", 80))
        cat_id = db.create_cat(name, daily_g)
        return jsonify({"id": cat_id, "name": name}), 201

    @app.route("/api/cats/<int:cat_id>", methods=["PATCH"])
    def update_cat(cat_id):
        data = request.get_json(force=True)
        db.update_cat(cat_id, **data)
        return jsonify(db.get_cat(cat_id))

    # ── Feeding ───────────────────────────────────────────────────────────────

    @app.route("/api/feed", methods=["POST"])
    def manual_feed():
        data = request.get_json(force=True)
        cat_id  = data.get("cat_id")
        portion = int(data.get("portion_g", 80))
        if not cat_id:
            return jsonify({"error": "cat_id required"}), 400
        if scheduler:
            scheduler.manual_feed(cat_id, portion)
        return jsonify({"status": "dispensing", "portion_g": portion})

    @app.route("/api/feeding-log")
    def feeding_log():
        limit = int(request.args.get("limit", 50))
        return jsonify(db.get_feeding_log(limit))

    # ── Schedule ──────────────────────────────────────────────────────────────

    @app.route("/api/schedule")
    def get_schedule():
        return jsonify(db.get_schedules(FEEDER_ID))

    @app.route("/api/schedule", methods=["POST"])
    def add_schedule():
        data = request.get_json(force=True)
        cat_id    = data.get("cat_id")
        time_str  = data.get("time")       # "HH:MM"
        portion_g = int(data.get("portion_g", 80))
        if not cat_id or not time_str:
            return jsonify({"error": "cat_id and time required"}), 400
        db.upsert_schedule(FEEDER_ID, cat_id, time_str, portion_g)
        return jsonify({"status": "created"}), 201

    @app.route("/api/schedule/<int:schedule_id>", methods=["DELETE"])
    def delete_schedule(schedule_id):
        db.delete_schedule(schedule_id)
        return jsonify({"status": "deleted"})

    # ── RFID Tags ─────────────────────────────────────────────────────────────

    @app.route("/api/rfid/tags")
    def list_tags():
        return jsonify(db.get_all_tags())

    @app.route("/api/rfid/pair", methods=["POST"])
    def pair_tag():
        data   = request.get_json(force=True)
        uid    = data.get("uid", "").strip()
        cat_id = data.get("cat_id")
        if not uid or not cat_id:
            return jsonify({"error": "uid and cat_id required"}), 400
        db.register_tag(uid, cat_id)
        return jsonify({"status": "paired", "uid": uid, "cat_id": cat_id}), 201

    @app.route("/api/rfid/tags/<uid>", methods=["DELETE"])
    def remove_tag(uid):
        db.deactivate_tag(uid)
        return jsonify({"status": "deactivated", "uid": uid})

    # ── Gate ──────────────────────────────────────────────────────────────────

    @app.route("/api/gate/open", methods=["POST"])
    def gate_open():
        if not gate:
            return jsonify({"error": "gate not available"}), 503
        # Manual override — open with no cat context
        if serial:
            serial.send("GATE:OPEN")
        return jsonify({"status": "opening"})

    @app.route("/api/gate/close", methods=["POST"])
    def gate_close():
        if not gate:
            return jsonify({"error": "gate not available"}), 503
        gate.close(reason="manual_api")
        return jsonify({"status": "closing"})

    # ── Access Log ────────────────────────────────────────────────────────────

    @app.route("/api/access-log")
    def access_log():
        limit = int(request.args.get("limit", 50))
        return jsonify(db.get_access_log(limit))

    # ── Camera ────────────────────────────────────────────────────────────────

    @app.route("/api/camera/snapshot")
    def snapshot():
        if not camera or not camera.enabled:
            return jsonify({"error": "camera not available"}), 503
        path = camera.capture_snapshot()
        if not path:
            return jsonify({"error": "capture failed"}), 500
        return send_file(path, mimetype="image/jpeg")

    @app.route("/api/camera/latest")
    def latest_snapshot():
        if not camera:
            return jsonify({"error": "camera not available"}), 503
        path = camera.get_latest_snapshot_path()
        if not path:
            abort(404)
        return send_file(path, mimetype="image/jpeg")

    # ── Error handlers ────────────────────────────────────────────────────────

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "internal server error"}), 500

    return app
