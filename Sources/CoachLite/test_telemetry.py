import uuid
import unittest
from pathlib import Path
from telemetry import read, segment


def row(distance, time, speed=100, tc="n/a", brake=0):
    return f"{distance};1;{brake};0;3;5000;{speed};{tc};n/a;0;0;0;0;{time}\n"


class TelemetryTests(unittest.TestCase):
    def setUp(self):
        test_root = Path(__file__).resolve().parent
        self.path = test_root / ("test-" + uuid.uuid4().hex + ".telemetry")
        self.path.touch(exist_ok=False)
        self.addCleanup(self.path.unlink, missing_ok=True)

    def load(self, text):
        self.path.write_text(text, encoding="utf-8")
        return read(self.path)

    def test_units_and_missing_preserved(self):
        r = self.load(row(0, 0) + row(10, 1000))
        self.assertEqual(r.summary()["elapsed_s"], 1)
        self.assertIsNone(r.samples[0].tc)
        self.assertEqual(r.summary()["missing"]["abs"], 2)
        self.assertFalse(r.summary()["coaching_ready"])

    def test_resets_rejected(self):
        for text in (row(10, 0) + row(0, 100), row(0, 100) + row(10, 0)):
            with self.assertRaises(ValueError):
                self.load(text)

    def test_nonfinite_and_percent_pedals_rejected(self):
        for tail in (row(10, 100, speed="nan"), row(10, 100, brake=50)):
            with self.assertRaises(ValueError):
                self.load(row(0, 0) + tail)

    def test_missing_time_not_invented(self):
        r = self.load(row(0, "n/a") + row(10, "n/a"))
        self.assertIsNone(r.summary()["elapsed_s"])

    def test_explicit_csv_units(self):
        self.path.write_text("DISTANCE,TIME,SPEED,THROTTLE,BRAKE\n0,0,100,1,0\n1,50,120,1,0\n")
        with self.assertRaises(ValueError):
            read(self.path, "csv-fraction-v1")
        r = read(self.path, "csv-fraction-v1", 2000)
        self.assertEqual(r.samples[-1].distance_m, 2000)
        self.assertEqual(r.summary()["elapsed_s"], 50)

    def test_segment_does_not_invent_boundary_time(self):
        r = self.load(row(0, 0, 90) + row(5, 100, 80) + row(10, 200, 100))
        result = segment(r, 0, 10)
        self.assertEqual(result["minimum_observed_speed_kmh"], 80)
        self.assertIsNone(result["exact_segment_time_s"])
        with self.assertRaises(ValueError):
            segment(r, 0, 20)


if __name__ == "__main__":
    unittest.main()
