"""Independent known answers, mutation probe, and boundary tests (stdlib)."""
import contextlib
import io
import unittest
from unittest.mock import patch

import mandate as m


class MandateTests(unittest.TestCase):
    def test_course_known_answers(self):
        self.assertAlmostEqual(m.reserve_minimum(), 3.0)
        expected = {
            "A": ([100, 0, 14, 100, 0], [True]*5),
            "B": ([100, 0, 1, 85, 9], [True, True, False, False, False]),
            "C": ([100, 0, 2, 100, 8], [True, True, False, True, True]),
        }
        for name, (values, passes) in expected.items():
            with self.subTest(candidate=name):
                actual = list(m.evaluate(m.CANDIDATES[name]).values())
                self.assertEqual([v for v, _ in actual], values)
                self.assertEqual([p for _, p in actual], passes)

    def test_required_negative_weight_probe(self):
        # Copy: the required probe never changes the saved A inputs.
        probe = dict(m.CANDIDATES["A"])
        probe["Cash"], probe["Global equity index fund"] = -2, 64
        actual = list(m.evaluate(probe).values())
        self.assertEqual([v for v, _ in actual], [100, -2, 10, 100, 0])
        self.assertEqual([p for _, p in actual], [True, False, True, True, True])
        self.assertEqual(m.CANDIDATES["A"]["Cash"], 2)

    def test_attack_passes(self):
        self.assertTrue(all(p for _, p in m.evaluate(m.CANDIDATES["D"]).values()))

    def test_exact_boundaries_and_company_aggregation(self):
        weights = dict.fromkeys(m.HOLDINGS, 0)
        weights.update({"Cash": 3, "Private real estate fund": 10,
                        "Acme Corp stock": 4, "Acme Corp bonds": 4,
                        "Global equity index fund": 79})
        self.assertTrue(all(p for _, p in m.evaluate(weights).values()))
        weights["Acme Corp bonds"] += 0.01
        weights["Global equity index fund"] -= 0.01
        self.assertFalse(list(m.evaluate(weights).values())[-1][1])

    def test_threshold_computed_from_inputs(self):
        with patch.object(m, "QUARTERLY_DISTRIBUTION", 1.25):
            self.assertEqual(m.reserve_minimum(), 5)
            self.assertFalse(list(m.evaluate(m.CANDIDATES["C"]).values())[2][1])

    def test_invalid_sum_and_data(self):
        bad = dict(m.CANDIDATES["A"])
        bad["Cash"] += 1
        self.assertFalse(list(m.evaluate(bad).values())[0][1])
        bad["Cash"] = float("nan")
        with self.assertRaises(ValueError):
            m.evaluate(bad)
        with self.assertRaises(ValueError):
            m.evaluate({"unknown": 100})

    def test_output_defers_loss_rule(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            m.main()
        self.assertEqual(output.getvalue().count("requires CIO clarification"), 4)
        self.assertIn("fails 3 rule(s)", output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
