"""Local immutable lap archive. Metadata is supplied by a trusted collector adapter.

Parsing a file never establishes lap validity or condition compatibility.
Bytes, units, metadata, and digest are committed together in SQLite.
"""
from dataclasses import asdict
import hashlib
import json
import sqlite3

from reference import Lap
from telemetry import read_bytes


class Archive:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS laps (
                id TEXT PRIMARY KEY, metadata TEXT NOT NULL, raw BLOB NOT NULL,
                digest TEXT NOT NULL, format TEXT NOT NULL, track_length REAL,
                reference_id TEXT REFERENCES laps(id));
            CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
        """)
        self.db.execute("PRAGMA foreign_keys = ON")

    def close(self):
        self.db.close()

    def laps(self):
        return [Lap(**json.loads(row[0])) for row in self.db.execute(
            "SELECT metadata FROM laps ORDER BY id")]

    def save(self, lap, raw, format="official", track_length_m=None, reference_id=None):
        if not lap.id or not lap.session or not lap.car or not lap.layout:
            raise ValueError("Lap identity, session, car and layout are required")
        recording = read_bytes(raw, format, track_length_m)
        metadata = json.dumps(asdict(lap), sort_keys=True, allow_nan=False)
        values = (lap.id, metadata, raw, recording.sha256, format, track_length_m, reference_id)
        with self.db:
            previous = self.db.execute("SELECT * FROM laps WHERE id=?", (lap.id,)).fetchone()
            if previous is not None:
                if previous != values:
                    raise ValueError("Archived lap cannot be overwritten")
            else:
                self.db.execute("INSERT INTO laps VALUES (?,?,?,?,?,?,?)", values)
        return recording

    def load(self, lap_id):
        row = self.db.execute("SELECT * FROM laps WHERE id=?", (lap_id,)).fetchone()
        if row is None:
            raise ValueError("Archived lap not found")
        _, metadata, raw, digest, format, length, reference_id = row
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError("Archived telemetry checksum mismatch")
        return Lap(**json.loads(metadata)), read_bytes(raw, format, length), reference_id

    def pin(self, lap_id):
        if lap_id is not None and not self.load(lap_id)[0].usable:
            raise ValueError("Selected reference is unavailable or invalid")
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO settings VALUES ('pinned', ?)", (lap_id,))

    def pinned(self):
        row = self.db.execute("SELECT value FROM settings WHERE key='pinned'").fetchone()
        return row[0] if row else None
