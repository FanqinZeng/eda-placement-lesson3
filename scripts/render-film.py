"""Reproducible native 1080p/30fps film. Run after export-data.mjs and speech.py.
--stills writes representative frames; no argument encodes the full film.
"""
from pathlib import Path
from functools import lru_cache
import argparse,json,math,subprocess,sys,wave,io,time,importlib.util
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];W,H,FPS=1920,1080,30
DEST=ROOT/'site/media';CACHE=ROOT/'.cache';DEST.mkdir(exist_ok=True);CACHE.mkdir(exist_ok=True)
STORY=json.loads((ROOT/'video/story.json').read_text());DATA=json.loads((ROOT/'video/data.json').read_text());FF=imageio_ffmpeg.get_ffmpeg_exe()
spec=importlib.util.spec_from_file_location('ref',ROOT/'site/downloads/reference.py');ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
BG='#061219';PANEL='#0b2029';IVORY='#eeeadd';MUTED='#8fa3a3';GOLD='#ddbd78';TEAL='#76cbb5';BLUE='#86a9e0';FAINT='#2a4048'
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def mix(a,b,t):return a+(b-a)*t
@lru_cache(None)
def font(size,mono=False):return ImageFont.truetype(str(ROOT/'video/fonts'/('JetBrainsMono-Regular.ttf' if mono else 'NotoSansSC-Regular.otf')),size)
@lru_cache(4096)
def sprite(content,size,color,mono=False):
    f=font(size,mono);box=f.getbbox(content);im=Image.new('RGBA',(math.ceil(f.getlength(content))+8,box[3]-box[1]+8));ImageDraw.Draw(im).text((4,4-box[1]),content,font=f,fill=color);return im
def text(im,s,x,y,size=40,color=IVORY,mono=False):
    sp=sprite(str(s),size,color,mono);im.paste(sp,(round(x),round(y)),sp)
def wrapped(s,size,width):
    lines=[];line=''
    for c in s:
        if font(size).getlength(line+c)>width:lines.append(line);line=''
        line+=c
    if line:lines.append(line)
    if len(lines)>1 and lines[-1] in '。，？！；：':
        last=lines.pop();lines[-1]+=last
    return lines
def n(v):return str(round(v,1)).removesuffix('.0')
def timeline():
    cursor=0;scenes=[];wavepath=CACHE/'narration.wav'
    with wave.open(str(wavepath),'wb') as out:
        out.setnchannels(1);out.setsampwidth(2);out.setframerate(24000)
        for i,b in enumerate(STORY):
            pcm=subprocess.check_output([FF,'-v','error','-i',str(ROOT/'video/audio'/f'{i:02}.mp3'),'-f','s16le','-ar','24000','-ac','1','pipe:1'])
            samples=len(pcm)//2;duration=math.ceil((samples/24000+1.1)*FPS)/FPS;silence=round(duration*24000)-samples
            out.writeframes(pcm+b'\0\0'*silence);scenes.append({'index':i,'chapter':b[0],'kind':b[1],'title':b[2],'caption':b[3],'speech':b[4],'start':cursor,'end':cursor+duration,'duration':duration});cursor+=duration
    return scenes,cursor
SCENES,DURATION=timeline()
@lru_cache(1)
def background():
    y,x=np.mgrid[:H,:W];v=np.maximum(0,1-((x-W*.4)/(W*1.1))**2-((y-H*.35)/H)**2)[...,None];a=np.array([6,18,25]);b=np.array([11,31,41]);return Image.fromarray(np.uint8(a+(b-a)*v))
def positions(key):return [dict(p) for p in DATA[key]['pins']]
def morph(a,b,t):return [{**p,'x':mix(p['x'],q['x'],t),'y':mix(p['y'],q['y'],t)} for p,q in zip(a,b)]
def edge(im,a,b,progress,color,scale=1):
    # Manhattan path with a length-based pen, so both legs draw continuously.
    x1,y1=a;x2,y2=b;dx=abs(x2-x1);dy=abs(y2-y1);length=(dx+dy)*max(0,min(1,progress));draw=ImageDraw.Draw(im)
    mid=(x1+math.copysign(min(dx,length),x2-x1),y1);draw.line((a,mid),fill=color,width=max(2,round(3*scale)))
    if length>dx:draw.line((mid,(x2,y1+math.copysign(min(dy,length-dx),y2-y1))),fill=color,width=max(2,round(3*scale)))
