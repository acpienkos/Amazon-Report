"""Compatibility entry point: render reviewed Markdown without regenerating stale prose.

Historical financial-review generation is preserved in the experiment Git commit.
Final packaging uses the authored Markdown as its source of truth.
"""
import sys
sys.dont_write_bytecode=True
from build_documents import main
if __name__=='__main__':main()
