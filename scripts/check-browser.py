"""Real desktop/mobile interaction checks, using an isolated installed Edge instance."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.qa';OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:8173',wait_until='networkidle');page.screenshot(path=str(OUT/'desktop.png'),full_page=True)
    assert page.locator('.readout').all_text_contents()==['4','16','8']
    page.locator('#preset').select_option('asymmetric');page.locator('#hub').select_option('B');assert page.locator('.readout').all_text_contents()==['11','36','22']
    x=page.locator('input[data-id="A"][data-axis="x"]');x.fill('');x.dispatch_event('change');assert x.get_attribute('aria-invalid')=='true';assert page.locator('.readout').all_text_contents()==['11','36','22']
    page.locator('#reset-lab').click();page.locator('#preset').select_option('golden')
    pin=page.locator('.board').first.locator('[data-pin="A"]');pin.focus();page.keyboard.press('ArrowRight');assert page.locator('input[data-id="A"][data-axis="x"]').input_value()=='3'
    page.locator('#reset-lab').click();pin=page.locator('.board').first.locator('[data-pin="A"] circle');box=pin.bounding_box();svg=page.locator('.board').first.locator('svg').bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();page.mouse.move(box['x']+box['width']/2+svg['width']*30/330,box['y']+box['height']/2,steps=10);page.mouse.up();assert page.locator('input[data-id="A"][data-axis="x"]').input_value()=='3'
    page.locator('#step-next').click();assert '第 1/6' in page.locator('#step-copy').inner_text()
    page.locator('#preset').select_option('golden');page.locator('#answer-0').fill('4');page.locator('[data-task="0"] button[type="submit"]').click();assert '1 / 12' in page.locator('#progress').inner_text()
    page.reload(wait_until='networkidle');assert '1 / 12' in page.locator('#progress').inner_text();page.locator('#clear-progress').click();assert '0 / 12' in page.locator('#progress').inner_text()
    page.locator('#motion').click();assert page.locator('body').evaluate('(el)=>el.classList.contains("reduced")')
    for width in [390,768,1440]:
        page.set_viewport_size({'width':width,'height':900});page.goto('http://127.0.0.1:8173',wait_until='networkidle');assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),f'overflow {width}'
        if width==390:page.screenshot(path=str(OUT/'mobile.png'),full_page=True)
    blocked=browser.new_context();blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('disabled')}})");q=blocked.new_page();q.goto('http://127.0.0.1:8173',wait_until='networkidle');assert '不可用' in q.locator('#storage-status').inner_text();assert q.locator('.readout').all_text_contents()==['4','16','8'];blocked.close()
    assert not errors,errors
    (ROOT/'docs/qa/browser.json').write_text(json.dumps({'status':'passed','browser':'Microsoft Edge headless, isolated context','viewports':[390,768,1440],'checks':['standard metrics','asymmetric hub','invalid coordinate preserves state','keyboard movement','pointer movement','trace stepping','explicit task completion','progress persistence/reset','reduced motion','no horizontal overflow','storage denied fallback','no uncaught JS errors']},ensure_ascii=False,indent=2)+'\n')
    browser.close();print('PASS: real browser interaction and three viewport checks')
