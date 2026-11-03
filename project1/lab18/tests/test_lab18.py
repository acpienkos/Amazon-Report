import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine import sec


class ExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cost = sec.analyze(json.loads((ROOT / 'sources/COST.json').read_text()), 'COST')
        cls.jpm = sec.analyze(json.loads((ROOT / 'sources/JPM.json').read_text()), 'JPM')

    def test_all_cost_rows_against_official_table(self):
        lines = (ROOT / 'sources/lab18.md').read_text(encoding='utf-8').splitlines()
        expected = []
        for line in lines:
            parts = [x.strip() for x in line.strip('|').split('|')]
            if len(parts) == 8 and __import__('re').fullmatch(r'202\d-\d\d-\d\d', parts[0]):
                expected.append(parts)
        self.assertEqual(len(expected), 5)
        keys = ['revenue', 'net_income', 'operating_cash_flow', 'capital_spending', 'equity', 'roe', 'owner_earnings']
        self.assertEqual(len(self.cost['rows']), 5)
        for row, values in zip(self.cost['rows'], expected):
            with self.subTest(end=values[0]):
                self.assertEqual(row['fiscal_year_end'], values[0])
                for key, value in zip(keys, values[1:]):
                    self.assertEqual(sec.display(key, row[key]).rstrip('%'), value)
        self.assertEqual(list(self.cost['checks'].values()), ['pass'] * 3)

    def test_jpm_missing_not_zero(self):
        self.assertEqual(len(self.jpm['rows']), 5)
        for r in self.jpm['rows']:
            for key in ['capital_spending', 'owner_earnings']:
                self.assertIsNone(r[key]['value'])
                self.assertEqual(sec.display(key, r[key]), 'not found')
        self.assertEqual(list(self.jpm['checks'].values())[1:], ['not known', 'not known'])
        self.assertIn('cannot judge owner earnings', (ROOT / 'memos/JPM.md').read_text())

    def test_memo_and_injected_number(self):
        memo = (ROOT / 'memos/COST.md').read_text(encoding='utf-8')
        self.assertEqual(sec.unsupported_numbers(memo, self.cost), [])
        self.assertEqual([x['number'] for x in sec.unsupported_numbers(memo + '\nROE was 40.0%.', self.cost)], ['40.0%'])
        self.assertTrue(sec.unsupported_numbers('ROE was -28.3%.', self.cost))

    def test_annual_filter(self):
        self.assertTrue(sec.annual({'start': '2022-08-29', 'end': '2023-09-03'}))
        for start in ['2023-06-01', '2023-01-01', '2021-01-01']:
            self.assertFalse(sec.annual({'start': start, 'end': '2023-09-03'}))

    def test_latest_filing_fallback_and_10k_only(self):
        def f(value, filed, form='10-K', start='2025-01-01'):
            return {'val': value, 'end': '2025-12-31', 'start': start, 'filed': filed, 'form': form}
        primary, fallback = sec.TAGS['revenue']
        data = {'facts': {'us-gaap': {
            primary: {'units': {'USD': [f(10, '2026-02-01'), f(12, '2026-03-01'), f(99, '2026-04-01', '10-Q'), f(98, '2026-05-01', start='2025-10-01')]}},
            fallback: {'units': {'USD': [f(20, '2026-06-01')]}},
        }}}
        self.assertEqual(sec.select(data, 'revenue', '2025-12-31')['value'], 12)
        data['facts']['us-gaap'][primary]['units']['USD'] = []
        self.assertEqual(sec.select(data, 'revenue', '2025-12-31')['value'], 20)
        self.assertEqual(sec.select(data, 'capital_spending', '2025-12-31')['value'], None)

    def test_invalid_equity_and_missing_checks(self):
        data = json.loads((ROOT / 'sources/COST.json').read_text())
        for equity in [0, -1]:
            test = copy.deepcopy(data)
            for f in test['facts']['us-gaap']['StockholdersEquity']['units']['USD']:
                f['val'] = equity
            r = sec.analyze(test, 'COST')
            self.assertTrue(all(x['roe']['value'] is None and x['liabilities_to_equity']['value'] is None for x in r['rows']))
            self.assertEqual(list(r['checks'].values())[0], 'not known')
        short = self.cost['rows'][:4]
        self.assertEqual(list(sec.checks(short).values()), ['not known'] * 3)


class AppTests(unittest.TestCase):
    def test_cost_chart_table_checks_and_memo_probe(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.dataframe), 1)
        self.assertEqual(len(app.table), 1)
        self.assertEqual(len(app.dataframe[0].value), 5)
        self.assertEqual(len(app.get('vega_lite_chart')), 1)
        self.assertTrue(any('Every numeric token matches' in x.value for x in app.success))
        app.text_area[0].set_value(app.text_area[0].value + '\nROE was 40.0%.').run()
        self.assertTrue(any('40.0%' in x.value for x in app.error))
        app.text_input[0].set_value('JPM').run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(all(x == 'not found' for x in app.dataframe[0].value['capital_spending']))
        self.assertIn('cannot judge owner earnings', app.text_area[0].value)


if __name__ == '__main__':
    unittest.main(verbosity=2)
