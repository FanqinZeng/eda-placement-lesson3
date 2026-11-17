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
p=Links();p.feed((SITE/'index.html').read_text());errors=[]
for u in p.urls:
    x=urlsplit(u)
    if x.scheme or x.netloc:continue
    if x.path and not (SITE/unquote(x.path)).is_file():errors.append('Missing '+u)
    if not x.path and x.fragment and x.fragment not in p.ids:errors.append('Missing anchor '+u)
assert not errors,'\n'.join(errors)
for id in ['film','learn','lab','practice','resources','sources']:assert id in p.ids
print(f'PASS: {len(p.urls)} resource/anchor references and all course sections')
