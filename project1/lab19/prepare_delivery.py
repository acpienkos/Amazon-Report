"""Write final checkout text after committing; clipboard transfer is a separate verified step."""
from pathlib import Path
import json,subprocess,re
ROOT=Path(__file__).resolve().parent
GIT='C:/Program Files/Git/cmd/git.exe'

def main():
    commit=subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    base=f'https://github.com/acpienkos/Amazon-Report/blob/{commit}/project1/lab19'
    tree=f'https://github.com/acpienkos/Amazon-Report/tree/{commit}/project1/lab19'
    verification=json.loads((ROOT/'evidence/verification.json').read_text())
    audit=json.loads((ROOT/'evidence/package_audit.json').read_text())
    inventory=(ROOT/'FILES.md').read_text(encoding='utf-8')
    count=re.search(r'(\d+) files:',inventory).group(1)
    disclosure='Codex read the official instructions and investor references, built the skills and app, downloaded SEC data, wrote the simulated investor memos and answer drafts, and ran the checks. I still need to review the decision and complete the personal checkout activities; those are not claimed as my own completed checks.'
    brightspace=f'''Lab 19 — Legend Panel

I extended the Buffett screen with cathie-wood-panel and burry-panel; buffett-panel keeps the original checks. All three use the same SEC 10-K facts, with calculations in code and separate AI-written business memos.

COST matches the official answer: Buffett passes all three checks, Wood's growth check fails at 7.51% and R&D stays not known, and Burry passes both. Changing Wood's skill threshold to 5% makes growth pass without changing the R&D gap. The retained threshold is 15% to keep the growth standard consistent.

For the company run, VT is the working fund assumption from my proposed Project 2 universe, still needing confirmation. Its saved September 30 holdings page lists NVDA as the largest company. NVIDIA passes Buffett's three and Wood's two checks; Burry's cash-flow check fails while leverage passes. The verdicts are watch / own / watch. Latest operating cash flow is 102,718 versus net income of 120,067 USD millions, so the disagreement has a clear basis in the same facts.

Bull: NVIDIA passes Buffett's profitability and owner-earnings checks, and its 68.30% revenue CAGR and 8.57% latest R&D/revenue pass Wood's screens. Latest liabilities/equity of 0.31 also passes Burry's leverage check, supporting more research.

Bear: Burry's cash-conversion check fails, with operating cash flow below net income in several years. The other passes do not explain that gap or establish durable future earning power.

My proposed decision is conditional: use the panel to shortlist research candidates only after verifying the fund holding and SEC inputs, then investigate NVIDIA's cash-versus-earnings gap and business durability before acting.

Codex executed {verification['tests_run']} Lab 19 tests and 7 Lab 18 regression tests, all passing; all three skills validated and were discovered by Codex. Nine skill runs succeeded, nine memos had no unsupported numeric tokens, and inserting 40.0% was flagged in every investor column. Missing COST R&D and JPM owner earnings were preserved.

Files: {tree}
Results and memos: {base}/RESULTS.md
Skills: {tree}/.agents/skills
App: {base}/app.py
Calculations: {base}/panel.py
Evidence: {tree}/evidence
Checklist: {base}/CHECKLIST.md
Commit: {commit}

Status: this is a prepared checkout response. The commit is local and must be pushed before these GitHub links resolve. Fund confirmation, student review, partner discussion/no-AI explanation, and the actual Brightspace quiz submission are not claimed complete. The private quiz questions were not accessed.

AI use: {disclosure}'''
    final=f'''Lab 19's local implementation is complete and committed. Personal checkout and publication remain open; I cannot honestly mark the whole assignment complete yet.

**A. Official requirement checklist**

| Requirement | Result |
|---|---|
| Read official Lab 19, embedded rubric, handout, prework, slides and investor references | PASS |
| Preserve Lab 18 functionality and prior files | PASS |
| Discoverable, executable Buffett/Wood/Burry skills | PASS |
| Shared SEC 10-K facts, required tags, formulas and seven checks | PASS |
| COST known answer, honest gaps and 5% threshold probe | PASS |
| Separate printed-number-only memos; three-column app, verdicts and flags | PASS |
| NVDA company panel, verdicts and memos | PASS; VT fund assumption unconfirmed |
| Two-sentence bull/bear and conditional decision | PASS as reviewable drafts |
| Personal fund confirmation, partner activities and no-AI explanation | FAIL — not verified complete |
| Published GitHub evidence and individual Brightspace checkout | FAIL — not performed |

The [full requirement checklist]({base}/CHECKLIST.md) records each artifact and personal-activity boundary. No grade is claimed.

**B. Files**

Created **{count} files**, all under `project1/lab19/`; **no existing tracked files modified**. The [exact file inventory]({base}/FILES.md) lists every path. Main files: `README.md`, `ANSWERS.md`, `RESULTS.md`, `CHECKLIST.md`, `panel.py`, `engine.py`, `app.py`, `tests/test_panel.py`; three `.agents/skills/*-panel/` packages; nine `memos/*.md`; SEC/reference snapshots and actual execution evidence. Local delivery copies are `lab19/submission/FINAL_RESPONSE.txt` and `BRIGHTSPACE.txt`.

**C. Validation**

- {verification['tests_run']}/{verification['tests_run']} Lab 19 tests and 7/7 Lab 18 tests passed; zero failures/errors.
- 3/3 skills validated and discovered by Codex, with zero discovery errors.
- 9/9 skill executions succeeded; 9/9 memos had zero unsupported-number flags.
- All 35 inherited COST financial cells, ten new ratio/gap cells, CAGR and seven checks match the official tables.
- 5% probe passes growth; R&D stays unknown; retained 15% restored.
- Number injection flagged in all three app columns; {audit['source_hashes_verified']} source hashes verified; no scanned credential-pattern hits.

The UI was checked with Streamlit AppTest; no manual visual inspection is claimed. Prior untracked Lab 13 work was preserved.

**D. Commit and links**

`{commit}` — Complete Lab 19 legend panel skills and verified SEC workflow.

[Lab folder]({tree}) · [Results/memos]({base}/RESULTS.md) · [Skills]({tree}/.agents/skills) · [Tests/evidence]({tree}/evidence)

**Not pushed. These commit links will resolve only after publication.**

**E. READY-TO-PASTE BRIGHTSPACE SUBMISSION**

{brightspace}

**F. BRIEF AI DISCLOSURE**

{disclosure}

**G. Remaining manual checkout**

Confirm VT is a Project 2 fund, review/adopt the draft decision, complete the partner activities and no-AI code explanation, publish the commit, and open Brightspace → Quizzes → Lab 19 to answer the actual questions and submit. Public instructions request GitHub file links; no private quiz questions or submission receipt were accessed. The stated deadline is November 5 at 6:00 PM Eastern.

The complete response and Brightspace-only text are saved as UTF-8 delivery files. Clipboard transfer is reported separately only after an actual read-back check.'''
    directory=ROOT/'submission'
    directory.mkdir(exist_ok=True)
    (directory/'BRIGHTSPACE.txt').write_text(brightspace,encoding='utf-8')
    (directory/'FINAL_RESPONSE.txt').write_text(final,encoding='utf-8')
    print(commit)
    print('Final response saved:',directory/'FINAL_RESPONSE.txt')

if __name__=='__main__':main()
