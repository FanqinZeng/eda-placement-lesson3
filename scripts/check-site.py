"""Validate all local HTML resources and authored lesson requirements."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
class Links(HTMLParser):
    def __init__(self):super().__init__();self.urls=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ('href','src','poster'):
            if a.get(k):self.urls.append(a[k])
pages={}
for file in SITE.rglob('*.html'):
    p=Links();p.feed(file.read_text());pages[file.resolve()]=p
errors=[];count=0
for file,p in pages.items():
    for u in p.urls:
        count+=1;x=urlsplit(u)
        if x.scheme or x.netloc:continue
        target=(file.parent/unquote(x.path)).resolve() if x.path else file
        if target.is_dir():target=target/'index.html'
        if not target.is_file():errors.append(f'{file.name}: Missing '+u)
        if x.fragment and target in pages and x.fragment not in pages[target].ids:errors.append(f'{file.name}: Missing anchor '+u)
assert not errors,'\n'.join(errors)
for id in ['film','learn','lab','practice','resources','sources']:assert id in pages[(SITE/'index.html').resolve()].ids
for id in ['exercise','reference','data','notes','transcript-zh','transcript-en','reproduce']:assert id in pages[(SITE/'reading/index.html').resolve()].ids
print(f'PASS: {count} resource/anchor references across {len(pages)} HTML pages')
