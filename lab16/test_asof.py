"""Known-answer and boundary tests; no external packages or network required."""
from datetime import date
from decimal import Decimal
import unittest

import asof


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.rows = asof.parse_rows(asof.DATA)
        self.panel, self.funnel = asof.filter_panel(self.rows, date(2026, 3, 31))

    def test_exact_dataset_and_default(self):
        self.assertEqual(asof.DECISION_DATE, "2026-03-31")
        self.assertEqual(len(self.rows), 12)
        self.assertEqual([r.row for r in self.rows], list(range(1, 13)))

    def test_ordered_funnel_and_panel(self):
        self.assertEqual([name for name, _ in self.funnel], [
            "Missing ticker", "Exact duplicate", "Published after decision date",
            "Superseded vintage"])
        self.assertEqual([[r.row for r in rows] for _, rows in self.funnel],
                         [[11], [7], [3, 8, 10], [2]])
        self.assertEqual([r.row for r in self.panel], [1, 4, 5, 6, 9, 12])
        audited = [r.row for _, rows in self.funnel for r in rows]
        self.assertEqual(sorted(audited + [r.row for r in self.panel]), list(range(1, 13)))

    def test_six_signals(self):
        naive, _ = asof.filter_panel(self.rows, None)
        for panel, expected in [
            (self.panel, {"AAA": ("1.98", 2, 103, 101),
                          "BBB": ("-1.02", 2, 97, 98), "CCC": ("0.91", 2, 111, 110)}),
            (naive, {"AAA": ("5.83", 3, 109, 103),
                     "BBB": ("-5.15", 3, 92, 97), "CCC": ("1.82", 2, 112, 110)})]:
            signals, unavailable = asof.calculate_signals(panel)
            self.assertFalse(unavailable)
            self.assertEqual(set(signals), set(expected))
            for ticker, (rounded, month, numerator, denominator) in expected.items():
                with self.subTest(ticker=ticker, rounded=rounded):
                    signal = signals[ticker]
                    self.assertEqual(f"{signal.percent:.2f}", rounded)
                    self.assertEqual(signal.month, date(2026, month, 1))
                    self.assertEqual(signal.percent,
                                     (Decimal(numerator) / Decimal(denominator) - 1) * 100)

    def test_revisions_independent_of_input_order(self):
        reversed_panel, _ = asof.filter_panel(list(reversed(self.rows)), date(2026, 3, 31))
        identity = lambda r: (r.ticker, r.month, r.published, r.value)
        self.assertEqual({identity(r) for r in reversed_panel},
                         {identity(r) for r in self.panel})
        self.assertIn(self.rows[3], self.panel)  # AAA March 25 revision
        self.assertIn(self.rows[11], self.panel)  # CCC April revision still unknowable

    def test_inclusive_cutoff(self):
        before, _ = asof.filter_panel(self.rows, date(2026, 3, 24))
        on, _ = asof.filter_panel(self.rows, date(2026, 3, 25))
        self.assertIn(2, [r.row for r in before])
        self.assertIn(4, [r.row for r in on])
        self.assertTrue(all(r.published <= date(2026, 3, 25) for r in on))

    def test_duplicate_identity_excludes_row_id_but_includes_publication(self):
        _, funnel = asof.filter_panel(self.rows, None)
        self.assertEqual([r.row for r in funnel[1][1]], [7])
        self.assertEqual(sorted(r.row for r in funnel[3][1]), [2, 12])
        extra = asof.parse_rows([(13, "BBB", "2026-02", "2026-03-11", 97.0)])
        panel, funnel = asof.filter_panel(self.rows + extra, date(2026, 3, 31))
        self.assertEqual([r.row for r in funnel[1][1]], [7])
        self.assertIn(13, [r.row for r in panel])

    def test_april_15_equals_naive_without_changing_default(self):
        april, _ = asof.filter_panel(self.rows, date(2026, 4, 15))
        naive, _ = asof.filter_panel(self.rows, None)
        self.assertEqual([r.row for r in april], [1, 3, 4, 5, 6, 8, 9, 10])
        self.assertEqual(asof.calculate_signals(april), asof.calculate_signals(naive))
        self.assertEqual(asof.DECISION_DATE, "2026-03-31")

    def test_empty_and_whitespace_ticker(self):
        self.assertEqual(asof.calculate_signals([]), ({}, {}))
        blank = asof.parse_rows([(1, "  ", "2026-01", "2026-02-01", 1)])
        panel, funnel = asof.filter_panel(blank, date(2026, 3, 31))
        self.assertEqual(panel, [])
        self.assertEqual(len(funnel[0][1]), 1)

    def test_unavailable_previous_month_and_zero(self):
        for data, reason in [
            ([(1, "X", "2026-01", "2026-02-01", 1)], "previous available month unavailable"),
            ([(1, "X", "2026-12", "2027-01-01", 0),
              (2, "X", "2027-01", "2027-02-01", 2)], "previous index is zero")]:
            with self.subTest(reason=reason, data=data):
                signals, unavailable = asof.calculate_signals(asof.parse_rows(data))
                self.assertFalse(signals)
                self.assertEqual(unavailable["X"], reason)

    def test_year_boundary(self):
        rows = asof.parse_rows([(1, "X", "2026-12", "2027-01-01", 100),
                                (2, "X", "2027-01", "2027-02-01", 105)])
        signals, _ = asof.calculate_signals(rows)
        self.assertEqual(signals["X"].percent, Decimal("5"))

    def test_preceding_available_month_and_dynamic_inputs(self):
        rows = asof.parse_rows([(81, "NEW", "2025-01", "2025-02-01", 20),
                                (82, "NEW", "2025-03", "2025-03-31", 25),
                                (83, "NEW", "2025-03", "2025-04-01", 30)])
        panel, funnel = asof.filter_panel(rows, date(2025, 3, 31))
        self.assertEqual([r.row for r in panel], [81, 82])
        self.assertEqual([r.row for r in funnel[2][1]], [83])
        self.assertEqual(asof.calculate_signals(panel)[0]["NEW"].percent, Decimal(25))
        naive, _ = asof.filter_panel(rows, None)
        self.assertEqual(asof.calculate_signals(naive)[0]["NEW"].percent, Decimal(50))

    def test_yields_and_separate_economic_warnings(self):
        before = list(self.panel)
        checks = asof.economic_checks(self.panel)
        self.assertEqual({r.row: f"{y:+.2f}" for r, y, _ in checks},
                         {1: "-0.99", 4: "-2.91", 5: "+2.04", 6: "+3.09",
                          9: "-9.09", 12: "-9.91"})
        self.assertEqual([r.row for r, y, _ in checks if y < 0], [1, 4, 9, 12])
        for row, _, concerns in checks:
            if row.ticker == "CCC":
                self.assertEqual(len(concerns), 2)
            elif row.ticker == "BBB":
                self.assertEqual(concerns, [])
        self.assertEqual(self.panel, before)
        self.assertEqual(asof.zero_coupon_yield(Decimal(80)), Decimal(25))
        with self.assertRaises(ValueError):
            asof.zero_coupon_yield(Decimal(0))

    def test_ambiguous_or_invalid_inputs(self):
        with self.assertRaises(ValueError):
            asof.parse_rows([asof.DATA[0], asof.DATA[0]])
        with self.assertRaises(ValueError):
            asof.parse_rows([(1, "X", "2026-01", "2026-02-01", "NaN")])
        conflicting = asof.parse_rows([(1, "X", "2026-01", "2026-02-01", 1),
                                       (2, "X", "2026-01", "2026-02-01", 2)])
        with self.assertRaisesRegex(ValueError, "Conflicting same-date"):
            asof.filter_panel(conflicting, None)
        with self.assertRaises(ValueError):
            asof.calculate_signals(conflicting)


if __name__ == "__main__":
    unittest.main()