def graph(im,pins,kind='bbox',hub='A',progress=1,origin=(160,285),scale=1):
    ox,oy=origin;unit=61*scale;xy=lambda p:(ox+p['x']*unit,oy+(8-p['y'])*unit);draw=ImageDraw.Draw(im)
    for i in range(9):
        draw.line((ox,oy+i*unit,ox+8*unit,oy+i*unit),fill=FAINT,width=1);draw.line((ox+i*unit,oy,ox+i*unit,oy+8*unit),fill=FAINT,width=1)
        if scale>.8:text(im,i,ox+i*unit-5,oy+8*unit+17,20,MUTED,True)
    if kind=='bbox':
        xs=[p['x'] for p in pins];ys=[p['y'] for p in pins];a=xy({'x':min(xs),'y':max(ys)});b=xy({'x':max(xs),'y':min(ys)});corners=[a,(b[0],a[1]),b,(a[0],b[1]),a]
        for i in range(4):
            t=max(0,min(1,progress*4-i));q=(mix(corners[i][0],corners[i+1][0],t),mix(corners[i][1],corners[i+1][1],t));draw.line((corners[i],q),fill=GOLD,width=round(4*scale))
    else:
        pairs=[(a,b) for i,a in enumerate(pins) for b in pins[i+1:]] if kind=='clique' else [(next(p for p in pins if p['id']==hub),p) for p in pins if p['id']!=hub]
        for i,(a,b) in enumerate(pairs):edge(im,xy(a),xy(b),max(0,min(1,progress*len(pairs)-i)),BLUE if kind=='clique' else TEAL,scale)
    for p in pins:
        x,y=xy(p);r=(15 if kind=='star' and p['id']==hub else 11)*scale;draw.ellipse((x-r,y-r,x+r,y+r),fill=PANEL,outline=TEAL if kind=='star' and p['id']==hub else IVORY,width=max(2,round(3*scale)));text(im,p['id'],x+15*scale,y-31*scale,round(30*scale),IVORY,True)
    return ref.evaluate(pins,hub)
def render_frame(t):
    scene=next((s for s in SCENES if s['start']<=t<s['end']),SCENES[-1]);local=t-scene['start'];phase=local/scene['duration'];kind=scene['kind'];p=positions('golden');mode='bbox';hub='A';progress=ease(local/3)
    if kind=='intro':p=morph(positions('starter'),p,ease(local/5)) if scene['index']==0 else p
    elif kind=='clique':mode='clique';progress=ease(local/max(3,scene['duration']*.75))
    elif kind=='star':mode='star';progress=ease(local/4)
    elif kind=='asymmetric':p=morph(p,positions('asymmetric'),ease(local/4))
    elif kind=='hubs':p=positions('asymmetric');mode='star';hub='ABCD'[min(3,int(phase*4))];progress=ease((phase*4%1)*4)
    elif kind=='inside':
        p=positions('interior');q=[dict(x) for x in p];q[3].update(x=2,y=2);p=morph(p,q,ease((phase-.1)/.65));mode='clique'
    elif kind=='collapse':p=morph(p,[{**x,'x':4,'y':4} for x in p],ease(local/5));mode='clique'
    elif kind=='starter':p=morph(positions('starter'),p,ease(local/6))
    elif kind=='close':mode='star'
    im=background().copy();d=ImageDraw.Draw(im)
    text(im,'PLACEMENT / LESSON 03',104,57,24,TEAL,True);text(im,f'{scene["index"]+1:02} / {len(SCENES)}',1655,57,24,MUTED,True)
    text(im,scene['title'],104,132,62);d.line((104,235,1816,235),fill=FAINT,width=1)
    if kind=='compare':
        for j,(m,label,c) in enumerate([('bbox','HPWL',GOLD),('clique','Clique',BLUE),('star','Star A',TEAL)]):
            x=155+j*580;vals=graph(im,p,m,'A',ease(local/5),origin=(x,345),scale=.72);v=vals[{'bbox':0,'clique':1,'star':2}[m]];text(im,label,x,280,31,c,True);text(im,n(v),x+140,760,56,c,True)
    else:
        vals=graph(im,p,mode,hub,progress);text(im,'SAME NET / UNIT WEIGHT',990,285,24,MUTED,True)
        if kind=='distance':
            a=(160+2*61,285+6*61);b=(160+4*61,285+4*61);edge(im,a,b,ease(local/5),TEAL);text(im,'A → D',1000,375,42,TEAL);text(im,'2 + 2 = 4',1000,470,60,IVORY,True);text(im,'横向差 + 竖向差',1000,580,33,MUTED)
        else:
            for j,(label,value,c) in enumerate([('HPWL',vals[0],GOLD),('Clique',vals[1],BLUE),(f'Star {hub}',vals[2],TEAL)]):text(im,label,1000,370+j*115,32,c,True);text(im,n(value),1440,352+j*115,64,c,True)
            if kind=='hubs':text(im,'A 16 / B 22 / C 14 / D 20',970,755,27,MUTED,True)
            elif kind=='clique':text(im,'AB 2 / AC 2 / AD 4',990,745,27,MUTED,True);text(im,'BC 4 / BD 2 / CD 2',990,790,27,MUTED,True)
    d.line((104,879,1816,879),fill=FAINT,width=1)
    for i,line in enumerate(wrapped(scene['caption'],40,1660)):text(im,line,112,907+i*56,40,IVORY)
    # A continuous progress bar; page captions provide the full spoken text.
    d.rectangle((104,1036,1816,1040),fill=FAINT);d.rectangle((104,1036,104+1712*t/DURATION,1040),fill=TEAL)
    return im
