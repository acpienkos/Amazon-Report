from html.parser import HTMLParser
from pathlib import Path
import re, json
class Tables(HTMLParser):
    def __init__(self): super().__init__(); self.depth=0; self.row=None; self.cell=None; self.rows=[]
    def handle_starttag(self,t,a):
        if t=='tr': self.row=[]
        if t in ('td','th'): self.cell=[]
    def handle_data(self,d):
        if self.cell is not None: self.cell.append(d)
    def handle_endtag(self,t):
        if t in ('td','th') and self.cell is not None:
            if self.row is not None:self.row.append(re.sub(r'\s+',' ',' '.join(self.cell)).strip())
            self.cell=None
        if t=='tr' and self.row is not None:
            self.rows.append(self.row);self.row=None
def rows(key):
    p=Tables();p.feed((Path(__file__).parent/'sources'/(key+'.html')).read_text(encoding='utf-8',errors='replace'));return p.rows
if __name__=='__main__':
    import sys
    for key in sys.argv[1:]:
        print(key)
        for r in rows(key):
            s=' | '.join(r)
            if re.search('cash and cash|short-term investment|long-term debt|short-term borrow|depreciation|noncontrolling|outstanding|weighted.average|operating income|total revenue|net sales|finance lease|financing obligation',s,re.I):
                print(s[:450])
