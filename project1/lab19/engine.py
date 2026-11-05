"""Lab 19 uses a self-contained copy of Lab 18's EDGAR extraction rules."""
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).parent / '.agents/skills/buffett-panel/scripts/companyfacts.py'
spec = importlib.util.spec_from_file_location('panel_companyfacts', SCRIPT)
sec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sec)
