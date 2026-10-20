"""Verify preserved Lab 13 / Project 1 source and artifact hashes."""
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
manifest = json.loads((here / "preservation_manifest.json").read_text())
changed = [name for name, expected in manifest.items()
           if not (here.parent / name).is_file()
           or hashlib.sha256((here.parent / name).read_bytes()).hexdigest() != expected]
if changed:
    raise SystemExit("Preservation failed: " + ", ".join(changed))
print(f"PASS: {len(manifest)} preserved Lab 13 / Project 1 source and artifact files")
