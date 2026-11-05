import copy
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import panel
sec = panel.sec

class PanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = json.loads((ROOT/'sources/COST.json').read_text())
        cls.cost = panel.analyze(cls.raw, 'COST')
        cls.nvda = panel.analyze(json.loads((ROOT/'sources/NVDA.json').read_text()), 'NVDA')
        cls.jpm = panel.analyze(json.loads((ROOT/'sources/JPM.json').read_text()), 'JPM')

    def test_all_lab18_cost_values_from_official_table(self):
        expected = []
        for line in (ROOT/'sources/lab-18-legend-investor-as-skill.md').read_text(encoding='utf-8').splitlines():
            parts = [x.strip() for x in line.strip('|').split('|')]
            if len(parts) == 8 and re.fullmatch(r'202\d-\d\d-\d\d', parts[0]):
                expected.append(parts)
        self.assertEqual(len(expected), 5)
        keys = ('revenue','net_income','operating_cash_flow','capital_spending','equity','roe','owner_earnings')
        for row, values in zip(self.cost['rows'], expected):
            self.assertEqual(row['fiscal_year_end'], values[0])
            for key, value in zip(keys, values[1:]):
                self.assertEqual(panel.display(key,row[key]).rstrip('%'),value)

    def test_new_cost_ratios_from_official_table(self):
        source = (ROOT/'sources/lab-19-legend-panel.md').read_text(encoding='utf-8')
        for label, key in [('Liabilities ÷ equity','liabilities_to_equity'), ('R&D ÷ revenue','rd_to_revenue')]:
            line = next(x for x in source.splitlines() if x.startswith('| '+label+' |'))
            expected = [x.strip() for x in line.strip('|').split('|')][1:]
            self.assertEqual([panel.display(key,r[key]) for r in self.cost['rows']],expected)
        self.assertIn(f"{self.cost['growth']:.2%}",source)

    def test_seven_cost_checks(self):
        values = [v for checks in self.cost['panel'].values() for v in checks.values()]
        self.assertEqual(values,['pass','pass','pass','fail','not known','pass','pass'])

    def test_probe_from_actual_skill_execution(self):
        report = json.loads((ROOT/'evidence/COST_probe_report.json').read_text())
        self.assertEqual(list(report['panel']['Cathie Wood'].values()),['pass','not known'])
        self.assertEqual(json.loads((ROOT/'.agents/skills/cathie-wood-panel/scripts/config.json').read_text())['growth_threshold'],.15)

    def test_nvda_cash_check_and_growth_recomputed(self):
        rows = self.nvda['rows']
        self.assertEqual(list(self.nvda['panel']['Buffett'].values()),['pass']*3)
        self.assertEqual(list(self.nvda['panel']['Cathie Wood'].values()),['pass']*2)
        self.assertEqual(list(self.nvda['panel']['Burry'].values()),['fail','pass'])
        self.assertAlmostEqual(self.nvda['growth'],(rows[-1]['revenue']['value']/rows[0]['revenue']['value'])**.25-1)
        self.assertTrue(any(r['operating_cash_flow']['value'] < r['net_income']['value'] for r in rows))

    def test_jpm_gaps_preserved(self):
        for row in self.jpm['rows']:
            for key in ('capital_spending','owner_earnings','research_and_development','rd_to_revenue'):
                self.assertIsNone(row[key]['value'])
                self.assertEqual(panel.display(key,row[key]),'not found')
        self.assertEqual(list(self.jpm['panel']['Buffett'].values())[1:],['not known']*2)
        self.assertIn('cannot judge owner earnings',(ROOT/'memos/JPM_buffett.md').read_text())

    def test_all_nine_memos_and_three_injections(self):
        for ticker, report in [('COST',self.cost),('NVDA',self.nvda),('JPM',self.jpm)]:
            for slug in panel.SLUGS:
                memo = panel.memo_path(ticker,slug).read_text(encoding='utf-8')
                self.assertEqual(panel.unsupported_numbers(memo,report),[])
                self.assertEqual([f['number'] for f in panel.unsupported_numbers(memo+' ROE 40.0%.',report)],['40.0%'])
        self.assertTrue(panel.unsupported_numbers('-28.3%',self.cost))

    def test_annual_not_quarterly(self):
        self.assertTrue(sec.annual({'start':'2022-08-29','end':'2023-09-03'}))
        self.assertFalse(sec.annual({'start':'2023-06-01','end':'2023-09-03'}))

    def test_latest_filing_10k_and_rd_fallback(self):
        p,f = sec.TAGS['research_and_development']
        def obs(v, filed, form='10-K', start='2025-01-01'):
            return {'val':v,'filed':filed,'form':form,'start':start,'end':'2025-12-31'}
        data = {'facts':{'us-gaap':{
            p:{'units':{'USD':[obs(1,'2026-02-01'),obs(2,'2026-03-01'),obs(99,'2026-04-01','10-Q'),obs(98,'2026-05-01',start='2025-10-01')]}},
            f:{'units':{'USD':[obs(3,'2026-06-01')]}}}}}
        self.assertEqual(sec.select(data,'research_and_development','2025-12-31')['value'],2)
        data['facts']['us-gaap'][p]['units']['USD']=[]
        self.assertEqual(sec.select(data,'research_and_development','2025-12-31')['value'],3)

    def test_nonpositive_equity(self):
        for value in (0,-1):
            data = copy.deepcopy(self.raw)
            for f in data['facts']['us-gaap']['StockholdersEquity']['units']['USD']:
                f['val']=value
            report = panel.analyze(data,'COST')
            self.assertTrue(all(r['roe']['value'] is None and r['liabilities_to_equity']['value'] is None for r in report['rows']))
            self.assertEqual(list(report['panel']['Burry'].values())[-1],'not known')

    def test_missing_revenue_and_incomplete_history(self):
        data = copy.deepcopy(self.raw)
        for tag in sec.TAGS['revenue']:
            data['facts']['us-gaap'].pop(tag,None)
        report = panel.analyze(data,'COST')
        self.assertIsNone(report['growth'])
        self.assertEqual(list(report['panel']['Cathie Wood'].values()),['not known']*2)
        report=panel.analyze({'facts':{}},'EMPTY')
        self.assertTrue(all(v=='not known' for checks in report['panel'].values() for v in checks.values()))

    def test_threshold_boundaries_unrounded(self):
        rows = copy.deepcopy(self.cost['rows'])
        rows[-1]['rd_to_revenue']['value']=.05
        self.assertEqual(list(panel.cathie_checks(rows,.15,.15).values()),['pass','pass'])
        rows[-1]['rd_to_revenue']['value']=.04999999
        self.assertEqual(list(panel.cathie_checks(rows,.14999999,.15).values()),['fail','fail'])
        with self.assertRaises(ValueError):
            panel.analyze(self.raw,'COST',float('nan'))

    def test_script_executions_and_shared_snapshot(self):
        runs=json.loads((ROOT/'evidence/skill_executions.json').read_text())
        self.assertEqual(len(runs),9)
        self.assertTrue(all(r['exit_code']==0 for r in runs))
        for ticker in ('COST','NVDA','JPM'):
            outputs=[(ROOT/'evidence'/f'{ticker}_{slug}_execution.txt').read_text(encoding='utf-8').split('Memo task:')[0] for slug in panel.SLUGS]
            self.assertEqual(len(set(outputs)),1)

