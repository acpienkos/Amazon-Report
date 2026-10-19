from pathlib import Path
import pymupdf,json
HERE=Path(__file__).resolve().parent
(HERE/'tmp/pdfs').mkdir(parents=True,exist_ok=True)
result=[]
for name in ['decision-memo','research-evolution','validation-and-ai-use']:
    doc=pymupdf.open(HERE/f'docs/{name}.pdf')
    for i,page in enumerate(doc):
        target=HERE/f'tmp/pdfs/{name}-{i+1}.png'
        page.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(target)
        result.append(dict(file=name,page=i+1,image=str(target),text_length=len(page.get_text())))
(HERE/'evidence/pdf_render_inventory.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('Rendered',len(result),'pages for visual inspection')
