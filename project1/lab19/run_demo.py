"""Execute every skill on saved facts, probe skill configuration, and audit real memos."""
from pathlib import Path
import sys, subprocess, json
sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel

ROOT = panel.ROOT

def main():
    executions = []
    for ticker in ('COST','NVDA','JPM'):
        for slug in panel.SLUGS:
            script = ROOT/'.agents/skills'/f'{slug}-panel/scripts/run.py'
            run = subprocess.run([sys.executable, '-B', str(script), ticker, '--offline'], capture_output=True, text=True)
            executions.append({'ticker':ticker, 'skill':slug+'-panel', 'exit_code':run.returncode})
            (ROOT/'evidence'/f'{ticker}_{slug}_execution.txt').write_text(run.stdout+run.stderr, encoding='utf-8')
            if run.returncode:
                raise RuntimeError(run.stderr)
    config = ROOT/'.agents/skills/cathie-wood-panel/scripts/config.json'
    original = config.read_bytes()
    try:
        config.write_text('{"growth_threshold": 0.05}\n', encoding='utf-8')
        run = subprocess.run([sys.executable, '-B', str(config.with_name('run.py')), 'COST', '--offline'], capture_output=True, text=True)
        (ROOT/'evidence/threshold_probe.txt').write_text('Actual skill config temporarily changed to 0.05.\n'+run.stdout+run.stderr, encoding='utf-8')
        if run.returncode:
            raise RuntimeError(run.stderr)
    finally:
        config.write_bytes(original)
    audit = {}
    for ticker in ('COST','NVDA','JPM'):
        report = json.loads((ROOT/'evidence'/f'{ticker}_report.json').read_text())
        for slug in panel.SLUGS:
            path = panel.memo_path(ticker, slug)
            audit[path.name] = panel.unsupported_numbers(path.read_text(encoding='utf-8'), report)
    (ROOT/'evidence/skill_executions.json').write_text(json.dumps(executions,indent=2),encoding='utf-8')
    (ROOT/'evidence/memo_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    assert all(not flags for flags in audit.values()), audit
    print(f'{len(executions)} skill executions succeeded; {len(audit)} saved memos audited; threshold configuration restored.')

if __name__ == '__main__':
    main()
