from dataclasses import replace
from pathlib import Path
import unittest
import uuid

from pipeline import Pipeline
from reference import Lap
from storage import Archive


RAW = b"0;0;0;0;2;5000;100;n/a;n/a;0;0;0;0;0\n100;0;1;0;2;5000;80;n/a;n/a;0;0;0;0;1000\n"


class PipelineTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent
        token = uuid.uuid4().hex
        self.dbpath = root / (token + '.sqlite')
        self.file = root / (token + '.telemetry')
        self.file.write_bytes(RAW)
        self.archive = Archive(self.dbpath)
        self.addCleanup(self.cleanup)
        self.pipeline = Pipeline(self.archive)
        self.lap = Lap('one', 'session', 'car', 'layout', 'dry', 1, True, True)

    def cleanup(self):
        self.archive.close()
        self.file.unlink(missing_ok=True)
        self.dbpath.unlink(missing_ok=True)

    def finish(self, lap):
        self.pipeline.begin(lap.id, lap.session, lap.car, lap.layout, lap.conditions)
        return self.pipeline.finish(lap, self.file)

    def test_frozen_reference_persists_across_restart(self):
        self.assertIsNone(self.finish(self.lap))
        second = replace(self.lap, id='two', seconds=.9)
        self.assertEqual(self.finish(second), self.lap)
        self.pipeline.select('one')
        self.archive.close()
        self.archive = Archive(self.dbpath)
        self.pipeline = Pipeline(self.archive)
        self.assertEqual(self.pipeline.references.pinned, 'one')
        result = self.pipeline.compare('two', 0, 100)
        self.assertEqual(result['reference_lap_id'], 'one')
        self.assertIsNone(result['driving_advice'])
        with self.assertRaises(ValueError):
            self.pipeline.compare('one', 0, 100)

    def test_source_change_cannot_mutate_archive(self):
        self.finish(self.lap)
        self.file.write_bytes(RAW.replace(b';80;', b';60;'))
        self.assertEqual(self.archive.load('one')[1].samples[-1].speed_kmh, 80)
        with self.assertRaises(ValueError):
            self.pipeline.import_reference(self.lap, self.file)
        self.assertEqual(len(self.archive.laps()), 1)

    def test_disconnect_restart_and_wrong_session_reject_late_completion(self):
        self.pipeline.begin('one', 'session', 'car', 'layout', 'dry')
        with self.assertRaises(ValueError):
            self.pipeline.finish(replace(self.lap, session='different'), self.file)
        self.pipeline.disconnect()
        with self.assertRaises(ValueError):
            self.pipeline.finish(self.lap, self.file)
        self.pipeline.begin('one', 'session', 'car', 'layout', 'dry')
        restarted = Pipeline(self.archive)
        with self.assertRaises(ValueError):
            restarted.finish(self.lap, self.file)
        self.assertEqual(self.archive.laps(), [])

    def test_bad_file_keeps_active_lap_for_retry(self):
        self.pipeline.begin('one', 'session', 'car', 'layout', 'dry')
        self.file.write_bytes(b'incomplete')
        with self.assertRaises(ValueError):
            self.pipeline.finish(self.lap, self.file)
        self.assertEqual(self.archive.laps(), [])
        self.assertIsNotNone(self.pipeline.references.active)
        self.file.write_bytes(RAW)
        self.pipeline.finish(self.lap, self.file)
        self.assertIsNone(self.pipeline.references.active)

    def test_invalid_external_lap_is_stored_but_never_selected(self):
        self.pipeline.import_reference(replace(self.lap, valid=False), self.file)
        with self.assertRaises(ValueError):
            self.pipeline.select('one')
        self.assertIsNone(self.pipeline.begin('two', 'session', 'car', 'layout', 'dry'))

    def test_archive_corruption_is_detected(self):
        self.finish(self.lap)
        with self.archive.db:
            self.archive.db.execute('UPDATE laps SET raw=?', (RAW + b'\n',))
        with self.assertRaisesRegex(ValueError, 'checksum'):
            self.archive.load('one')


if __name__ == '__main__':
    unittest.main()
