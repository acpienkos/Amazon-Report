# Step 2 completion report | Amazon Project 1

Documentation cleanup and local submission preparation are complete. The project is NOT SUBMITTED and is not ready for a final readiness claim until the student completes recordings, transcripts, access checks, final version freeze and authoritative Brightspace checks.

## Files modified or added

Paths are relative to the repository root. This list compares SHA256 against the start of Step 2; generated files whose bytes remained identical are excluded. No student-only files are in this list.

- `project1/.gitattributes`
- `project1/README.md`
- `project1/analysis.py`
- `project1/audit_package.py`
- `project1/build_documents.py`
- `project1/docs/decision-memo.md`
- `project1/docs/decision-memo.pdf`
- `project1/docs/final-submission-checklist.md`
- `project1/docs/recording-guide.md`
- `project1/docs/research-evolution.pdf`
- `project1/docs/step2-completion-report.md`
- `project1/docs/student-ai-off-worksheet.md`
- `project1/docs/validation-and-ai-use.md`
- `project1/docs/validation-and-ai-use.pdf`
- `project1/docs/video-1-recording-outline.md`
- `project1/docs/video-1-script.md`
- `project1/docs/video-2-recording-outline.md`
- `project1/docs/video-2-script.md`
- `project1/docs/video-3-recording-outline.md`
- `project1/docs/video-3-script.md`
- `project1/evidence/documentation_cleanup.json`
- `project1/evidence/final_audit.json`
- `project1/evidence/final_audit.md`
- `project1/evidence/pdf_render_inventory.json`
- `project1/evidence/step2_test_results.txt`
- `project1/evidence/step2_test_summary.json`
- `project1/evidence/validation_results.txt`
- `project1/evidence/validation_summary.json`
- `project1/exercise_audit.py`
- `project1/outputs/valuation-report.md`
- `project1/outputs/valuation.json`
- `project1/outputs/visible_output.json`
- `project1/review_documents.py`
- `project1/submission/Decision-Memo.pdf`
- `project1/submission/Research-Evolution.pdf`
- `project1/submission/Validation-and-AI-Use.pdf`
- `project1/submission/project-submission-manifest.csv`
- `project1/tests/test_exercise_audit.py`
- `project1/tests/test_project.py`

The ordinary dashboard test report project1/evidence/app_test.json was refreshed but its bytes remained identical. Temporary ignored QA artifacts: project1/tmp/step2/ hash snapshots and contact sheet, plus 12 rendered page PNGs in project1/tmp/pdfs/. No runtime, historical lab, frozen model, original prediction or experiment-input changes were made.

## Test and audit results

- All 59 existing model tests pass; all 6 new memory-only evidence-verifier tests pass. Full 65-test run: project1/evidence/step2_test_results.txt and step2_test_summary.json.
- Seven dashboard pages execute successfully with Streamlit AppTest. The bare-mode ScriptRunContext warning is informational; there are no page exceptions.
- Corrected package audit: 40 technical checks pass, zero fail. Eight submission gates remain incomplete: three videos with metadata/access, three actual transcripts, final repository access confirmation, and the final package version freeze.
- Video 2 commands were executed successfully: exact saved-baseline reproduction and both deliberate fault-injection tests.
- PDF visual inspection passed for all 12 pages: memo 2, research evolution 4, validation 6. Submission copies are byte-identical. The PDF contains the original prediction, receipt and updated reconciliation; source/PDF text-fidelity checks pass.
- All five student-only files plus project1/data/student-change.json match their Step 2 starting SHA256 exactly. All nine frozen source hashes match the saved runs; source contents match commit 99b99d0141f9a52510d71494943864c8cf4b6f71. HEAD remains that commit.
- Financial output is unchanged against the frozen commit except for updated AI/evidence disclosure metadata. No model or scenario assumption was changed and no assessed runner was executed.

## Technical disposition

No unresolved test or package-verification failure. Audit checks distinguish technical consistency from student-reported independent conduct; they cannot certify AI-OFF compliance. Source definitions, seasonal/date alignment, tax and diluted-share proxies, terminal investment normalization, strategic-asset value and segment profitability remain disclosed financial limitations rather than resolved facts. The previously recorded isolated technical cold run remains evidence; a new human-observed cold run is not claimed.

## Personal checklist

- Review the six-page validation PDF against your preserved work and verify consequential sources, financial judgments and the DO NOT INITIATE decision.
- Read and rehearse the three complete scripts. Record personally with clear audio and a small webcam view unless an approved accommodation provides an equivalent.
- Create actual corrected transcripts at project1/docs/transcript-video-1.txt, transcript-video-2.txt and transcript-video-3.txt after recording; existing placeholders remain untouched.
- Supply three separate descriptive YouTube links (Unlisted or Public, never Private) or approved Purdue-hosted alternatives, actual titles/durations, evidence timestamps and access confirmations. Enter them in project1/submission/project-submission-manifest.csv and verify instructional-team playback/captions through the appeal window.
- Obtain the authoritative Brightspace brief and rubric: deadline, filename prefix, grader access identity, any human cold-run requirement, approved accommodations and any separate early-AI recovery directions. Do not fabricate an Edition A receipt or assume the October clarification waives another rule.
- Review all final PDF/transcript/repository versions for agreement. Authorize the final commit and push separately; the post-run evidence and cleanup are currently local. Verify repository access, personally upload the required bundle and retain the actual submission receipt.

## Exact recording sequence

1. Video 1: open project1/docs/video-1-script.md. Pre-open the historical original, Edition B change table, financial-review waterfall, compiled validation PDF and reconciliation in read-only view. Rehearse its 0:00-2:50 sequence, then record below 3:00. Show one AI-generated result and its correction, research evolution, and the independent changed-input result. No assessed rerun.
2. Video 2: open project1/docs/video-2-script.md. From the repository-root terminal run its exact read-only baseline comparison and two deliberate-failure tests on camera, then the 59-test model suite. Show model.py, statements.py, README, the tests and visible report. Rehearse to 4:45 and keep below 5:00. The commands have been verified on this checkout.
3. Video 3: start `project1/.runtime/python.exe -m streamlit run project1/app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false`, open http://127.0.0.1:8501 and follow project1/docs/video-3-script.md. Keep the live product visible while navigating decision, base funding, FCFF/bridge, sensitivity and comparables. Return to the committee ask. Rehearse to 4:45 and keep below 5:00; stop the server with Ctrl+C afterward.

Script section times are rehearsal targets. Replace them with actual evidence timestamps only after recording. Prepared scripts are not transcripts. The full final checklist is project1/docs/final-submission-checklist.md; the machine-readable protection and verification receipt is project1/evidence/documentation_cleanup.json.
