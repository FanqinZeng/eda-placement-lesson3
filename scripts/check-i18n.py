"""Browser regression checks for UI language, translated interactions, and reading room."""
import argparse,re
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://localhost:8173/');args=parser.parse_args()
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless=True)
    page=browser.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    def english_prose():
        return page.evaluate('''() => {const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),out=[];while(w.nextNode()){const n=w.currentNode;if(/[\\u4e00-\\u9fff]/.test(n.nodeValue)&&!n.parentElement.closest('pre,code,script,style,[data-original-language]')&&n.parentElement.checkVisibility())out.push(n.nodeValue)}return out}''')
    page.goto(args.base+'?lang=en');page.wait_for_timeout(200)
    assert page.locator('html').get_attribute('lang')=='en'
    assert not english_prose(),english_prose()
    # An English UI must preserve the mathematical i<j in its concept question.
    assert 'i<j' in page.locator('[data-quiz="1"] h4').inner_text()
    page.locator('#preset').select_option('asymmetric');page.locator('#hub').select_option('B')
    assert 'Star-from-B 22' in page.locator('#lab-summary').inner_text()
    page.locator('[data-language-picker]').select_option('zh');page.wait_for_timeout(100)
    assert '当前单个 ABCD' in page.locator('#lab-summary').inner_text()
    assert page.locator('#hub').input_value()=='B'
    page.locator('[data-language-picker]').select_option('en');page.wait_for_timeout(100)
    page.locator('#coordinates input').first.fill('9');page.locator('#coordinates input').first.dispatch_event('change');page.wait_for_timeout(100)
    assert 'integer from 0 to 8' in page.locator('#input-status').inner_text()
    page.locator('[data-task-load="0"]').click()
    page.locator('#answer-0').fill('4');page.locator('[data-task="0"] button[type="submit"]').click();page.wait_for_timeout(100)
    assert 'HPWL = 4' in page.locator('[data-task="0"] .feedback').inner_text()
    assert 'completed' in page.locator('#progress').inner_text()
    page.locator('#step-next').click();page.wait_for_timeout(100)
    assert 'Pair 1/6' in page.locator('#step-copy').inner_text()
    assert not english_prose(),english_prose()
    page.goto(args.base+'reading/?lang=en');page.wait_for_timeout(200)
    assert 'Three counterexamples' in page.locator('#notes').inner_text()
    assert 'Run the whole website offline' in page.locator('#reproduce').inner_text()
    assert not english_prose(),english_prose()
    page.locator('[data-language-picker]').select_option('zh');page.wait_for_timeout(100)
    assert '三个反例' in page.locator('#notes').inner_text()
    # The language persists across page loads and remains usable without storage.
    page.goto(args.base);page.wait_for_timeout(100)
    assert page.locator('html').get_attribute('lang')=='zh-CN'
    blocked=browser.new_context();blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})")
    other=blocked.new_page();other.goto(args.base+'?lang=en');other.wait_for_timeout(100)
    assert other.locator('html').get_attribute('lang')=='en'
    other.locator('[data-language-picker]').select_option('zh')
    assert other.locator('html').get_attribute('lang')=='zh-CN'
    # Narrow-screen layout must not force horizontal page scrolling.
    page.set_viewport_size({'width':390,'height':844});page.goto(args.base+'?lang=en');page.wait_for_timeout(100)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Mobile page overflows'
    assert not errors,errors
    browser.close()
print('PASS: bilingual static UI, interactions, preserved state, reading content, storage fallback, mobile layout')
