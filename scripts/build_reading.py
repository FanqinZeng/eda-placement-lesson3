"""Build static, readable HTML from the lesson's authored source files. No dependencies."""
from pathlib import Path
import argparse,hashlib,html,json,re
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
SOURCES=['exercise.py','reference.py','examples.json','lesson.md','transcript.md','transcript.en.md','reproduction.md','lesson.en.md','reproduction.en.md']
def inline(text):
    pattern=re.compile(r'`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*');out=[];end=0
    for m in pattern.finditer(text):
        out.append(html.escape(text[end:m.start()]));end=m.end()
        if m[1] is not None:out.append('<code>'+html.escape(m[1])+'</code>')
        elif m[2] is not None:
            url=m[3];label=html.escape(m[2]);out.append('<a href="'+html.escape(url,quote=True)+'">'+label+'</a>' if urlsplit(url).scheme in ('','http','https') else label)
        else:out.append('<strong>'+html.escape(m[4])+'</strong>')
    out.append(html.escape(text[end:]));return ''.join(out)
def render_markdown(source,heading_level=2):
    """Render the controlled heading/paragraph/list/table/code subset used by this course."""
    lines=source.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('```'):
            body=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):body.append(lines[i]);i+=1
            out.append('<pre><code>'+html.escape('\n'.join(body))+'</code></pre>');i+=1;continue
        match=re.match(r'^(#{1,6})\s+(.+)',line)
        if match:
            level=min(6,heading_level+len(match[1])-1);out.append(f'<h{level}>'+inline(match[2])+f'</h{level}>');i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',x) for x in cells):rows.append(cells)
                i+=1
            if rows:
                out.append('<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+inline(x)+'</th>' for x in rows[0])+'</tr></thead><tbody>')
                out.extend('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in row)+'</tr>' for row in rows[1:]);out.append('</tbody></table></div>')
            continue
        ordered=bool(re.match(r'^\d+\. ',line));unordered=line.startswith('- ')
        if ordered or unordered:
            tag='ol' if ordered else 'ul';pattern=r'^\d+\. ' if ordered else r'^- ';items=[]
            while i<len(lines) and re.match(pattern,lines[i]):items.append(re.sub(pattern,'',lines[i]));i+=1
            out.append('<'+tag+'>'+''.join('<li>'+inline(x)+'</li>' for x in items)+'</'+tag+'>');continue
        body=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|```|\||- |\d+\. )',lines[i]):body.append(lines[i]);i+=1
        out.append('<p>'+inline(' '.join(body))+'</p>')
    return '\n'.join(out)
def source(name):return (SITE/'downloads'/name).read_text()
def code_block(name,id,label):
    return '<div class="code-heading"><span>'+label+'</span><button type="button" class="code-copy" data-copy="'+id+'">复制代码</button></div><pre><code id="'+id+'">'+html.escape(source(name))+'</code></pre><p class="optional"><a href="../downloads/'+name+'" download>可选：下载原文件 ↓</a></p>'
def build_page():
    fingerprint=hashlib.sha256(''.join(name+'\n'+source(name) for name in SOURCES).encode()).hexdigest()
    sections=[]
    def section(id,title,body,lang=None):
        sections.append('<section id="'+id+'" class="reading-section"'+(' lang="'+lang+'"' if lang else '')+'><p class="eyebrow">'+str(len(sections)+1).zfill(2)+' / READ ONLINE</p><h2>'+title+'</h2>'+body+'</section>')
    section('exercise','Python 练习：自己实现三把尺子','<p><a href="../python/">在浏览器中编辑并运行 Python →</a></p><p>直接阅读并复制下面的模板。补齐三个函数，标准四引脚的结果应为 <strong>4 / 16 / 8</strong>。<code>NotImplementedError</code> 是留给你完成的位置，不是网页出错。</p>'+code_block('exercise.py','exercise-code','PYTHON / exercise.py'))
    section('reference','参考实现：逐项核对结果','<p>这是独立于网页 JavaScript 引擎的 Python 实现。先完成练习，再对照坐标扫描、无序对求和与中心选择。</p>'+code_block('reference.py','reference-code','PYTHON / reference.py'))
    data=json.loads(source('examples.json'));labels={'golden':'标准正方形 · Golden','starter':'分散正方形 · Starter','asymmetric':'非对称 · Asymmetric','interior':'内部点 · Interior'}
    tables='<p>与实验台共享以下四组坐标。原点在左下、y 向上；一张表就是一个 net 的引脚列表。</p><div class="datasets">'
    for key,pins in data.items():tables+='<article><h3>'+labels[key]+'</h3><table><thead><tr><th>Pin</th><th>x</th><th>y</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+html.escape(p['id'])+'</th><td>'+str(p['x'])+'</td><td>'+str(p['y'])+'</td></tr>' for p in pins)+'</tbody></table></article>'
    tables+='</div><details><summary>查看与复制原始 JSON</summary>'+code_block('examples.json','data-code','JSON / examples.json')+'</details>'
    section('data','标准坐标：先看表，再看 JSON',tables)
    section('notes','完整中文讲义','<div data-site-language="zh">'+render_markdown(source('lesson.md'),3)+'</div><div data-site-language="en" lang="en" hidden>'+render_markdown(source('lesson.en.md'),3)+'</div>'+'<p class="optional" data-site-language="zh"><a href="../downloads/lesson.md" download>可选：下载 Markdown 讲义 ↓</a></p><p class="optional" data-site-language="en" lang="en" hidden><a href="../downloads/lesson.en.md" download>Optional: download English Markdown notes ↓</a></p>')
    section('transcript-zh','视频文字稿 · 中文','<p><a href="../#film">返回双语影片 →</a></p><div data-original-language="zh">'+render_markdown(source('transcript.md'),3)+'</div>'+'<p class="optional"><a href="../downloads/transcript.md" download>可选：下载中文文字稿 ↓</a></p>','zh-CN')
    section('transcript-en','Video transcript · English','<p><a href="../#film">返回影片，在配音菜单选择 English →</a></p>'+render_markdown(source('transcript.en.md'),3)+'<p class="optional"><a href="../downloads/transcript.en.md" download>Optional: download the English transcript ↓</a></p>','en')
    section('reproduce','源码与复现：看懂之后再动手','<div data-site-language="zh">'+render_markdown(source('reproduction.md'),3)+'</div><div data-site-language="en" lang="en" hidden>'+render_markdown(source('reproduction.en.md'),3)+'</div>')
    nav=[('exercise','Python 练习'),('reference','参考实现'),('data','标准坐标'),('notes','中文讲义'),('transcript-zh','中文文字稿'),('transcript-en','English transcript'),('reproduce','源码与复现')]
    return '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f4f1e9"><title>学习资料在线阅读 · Placement Lesson 03</title><meta name="description" content="直接在线阅读 Python 练习、参考实现、坐标表、中文讲义、中英文视频文字稿和复现说明。"><link rel="stylesheet" href="../assets/style.css"><link rel="stylesheet" href="../assets/reading.css"><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"></head><body><a class="skip" href="#main">跳到正文</a><header><div class="wrap top"><a class="brand" href="../"><span class="brand-mark">⌗</span> Placement <em>03</em></a><nav aria-label="阅读导航"><a href="../#resources">返回课程</a><a href="../#lab">互动实验</a><a href="#notes">读讲义</a><a href="#transcript-zh">读文字稿</a></nav></div></header><main id="main"><div class="wrap reading-hero"><p class="eyebrow">PLACEMENT / 03 / THE READING ROOM</p><h1>把资料摊开，<br>慢慢读。</h1><p class="lead">公式、代码、数据和讲解，都在这一页。<br>先在线阅读，需要时再复制或下载。</p><a class="section-link" href="../#lab">读完一个例子，回实验台试试 →</a></div><div class="wrap reading-layout"><aside class="reading-index"><p class="eyebrow">本页目录</p><nav aria-label="学习资料目录">'''+''.join('<a href="#'+id+'">'+label+'</a>' for id,label in nav)+'''</nav><p class="note">代码和正文已完整载入，关闭 JavaScript 也能阅读。</p></aside><div class="reading-content">'''+''.join(sections)+'''</div></div></main><footer><div class="wrap">PLACEMENT / 03 · 学习资料<span>代码 MIT / 新教材 CC BY 4.0</span><a href="../#resources">返回课程 ↑</a></div></footer><p id="copy-status" class="copy-status" role="status" aria-live="polite"></p><script type="module" src="../assets/reading.mjs"></script></body></html>
<!-- source-sha256: '''+fingerprint+''' -->
'''
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();dest=SITE/'reading/index.html';output=build_page()
    if args.check:assert dest.is_file() and dest.read_text()==output,'Reading page is out of date: run python3 scripts/build_reading.py';print('PASS: online reading content matches source files')
    else:dest.parent.mkdir(exist_ok=True);dest.write_text(output);print('Built site/reading/index.html from authored bilingual source files')
