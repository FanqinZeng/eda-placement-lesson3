"""Regress the reported English-page/Chinese-video mismatch in a real browser."""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8173/');parser.add_argument('--report',default='voice-ui.json');args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1];BASE=args.url.rstrip('/')+'/'
versions=json.loads((ROOT/'site/media/versions.json').read_text())
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless=True)
    page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    def settled(lang):
        page.wait_for_function('(lang)=>document.querySelector("video").dataset.language===lang && document.querySelector("video").readyState>=2',arg=lang)
        assert page.locator('#voice-language').input_value()==lang
        assert page.locator('video').evaluate('(v)=>v.currentSrc').endswith(f'lesson.{lang}.mp4')
        assert page.locator('#download-video').get_attribute('href')==f'media/lesson.{lang}.mp4'
    page.goto(BASE+'?lang=en',wait_until='networkidle')
    page.wait_for_function('!document.querySelector("#voice-language").disabled')
    assert page.locator('#voice-language').input_value()=='en','English UI still defaults to Chinese narration/video'
    settled('en')
    video=page.locator('video');old=versions['en']['scenes'][12];t=(old['start']+old['end'])/2
    video.evaluate('(v,t)=>{v.pause();v.currentTime=t;v.playbackRate=1.5}',t)
    page.locator('[data-language-picker]').select_option('zh');settled('zh')
    target=versions['zh']['scenes'][12];assert abs(video.evaluate('(v)=>v.currentTime')-(target['start']+target['end'])/2)<.3
    assert video.evaluate('(v)=>v.paused && v.playbackRate===1.5')
    assert page.locator('#caption-mode').input_value()=='bilingual'
    # Voice remains independently selectable, without changing the interface.
    page.locator('#voice-language').select_option('en');settled('en')
    assert page.locator('html').get_attribute('lang')=='zh-CN'
    page.locator('[data-language-picker]').select_option('en');settled('en')
    page.locator('[data-language-picker]').select_option('zh');settled('zh')
    page.locator('[data-language-picker]').select_option('en');settled('en')
    page.reload(wait_until='networkidle');settled('en')
    # A stored English preference on an unqualified URL also chooses English video.
    page.goto(BASE,wait_until='networkidle');settled('en')
    page.goto(BASE+'?lang=zh',wait_until='networkidle');settled('zh')
    assert not errors,errors
    browser.close()
    report={'status':'passed','url':args.url,'checks':['English link defaults to English pictures and narration','Chinese link defaults to Chinese video','interface changes synchronize video and voice','same scene, fraction, paused state and speed preserved','bilingual captions stay selected','voice can still be chosen independently','reload and saved English preference retain matching video','no uncaught browser errors']}
    (ROOT/'docs/qa'/args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: interface language selects matching video and voice, retaining independent voice selection and playback state')
