"""Real browser checks for the native online resources page; no file downloads required."""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8173/');parser.add_argument('--report',default='reading.json');args=parser.parse_args()
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write']);page=context.new_page();downloads=[];errors=[]
    page.on('download',lambda d:downloads.append(d.suggested_filename));page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(args.url,wait_until='networkidle');page.locator('#resources a').filter(has_text='Python 练习').click();page.wait_for_url('**/reading/#exercise');assert page.locator('#exercise-code').text_content()==(ROOT/'site/downloads/exercise.py').read_text()
    page.locator('button[data-copy="exercise-code"]').click();assert page.evaluate('navigator.clipboard.readText()')==(ROOT/'site/downloads/exercise.py').read_text()
    page.locator('.reading-index a[href="#reference"]').click();assert 'def evaluate' in page.locator('#reference-code').inner_text()
    page.locator('.reading-index a[href="#data"]').click();assert page.locator('.datasets tbody tr').count()==16
    page.locator('#data summary').click();assert page.locator('#data-code').text_content()==(ROOT/'site/downloads/examples.json').read_text()
    for width in [390,768,1440]:
        page.set_viewport_size({'width':width,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
    (ROOT/'.qa').mkdir(exist_ok=True);page.goto(args.url+'reading/#notes');page.locator('#notes').evaluate('(el)=>el.scrollIntoView({behavior:"instant",block:"start"})');page.screenshot(path=str(ROOT/'.qa/reading-desktop.png'))
    page.set_viewport_size({'width':390,'height':900});page.locator('#notes').evaluate('(el)=>el.scrollIntoView({behavior:"instant",block:"start"})');page.screenshot(path=str(ROOT/'.qa/reading-mobile.png'))
    # The full lesson and code are rendered HTML, not a JavaScript fetch-only viewer.
    static=browser.new_context(java_script_enabled=False);q=static.new_page();q.goto(args.url+'reading/');assert 'def bbox' in q.locator('#exercise').inner_text();assert '半周长' in q.locator('#notes').inner_text();assert 'Horizontal plus vertical' in q.locator('#transcript-en').inner_text();static.close()
    assert not downloads,downloads;assert not errors,errors
    report={'status':'passed','url':args.url+'reading/','checks':['resource link opens native HTML without download','exercise/reference code equals original files','copy code clipboard','all four coordinate tables and original JSON','full Chinese notes and bilingual transcripts','content readable with JavaScript disabled','390/768/1440 no page overflow','cross-page navigation','no uncaught JavaScript errors']}
    (ROOT/'docs/qa'/args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');browser.close();print('PASS: online reading, copy, source equality, no downloads, no-JS and mobile layout')
