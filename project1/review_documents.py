"""Final-review documents: one consistent source of current figures and decisions."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
import json,csv,shutil,re
from pypdf import PdfReader
from pdf_layout import pdf,write,money,mdtable
import config as c

def main():
    d=json.loads((HERE/'outputs/valuation.json').read_text());v=d['base']['valuation'];base=d['base'];rows=base['rows']
    t=v['terminal'];s=d['strategic_investments'];review=json.loads((HERE/'evidence/financial_review.json').read_text())
    tests=json.loads((HERE/'evidence/validation_summary.json').read_text());cold=json.loads((HERE/'evidence/cold_run.json').read_text())
    gross=s['cases'][0]['per_share'];hair=s['cases'][1]['per_share'];old=review['old_per_share']
    cases=[dict(case=x['case'],funding='PASS' if x['funding_feasible'] else 'FAIL',core=money(x['valuation']['per_share']) if x['valuation'] else 'unavailable',status=x['valuation_status']) for x in d['cases']]
    fifteen=[
      dict(item='1. FY2025 inputs',finding='Twelve annual statement rows independently matched to source-table columns; revenue less six operating-cost categories reconciles reported EBIT79975. Exclude only the named2500 FTC settlement from recurring cost: normalized EBIT82475 and NOPAT64330.5 at22%. Reported history/equity remain unchanged.',status='Source/arithmetic checked; student verification pending'),
      dict(item='2. Growth / margins / expenses',finding='Consolidated growth16/14/12/10/8%; gross margin51/52/53/53.5/54%. AWS/advertising decomposition is illustrative, not a segment-profitability forecast. Residual cost changes23.2058% to22.8571% only for the sourced FTC normalization; SG&A/gross profit16%-15.2% remains inherited judgment.',status='Conditional forecast, not verified future results'),
      dict(item='3. Infrastructure investment',finding='Net cash capex220/230/220/210/200bn. FY2026 outlook reused from dated source record; FY2027-2030 taper is not guidance. No adjustment made to make the stock look cheaper or dearer.',status='First year sourced; later path judgment'),
      dict(item='4. Cash vs financed additions',finding='PP&E additions = net cash purchases + change capital AP + finance-lease/facility additions. Capital AP credit avoids mistaking accrued investment for extra cash spending. Finance-lease additions2911m remain explicit analyst assumption.',status='Reconciled'),
      dict(item='5. Lease conventions',finding='Operating leases remain rent with no debt deduction. Finance leases/facility obligations are deducted and new assets count as investment; principal is not FCFF. Equal modeled lease rent/cash differs from reported H1 expense8035/cash7804; identified simplification.',status='Consistent policy; cash timing simplified'),
      dict(item='6. WC / cash flows',finding='Separate cash/security/debt/lease accounts and capital AP are excluded from operating WC. Receivables/other still aggregates prepaids and restricted-cash subbalances; it is not a fully decomposed operating-asset schedule. Investment purchases now increase other assets/reduce CFI. Prior base funding pass omitted known flows.',status='Corrected funding; composite WC and seasonality limits'),
      dict(item='7. EBIT / taxes',finding='EBIT excludes investment gains/interest. 22% of positive EBIT is a normalized unlevered tax provision-as-cash proxy. H1 actual paid tax3978 is not a substitute unlevered operating tax rate; refund/deferred-tax timing is not modeled.',status='Proxy explicitly qualified'),
      dict(item='8. D&A',finding='PPE D&A41860m is different from total cash-flow D&A. Fifteen percent of opening net PPE is a blended forecast proxy, not an asset-vintage/useful-life model. Actual server-life changes in Note1 support caution, not a blanket new rate.',status='Definition checked; forecast approximation'),
      dict(item='9. Signed FCFF',finding='Two routes reconcile. Negative flows are retained; debt proceeds, investment purchases and securities liquidation do not become operating FCFF. Known nonoperating cash purchases change funding, not operating FCFF.',status='Automated reconciliation passes'),
      dict(item='10. Terminal FY2031',finding=f'Old D&A138898.13m was a sales-growth scale-up. Correct D&A145304.85m applies15% to opening PPE968698.97m. Rent17842.91m uses opening ROU/liability. EBIT falls to{t["ebit"]:,.2f}; FCFF to{t["fcff"]:,.2f}. Required investment still drops from2030; normalization is favorable and unsupported, not permanently punitive capex.',status='Mechanical inconsistency corrected; transition remains judgment'),
      dict(item='11. WACC',finding=f'Add July25bn note issue to market-debt proxy. WACC changes11.7381% to{v["wacc"]:.4%}. RF4.95%, beta1.44, ERP5%, debt yield5.341%, tax22%. Beta method remains unverified; lease/facility debt proxies and current bond pricing are approximate.',status='Known debt omission corrected; input limitations'),
      dict(item='12. EV to equity',finding='Cash/debt proceeds25bn paired; subsequent OpenAI cash payment21.3bn deducted once. Investment asset21.3bn added once in strategic reference. No operating-lease debt double count; no capital-AP debt deduction.',status='Known transactions reconciled; exact date incomplete'),
      dict(item='13. Strategic assets',finding='June30 private equity122.3bn, notes97.9bn, equity-method395m, warrants4.3bn; subsequent OpenAI21.3bn. Gross reference246.195bn. Related tax bases, liquidity restrictions, commitments and economic appraisal remain unresolved. Haircut22% of preexisting gross is a diagnostic, not reported tax.',status='Omission corrected with separate references; no verified appraisal'),
      dict(item='14. Diluted shares',finding='10786.313572m July22 common +134m Q2 treasury-stock incremental awards =10920.313572m. Existing awards distinct from assumed cash-replacement future compensation. Not exact September10 dilution.',status='Reconciled proxy; exact denominator unresolved'),
      dict(item='15. Date / market comparison',finding='September10 close251.89 aligns peer prices and RF evidence. All factual inputs were public by cutoff, but forecasts were constructed later. Remaining112/365 of full-year2026 FCFF is a uniform proxy; known July cash/debt corrected, other quarterly movements not rolled forward.',status='Explicit retrospective model; not exact point-in-time valuation'),
    ]
    change_table=mdtable([dict(step=x['step'],per_share=money(x['per_share'])) for x in review['waterfall']],['step','per_share'])
    detail=f'''# Final financial review | Amazon

## Conclusion

The prior {money(old)} was reproducible arithmetic for an incomplete core subtotal, not verified Amazon intrinsic value. The corrected subtotal is {money(v['per_share'])}; the corrected base fails funding. Reported strategic-investment carrying references produce {money(hair)} to {money(gross)} under explicit diagnostic haircut conventions; this is not a fair-value confidence interval. The recommendation is **DO NOT INITIATE at the September10 comparison price of {money(d['price'])}** for a fund with no shares. This is not a short recommendation or proof of issuer distress/80% market mispricing.

## Old-to-new attribution | no price-target fitting

{change_table}

Operating FCFF is unchanged by merely including nonoperating purchases and borrowing. The only annual operating-FCFF change is the after-tax effect of removing the named FY2025 FTC settlement from the recurring residual-cost ratio. That is an explicit normalization judgment supported by Note1, not an assumption fitted to price. Other charges and ongoing regulatory risk are retained. The omitted purchases and debt change funding, interest income/expense and the bridge; unlevering prevents financing items contaminating operating value. Known FY2026 purchases39767+21300=61067m and July notes25000m are source facts, not a newly invented bear scenario.

## Fifteen-point audit

{mdtable(fifteen,['item','finding','status'])}

## Annual forecast | USD millions

{mdtable([dict(year=r['year'],sales=f"{r['revenue']:,.1f}",EBIT=f"{r['operating_income']:,.1f}",DA=f"{r['depreciation']:,.1f}",cash_capex=f"{r['capex']:,.1f}",FCFF=f"{r['fcff']:,.1f}",cash=f"{r['cash']:,.1f}") for r in rows],['year','sales','EBIT','DA','cash_capex','FCFF','cash'])}

Negative ending cash in an infeasible path is a funding diagnostic, not a permitted negative cash asset or an articulated viable forecast. Identities may reconcile while the forecast fails economic constraints. No unlimited debt plug is introduced.

## Terminal review

FY2030 operating investment {rows[-1]['operating_investment']:,.2f}; FY2031 asset investment {t['capital_investment']:,.2f} less capital-AP credit {t['capital_payable_credit']:,.2f}. Terminal NOPAT {t['nopat']:,.2f}; net reinvestment {t['net_reinvestment']:,.2f}; FCFF {t['fcff']:,.2f}. The model therefore assumes a substantial investment normalization. It does not extrapolate $200bn cash capex plus high growth forever. This normalization increases value versus retaining final-year spending intensity; it is a major source of optimistic model risk, not an explanation that the DCF is low only because capex never normalizes.

The corrected terminal D&A/rental policy is mechanically consistent for FY2031. Subsequent g-growth and stable capital ratios remain an analyst steady-state assumption, not a supported infrastructure-return study. TV/PV operating EV is {v['terminal_dependence']:.2%}; negative explicit PV explains the value above100%. No percentage is capped or hidden.

Source precision is not model-test tolerance: capital AP and facility-financing inputs include reported rounded billions, while identity tests use a numerical1e-6 USDm tolerance. Passing a$1 arithmetic check does not create$1 economic input precision. Cash-replacement SBC plus a diluted-award proxy also requires an award-level review to rule out overlap between existing service costs and new compensation; the proxy is not a certified dilution model.

## Strategic assets and known cash transactions

{mdtable([dict(component=k,USDm=f'{val:,.0f}') for k,val in s['components'].items()],['component','USDm'])}

{mdtable([dict(case=x['case'],per_share=money(x['per_share']),haircut_USDm=f"{x['haircut']:,.1f}") for x in s['cases']],['case','per_share','haircut_USDm'])}

The 22% gross-asset haircut is deliberately labeled a sensitivity: taxes ordinarily apply to gains and depend on basis/timing; it is not an estimate of Amazon's reported tax liability. Neither zero haircut nor this gross haircut establishes a true upper/lower fair-value bound. Correlated commercial relationships, restrictions and future funding commitments matter. The subsequent21.3bn cash payment is already in the core bridge and is never deducted twice. The H139.767bn cash outflow is already reflected in June30 cash; it is included in the full-year funding forecast, not deducted again from the June30 bridge.

Debt basis is also explicit: the bridge uses158320m face proxy after July; WACC uses149980m notes/other market proxy plus22766m finance-lease/facility claims. The modeled H1 carrying proxy133097 differs from reported carrying debt132549 by548m; this unresolved fees/FX/other-carrying movement is disclosed, not plugged. See outputs/debt_basis_reconciliation.csv. Comparables retain reported annual EBIT/EPS definitions, whereas the DCF normalizes the named FTC charge; that is another reason not to average the methods.

## Committee decision and reversal conditions

Do not initiate now: there is no validated positive purchase case, and the corrected base funding plan fails. Watch/defer would be appropriate only as an explicit research-monitoring decision, not as a way to ignore a supposed precise83.83% downside. The original downside claim is withdrawn as a comprehensive valuation claim. Keep AMZN on a research list without authorizing a position.

Reopen the decision when documented financing/available liquidity covers known investment obligations without cash-floor or facility-limit breaches; an independently reconciled dated asset/tax/share bridge exists; reinvestment/operating returns are supported by disclosures; and downside-supported value exceeds a then-dated purchase price with a stated, student-defended margin of safety. No arbitrary quantitative threshold or new upside is invented. Strong evidence that infrastructure returns cannot cover capital costs, or that funding is unavailable, reinforces do not initiate; failure is not automatically covenant breach or default.

## Sources and independent-check boundary

Amazon FY2025 Form10-K: {c.K} (statements; Note1 useful lives, Note3/4 leases/investment, debt and segment notes). Q2 Form10-Q: {c.SEC} (cash-flow statement p3; Note2 Non-Marketable Investments and subsequent OpenAI payment; Note5 subsequent25bn note issuance; lease and EPS tables). Source HTML, table extraction and actual download hashes are preserved. Original source-row check details are evidence/financial_review.json. This is Codex's separate source/arithmetic review; it is not a claim of unaided student verification or the assessed AI-off exercise.
'''
    write(HERE/'docs/financial-review.md',detail)
    report=f'''# Amazon | reviewed visible valuation report

Prepared October19; dated valuation/comparison September10 2026. USD millions except per-share data. **DO NOT INITIATE.** All core values below are conditional diagnostics; base funding fails and comprehensive intrinsic value is not verified.

## Current results

Core operating-business/liquid-asset subtotal {money(v['per_share'])}; dated price {money(d['price'])}; arithmetic core gap {v['upside']:.2%} is **not** a claim of full-company downside. WACC {v['wacc']:.6%}; g {v['terminal_growth']:.2%}; diluted proxy {v['diluted_shares']:,.6f} million. Operating EV {v['enterprise_value']:,.2f}; core common equity {v['equity_value']:,.2f}; terminal dependence {v['terminal_dependence']:.2%}.

Including reported strategic assets at carrying references gives {money(hair)}-{money(gross)}, subject to unappraised taxes, restrictions and economic value. Only high passes funding among low/base/high; its core reference is {money(d['valid_low_high_range'][0])}. One funded case is not a range. See the fifteen-point review before using a figure.

{mdtable(cases,['case','funding','core','status'])}

## Reversal and committee ask

{d['committee_ask']}

## Full evidence

Financial review: ../docs/financial-review.md. Statements and FCFF reconciliation: statements.csv / fcff_reconciliation.csv. Sources: ../data/source_register.csv and ../evidence/source_checks.md. Research evolution, validation/AI record and committee memo are in ../docs/. Source facts were public by September10; forecasts are later retrospective judgments, not a point-in-time backtest.

## Material limits

Uniform remaining-year accrual rather than seasonal actual/forecast split; June30 bridge plus known subsequent transactions rather than exact September10 balances; diluted-share proxy; 22% provision-as-cash tax proxy; aggregate rather than segment profitability; judgmental investment taper/terminal transition; strategic references instead of a net economic appraisal. No source or model number supports a precise verified Amazon fair-value claim.

## Validation

{tests['passed']} model tests passed, {tests['failed']} failed, {tests['errors']} errors and {tests['skipped']} skipped. Seven dashboard pages execute. Technical clean-environment status: {cold['status']}. Human AI-off assessment and recordings remain incomplete. Historical64-file preservation verified; nothing committed, pushed or submitted.
'''
    write(HERE/'outputs/valuation-report.md',report)
    memo=f'''# Amazon | reviewed committee memo

Decision date reference: September10 2026. Prepared October19 2026. Fund holds no AMZN. AI-assisted educational analysis; student review required.

## Decision and committee ask

**DO NOT INITIATE at the dated $251.89 price.** There is no validated positive purchase case, and the corrected funding plan fails. Keep a research watchlist if useful, without authorizing capital. This is neither a short recommendation nor proof of issuer default or80% mispricing.

## Evidence and valuation

The previous {money(old)} headline was an incomplete core subtotal. Correcting terminal depreciation/rental policy, known July debt and cash transactions yields {money(v['per_share'])}. This excludes strategic investment value and is diagnostic because base funding fails. With reported investment carrying references, results are {money(hair)}-{money(gross)} under zero versus22%-of-preexisting-gross haircut cases. Those cases are not fair-value bounds or issuer tax estimates.

WACC is {v['wacc']:.2%}, g2.50%, diluted proxy {v['diluted_shares']:,.3f} million. Core operating EV is ${v['enterprise_value']/1000:,.1f}bn; core equity ${v['equity_value']/1000:,.1f}bn. Terminal PV represents {v['terminal_dependence']:.1%} of EV because explicit PV is negative. No complete low/high investable range is available: only high passes funding, with core reference {money(d['valid_low_high_range'][0])}.

## Operating outlook and accounting

AWS/advertising prospects do not establish infrastructure returns. Inherited consolidated growth16% fading to8%, gross margin51% to54%, and net cash capex220/230/220/210/200bn are conditional judgments; later-year taper is not guidance. Segment profitability is not independently forecast. Signed FCFF excludes borrowing/reserve sales. Operating leases stay rental costs; finance-lease assets are investment and financing claims deducted once. Taxes are a22% unlevered provision-as-cash proxy.

<!-- PAGEBREAK -->

## Corrections, risks and funding

The reviewed forecast includes $39.767bn H1 acquisition/nonmarketable-investment cash uses, $21.3bn subsequent OpenAI funding and $25bn subsequent notes. Including both cash uses and funding causes base cash-floor breaches in2028-2029. They are liquidity diagnostics, not viable negative cash assets. The recurring-cost ratio also excludes only the specifically identified$2.5bn FY2025 FTC settlement; other charges/regulatory risks are retained.

FY2031 FCFF is ${t['fcff']/1000:,.2f}bn after policy-consistent D&A and rent. Terminal investment still falls materially versus2030, so normalization is favorable, unproven model risk. The original low DCF was not caused by perpetual maintenance of peak infrastructure spending.

Gross strategic carrying references total$246.195bn including the subsequent purchase; its cash payment is deducted once. Tax bases, restrictions, commercial correlations and commitments prevent an asserted net fair value. Annual stub accrual, dated balances and dilution proxies also limit precision.

## Comparable valuation and decision conditions

Qualified WMT/MSFT P/E references are {money(d['comparables']['summary']['pe']['low'])}-{money(d['comparables']['summary']['pe']['high'])}. EV/revenue core references {money(d['comparables']['summary']['ev_revenue']['low'])}-{money(d['comparables']['summary']['ev_revenue']['high'])}; EV/EBITDA {money(d['comparables']['summary']['ev_ebitda']['low'])}-{money(d['comparables']['summary']['ev_ebitda']['high'])}. Periods, business mix and investment earnings differ; EV references exclude Amazon strategic assets. No unsupported method averaging is used.

Reopen only after documented funding covers commitments, operating returns support required reinvestment, an exact dated asset/tax/share bridge is defensible, and downside-supported value offers a student-defended margin of safety against a new dated price. Monitor disclosures on infrastructure cash returns, funding and investments. See Financial Review and Validation-and-AI-Use for limitations, tests and pending independent work.

Sources: Amazon FY2025 10-K and Q2 2026 10-Q (statements, Note2 investments/subsequent funding, debt note); MSFT/WMT annual filings; September10 historical closes. Direct URLs, dates and locators: data/source_register.csv; docs/financial-review.md.
'''
    write(HERE/'docs/decision-memo.md',memo)
    original=(HERE/'docs/historical/amazon-edition-a.md').read_text(encoding='utf-8')
    evolution=f'''# Research evolution | preserved original and reviewed Edition B

## Provenance

Original September1 Markdown is included unchanged below and byte-identically as docs/historical/amazon-edition-a.md. It is not replaced by the October19 completed copy. Original checkout disclosure remains: "I used Codex after AI use was allowed to read Amazon's SEC filing, organize filing facts, and help draft the Edition A and checkout language." No Brightspace receipt or entirely AI-free authorship is asserted. Its submission/permission wording is unverified historical text.

Dr. Z's October19 announcement, supplied by the student and retained verbatim in evidence/course_update.md, says to preserve originals and continue the final submission. Missing receipt alone is not used to halt work. Separate early-AI recovery is not represented as expressly waived. No original announcement posting was accessed.

## Original September1 draft | unchanged content

{original}

<!-- PAGEBREAK -->

# Edition B | subsequent development and financial review

## October19 addition

The user supplied this later question: "If Amazon's AWS growth and operating cash flows slow materially over the next several years, would the company's heavy infrastructure investments still generate returns sufficient to justify the current valuation?" The later significance concerned moving watch/defer toward do not initiate. This was added October19, not September1; no historical partner provenance is fabricated.

## Model evolution

Lab06 used FCFF growth guesses, WACC and a bridge; Lab08 added qualified P/E comparisons; Lab10 integrated statements but valued positive-only FCFE; Lab11 retained stress/funding failures; Lab12 retained watch/defer. Initial Edition B added signed FCFF and produced a provisional$40.74 core subtotal. A preserved105-file snapshot contains that prior build and failed/corrected development evidence.

## Review changes and evidence

{change_table}

| Item | Earlier position | Reviewed Edition B | Reason/evidence |
|---|---|---|---|
| Action | Watch/defer | Do not initiate at dated price | No verified purchase case; corrected base funding fails |
| Known investments | Omitted from funding | FY2026 cash uses61067m | Q2 cash-flow statement plus Note2 subsequent OpenAI funding |
| Known financing | July notes omitted | July25000m included, separate from assumed2027 issue | Q2 subsequent-event debt note |
| Strategic assets | Excluded, not valued | Separate carrying references; not a fair-value appraisal | Q2 Note2 components; tax/liquidity uncertainty explicit |
| Terminal policy | D&A scaled with sales | Opening PP&E and ROU policies applied | Correct mechanics; investment normalization still needs evidence |
| Headline valuation | Incomplete$40.74 subtotal | {money(v['per_share'])} core diagnostic; {money(hair)}-{money(gross)} carrying references | Full verified Amazon point value not claimed |

<!-- PAGEBREAK -->

## AI output challenged and disposition

The first model's source-token checks did not detect omitted cash investments or financing; passing arithmetic tests did not validate economic completeness. The financial review rejected the complete-value interpretation, corrected disclosed transactions and terminal consistency, and added targeted regression tests. Codex performed this separate review; it is not the student's assessed AI-off work. No forecast was tuned toward the market price.

## What changed from Edition A to Edition B, and why?

The recommendation changes to do not initiate because the evidence does not support authorizing a new position and the corrected base needs unsupported funding. The infrastructure-return concern remains, but it is now linked to signed operating cash flow, actual disclosed investments/funding, and an incomplete strategic-asset appraisal. The former83.83% downside is withdrawn as a full-company claim. Subsequent work remains transparently AI-assisted.
'''
    write(HERE/'docs/research-evolution.md',evolution)
    validation=f'''# Validation and AI Use | reviewed package

## Decision, version, and as-of boundary

Do not initiate at September10 2026 reference price. Local uncommitted Edition B; actual output timestamp {d['generated_at_utc']}. Source availability is distinguished from later retrieval and retrospective judgments. No upload or receipt is claimed.

## Data and convention ledger

data/assumptions.csv and data/source_register.csv retain source/units/classification records. New review facts and exact locators are in docs/financial-review.md, evidence/financial_review.json and data/financial-review-inputs.csv. The adapted statements.py leaves lab10 unchanged. The model is not an exact seasonal or September10 balance roll-forward; strategic cases are carrying references, not a net economic appraisal.

## Actual validation register

{tests['tests_run']} model tests executed: {tests['passed']} passed, {tests['failed']} failed, {tests['errors']} errors, {tests['skipped']} skipped. Seven dashboard pages execute. Technical cold-run status {cold['status']}; see evidence/cold_run.md. Historical64-file hashes pass. Latest logs are evidence/validation_results.txt and validation_summary.json. No test is credited merely because code exists.

| Claim/failure | Test and actual result | Disposition/evidence |
|---|---|---|
| Legacy calculations | Original Lab10 outputs reproduce | Historical files unchanged |
| Arithmetic and definitions | Signed-flow, statement, WC/PPE/lease, WACC, bridge, shares, peer, scenario and solver tests pass | Automated evidence; not source truth |
| Review omission: cash investments | Known61067m enters other assets/CFI; does not enter FCFF | Funding pass withdrawn; tests50/52/57 |
| Review omission: July notes |25000m added to funding, bridge and debt weight | Test51 and known-cash bridge test58 |
| Terminal policy mismatch | Opening-asset D&A/rental schedules recomputed | Tests53/54; source-backed policies retained |
| Strategic-asset double count | Payment deducted once; gross assets added separately | Tests55/56/58; tax case explicitly hypothetical |
| Source correctness | Twelve annual statement rows matched in relevant table columns, EBIT identity reconciled | financial_review.json; AI-executed separate review |

Earlier actual development failures are retained in validation_first_run_failed.txt and environment_failures.md. The first49-test build passed despite financial omissions: that is why the source/economic review matters. No artificial failed tests or human checks are added for appearance.

## Locked Changed-Input Record | awaiting independent student work

Exact course requirement: human-authored prediction before AI assistance on it and before execution; timestamp/repository commit; exact old/new units; expected direction and decision effect; AI-closed run; actual before/after results and diagnosis. docs/student-ai-off-worksheet.md supplies mechanical instructions and an unexecuted runner. No new input value, prediction, precommit or assessed output has been filled in. Ordinary automated scenarios do not satisfy this record. The PDF must be updated with actual student evidence before claiming completion.

## Named AI-use and disposition register

| Tool/surface | Date | Material contribution | Check/disposition | Decision effect |
|---|---|---|---|---|
| Codex; underlying model/version not exposed in runtime evidence | October19 2026 | Initial implementation, research, tests, dashboard and drafts | Qualified; prior core subtotal was incomplete | Old headline withdrawn |
| Codex separate final review | October19 2026 | Filing-table/economic audit; known-transaction and terminal corrections; documents | Source-row checks, dual FCFF routes, targeted regressions; student review pending | Do not initiate; no verified full-company point value |
| Historical Codex disclosure | September1 draft metadata / lab records | Filing organization, original drafting and lab assistance | Preserve actual disclosures; no AI-free attestation | Accurate provenance |

| Material AI claim | Disposition | Evidence |
|---|---|---|
| $40.74 is an adequate company-value headline | Reject | Omitted strategic assets and funding cash flows |
| Funding passes under base | Correct | Include both investment61067m and July notes25000m; base fails2028-2029 |
| Terminal proportional D&A preserves original policy | Correct | Apply15% to opening net PPE and opening ROU/liability rent |
|22% of strategic gross assets is an actual tax liability | Reject | It is only a transparent haircut sensitivity; no tax basis appraisal |
| Original Edition A is AI-free/submitted | Reject | Historical checkout and absent receipt; later addition separately dated |

## Limits, monitoring and student evidence

Unlevered taxes are a provision-as-cash proxy; strategic tax/liquidity appraisal, actual/forecast stub and exact-date share bridge remain unresolved. Segment margins are not independently forecast. Full Brightspace assignment and analytic rubric were not accessible. Human source checks, assessed AI-off evidence, actual videos/transcripts and access checks remain pending. User-supplied October19 announcement is retained without inventing original posting access or recovery waiver.
'''
    write(HERE/'docs/validation-and-ai-use.md',validation)
    write(HERE/'evidence/convention_decisions.md',detail)
    # Source locators for every new material fact and correction.
    inputs=[dict(item='H1 acquisition/nonmarketable cash uses',old=0,new=39767,unit='USD million',classification='reported',source=c.SEC,locator='Cash-flow statement p3; six months ended June30 2026'),
      dict(item='Subsequent OpenAI investment payment',old=0,new=21300,unit='USD million',classification='reported subsequent event',source=c.SEC,locator='Note2 Non-Marketable Investments; subsequent to June30'),
      dict(item='Subsequent July notes',old=0,new=25000,unit='USD million',classification='reported subsequent event',source=c.SEC,locator='Note5 Debt; subsequent issuance; July pricing source'),
      dict(item='Strategic gross assets incl subsequent purchase',old=0,new=246195,unit='USD million',classification='reported carrying references',source=c.SEC,locator='Note2 private equity122300 / notes97900 / equity-method395 / warrants4300 + subsequent21300'),
      dict(item='Strategic haircut diagnostic',old='none',new=.22,unit='fraction of preexisting gross carrying assets',classification='sensitivity assumption, not reported tax',source='Inherited normalized tax proxy; not issuer tax basis',locator='Explicit diagnostic only'),
      dict(item='FY2031 D&A',old=review['old_terminal']['eligible_da'],new=t['eligible_da'],unit='USD million',classification='formula correction',source='Forecast opening PP&E policy, model.py',locator='15% * ending2030 PP&E'),
      dict(item='Recurring residual cost ratio',old=.23205807031149744,new=d['base']['inputs']['other_cost_ratio'],unit='fraction of revenue',classification='Named nonrecurring-charge normalization judgment',source=c.K,locator='Note1 Q3 2025 FTC settlement2500; remove2500/716924 from recurring residual cost only'),
      dict(item='WACC',old=review['old_wacc'],new=v['wacc'],unit='annual decimal rate',classification='known debt-weight correction',source=c.SEC,locator='Known July issuance included; other CAPM assumptions unchanged')]
    with (HERE/'data/financial-review-inputs.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(inputs[0]));w.writeheader();w.writerows(inputs)
    update_recordings(d,tests)
    for name,title in [('decision-memo','Reviewed committee decision'),('research-evolution','Research evolution'),('validation-and-ai-use','Validation and AI use')]:
        pdf((HERE/f'docs/{name}.md').read_text(encoding='utf-8'),HERE/f'docs/{name}.pdf',title)
    pages=len(PdfReader(HERE/'docs/decision-memo.pdf').pages)
    if pages>2:raise ValueError('Memo exceeds two-page limit')
    for name,target in [('decision-memo','Decision-Memo'),('research-evolution','Research-Evolution'),('validation-and-ai-use','Validation-and-AI-Use')]:shutil.copyfile(HERE/f'docs/{name}.pdf',HERE/f'submission/{target}.pdf')
    with (HERE/'submission/project-submission-manifest.csv').open(encoding='utf-8',newline='') as f:manifest=list(csv.DictReader(f))
    for item in manifest:
        if item['item'] in ['Research-Evolution.pdf','Decision memo or deck']:item['notes']='Reviewed local draft; requires student review; no upload/receipt claimed.'
    with (HERE/'submission/project-submission-manifest.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(manifest[0]));w.writeheader();w.writerows(manifest)
    print(f'Reviewed documents generated; memo {pages} pages. No complete intrinsic-value point estimate asserted.')

def update_recordings(d,tests):
    v=d['base']['valuation'];s=d['strategic_investments'];lo=s['cases'][1]['per_share'];hi=s['cases'][0]['per_share']
    scripts={
    1:('Research evolution',3,f'''[Display docs/historical/amazon-edition-a.md.]

My original September1 draft said watch/defer because I did not know whether AWS growth would produce enough cash to justify infrastructure spending. That original is unchanged. The checkout disclosed Codex help; I do not claim an AI-free baseline or verified receipt.

[Display research-evolution.md, October19 addition and change table.]

The falsification question was added October19, not backdated. It asks what happens if AWS growth and cash flow weaken while investment stays high. The professor's clarification says preserve the original and continue; the package keeps that provenance accurately.

[Display financial-review.md waterfall.]

The initial Edition B produced40.74, but passing tests did not make it economically complete. The final review found omitted investment cash uses and July financing. It also found that terminal depreciation no longer followed the forecast's own rule. These were corrected from the filing and accounting policies, without targeting the market price.

The action changes to do not initiate. That is a decision not to authorize a new position under present evidence, not proof of an80% market mispricing. The core subtotal is $39.05 and excludes strategic assets; it is not total fair value. The corrected base fails funding and the strategic investment appraisal remains incomplete. The main lesson is that reproducible arithmetic and defensible investment judgment require different checks.

[Display validation record.]

Codex assisted the code, review and drafts. Automated evidence is identified as automated. The separate human AI-off record and actual recording evidence must be completed honestly; neither is reconstructed as historical work.'''),
    2:('Code and validation',5,f'''[Display README, then model.py and statements.py.]

The application uses a separate Edition B workspace; historical labs and original evidence are unchanged. The adapted statement engine starts with reported FY2025 balances and forecasts2026 through2030. Cash follows operating, investing and financing cash flows; it is not a balance-sheet plug.

[Display financial statements and nonoperating investment row.]

The review added39.767billion of first-half investment uses,21.3billion of subsequent OpenAI funding and25billion of July notes. The asset purchases reduce cash and increase other assets; borrowing enters financing. Neither becomes operating FCFF. The corrected base fails the funding floor in2028 and2029, even though accounting identities reconcile.

[Display FCFF reconciliation and terminal schedule.]

FCFF uses EBIT, an explicitly qualified22% unlevered tax proxy, eligible depreciation, capital investment and working capital. Negative cash flows remain signed. New finance-lease assets count as investment; principal is financing. Operating leases remain rent, so their liability is not deducted again. Capital AP provides investment working-capital funding.

The terminal correction applies15% to opening net PP&E, rather than growing last year's D&A with sales. Rental expense also follows opening assets and liabilities. Terminal investment still normalizes downward: that is an important assumption requiring evidence, not an established fact.

[Display tests and actual log.]

The latest suite has{tests['passed']} passing model tests. It includes the original known answer and statement regression, cash-flow identities, negative FCFF, WACC/bridge/share checks, peers, scenario isolation, reverse repricing and deliberate accounting failures. New targeted tests cover the omitted investments, July debt, terminal policy and strategic-asset double counting. Seven dashboard pages and the technical cold run also execute.

[Display student worksheet and limitations.]

Those results do not certify my independent source checking or the AI-off exercise. The model remains approximate on seasonality, exact-date balances, diluted shares, taxes and segment profitability. The code makes these limits and funding failures visible rather than producing a false precise fair value.'''),
    3:('Committee defense and live application',5,f'''[Decision page: lead with action.]

I recommend do not initiate Amazon at the dated251.89price. The fund has no position. I am not recommending a short or claiming the market is demonstrably wrong; I am declining to authorize a purchase on incomplete and funding-constrained evidence.

[Show strategic bridge and core diagnostic.]

The corrected core subtotal is{money(v['per_share'])}, with WACC{v['wacc']:.2%} and terminal growth2.5%. This is not total Amazon fair value. Adding strategic investments at reported carrying references gives{money(lo)}to{money(hi)}under two clearly labeled haircut conventions. They are not fair-value bounds: tax basis, liquidity, restrictions and commercial correlations remain unappraised.

[Financial statements, select base; then Scenarios & funding.]

AWS and advertising growth do not establish infrastructure returns. The review included both disclosed investment cash uses and July financing. Even so, the base fails its cash floor in2028-2029. Only high passes among low, base and high; one valid case is not a valuation range. A negative cash balance here is a diagnostic funding shortfall, not a viable asset forecast or proof of default.

[FCFF & capital: cash flows, terminal, bridge.]

Signed operating FCFF excludes borrowing and investment-asset purchases. Leases and capital payables are reconciled consistently. The old terminal calculation understated policy-consistent D&A; that is corrected. Terminal investment still falls below the forecast level, so the remaining normalization is favorable model risk. Terminal dependence above100% results from negative explicit-period present value.

[Comparable companies page.]

Walmart and Microsoft are qualified retail and cloud references, not replicas of Amazon. P/E includes different reported earnings and investment effects. EV multiples require an equity bridge. Fiscal periods and omitted nonoperating appraisals limit comparability, so I do not average methods to create a target.

[Return to Decision page.]

Reopen only with documented funding covering commitments, supported operating returns and reinvestment, an exact dated equity bridge and a defensible margin of safety versus a new price. The committee ask today is no new position, with a clearly defined evidence review rather than a forced valuation conclusion.''')}
    for n,(title,limit,text) in scripts.items():
        text=re.sub(r'(?<=\d)(?=[A-Za-z])',' ',text)
        text=re.sub(r'(?<=[A-Za-z])(?=\d)',' ',text)
        words=len(re.findall(r'\b[\w\'-]+\b',re.sub(r'\[[^\]]*\]','',text)))
        estimate=words/125+({1:.3,2:.9,3:1.2}[n])
        header=f'# Video {n} | {title}\n\nAI-assisted speaking draft, NOT an actual transcript. {words} approximate spoken words; about {estimate:.1f} minutes at 125 wpm including transitions; hard limit {limit}:00. Review and use your own words. Do not claim checks not personally performed.\n\n'
        write(HERE/f'docs/video-{n}-script.md',header+text)
        displays={1:'Original Markdown -> research evolution later addition/table -> financial-review waterfall -> AI-use record',2:'README -> model.py/statements.py -> statements/CFI -> FCFF/terminal -> actual tests/log -> student worksheet',3:'Decision -> strategic bridge -> base financials -> Scenarios & funding -> FCFF/terminal/bridge -> Comparables -> Decision'}
        questions={1:'Why did your decision change? The reviewed funding and bridge evidence changed; the original was preserved. Was Edition A AI-free/submitted? Not claimed; the actual disclosure and absence of receipt are explicit.',2:'Do passing tests validate economics? No; source and definition checks found omissions after49 tests passed. Is22% actual cash tax? No; normalized provision-as-cash proxy. Did AI perform your assessment? No assessed run is claimed.',3:'Why no purchase rather than watch? No validated positive purchase case and corrected base funding failure; a research watchlist can continue without capital. Is the stock80% overvalued? No such comprehensive claim is made. Why TV over100%? Explicit-period PV is negative. What changes the decision? Documented funding, supported reinvestment and complete dated valuation with margin of safety.'}
        write(HERE/f'docs/video-{n}-recording-outline.md',header+f'## Display sequence\n\n{displays[n]}\n\n## Committee questions and defensible answers\n\n{questions[n]}\n\n## Numbers\n\nCore{money(v["per_share"])}is diagnostic; strategic carrying references{money(lo)}-{money(hi)}are not fair-value bounds; price251.89as ofSeptember10; WACC{v["wacc"]:.2%}; g2.5%; base funding fails2028-2029. Only high passes funding. Show values in the current application rather than memorizing stale figures.')
    write(HERE/'docs/recording-guide.md','# Recording guide | final review\n\nRead the three scripts and paired outlines. They contain display sequences, timing estimates and committee Q&A. No recordings or actual transcripts are claimed. Use the current generated values and clearly distinguish core subtotal from strategic carrying references. The old $40.74 and 83.83% downside are historical, withdrawn headline claims.\n\nVideo 1 <=3:00; Video 2 <=5:00; Video 3 <=5:00 with live product demonstration as its main delivery. Include the small webcam view specified in the architecture unless an approved accommodation provides an equivalent. Record personally; correct finance terms, numbers, names and speaker attribution in actual transcripts afterward. Provide three separate descriptive Unlisted or Public YouTube links, never Private, or an approved Purdue-hosted equivalent. Add actual durations, evidence timestamps and logged-out/grader access checks to the 12-row manifest. Do not replace a frozen final recording after the applicable deadline.\n\nThe existing transcript files are clearly labeled templates and must not be submitted as completed transcripts.')

if __name__=='__main__':main()