class AppTests(unittest.TestCase):
    def app(self):
        from streamlit.testing.v1 import AppTest
        return AppTest.from_file(str(ROOT/'app.py')).run(timeout=40)

    def test_three_columns_verdicts_chart_table_and_flags(self):
        app=self.app()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(len(app.get('column')),3)
        self.assertEqual(len(app.text_area),3)
        self.assertEqual(len(app.success),3)
        self.assertEqual(len(app.get('vega_lite_chart')),1)
        self.assertEqual(len(app.dataframe[0].value),5)
        self.assertEqual(len(app.table[0].value),7)
        self.assertEqual(sum(x.value.startswith('Verdict:') and len(x.value.splitlines())==1 for x in app.markdown),3)
        for i in range(3):
            app.text_area[i].set_value(app.text_area[i].value+' ROE was 40.0%.').run()
            self.assertEqual(len(app.error),i+1)
            self.assertTrue(all('40.0%' in x.value for x in app.error))

    def test_probe_nvda_and_jpm_in_app(self):
        app=self.app()
        app.selectbox[0].select(.05).run()
        states=app.table[0].value
        self.assertEqual(states[states.Investor=='Cathie Wood'].Result.tolist(),['pass','not known'])
        app.selectbox[0].select(.15).run()
        app.text_input[0].set_value('NVDA').run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(len(app.success),3)
        self.assertEqual(app.table[0].value.Result.tolist(),['pass']*5+['fail','pass'])
        app.text_input[0].set_value('JPM').run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(all(x=='not found' for x in app.dataframe[0].value.capital_spending))
        self.assertEqual(len(app.success),3)

    def test_invalid_ticker_and_missing_saved_snapshot(self):
        app=self.app()
        app.text_input[0].set_value('../COST').run()
        self.assertEqual(len(app.exception),0)
        self.assertIn('Invalid ticker',app.error[0].value)
        app.text_input[0].set_value('NONEXISTENT').run()
        self.assertEqual(len(app.exception),0)
        self.assertIn('Unable to load',app.error[0].value)

if __name__=='__main__':
    unittest.main(verbosity=2)
