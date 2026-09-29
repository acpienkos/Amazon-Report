"""40-digit independent reference adapted from Lab 10's validation, not its production engine.
All forecast financial lines rebuilt from supplied assumptions. Invalid liquidity is
assessed by the caller so the failed approved case can also be checked arithmetically.
Original Lab 10 files are untouched. No production functions imported or called.
"""
import json
from decimal import Decimal as D, getcontext
getcontext().prec=40
ASSETS=('cash','securities','inventory','receivables','ppe','operating_rou','goodwill','other_assets')
LIABILITIES=('trade_payables','capex_payables','operating_accruals','unearned','operating_lease','finance_lease','financing_obligation','debt','revolver','other_liabilities')
OPENING_KEYS=ASSETS+LIABILITIES+('equity','revenue')

def rebuild(values):
    a=json.loads(json.dumps(values),parse_float=D,parse_int=D)
    p={k:a['opening_'+k] for k in OPENING_KEYS}; results=[]

    for i,y in enumerate(range(2026,2031)):
        z={}
        z['revenue']=p['revenue']*(1+a['growth'][i]); z['gross_profit']=z['revenue']*a['gross_margin'][i]
        z['cost_of_sales']=z['revenue']-z['gross_profit']; z['sga']=z['gross_profit']*a['sga_to_gp'][i]
        z['other_operating_cost']=z['revenue']*a['other_cost_ratio']; z['depreciation']=p['ppe']*a['depreciation_rate']
        z['rou_amortization']=p['operating_rou']*a['rou_amortization_rate']
        z['operating_lease_accretion']=p['operating_lease']*a['operating_lease_rate']
        z['operating_lease_expense']=z['rou_amortization']+z['operating_lease_accretion']
        z['operating_lease_cash']=z['operating_lease_expense']
        z['operating_income']=z['revenue']-sum(z[k] for k in ('cost_of_sales','sga','other_operating_cost','depreciation','operating_lease_expense'))
        z['debt_net_change']=a['debt_net_change'][i]; z['debt']=p['debt']+z['debt_net_change']
        z['debt_interest']=(p['debt']+z['debt'])/2*a['debt_rate']
        z['finance_lease_interest']=p['finance_lease']*a['finance_lease_rate']
        z['financing_interest']=p['financing_obligation']*a['financing_rate']
        z['revolver_interest']=p['revolver']*a['revolver_rate']
        z['interest_expense']=z['debt_interest']+z['finance_lease_interest']+z['financing_interest']+z['revolver_interest']
        z['interest_income']=(p['cash']+p['securities'])*a['cash_yield']; z['other_income']=a['other_income']
        z['pretax_income']=z['operating_income']+z['interest_income']+z['other_income']-z['interest_expense']
        z['income_tax']=max(D(0),z['pretax_income'])*a['tax_rate'];z['net_income']=z['pretax_income']-z['income_tax']
        z['inventory']=z['cost_of_sales']/a['days_per_year']*a['inventory_days']; z['receivables']=z['revenue']*a['receivables_ratio']
        z['trade_payables']=z['cost_of_sales']*a['trade_payable_ratio']; z['operating_accruals']=z['revenue']*a['accrual_ratio']
        z['unearned']=z['revenue']*a['unearned_ratio']; z['capex']=a['capex_2026_guidance'] if i==0 else a['capex_later'][i-1]
        z['capex_payables']=z['capex']*a['capex_payable_ratio']; z['change_capex_payables']=z['capex_payables']-p['capex_payables']
        z['finance_lease_addition']=a['finance_lease_addition'];z['finance_lease_principal']=min(p['finance_lease'],p['finance_lease']*a['finance_lease_principal_rate'])
        z['finance_lease']=p['finance_lease']+z['finance_lease_addition']-z['finance_lease_principal']
        z['financing_addition']=a['new_financing_obligations'];z['financing_principal']=min(p['financing_obligation'],max(D(0),a['financing_payments'][i]-z['financing_interest']))
        z['financing_obligation']=p['financing_obligation']+z['financing_addition']-z['financing_principal']
        z['ppe_additions']=z['capex']+z['change_capex_payables']+z['finance_lease_addition']+z['financing_addition']
        z['ppe']=p['ppe']+z['ppe_additions']-z['depreciation']
        z['operating_lease_addition']=z['rou_amortization']+p['operating_rou']*a['rou_growth']
        z['operating_rou']=p['operating_rou']+z['operating_lease_addition']-z['rou_amortization']
        z['operating_lease']=p['operating_lease']+z['operating_lease_addition']+z['operating_lease_accretion']-z['operating_lease_cash']
        for k in ('goodwill','other_assets','other_liabilities'):z[k]=p[k]*(1+a['other_balance_growth'])
        z['distributions']=a['distributions'];z['equity']=p['equity']+z['net_income']-z['distributions']
        def nwc(q):return q['inventory']+q['receivables']-q['trade_payables']-q['operating_accruals']-q['unearned']
        z['change_operating_wc']=nwc(z)-nwc(p)
        z['change_other_net_assets']=(z['goodwill']+z['other_assets']-z['other_liabilities'])-(p['goodwill']+p['other_assets']-p['other_liabilities'])
        z['operating_cash_flow']=z['net_income']+z['depreciation']-z['change_operating_wc']
        z['fcfe_before_revolver']=z['operating_cash_flow']-z['capex']-z['change_other_net_assets']+z['debt_net_change']-z['finance_lease_principal']-z['financing_principal']
        basecash=p['cash']+z['fcfe_before_revolver']-z['distributions']
        z['securities_sale']=min(max(D(0),p['securities']-a['securities_liquidity_floor']),max(D(0),a['minimum_cash']-basecash))
        z['securities']=p['securities']-z['securities_sale'];z['cash_before_revolver']=basecash+z['securities_sale']
        z['revolver_draw']=min(max(D(0),a['minimum_cash']-z['cash_before_revolver']),max(D(0),a['revolver_limit']-p['revolver']))
        z['revolver_repayment']=min(p['revolver'],max(D(0),z['cash_before_revolver']-a['minimum_cash']))
        z['revolver']=p['revolver']+z['revolver_draw']-z['revolver_repayment']
        z['fcfe']=z['fcfe_before_revolver']+z['revolver_draw']-z['revolver_repayment']
        z['investing_cash_flow']=-z['capex']-z['change_other_net_assets']+z['securities_sale']
        z['financing_cash_flow']=z['debt_net_change']-z['finance_lease_principal']-z['financing_principal']+z['revolver_draw']-z['revolver_repayment']-z['distributions']
        z['net_cash_change']=z['operating_cash_flow']+z['investing_cash_flow']+z['financing_cash_flow']
        z['cash']=p['cash']+z['fcfe']+z['securities_sale']-z['distributions']
        results.append(z);p=z
    return results,a
