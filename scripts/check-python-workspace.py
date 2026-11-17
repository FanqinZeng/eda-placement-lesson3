"""Real CPython-in-browser checks. Start scripts/serve.py --port 8173 first."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('LESSON_QA_URL', 'http://127.0.0.1:8173').rstrip('/')
OUT = ROOT / '.qa'
OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge', headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 1000})
    page = context.new_page()
    errors, requests = [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('request', lambda r: requests.append(r.url))
    page.goto(BASE + '/python/?lang=en')
    expect(page.locator('#run')).to_be_enabled(timeout=60000)
    assert 'CPython' in page.locator('#status').inner_text()
    code = page.locator('#code').input_value()
    def run(source, output=None, error=None):
        page.locator('#code').fill(source)
        page.locator('#run').click()
        expect(page.locator('#run')).to_be_enabled(timeout=60000)
        if output is not None:
            expect(page.locator('#output')).to_have_text(output)
        if error is not None:
            expect(page.locator('#errors')).to_contain_text(error)
    run(code, 'BBox = 4\nClique = 16\nStar = 8\n')
    run(code.replace('[(2, 2), (4, 2), (2, 4), (4, 4)]', '[(0, 0), (6, 0), (1, 2), (2, 5)]'), 'BBox = 11\nClique = 36\nStar = 16\n')
    run('import sys\nprint("actual CPython", sys.implementation.name)\nprint(sum(i*i for i in range(6)))', 'actual CPython cpython\n55\n')
    run('print("<img src=x onerror=alert(1)>")', '<img src=x onerror=alert(1)>\n')
    assert page.locator('#output img').count() == 0
    run('print("no newline", end="")', 'no newline')
    run('print("x" * 100000)', error='Output limit reached')
    assert len(page.locator('#output').inner_text()) <= 40000
    run('if :', error='SyntaxError')
    run('print("before failure")\n1 / 0', output='before failure\n', error='ZeroDivisionError')
    # Keyboard command and automatic debounced execution.
    page.locator('#code').fill('print("keyboard")')
    page.locator('#code').press('Control+Enter')
    expect(page.locator('#output')).to_have_text('keyboard\n')
    page.locator('#live').check()
    page.locator('#code').fill('print("live update", 7 * 9)')
    expect(page.locator('#output')).to_have_text('live update 63\n', timeout=10000)
    page.locator('#live').uncheck()
    # Runaway Python is killable; UI responds before the timeout.
    page.locator('#code').fill('while True:\n    pass')
    page.locator('#run').click()
    page.locator('#language').select_option('zh')
    expect(page.locator('h1')).to_have_text('实时 Python 实验室')
    page.locator('#stop').click()
    expect(page.locator('#run')).to_be_enabled(timeout=60000)
    assert page.locator('#code').input_value() == 'while True:\n    pass'
    expect(page.locator('#errors')).to_contain_text('已停止运行')
    run('print("recovered")', 'recovered\n')
    page.locator('#language').select_option('en')
    run('print("before loop")\nwhile True:\n    pass', 'before loop\n', 'exceeded 5 seconds')
    run('print("after timeout")', 'after timeout\n')
    page.locator('#example').select_option('exercise')
    page.locator('#run').click()
    expect(page.locator('#errors')).to_contain_text('NotImplementedError')
    page.locator('#example').select_option('reference')
    page.locator('#code').fill('print("unsaved example edit")')
    page.locator('#reset').click()
    assert page.locator('#code').input_value() == code
    # Persistence and language query override.
    page.locator('#code').fill('print("persisted")')
    page.reload()
    expect(page.locator('#run')).to_be_enabled(timeout=60000)
    assert page.locator('#code').input_value() == 'print("persisted")'
    page.goto(BASE + '/python/?lang=zh')
    expect(page.locator('h1')).to_have_text('实时 Python 实验室')
    expect(page.locator('#run')).to_be_enabled(timeout=60000)
    page.locator('#reset').click()
    page.locator('#run').click()
    expect(page.locator('#output')).to_have_text('BBox = 4\nClique = 16\nStar = 8\n')
    page.screenshot(path=str(OUT / 'python-desktop.png'), full_page=True)
    for width in [390, 768, 1440]:
        page.set_viewport_size({'width': width, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'overflow {width}'
        if width == 390:
            page.wait_for_timeout(250)  # Let the compositor repaint after resizing.
            page.screenshot(path=str(OUT / 'python-mobile.png'))
            page.locator('#output').scroll_into_view_if_needed()
            page.wait_for_timeout(250)
            page.screenshot(path=str(OUT / 'python-mobile-results.png'))
            page.evaluate('window.scrollTo(0, 0)')
    # No CDN/package downloads: every request stays at this origin.
    assert all(url.startswith(BASE + '/') for url in requests), requests
    assert not errors, errors
    blocked = browser.new_context()
    blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('denied')}})")
    q = blocked.new_page()
    q.goto(BASE + '/python/?lang=en')
    expect(q.locator('#run')).to_be_enabled(timeout=60000)
    q.locator('#run').click()
    expect(q.locator('#output')).to_have_text('BBox = 4\nClique = 16\nStar = 8\n')
    blocked.close()
    report = {'status': 'passed', 'engine': 'actual CPython via vendored Pyodide in Worker', 'checks': ['golden 4/16/8', 'edited pins 11/36/16', 'Python import and computation', 'text-only output', 'partial-line output', '40k-character output cap', 'syntax/runtime errors', 'keyboard run', 'live debounce', 'infinite loop stop', '5-second timeout', 'rerun after restart', 'exercise/reset', 'code persistence', 'bilingual UI', '390/768/1440 no overflow', 'all runtime requests same origin', 'storage denied fallback', 'no page errors']}
    for report_path in [OUT / 'python-workspace.json', ROOT / 'docs/qa/python-workspace.json']:
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    browser.close()
    print('PASS: live Python workspace browser checks')
