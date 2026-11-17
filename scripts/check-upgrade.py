from pathlib import Path
from playwright.sync_api import sync_playwright
import json,argparse
parser=argparse.ArgumentParser();parser.add_argument("--url",default="http://127.0.0.1:8173/");args=parser.parse_args();BASE=args.url.rstrip("/")+"/"
R=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless=True)
 page=b.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE+'?lang=en',wait_until='networkidle');page.wait_for_function('document.documentElement.lang==="en"');print('title',page.title(),flush=True)
 page.wait_for_function('document.querySelector("#lesson-captions").track.cues?.length>0');v=page.locator('video');v.evaluate('(v)=>{v.currentTime=2;v.muted=true}');page.wait_for_timeout(300)
 cues=page.locator('#lesson-captions').evaluate('(t)=>[...t.track.cues].map(c=>c.text)');assert all(any('\u4e00'<=c<='\u9fff' for c in x) and any(c.isascii() and c.isalpha() for c in x) for x in cues)
 page.locator('#caption-mode').select_option('en');page.wait_for_function('document.querySelector("#lesson-captions").getAttribute("src").includes(".en.vtt")');page.locator('#caption-mode').select_option('bilingual')
 page.locator('#film').scroll_into_view_if_needed();page.screenshot(path=str(R/'.qa/bilingual-captions-ui.png'))
 page.goto(BASE+'python/?lang=en',wait_until='networkidle');page.wait_for_function('!document.querySelector("#run").disabled',timeout=30000);page.locator('#run').click();page.wait_for_function('document.querySelector("#output").textContent.includes("16")',timeout=15000)
 assert not errors,errors;b.close();print('PASS: English UI, real Python, bilingual subtitle cues and subtitle choice')
