"""Extract human-readable reference text without a browser dependency."""
from html.parser import HTMLParser
from pathlib import Path

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts=[]
        self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip+=1
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip=max(0,self.skip-1)
    def handle_data(self, data):
        if not self.skip and data.strip(): self.parts.append(data.strip())

if __name__=='__main__':
    for name in ('sec-api.html','streamlit.html'):
        parser=Text()
        parser.feed((Path(__file__).parent/'sources'/name).read_text(encoding='utf-8'))
        print(name+'\n'+'\n'.join(parser.parts))
