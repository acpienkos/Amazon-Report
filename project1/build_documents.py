"""Generate reviewed artifacts from current saved outputs."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.dont_write_bytecode=True
from review_documents import main
if __name__ == "__main__":
    main()
