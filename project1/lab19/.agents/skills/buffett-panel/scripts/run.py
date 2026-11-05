"""Executable entry point for the Buffett skill."""
from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
import panel
if __name__ == '__main__':
    config = json.loads(Path(__file__).with_name('config.json').read_text())
    panel.main('Buffett', config['growth_threshold'])
