import csv
import importlib.util
import json
import math
from pathlib import Path
import unittest
import portfolio as p
import mandate as m

HERE = Path(__file__).resolve().parent

class PortfolioTests(unittest.TestCase):
    def test_known_answers(self):
        self.assertEqual(p.ASSETS, ("Treasury bills", "Treasury 10-year note", "Investment-grade bond fund", "Global equity index fund"))
        cov = p.covariance_matrix(p.VOLATILITIES, p.CORRELATIONS)
        self.assertAlmostEqual(cov[2][3], .0024)
        for (name,w), ret, vol, reserve, meets in zip(p.baselines().items(), (.068,.052,.0377), (.1046,.0521,.0105), (0,.5,.903), (True,False,False)):
            self.assertAlmostEqual(sum(w),1)
            self.assertAlmostEqual(p.expected_return(w,p.RETURNS),ret,delta=.00005)
            self.assertAlmostEqual(p.portfolio_volatility(w,cov),vol,delta=.00005)
            self.assertAlmostEqual(p.reserve_allocation(w),reserve,delta=.0005)
            self.assertEqual(p.meets_objective(p.expected_return(w,p.RETURNS)),meets)
        self.assertAlmostEqual(p.portfolio_variance(p.BENCHMARK,cov),.010944)
        self.assertEqual(p.baselines()["Equal weight"],(.25,)*4)
        inverse=p.inverse_volatility_weights(p.VOLATILITIES)
        self.assertEqual([round(x*100,1) for x in inverse],[84.3,6.0,7.0,2.6])
        self.assertTrue(p.meets_objective(.065))
        self.assertFalse(p.meets_objective(.065-1e-10))

    def test_sensitivity_and_restore(self):
        changed=[list(row) for row in p.CORRELATIONS]
        changed[2][3]=changed[3][2]=.5
        before=p.portfolio_volatility(p.BENCHMARK,p.covariance_matrix(p.VOLATILITIES,p.CORRELATIONS))
        after=p.portfolio_volatility(p.BENCHMARK,p.covariance_matrix(p.VOLATILITIES,changed))
        restored=p.portfolio_volatility(p.BENCHMARK,p.covariance_matrix(p.VOLATILITIES,p.CORRELATIONS))
        self.assertAlmostEqual(after,math.sqrt(.012096))
        self.assertEqual(before,restored)
        self.assertEqual(p.CORRELATIONS[2][3],.25)
        self.assertEqual(p.CORRELATIONS[3][2],.25)
        print(f"Sensitivity: {before:.8%} -> {after:.8%} -> {restored:.8%}")

    def test_invalid_inputs(self):
        for label, matrix in (("correlation 1.3",[[1,0,0,0],[0,1,0,0],[0,0,1,1.3],[0,0,1.3,1]]),("asymmetry",[[1,0,0,0],[0,1,0,0],[0,0,1,.5],[0,0,.25,1]]),("dimensions",[[1]])):
            with self.subTest(label=label):
                with self.assertRaises(ValueError) as err: p.covariance_matrix(p.VOLATILITIES,matrix)
                print(f"Rejected {label}: {err.exception}")
        for w in ((.1,.2,.3),(-.1,.1,.4,.6),(.2,.2,.2,.2),(float('nan'),0,0,1)):
            with self.assertRaises(ValueError): p.validate_weights(w,4)
        with self.assertRaises(ValueError): p.inverse_volatility_weights((0,.1))

    def test_mandate_preservation(self):
        spec=importlib.util.spec_from_file_location('original',HERE.parent/'lab13/mandate.py')
        original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
        for name in 'ABCD':
            self.assertEqual(m.CANDIDATES[name],original.CANDIDATES[name])
            self.assertEqual(m.evaluate(m.CANDIDATES[name]),original.evaluate(original.CANDIDATES[name]))
        self.assertEqual([sum(not passed for _,passed in m.evaluate(m.CANDIDATES[n]).values()) for n in 'ABCDE'],[0,3,1,0,1])
        self.assertEqual(m.evaluate(m.CANDIDATES['E'])['Reserve >= 3.0%'],(0,False))

    def test_prices_against_raw_source(self):
        import datetime
        rows=list(csv.DictReader((HERE/'prices.csv').read_text().splitlines()))
        self.assertEqual(len(rows),60)
        self.assertEqual(list(rows[0]),['date','BIL','IEF','LQD','VT'])
        self.assertEqual(rows[0]['date'],'2021-10-01');self.assertEqual(rows[-1]['date'],'2026-09-01')
        self.assertEqual(len({r['date'] for r in rows}),60)
        expected_dates=[f'{2021 + (9+i)//12:04d}-{(9+i)%12+1:02d}-01' for i in range(60)]
        self.assertEqual([r['date'] for r in rows],expected_dates)
        for ticker in ('BIL','IEF','LQD','VT'):
            data=json.loads((HERE/'sources'/f'{ticker}_monthly.json').read_text())['chart']['result'][0]
            raw={datetime.datetime.fromtimestamp(t,datetime.timezone.utc).date().isoformat():v for t,v in zip(data['timestamp'],data['indicators']['adjclose'][0]['adjclose'])}
            for row in rows:
                self.assertGreater(float(row[ticker]),0)
                self.assertEqual(float(row[ticker]),raw[row['date']])

if __name__=='__main__': unittest.main(verbosity=2)
