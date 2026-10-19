"""Final mechanical package audit; never represents pending human work as done."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
import json,csv,hashlib,subprocess
from datetime import datetime,timezone
from pypdf import PdfReader
import analysis
def main():
    checks=[]
    def check(name,condition):checks.append(dict(check=name,passed=bool(condition)))
    d=json.loads((HERE/'outputs/valuation.json').read_text())
    v=json.loads((HERE/'evidence/validation_summary.json').read_text())
    app=json.loads((HERE/'evidence/app_test.json').read_text())
    cold=json.loads((HERE/'evidence/cold_run.json').read_text())
    check('Historical preservation',analysis.preserve_check()>=64)
    required=['app.py','model.py','config.py','analysis.py','README.md','requirements.txt','requirements-lock.txt',
      'data/historical_reported.csv','data/normalization.csv','data/assumptions.csv','data/source_register.csv',
      'outputs/valuation.json','outputs/visible_output.json','outputs/valuation-report.md','outputs/statements.csv',
      'outputs/fcff_reconciliation.csv','outputs/enterprise_equity_bridge.csv','outputs/comparables.csv','outputs/scenarios.csv',
      'outputs/sensitivity.csv','docs/research-evolution.pdf','docs/decision-memo.pdf','docs/validation-and-ai-use.pdf',
      'docs/historical/amazon-edition-a.md','docs/historical/lab-03-checkout-draft.md','submission/project-submission-manifest.csv',
      'docs/financial-review.md','docs/student-ai-off-worksheet.md','student_exercise.py','data/student-change.json',
      'outputs/review_waterfall.csv','outputs/debt_basis_reconciliation.csv',
      'docs/video-1-script.md','docs/video-2-script.md','docs/video-3-script.md']
    check('Required technical/local draft files exist',all((HERE/p).is_file() for p in required))
    check('Latest automated tests passed',v['failed']==0 and v['errors']==0 and v['passed']>=49)
    check('All dashboard pages executed',app['passed']==7 and app['failed']==0)
    check('Fresh environment technical cold run',cold['status']=='PASS' and cold['server']['health']=='ok')
    check('Visible JSON matches financial JSON',(HERE/'outputs/valuation.json').read_bytes()==(HERE/'outputs/visible_output.json').read_bytes())
    memo=(HERE/'docs/decision-memo.md').read_text(encoding='utf-8')
    check('Memo agrees with base result',f"${d['base']['valuation']['per_share']:,.2f}" in memo and f"{d['base']['valuation']['wacc']:.2%}" in memo)
    check('Committee memo <=2 pages',len(PdfReader(HERE/'docs/decision-memo.pdf').pages)<=2)
    check('PDF source/content copies identical',all((HERE/f'docs/{n}.pdf').read_bytes()==(HERE/f'submission/{s}.pdf').read_bytes() for n,s in [('research-evolution','Research-Evolution'),('decision-memo','Decision-Memo'),('validation-and-ai-use','Validation-and-AI-Use')]))
    with (HERE/'submission/project-submission-manifest.csv').open(encoding='utf-8',newline='') as f:manifest=list(csv.DictReader(f))
    check('Official 12-row manifest retained',len(manifest)==12 and sum(r['required']=='yes' for r in manifest)==11)
    check('Unrecorded transcripts clearly labeled',all('NOT RECORDED' in (HERE/f'docs/transcript-video-{i}.txt').read_text() for i in [1,2,3]))
    check('Only dated market observations claimed',d['as_of']=='2026-09-10' and d['price']==251.89)
    check('Reviewed recommendation consistent',d['recommendation']=='do not initiate' and 'DO NOT INITIATE' in memo)
    check('Base funding failure disclosed',not d['base']['funding_feasible'] and 'funding' in memo.lower())
    check('Strategic references separately disclosed','strategic_investments' in d and 'not' in d['strategic_investments']['status'].lower())
    check('Student exercise not fabricated',(HERE/'docs/student-ai-off-worksheet.md').exists() and not (HERE/'evidence/student-only/changed-result.json').exists())
    pending=['Student AI-off Locked Changed-Input Record and actual execution',
      'Personal source/definition verification and review of provisional financial judgments',
      'Actual recordings, corrected transcripts, stable video links and evidence timestamps',
      'Full Brightspace assignment/rubric/access requirements; precise separate early-AI recovery clarification',
      'Human independently observed cold run if required',
      'Final PDF review, permission for commit/push, grader access and personal submission']
    financial=['Seasonal/actual-period stub reconciliation','Exact valuation-date balance and diluted-share bridge',
               'Separate strategic-investment value and related taxes/commitments','Evidence for terminal capital-turnover transition']
    result=dict(audited_at_utc=datetime.now(timezone.utc).isoformat(),checks=checks,
      passed=sum(x['passed'] for x in checks),failed=sum(not x['passed'] for x in checks),
      student_tasks=pending,material_financial_limitations=financial,submission_ready=False,
      conclusion='Technical local draft built and tested; provisional financial results and essential student evidence prevent a claim of submission readiness.')
    (HERE/'evidence/final_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    text='# Final package audit\n\n'+result['conclusion']+'\n\n'+f"Mechanical checks: {result['passed']} passed, {result['failed']} failed.\n\n"
    text+='\n'.join(('- PASS ' if x['passed'] else '- FAIL ')+x['check'] for x in checks)
    text+='\n\n## Awaiting student action\n\n'+'\n'.join('- '+x for x in pending)
    text+='\n\n## Material financial limitations\n\n'+'\n'.join('- '+x for x in financial)
    text+='\n\nAll new work is local. No commit, push, deployment, Brightspace submission, checkpoint receipt, human prediction or recording is claimed. Original September1 Edition A is preserved; October19 additions remain later developments.\n'
    (HERE/'evidence/final_audit.md').write_text(text,encoding='utf-8')
    checklist=f'''# Final prioritized submission checklist

## A. Fully completed by Codex

- Preserved original September1 Edition A, October19 copy, checkout and Labs06-13;64-file hashes pass.105-file pre-review Project1 ZIP snapshot retained.
- Separate financial review of fifteen accounting/economic areas,12 annual source-row matches, corrected known investment/financing cash transactions and terminal policy; old/new waterfall retained.
- Integrated normalized statements, signed FCFF, WACC, terminal/bridge, seven cases, qualified comparables and reverse DCF. Outputs are correctly labeled diagnostic/provisional, not a verified intrinsic-value claim.
- Automated model and dashboard tests, technical cold run and package checks actually executed; failed development evidence retained.
- Reviewed PDF drafts, memo within2 pages, scripts/outlines, student worksheet and unexecuted assessed runner, visible reports and12-row manifest.

## B. Requires independent student work

1. With AI assistance off, choose the new input value, author and freeze the prediction, make the required actual repository-commit record personally if chosen, execute the assessed exercise and restoration check, and write the reconciliation. See student-ai-off-worksheet.md. No assessed run or prediction exists yet.
2. Personally verify consequential source definitions/calculations and explain the model. Automated/AI checks are not personal verification.
3. Record three videos, including the actual live application demonstration; correct the actual plain-text transcripts. Existing transcript files are placeholders, not submissions.
4. Perform or obtain any independently observed human README-only cold run required by the actual brief. The technical cold run is AI-operated.

## C. Requires review or approval

1. Review do-not-initiate decision, source-backed corrections and the distinction between {d['base']['valuation']['per_share']:.2f} core diagnostic and {d['strategic_investments']['cases'][1]['per_share']:.2f}-{d['strategic_investments']['cases'][0]['per_share']:.2f} carrying references. Approve a defensible research conclusion; do not claim precise total-company downside.
2. Review normalized tax, capital taper, terminal transition, dated bridge/dilution proxies and missing segment-profitability detail. No assumption was tuned to price.
3. Review all PDFs; incorporate actual independent exercise evidence into Validation-and-AI-Use.pdf before it is marked complete.
4. Obtain full Brightspace requirements, filename prefixes, rubric, grader access identity and any separate early-AI recovery clarification. Apply the newer October19 preserve-and-continue announcement accurately.
5. Authorize any desired Git commit/push separately; none performed by Codex. Complete real video/reader access checks. Personally submit before the actual deadline and save the real final receipt.

## D. Missing or unresolved

- Full Brightspace Project1 assignment and analytic rubric not accessible; no exact private assignment filename/access rules verified.
- Human AI-off assessed record, actual recordings/corrected transcripts, actual video URLs/durations/timestamps and access evidence are not complete.
- Exact September10 seasonal/actual-period cash-flow split and complete balance/dilution roll-forward; net economic appraisal/tax basis of strategic assets; supported terminal infrastructure returns; independently forecast segment margins remain unresolved. The package makes no complete verified fair-value claim.
- No checkpoint receipt is invented. The original AI-use disclosure remains. October19 additions are EditionB developments, not a backdated original or explicit recovery waiver.
- GitHub currently does not include uncommitted Project1 files. A repository URL by itself does not make this local package available to graders.

## Official-material comparison

Checklist: local reports, runnable code, visible outputs and manifest present; independent assessment and recording/transcript/access evidence incomplete.
Submission architecture: original included unchanged, reviewed research evolution and two-page memo present; three genuine ownership videos, locked record and frozen matching submission bundle still require completion.
AI Boundary Card: historical disclosure and unverified receipt preserved; independent AI-off task not fabricated; separate recovery interpretation unresolved rather than silently waived.
October19 clarification: original preserved; later improvements only in EditionB; no reconstructed original.
Analytic rubric: architecture identifies the six criteria but the actual rubric descriptors/weights were unavailable. No grade or full rubric compliance is claimed.

Submission readiness: NOT READY until essential student evidence, review/access and actual assignment checks are completed. A passing mechanical audit is not a completeness certificate.
'''
    (HERE/'docs/final-submission-checklist.md').write_text(checklist,encoding='utf-8')
    print(json.dumps(dict(passed=result['passed'],failed=result['failed'],submission_ready=False)))
    raise SystemExit(0 if result['failed']==0 else 1)
if __name__=='__main__':main()
