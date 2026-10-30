"""Session lifecycle connecting immutable files, reference selection and evidence.

An active lap intentionally does not survive restart: a fresh collector event is
required, so a late completion cannot accidentally resume the previous session.
"""
from pathlib import Path

from comparison import compare_segment
from reference import References


class Pipeline:
    def __init__(self, archive):
        self.archive = archive
        self.references = References()
        for lap in archive.laps():
            self.references.add(lap)
        self.references.select(archive.pinned())

    def import_reference(self, lap, path, format="official", track_length_m=None):
        self.archive.save(lap, Path(path).read_bytes(), format, track_length_m)
        self.references.add(lap)

    def select(self, lap_id):
        self.archive.pin(lap_id)
        self.references.select(lap_id)

    def begin(self, lap_id, session, car, layout, conditions):
        return self.references.begin(lap_id, session, car, layout, conditions)

    def disconnect(self):
        self.references.disconnect()

    def finish(self, lap, path, format="official", track_length_m=None):
        identity = (lap.id, lap.session, lap.car, lap.layout, lap.conditions)
        if identity != self.references.active:
            raise ValueError("Completion belongs to a different lap or session")
        reference = self.references.snapshot
        # Commit first; failed reads/writes leave the active lap available for retry.
        self.archive.save(lap, Path(path).read_bytes(), format, track_length_m,
                          reference.id if reference else None)
        self.references.finish(lap)
        return reference

    def finish_official(self, lap, directory, collector_lap_number):
        if type(collector_lap_number) is not int or collector_lap_number < 1:
            raise ValueError("Invalid collector lap number")
        # Upstream closes Lap N.tmp before renaming it to Lap N.telemetry.
        # Never infer validity/session from this filename: caller supplies metadata.
        return self.finish(lap, Path(directory) / f"Lap {collector_lap_number}.telemetry")

    def compare(self, lap_id, start_m, end_m):
        lap, recording, reference_id = self.archive.load(lap_id)
        if reference_id is None:
            raise ValueError("This lap had no compatible reference at its start")
        reference, reference_recording, _ = self.archive.load(reference_id)
        return compare_segment(recording, reference_recording, lap, reference, start_m, end_m)
