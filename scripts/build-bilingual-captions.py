"""Align authored translations by meaning, timed against each real narration.
Also mux a default bilingual subtitle stream into each downloadable MP4.
"""
from pathlib import Path
import json,textwrap,subprocess,argparse
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];MEDIA=ROOT/'site/media'
# Consecutive sentence counts manually aligned against both authored scripts.
GROUPS={2:([2,1],[1,1]),3:([2,1],[2,1]),4:([1,1],[2,1]),5:([1,1,1],[1,2,1]),6:([2,1],[1,2]),8:([2,1],[1,2]),10:([1,1],[1,2]),11:([1,1],[1,2]),12:([1,1,1],[1,1,2]),15:([1,1,1],[1,2,1]),18:([2,1],[2,1]),21:([1,1],[1,2]),23:([1,1],[1,2])}
def ts(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02}.{ms:03}'
def groups(cues,counts):
    assert sum(counts)==len(cues),(counts,len(cues));out=[];i=0
    for n in counts:out.append(cues[i:i+n]);i+=n
    return out
def line(text,lang):
    if lang=='zh':return '\n'.join(text[i:i+42] for i in range(0,len(text),42))
    return textwrap.fill(text,85,break_long_words=False)
def build(mux=False):
    timelines={l:json.loads((ROOT/('video/timeline.json' if l=='zh' else 'video/timeline.en.json')).read_text()) for l in ('zh','en')};alignments=[]
    results={l:{k:['WEBVTT',''] for k in ['bilingual','zh','en']} for l in ('zh','en')}
    for i in range(25):
        cues={l:[json.loads(s) for s in (ROOT/('video/audio' if l=='zh' else 'video/audio/en')/f'{i:02}.boundaries.jsonl').read_text().splitlines()] for l in ('zh','en')}
        counts=GROUPS.get(i,([1]*len(cues['zh']),[1]*len(cues['en'])));assert len(counts[0])==len(counts[1])
        paired={l:groups(cues[l],counts[j]) for j,l in enumerate(('zh','en'))}
        for j in range(len(counts[0])):
            text={l:('' if l=='zh' else ' ').join(c['text'] for c in paired[l][j]) for l in ('zh','en')};entry={'scene':i,'zh':text['zh'],'en':text['en'],'timing':{}}
            for lang in ('zh','en'):
                scene=timelines[lang]['scenes'][i];g=paired[lang][j];start=scene['start']+g[0]['offset']/1e7;end=min(scene['end'],scene['start']+(g[-1]['offset']+g[-1]['duration'])/1e7)
                if j+1<len(paired[lang]):end=min(end,scene['start']+paired[lang][j+1][0]['offset']/1e7)
                assert 0<=start<end<=timelines[lang]['duration'];entry['timing'][lang]={'start':start,'end':end}
                for mode in ('bilingual','zh','en'):
                    body=line(text['zh'],'zh')+'\n'+line(text['en'],'en') if mode=='bilingual' else line(text[mode],mode)
                    results[lang][mode].extend([f'{ts(start)} --> {ts(end)}',body,''])
            alignments.append(entry)
    for lang in ('zh','en'):
        for mode,vtt in results[lang].items():(MEDIA/f'lesson.{lang}.{mode}.vtt').write_text('\n'.join(vtt))
        if mux:
            src=MEDIA/f'lesson.{lang}.mp4';temp=MEDIA/f'.lesson.{lang}.mux.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe()
            subprocess.run([ff,'-v','error','-y','-i',str(src),'-i',str(MEDIA/f'lesson.{lang}.bilingual.vtt'),'-map','0:v:0','-map','0:a:0','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=mul','-metadata:s:s:0','title=Chinese + English','-disposition:s:0','default','-movflags','+faststart',str(temp)],check=True);temp.replace(src)
    (ROOT/'video/bilingual-alignment.json').write_text(json.dumps(alignments,ensure_ascii=False,indent=2)+'\n');print(f'Built {len(alignments)} bilingual semantic units on both voice timelines')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--mux',action='store_true');build(parser.parse_args().mux)
