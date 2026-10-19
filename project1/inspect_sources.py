from html.parser import HTMLParser
from pathlib import Path
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,d):
        if d.strip(): self.parts.append(d.strip())
for p in (Path(__file__).parent/'sources').glob('*.html'):
    t=Text(); t.feed(p.read_text(encoding='utf-8',errors='replace'))
    p.with_suffix('.txt').write_text('\n'.join(t.parts),encoding='utf-8')
print('Source text extracted; see raw HTML for table column alignment.')
