"""Exercise the actual two rendered voice versions in an isolated browser."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8173/');parser.add_argument('--report',default='bilingual.json');args=parser.parse_args()
versions=json.loads((ROOT/'site/media/versions.json').read_text())
def mapped(t,old,new):
    for a,b in zip(versions[old]['scenes'],versions[new]['scenes']):
        if t<a['end']:return b['start']+(t-a['start'])/(a['end']-a['start'])*(b['end']-b['start'])
    return versions[new]['duration']
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    response=page.goto(args.url,wait_until='networkidle',timeout=30000);assert response.status==200
    page.wait_for_function('!document.querySelector("#voice-language").disabled');video=page.locator('video')
    page.wait_for_function('document.querySelector("video").readyState>=1')
    scene=versions['zh']['scenes'][17];time=scene['start']+(scene['end']-scene['start'])*.4
    video.evaluate('(v,t)=>{v.pause();v.currentTime=t;v.playbackRate=1.5}',time)
    page.locator('#voice-language').select_option('en');page.wait_for_function('document.querySelector("video").dataset.language==="en" && document.querySelector("video").readyState>=2')
    assert abs(video.evaluate('(v)=>v.currentTime')-mapped(time,'zh','en'))<.3
    assert video.evaluate('(v)=>v.paused') and video.evaluate('(v)=>v.playbackRate')==1.5
    assert video.evaluate('(v)=>v.currentSrc').endswith('lesson.en.mp4')
    assert page.locator('#lesson-captions').get_attribute('srclang')=='en-US'
    assert page.locator('#download-video').get_attribute('href')=='media/lesson.en.mp4'
    assert page.locator('#download-captions').get_attribute('href')=='media/lesson.en.vtt'
    assert page.locator('#video-transcript').get_attribute('href')=='reading/#transcript-en'
    video.evaluate('(v)=>{v.muted=true;return v.play()}');page.wait_for_function('!document.querySelector("video").paused')
    old=video.evaluate('(v)=>v.currentTime');page.locator('#voice-language').select_option('zh');page.wait_for_function('document.querySelector("video").dataset.language==="zh" && !document.querySelector("video").paused')
    assert abs(video.evaluate('(v)=>v.currentTime')-mapped(old,'en','zh'))<2
    assert video.evaluate('(v)=>v.playbackRate')==1.5
    page.evaluate('''()=>{const s=document.querySelector('#voice-language');for(const lang of ['en','zh','en']){s.value=lang;s.dispatchEvent(new Event('change'));}}''')
    page.wait_for_function('document.querySelector("video").dataset.language==="en" && document.querySelector("video").readyState>=2')
    assert video.evaluate('(v)=>v.currentSrc').endswith('lesson.en.mp4')
    page.locator('#chapters button').nth(3).click();target=versions['en']['chapters'][3]['start'];page.wait_for_function('(t)=>document.querySelector("video").currentTime>=t-.1',arg=target)
    page.wait_for_function('document.querySelector("#lesson-captions").track.cues?.length>0');video.evaluate('(v)=>v.pause()')
    assert video.evaluate('(v)=>v.textTracks[0].language')=='en-US'
    # Keep the viewer's caption preference across a voice switch.
    video.evaluate('(v)=>v.textTracks[0].mode="disabled"')
    page.locator('#voice-language').select_option('zh');page.wait_for_function('document.querySelector("video").dataset.language==="zh" && document.querySelector("video").readyState>=2')
    assert video.evaluate('(v)=>v.textTracks[0].mode')=='disabled'
    video.evaluate('(v)=>v.textTracks[0].mode="showing"')
    # Reject a play request from an obsolete source after the latest source works.
    video.evaluate('(v)=>{v.muted=true;return v.play()}')
    video.evaluate('(v)=>{v.actualPlay=v.play.bind(v);v.play=()=>new Promise((resolve,reject)=>window.rejectOldPlay=reject)}')
    page.locator('#voice-language').select_option('en');page.wait_for_function('typeof window.rejectOldPlay==="function"')
    page.locator('#voice-language').select_option('zh');page.wait_for_function('document.querySelector("video").dataset.language==="zh" && document.querySelector("video").readyState>=2')
    video.evaluate('(v)=>v.actualPlay()');page.evaluate('window.rejectOldPlay(new DOMException("obsolete source", "AbortError"))')
    assert page.locator('#video-status').inner_text()==''
    video.evaluate('(v)=>{v.play=v.actualPlay;v.pause()}')
    for width in [390,1440]:
        page.set_viewport_size({'width':width,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert not errors,errors
    report={'status':'passed','url':args.url,'languages':['zh','en'],'checks':['two real MP4 files','paused voice switch preserves scene/fraction','playing switch resumes','playback speed preserved','rapid language changes finish on latest choice','matching captions and track language','caption off preference preserved','obsolete play rejection cannot overwrite current status','matching video/subtitle downloads and online transcript links','language-specific chapter seeking','mobile/desktop no horizontal overflow','no uncaught JS errors']}
    (ROOT/'docs/qa'/args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');browser.close();print('PASS: actual Chinese/English voice switching, playback, captions, downloads and chapter seeking')
