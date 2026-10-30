import unittest
from reference import Lap, References


def lap(name, seconds=100, **changes):
    values = dict(id=name, session="practice", car="car", layout="layout",
                  conditions="dry/test", seconds=seconds, valid=True, complete=True)
    return Lap(**(values | changes))


def begin(store, name):
    return store.begin(name, "practice", "car", "layout", "dry/test")


class ReferenceTests(unittest.TestCase):
    def test_first_lap_then_better_and_invalid(self):
        s = References()
        self.assertIsNone(begin(s, "one"))
        self.assertIsNone(s.finish(lap("one")))
        self.assertEqual(begin(s, "two").id, "one")
        self.assertEqual(s.finish(lap("two", 99)).id, "one")
        self.assertEqual(begin(s, "three").id, "two")
        s.finish(lap("three", 80, valid=False))
        self.assertEqual(begin(s, "four").id, "two")

    def test_pin_changes_next_lap_only(self):
        s = References()
        s.add(lap("old", 100))
        s.add(lap("external", 110, source="imported"))
        self.assertEqual(begin(s, "current").id, "old")
        s.select("external")
        self.assertEqual(begin(s, "current").id, "old")
        s.finish(lap("current", 90))
        self.assertEqual(begin(s, "next").id, "external")

    def test_wrong_layout_and_unknown_conditions(self):
        s = References()
        s.add(lap("wrong", 80, layout="other"))
        s.add(lap("unknown", 80, conditions=None))
        self.assertIsNone(begin(s, "new"))

    def test_late_result_after_disconnect(self):
        s = References()
        begin(s, "old")
        s.disconnect()
        begin(s, "new")
        with self.assertRaises(ValueError):
            s.finish(lap("old"))
        self.assertNotIn("old", s.laps)

    def test_nonfinite_and_incomplete_not_references(self):
        s = References()
        s.add(lap("infinite", float("inf")))
        s.add(lap("incomplete", 20, complete=False))
        self.assertIsNone(begin(s, "new"))

    def test_ids_are_immutable(self):
        s = References()
        s.add(lap("one"))
        with self.assertRaises(ValueError):
            s.add(lap("one", 50))


if __name__ == "__main__":
    unittest.main()
