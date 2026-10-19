"""One-time adaptation; historical source files are read only."""
from pathlib import Path
import ast
HERE=Path(__file__).resolve().parent
old=(HERE/'build_documents.py').read_text(encoding='utf-8');tree=ast.parse(old)
functions=[ast.get_source_segment(old,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'pdf','write','money','mdtable'}]
imports='from pathlib import Path\nimport html,re\nfrom reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle\nfrom reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle\nfrom reportlab.lib import colors\n'
(HERE/'pdf_layout.py').write_text(imports+'\n\n'.join(functions),encoding='utf-8')
p=(HERE.parent/'lab10/amazon_proforma.py').read_text(encoding='utf-8')
p=p.replace("HERE / 'amazon_assumptions.csv'","HERE / 'data/legacy_assumptions.csv'")
needle="        r['distributions'] = a['distributions']"
replacement="        r['nonoperating_investment_purchase'] = a.get('nonoperating_investments', [0.0]*5)[i]\n        r['other_assets'] += r['nonoperating_investment_purchase']\n"+needle
assert p.count(needle)==1
p=p.replace(needle,replacement)
(HERE/'statements.py').write_text('# Edition B adaptation: known investment cash outflows added; historical Lab10 unchanged.\n'+p,encoding='utf-8')
print('Adapted statement engine and PDF helper prepared')
