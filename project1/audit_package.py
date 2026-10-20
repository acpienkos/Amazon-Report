"""Final mechanical package audit; never represents pending human work as done."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
import json,csv,hashlib,subprocess,re
from datetime import datetime,timezone
from pypdf import PdfReader
import analysis
from exercise_audit import verify, FROZEN_COMMIT
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
      'docs/video-1-script.md','docs/video-2-script.md','docs/video-3-script.md',
      'exercise_audit.py','tests/test_exercise_audit.py']
    check('Required technical/local draft files exist',all((HERE/p).is_file() for p in required))
    check('Latest automated tests passed',v['failed']==0 and v['errors']==0 and v['passed']==59 and v['tests_run']==59)
    check('All dashboard pages executed',app['passed']==7 and app['failed']==0)
    check('Recorded isolated-environment technical cold run',cold['status']=='PASS' and cold['server']['health']=='ok')
    check('Visible JSON matches financial JSON',(HERE/'outputs/valuation.json').read_bytes()==(HERE/'outputs/visible_output.json').read_bytes())
    memo=(HERE/'docs/decision-memo.md').read_text(encoding='utf-8')
    check('Memo agrees with base result',f"${d['base']['valuation']['per_share']:,.2f}" in memo and f"{d['base']['valuation']['wacc']:.2%}" in memo)
    check('Committee memo <=2 pages',len(PdfReader(HERE/'docs/decision-memo.pdf').pages)<=2)
    check('PDF source/content copies identical',all((HERE/f'docs/{n}.pdf').read_bytes()==(HERE/f'submission/{s}.pdf').read_bytes() for n,s in [('research-evolution','Research-Evolution'),('decision-memo','Decision-Memo'),('validation-and-ai-use','Validation-and-AI-Use')]))
    with (HERE/'submission/project-submission-manifest.csv').open(encoding='utf-8',newline='') as f:manifest=list(csv.DictReader(f))
    check('Official 12-row manifest retained',len(manifest)==12 and sum(r['required']=='yes' for r in manifest)==11)
    check('Transcript state is explicit',all((HERE/f'docs/transcript-video-{i}.txt').is_file() and (HERE/f'docs/transcript-video-{i}.txt').stat().st_size>0 for i in [1,2,3]))
    check('Only dated market observations claimed',d['as_of']=='2026-09-10' and d['price']==251.89)
    check('Reviewed recommendation consistent',d['recommendation']=='do not initiate' and 'DO NOT INITIATE' in memo)
    check('Base funding failure disclosed',not d['base']['funding_feasible'] and 'funding' in memo.lower())
    check('Strategic references separately disclosed','strategic_investments' in d and 'not' in d['strategic_investments']['status'].lower())
    checks.extend(verify())
    validation=(HERE/'docs/validation-and-ai-use.md').read_text(encoding='utf-8')
    pdf_text=' '.join(page.extract_text() for page in PdfReader(HERE/'docs/validation-and-ai-use.pdf').pages)
    check('Validation PDF includes completed record and frozen commit',
          FROZEN_COMMIT in validation and FROZEN_COMMIT in pdf_text
          and 'completed student work' in validation
          and 'restored_exact_match' in pdf_text)
    normalize=lambda text:' '.join(re.sub(r'^#{1,6} +','',text,flags=re.MULTILINE).replace('**','').replace('`','').split())
    for name in ['prediction.md','commit-receipt.md','reconciliation.md']:
        original=(HERE/'evidence/student-only'/name).read_text(encoding='utf-8-sig')
        check('Validation source includes verbatim '+name, original in validation)
        check('Validation PDF includes student text: '+name, normalize(original) in normalize(pdf_text))
    pending=[
      'Personally review sources, financial judgments and the compiled validation PDF against preserved student evidence',
      'Record Videos 1/2/3, create corrected actual transcripts, supply stable URLs, durations and evidence timestamps',
      'Verify full Brightspace brief, rubric, filename prefixes, deadline and instructional-team access identity',
      'Resolve any separate historical early-AI recovery requirement with instructor; do not invent a checkpoint receipt',
      'Arrange human README-only cold-run observation if the authoritative brief requires one',
      'Verify grader access, authorize final commit/push separately, personally submit and retain actual receipt']
    financial=['Seasonal/actual-period stub reconciliation',
               'Exact valuation-date balance and diluted-share bridge',
               'Strategic-investment economic value and related taxes/commitments',
               'Evidence for terminal capital-turnover transition and segment profitability']
    readiness=[]
    def ready(name,passed,path):readiness.append(dict(check=name,passed=bool(passed),path=path))
    for i in [1,2,3]:
        video=next(row for row in manifest if row['item']==f'Video {i}')
        ready(f'Actual Video {i} and access metadata',
              all(video.get(k,'').strip() for k in ['location_or_url','title','duration_or_as_of','timestamp_index','access_checked']),
              'project1/submission/project-submission-manifest.csv')
        transcript=HERE/f'docs/transcript-video-{i}.txt'
        ready(f'Corrected actual transcript {i}', 'NOT RECORDED' not in transcript.read_text(),
              f'project1/docs/transcript-video-{i}.txt')
    repository=next(row for row in manifest if row['item']=='Repository')
    ready('Final repository access confirmed',bool(repository['access_checked'].strip()),
          'project1/submission/project-submission-manifest.csv')
    ready('Final package version frozen',all('final package uncommitted' not in row['frozen_or_commit_id'] for row in manifest if row['required']=='yes'),
          'project1/submission/project-submission-manifest.csv')
    result=dict(audited_at_utc=datetime.now(timezone.utc).isoformat(),checks=checks,
      passed=sum(x['passed'] for x in checks),failed=sum(not x['passed'] for x in checks),
      submission_checks=readiness,submission_checks_failed=sum(not x['passed'] for x in readiness),
      student_exercise=dict(status='COMPLETE: student-reported independent work; technically verified',frozen_commit=FROZEN_COMMIT,
                            ai_off_conduct_certified=False,student_files_modified=False),
      student_tasks=pending,material_financial_limitations=financial,submission_ready=False,
      conclusion='Completed independent experiment preserved and incorporated. Technical checks are separate from missing recordings, transcripts, access, final version freeze and personal submission. No submission is claimed.')
    (HERE/'evidence/final_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    text='# Final package audit\n\n'+result['conclusion']+'\n\n'+f"Technical checks: {result['passed']} passed, {result['failed']} failed. Submission gates incomplete: {result['submission_checks_failed']}.\n\n"
    text+='\n'.join(('- PASS ' if x['passed'] else '- FAIL ')+x['check']+((': '+x['detail']) if x.get('detail') else '') for x in checks)
    text+='\n\n## Submission checks\n\n'+'\n'.join(('- COMPLETE ' if x['passed'] else '- NEEDS STUDENT ACTION ')+x['check']+' | '+x['path'] for x in readiness)
    text+='\n\n## Student action\n\n'+'\n'.join('- '+x for x in pending)
    text+='\n\n## Financial limitations\n\n'+'\n'.join('- '+x for x in financial)
    text+='\n\nThe frozen prediction, input and model are unchanged. AI audited technical consistency after the student-reported independent run; automated checks do not prove AI-OFF conduct. Post-run evidence and cleanup are not yet a final committed package. No commit, push, recording, access confirmation or Brightspace submission was performed by this audit.\n'
    (HERE/'evidence/final_audit.md').write_text(text,encoding='utf-8')
    checklist='# Final submission checklist\n\n'+result['conclusion']+'\n\n## COMPLETE\n\n'
    checklist+='- Independent student prediction, commit receipt, changed run, restore result and reconciliation: `project1/evidence/student-only/`. Frozen input: `project1/data/student-change.json`.\n'
    checklist+='- Compiled record: `project1/docs/validation-and-ai-use.md`, matching PDF and `project1/submission/Validation-and-AI-Use.pdf`. AI development and later technical audit are separately disclosed.\n'
    checklist+='- Runnable dashboard, saved visible output, model tests and prepared timed scripts: `project1/app.py`, `project1/outputs/valuation-report.md`, `project1/tests/test_project.py`, `project1/docs/video-1-script.md`, `project1/docs/video-2-script.md`, `project1/docs/video-3-script.md`.\n'
    checklist+=f"- Latest technical audit: {result['passed']} passed, {result['failed']} failed; see `project1/evidence/final_audit.json`.\n"
    checklist+='\n## INCOMPLETE / NEEDS STUDENT ACTION\n\n'+'\n'.join('- '+x['check']+' | `'+x['path']+'`' for x in readiness if not x['passed'])
    checklist+='\n\n'+'\n'.join('- '+x for x in pending)
    checklist+='\n\n## Financial review and Brightspace boundary\n\n'
    checklist+='Core $39.05 is a funding-infeasible diagnostic. Strategic $57.06-$61.59 carrying references are not a verified fair-value range. The committee action remains DO NOT INITIATE. Full dated balance/dilution, seasonal cash flows, strategic tax/value, terminal investment and segment profitability remain limited. Review `project1/docs/financial-review.md`.\n\n'
    checklist+='The available course architecture requires three ownership videos (3/5/5 minute maxima), corrected transcripts, matching frozen PDFs, visible output and an accessible repository. Obtain the authoritative Brightspace brief, rubric, filename prefix, deadline, access identity, accommodation and any recovery directions. Preserve the historical Edition A disclosure and October 19 clarification; do not reconstruct a receipt or claim a waiver. No deployment is required by the inspected shared architecture, subject to Brightspace.\n\n'
    checklist+='No new assessed experiment is required by this cleanup. Do not edit or rerun student evidence. After actual recording and final review, authorize version control separately, verify access, personally upload the final bundle, and retain the real receipt. NOT SUBMITTED.\n'
    (HERE/'docs/final-submission-checklist.md').write_text(checklist,encoding='utf-8')
    print(json.dumps(dict(passed=result['passed'],failed=result['failed'],submission_checks_failed=result['submission_checks_failed'],submission_ready=False)))
    for item in checks:
        if not item['passed']:print('FAIL:',item['check'],item.get('detail',''))
    raise SystemExit(0 if result['failed']==0 else 1)
if __name__=='__main__':main()
