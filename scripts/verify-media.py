"""Verify encoded streams, decoded audio level and caption/scene coverage."""
from pathlib import Path
import json,subprocess,re,hashlib,argparse
from media_config import media_config
import imageio_ffmpeg
parser=argparse.ArgumentParser();parser.add_argument('--lang',choices=['zh','en'],default='zh');ARGS=parser.parse_args();CFG=media_config(ARGS.lang)
ROOT=Path(__file__).resolve().parents[1];media=ROOT/'site/media';ff=imageio_ffmpeg.get_ffmpeg_exe();path=media/CFG['video'];timeline=json.loads((ROOT/CFG['timeline']).read_text())
p=subprocess.run([ff,'-hide_banner','-i',str(path),'-map','0:a:0','-af','volumedetect','-f','null','-'],capture_output=True,text=True);assert p.returncode==0,p.stderr
assert '1920x1080' in p.stderr and '30 fps' in p.stderr and 'Video: h264' in p.stderr and 'Audio: aac' in p.stderr,p.stderr
mean=float(re.search(r'mean_volume: ([\-\d.]+) dB',p.stderr)[1]);peak=float(re.search(r'max_volume: ([\-\d.]+) dB',p.stderr)[1]);assert -35<mean<-8 and peak<0,(mean,peak)
def seconds(t):
 h,m,s=t.split(':');return int(h)*3600+int(m)*60+float(s)
cues=[(seconds(a),seconds(b)) for a,b in re.findall(r'(\d\d:\d\d:\d\d\.\d{3}) --> (\d\d:\d\d:\d\d\.\d{3})',(media/CFG['captions']).read_text())]
assert cues and all(0<=a<b<=timeline['duration']+.05 for a,b in cues)
assert all(cues[i][1]<=cues[i+1][0]+.01 for i in range(len(cues)-1))
assert 240<=timeline['duration']<=360 and timeline['fps']==30
for i,s in enumerate(timeline['scenes']):
 assert s['end']>s['start'];assert i==0 or abs(timeline['scenes'][i-1]['end']-s['start'])<1e-6
 assert (ROOT/CFG['audio_dir']/f'{i:02}.mp3').stat().st_size>1000
 assert json.loads((ROOT/CFG['audio_dir']/f'{i:02}.json').read_text())['voice']==CFG['voice']
assert cues[-1][1]>timeline['duration']-4
report={'language':ARGS.lang,'voice':CFG['voice'],'status':'passed','duration_seconds':round(timeline['duration'],3),'resolution':'1920x1080','fps':30,'video_codec':'H.264','audio_codec':'AAC','mean_volume_db':mean,'peak_volume_db':peak,'subtitle_cues':len(cues),'subtitle_timing':'speech-service sentence boundaries','scenes':len(timeline['scenes']),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'limits':['Automated stream/audio-level/timing validation and representative frame inspection; subjective human listening review remains open.']}
(ROOT/'docs/qa'/CFG['report']).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
