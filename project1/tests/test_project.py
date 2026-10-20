"""Independent fixtures, identities, failure injection and reproducibility checks."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
import unittest,copy,json,csv,math,hashlib,subprocess,io,contextlib
import model as m
import config as c
import analysis

class ProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.a,cls.rows=m.forecast();cls.v=m.value(cls.rows,cls.a)
    def near(self,a,b):self.assertAlmostEqual(a,b,places=6)
    def test_01_legacy_fcfe_regression(self):
        self.near(m.legacy.value_equity(m.legacy.project())['per_share'],32.67314175381166)
    def test_02_legacy_complete_statement_snapshot(self):
        old=json.loads((HERE.parent/'lab11/base_snapshot.json').read_text())
        # Snapshot format is inspected instead of guessing a schema.
        with io.StringIO() as out,contextlib.redirect_stdout(out):
            m.legacy.main();actual=out.getvalue()
        saved=(HERE.parent/'lab10/lab10_output.txt').read_text(encoding='utf-8')
        self.assertEqual(actual.replace('\r\n','\n'),saved.replace('\r\n','\n'))
    def test_03_synthetic_known_answer(self):
        cf=100;path=[]
        for g in [.08,.06,.05,.04,.03]:cf*=1+g;path.append(cf)
        d=m.dcf(path,.10,.03,path[-1]*1.03)
        self.assertAlmostEqual((d['enterprise_value']+50-300)/50,27.4974,places=4)
    def test_04_signed_cashflow_known_answer(self):
        d=m.dcf([-100,110],.1,0,11)
        self.near(d['pv_explicit'],0);self.near(d['enterprise_value'],110/1.1**2)
    def test_05_history_revenue_and_capex(self):
        with (HERE/'data/historical_reported.csv').open(newline='',encoding='utf-8') as f:r=list(csv.DictReader(f))
        h={(int(x['year']),x['metric']):x['value'] for x in r}
        for year,expected in [(2023,574785),(2024,637959),(2025,716924)]:self.near(float(h[year,'revenue']),expected)
        for year in [2023,2024,2025]:self.near(float(h[year,'gross_cash_capex'])-float(h[year,'capex_proceeds_incentives']),float(h[year,'net_cash_capex']))
    def test_06_history_source_artifact_checks(self):
        text=(HERE/'sources/amazon_2025.txt').read_text(encoding='utf-8')
        for token in ['716,924','357,025','411,065','131,819','41,860']:self.assertIn(token,text)
    def test_07_five_years(self):self.assertEqual([r['year'] for r in self.rows],[2026,2027,2028,2029,2030])
    def test_08_balance_sheets(self):
        for r in self.rows:self.near(sum(r[k] for k in m.legacy.ASSETS),sum(r[k] for k in m.legacy.LIABILITIES)+r['equity'])
    def test_09_cashflow_articulation(self):
        for r in self.rows:self.near(r['cash']-r['opening']['cash'],r['operating_cash_flow']+r['investing_cash_flow']+r['financing_cash_flow'])
    def test_10_working_capital(self):
        for r in self.rows:self.near(r['change_operating_wc'],m.operating_nwc(r)-m.operating_nwc(r['opening']))
    def test_11_ppe_continuity(self):
        for r in self.rows:self.near(r['ppe'],r['opening']['ppe']+r['ppe_additions']-r['depreciation'])
    def test_12_finance_lease_continuity(self):
        for r in self.rows:self.near(r['finance_lease'],r['opening']['finance_lease']+r['finance_lease_addition']-r['finance_lease_principal'])
    def test_13_operating_lease_continuity(self):
        for r in self.rows:
            self.near(r['operating_rou'],r['opening']['operating_rou']+r['operating_lease_addition']-r['rou_amortization'])
            self.near(r['operating_lease'],r['opening']['operating_lease']+r['operating_lease_addition']+r['operating_lease_accretion']-r['operating_lease_cash'])
    def test_14_debt_and_equity_continuity(self):
        for r in self.rows:
            self.near(r['debt']-r['opening']['debt'],r['debt_net_change'])
            self.near(r['equity']-r['opening']['equity'],r['net_income']-r['distributions'])
    def test_15_fcff_components(self):
        for r in self.rows:self.near(r['fcff'],r['operating_income']-r['operating_cash_taxes']+r['depreciation']-r['capex']-r['finance_lease_addition']-r['financing_addition']-r['operating_residual_investment']-r['change_operating_wc'])
    def test_16_fcff_independent_cfo_route(self):
        for r in self.rows:self.near(r['fcff'],r['fcff_from_cfo'])
    def test_17_actual_negative_fcff_retained(self):
        self.assertTrue(any(r['fcff']<0 for r in self.rows))
        self.near(self.v['pv_explicit'],sum(cf/(1+self.v['wacc'])**t for cf,t in zip(self.v['discounted_period_fcff'],self.v['discount_times'])))
        self.assertTrue(any(x<0 for x in self.v['pv_cashflows']))
    def test_18_wacc_components(self):
        p=m.wacc();self.near(p['wacc'],p['equity_weight']*(.0495+1.44*.05)+p['debt_weight']*.05341*.78)
    def test_19_wacc_growth_boundaries(self):
        for rate,g in [(.03,.03),(.02,.03),(-1,-1.1)]:
            with self.assertRaises(ValueError):m.dcf([1]*5,rate,g,1)
    def test_20_nonfinite_boundary(self):
        with self.assertRaises(ValueError):m.dcf([float('nan')],.1,.02,1)
    def test_21_bridge_identity(self):
        b=m.equity_bridge(1000000)
        self.near(b['equity_value'],1000000+78213+25000-21300-25000+44775-158320-13451-9315)
    def test_22_bridge_no_operating_lease_double_count(self):
        b=m.equity_bridge(1000000);self.assertFalse(any('Operating lease' in r['item'] for r in b['adjustments']))
        self.near(b['excluded_operating_lease_liability'],96320)
    def test_23_diluted_share_reconciliation(self):
        self.near(self.v['diluted_shares'],10786.313572+134)
        self.near(self.v['per_share']*self.v['diluted_shares'],self.v['equity_value'])
        with self.assertRaises(ValueError):m.equity_bridge(1,dict(c.BRIDGE,common_shares=-134))
    def test_24_synthetic_monotonicity(self):
        self.assertGreater(m.dcf([100]*5,.09,.02,102)['enterprise_value'],m.dcf([100]*5,.11,.02,102)['enterprise_value'])
        self.assertGreater(m.dcf([100]*5,.1,.03,103)['enterprise_value'],m.dcf([100]*5,.1,.02,102)['enterprise_value'])
    def test_25_terminal_reinvestment_identity(self):
        t=self.v['terminal'];self.near(t['fcff'],t['nopat']+t['eligible_da']-t['capital_investment']+t['capital_payable_credit']-t['change_operating_nwc']-t['operating_cash_investment'])
    def test_26_peer_enterprise_definition(self):
        for p in c.PEERS:
            v=m.peer_multiples(p);self.near(v['ev'],p['price']*p['shares']+p['debt']+p['finance_leases']+p['minority']-p['cash']-p['securities']+p['restricted_securities'])
    def test_27_peer_ebitda_definitions(self):
        for p in c.PEERS:
            v=m.peer_multiples(p);self.near(v['ev_ebitda']*(p['ebit']+p['da']),v['ev'])
    def test_28_pe_has_no_debt_subtraction(self):
        comp=m.comps()
        for r,p in zip(comp['implied'],c.PEERS):self.near(r['pe'],p['price']/p['eps']*7.17)
    def test_29_peer_policy_exclusion(self):
        for p in [dict(c.PEERS[0],ticker='AMZN'),dict(c.PEERS[0],decision='exclude')]:
            with self.assertRaises(ValueError):m.peer_multiples(p)
    def test_30_peer_dates(self):
        for p in [dict(c.PEERS[0],price_date='2026-09-11'),dict(c.PEERS[0],published='2026-09-11')]:
            with self.assertRaises(ValueError):m.peer_multiples(p)
    def test_31_peer_negative_denominator(self):
        for k in ['shares','eps','revenue']:
            with self.assertRaises(ValueError):m.peer_multiples(dict(c.PEERS[0],**{k:0}))
    def test_32_leave_one_out(self):
        for r in m.comps()['leave_one_out']:self.assertEqual(r['remaining'],1)
    def test_33_scenario_isolation(self):
        original=m.fresh();m.evaluate('infrastructure_stress');self.assertEqual(m.fresh(),original)
        self.assertEqual(m.forecast()[0],self.a)
    def test_34_restored_base(self):
        before=m.evaluate();[m.evaluate(k) for k in c.SCENARIOS];self.assertEqual(before,m.evaluate())
    def test_35_funding_failure_retained(self):
        v=m.evaluate('funding_stress');self.assertFalse(v['funding_feasible']);self.assertTrue(v['accounting_valid']);self.assertIn('diagnostic',v['valuation_status'])
    def test_36_reverse_boundaries(self):
        with self.assertRaises(ValueError):m.reverse(1,.1,-.1)
        self.assertIsNone(m.reverse(1e9)['solution'])
    def test_37_reverse_repricing(self):
        r=m.reverse(c.PRICE);self.assertIsNotNone(r['solution']);self.assertAlmostEqual(r['repriced'],c.PRICE,places=6)
    def test_38_deliberate_high_risk_failure(self):
        bad=copy.deepcopy(self.rows);bad[2]['ppe_additions']-=bad[2]['finance_lease_addition']
        self.assertFalse(m.diagnose(bad,self.a)['accounting_valid'])
        with self.assertRaises(ValueError):m.value(bad,self.a)
    def test_39_deliberate_cash_failure(self):
        bad=copy.deepcopy(self.rows);bad[0]['cash']=bad[0]['opening']['cash']
        self.assertFalse(m.diagnose(bad,self.a)['accounting_valid'])
    def test_40_historical_preservation(self):self.assertGreaterEqual(analysis.preserve_check(),64)
    def test_41_original_edition_a_copy(self):
        manifest=json.loads((HERE/'evidence/preservation_manifest.json').read_text())
        for p,h in manifest['sha256'].items():
            if p.endswith('amazon-edition-a.md'):self.assertEqual(hashlib.sha256((HERE/'docs/historical/amazon-edition-a.md').read_bytes()).hexdigest(),h)
    def test_42_business_revenue_reconciles(self):
        for r in self.rows:self.near(r['aws_revenue']+r['advertising_revenue']+r['retail_and_other_revenue'],r['revenue'])
    def test_43_operating_fcff_unaffected_by_financing(self):
        _,r=m.forecast('funding_stress')
        for x,y in zip(r,self.rows):self.near(x['fcff'],y['fcff'])
    def test_44_market_data_evidence(self):
        for name,price in [('amzn_price','251.89'),('msft_price','492.44'),('wmt_price','105.73')]:
            s=(HERE/'sources'/f'{name}.txt').read_text(encoding='utf-8')
            pos=s.find('2026-09-10');self.assertGreaterEqual(pos,0);self.assertIn(price,s[pos:pos+200])
    def test_45_tax_normalization_no_financing_shield(self):
        for r in self.rows:self.near(r['operating_cash_taxes'],max(0,r['operating_income'])*.22)
    def test_46_terminal_growth_coupled_reinvestment(self):
        t1=m.terminal(self.rows[-1],self.a,.015);t2=m.terminal(self.rows[-1],self.a,.035)
        self.assertGreater(t2['net_reinvestment'],t1['net_reinvestment'])
    def test_47_stub_discounting(self):
        self.near(self.v['discount_times'][0],112/365)
        self.near(self.v['discounted_period_fcff'][0],self.rows[0]['fcff']*112/365)
    def test_48_source_download_integrity(self):
        for r in json.loads((HERE/'evidence/source_downloads.json').read_text()):
            if 'sha256' in r:self.assertEqual(hashlib.sha256((HERE/r['path']).read_bytes()).hexdigest(),r['sha256'])
    def test_49_reported_to_normalized_income(self):
        self.near(77670+554+19087-(15229+4381-2274),79975)
        self.near(82475-82475*.22,64330.5)
    def test_50_known_investment_outflows(self):
        self.near(self.rows[0]['nonoperating_investment_purchase'],39767+21300)
        self.near(self.rows[0]['other_assets']-self.rows[0]['opening']['other_assets'],61067)
        self.near(self.rows[0]['investing_cash_flow'],-self.rows[0]['capex']-61067+self.rows[0]['securities_sale'])
    def test_51_known_july_issuance(self):
        self.near(self.a['debt_net_change'][0],64246+25000)
        self.near(c.WACC_INPUTS['market_debt'],124980+25000+13451+9315)
    def test_52_core_base_not_funding_valid(self):
        b=m.evaluate();self.assertFalse(b['funding_feasible']);self.assertIn('diagnostic',b['valuation_status'])
    def test_53_terminal_opening_asset_depreciation(self):
        self.near(self.v['terminal']['eligible_da'],self.rows[-1]['ppe']*self.a['depreciation_rate'])
    def test_54_terminal_ebit_schedule(self):
        t=self.v['terminal'];gp=t['revenue']*self.a['gross_margin'][-1]
        self.near(t['ebit'],gp-gp*self.a['sga_to_gp'][-1]-t['revenue']*self.a['other_cost_ratio']-t['eligible_da']-t['operating_lease_expense'])
    def test_55_strategic_no_double_count(self):
        s=m.strategic_bridge(self.v['enterprise_value'])
        self.near(s['gross_assets'],122300+97900+395+4300+21300)
        self.near(s['cases'][0]['equity_value'],self.v['equity_value']+s['gross_assets'])
        self.near(s['additional_cash_adjustment'],0)
    def test_56_strategic_haircut_labeled(self):
        s=m.strategic_bridge(self.v['enterprise_value']);self.near(s['cases'][1]['haircut'],224895*.22)
        self.assertIn('diagnostic',s['cases'][1]['case'])
    def test_57_financing_investment_not_in_fcff(self):
        a,r=m.forecast(override={'nonoperating_investments':[0]*5})
        for old,new in zip(r,self.rows):self.near(old['fcff'],new['fcff'])
    def test_58_date_cash_bridge_known_transactions(self):
        b=m.equity_bridge(1000000)
        self.assertEqual(sum(x['item']=='Known subsequent OpenAI cash payment' for x in b['adjustments']),1)
    def test_59_named_nonrecurring_cost_normalization(self):
        self.near(self.a['other_cost_ratio'],m.fresh()['other_cost_ratio']-2500/716924)
        text=(HERE/'sources/amazon_2025.txt').read_text(encoding='utf-8')
        self.assertIn('FTC',text);self.assertIn('2.5',text)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ProjectTests)
    log=io.StringIO();result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    text=log.getvalue();print(text)
    (HERE/'evidence/validation_results.txt').write_text(text,encoding='utf-8')
    summary=dict(tests_run=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
                 failed=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
                 command='python -B project1/tests/test_project.py',
                 unresolved=['Actual recordings/corrected transcripts','Human independent source verification','Brightspace rubric and early-AI recovery clarification'])
    (HERE/'evidence/validation_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
