"""Import the skill's single implementation without copying calculation logic."""
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).parent / '.agents/skills/buffett-edgar/scripts/companyfacts.py'
spec = importlib.util.spec_from_file_location('buffett_companyfacts', SCRIPT)
sec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sec)
