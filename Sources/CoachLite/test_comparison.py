from dataclasses import replace
import unittest
from telemetry import Recording, Sample
from reference import Lap
from comparison import compare_segment


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.lap = Lap("current", "session", "car", "layout", "dry", 100, True, True)
        self.ref = replace(self.lap, id="reference")
        self.current = Recording((Sample(0, 80, 0, 1, 0, None, None),
                                  Sample(10, 100, 1, 0, 1, None, None)), "a", "test")
        self.reference = Recording((Sample(0, 90, 0, 1, 0, None, None),
                                    Sample(10, 120, 1, 0, 1, None, None)), "b", "test")

    def test_signed_deltas_and_provenance(self):
        result = compare_segment(self.current, self.reference, self.lap, self.ref, 0, 10)
        self.assertEqual(result["delta_current_minus_reference"]["minimum_observed_speed_kmh"], -10)
        self.assertEqual(result["current"]["source_sha256"], "a")
        self.assertIsNone(result["driving_advice"])

    def test_rejects_wrong_reference_and_self(self):
        for ref in (self.lap, replace(self.ref, layout="wrong"),
                    replace(self.ref, conditions=None), replace(self.ref, valid=False)):
            with self.assertRaises(ValueError):
                compare_segment(self.current, self.reference, self.lap, ref, 0, 10)


if __name__ == "__main__":
    unittest.main()