def ts(s):
    ms=round(s*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{sec:02}.{ms:03}'
def outputs():
    captions=['WEBVTT',''];trans=['# 同一组引脚，三把尺子','',f'普通话合成旁白：zh-CN-XiaoxiaoNeural；总长 {DURATION:.2f} 秒。',''];chap=[];last=None
    for s in SCENES:
        if s['chapter']!=last:chap.append({'title':s['chapter'],'start':round(s['start'],3)});last=s['chapter']
        # Use actual sentence boundaries returned by the speech service.
        boundaries=[json.loads(line) for line in (ROOT/'video/audio'/f"{s['index']:02}.boundaries.jsonl").read_text().splitlines() if line.strip()]
        for index,cue in enumerate(boundaries):
            start=s['start']+cue['offset']/1e7;end=min(s['end'],start+cue['duration']/1e7)
            if index+1<len(boundaries):end=min(end,s['start']+boundaries[index+1]['offset']/1e7)
            if end>start:captions.extend([f'{ts(start)} --> {ts(end)}','\n'.join(wrapped(cue['text'],38,1350)),''])
        trans.extend([f'## {ts(s["start"])} · {s["title"]}',s['speech'],''])
    (DEST/'lesson.zh.vtt').write_text('\n'.join(captions));(DEST/'chapters.json').write_text(json.dumps(chap,ensure_ascii=False,indent=2)+'\n');(ROOT/'site/downloads/transcript.md').write_text('\n'.join(trans));(ROOT/'video/timeline.json').write_text(json.dumps({'width':W,'height':H,'fps':FPS,'duration':DURATION,'scenes':SCENES},ensure_ascii=False,indent=2)+'\n');render_frame(SCENES[6]['start']+4).save(DEST/'poster.jpg',quality=92)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stills',action='store_true');args=parser.parse_args();outputs();print(f'Timeline {DURATION:.2f}s / {len(SCENES)} beats',flush=True)
    qa=ROOT/'.qa';qa.mkdir(exist_ok=True)
    if args.stills:
        contact=Image.new('RGB',(960*3,540*math.ceil(len(SCENES)/3)),BG)
        for i,s in enumerate(SCENES):
            im=render_frame(s['start']+s['duration']*.7);im.save(qa/f'scene-{i:02}.jpg',quality=88);contact.paste(im.resize((960,540)),((i%3)*960,(i//3)*540))
        contact.save(qa/'contact.jpg',quality=90);return
    assert 240<=DURATION<=360,f'Film must be 4–6 minutes, actual {DURATION}'
    process=subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(CACHE/'narration.wav'),'-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-threads','4','-t',str(DURATION),str(DEST/'lesson.zh.mp4')],stdin=subprocess.PIPE)
    began=time.monotonic();frames=round(DURATION*FPS)
    try:
        for f in range(frames):
            process.stdin.write(render_frame(f/FPS).tobytes())
            if f%300==0:print(f'{f}/{frames} frames / {time.monotonic()-began:.1f}s elapsed',flush=True)
        process.stdin.close();assert process.wait()==0
    except BaseException:process.kill();raise
    print('Encoded',DEST/'lesson.zh.mp4',flush=True)
if __name__=='__main__':main()
