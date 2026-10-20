"""Render reviewed Markdown; never replace authored records or run the assessed exercise."""
import sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import shutil
from pypdf import PdfReader
from pdf_layout import pdf

def main():
    for name,target,title in [('decision-memo','Decision-Memo','Reviewed committee decision'),('research-evolution','Research-Evolution','Research evolution'),('validation-and-ai-use','Validation-and-AI-Use','Validation and AI use')]:
        source=HERE/f'docs/{name}.md'
        dest=source.with_suffix('.pdf')
        pdf(source.read_text(encoding='utf-8-sig'),dest,title)
        pages=len(PdfReader(dest).pages)
        if name=='decision-memo' and pages>2:raise ValueError('Memo exceeds two pages')
        shutil.copyfile(dest,HERE/f'submission/{target}.pdf')
        print(f'{dest.name}: {pages} pages; submission copy identical')
if __name__=='__main__':main()
