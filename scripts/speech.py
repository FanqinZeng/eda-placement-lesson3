"""Freeze authored Mandarin speech; network required only for missing/changed beats."""
import asyncio,json,hashlib,os,ssl
from pathlib import Path
import edge_tts,certifi
ROOT=Path(__file__).resolve().parents[1]
VOICE='zh-CN-XiaoxiaoNeural';RATE='+0%'
async def main():
    story=json.loads((ROOT/'video/story.json').read_text());sem=asyncio.Semaphore(3)
    async def one(i,beat):
        path=ROOT/'video/audio'/f'{i:02}.mp3';meta=path.with_suffix('.json');digest=hashlib.sha256((VOICE+RATE+beat[4]).encode()).hexdigest()
        if path.exists() and meta.exists() and json.loads(meta.read_text()).get('digest')==digest:return
        async with sem:
            for attempt in range(3):
                try:
                    await edge_tts.Communicate(beat[4],VOICE,rate=RATE).save(str(path),str(path.with_suffix('.boundaries.jsonl')));break
                except Exception:
                    if attempt==2:raise
                    await asyncio.sleep(1+attempt)
            meta.write_text(json.dumps({'digest':digest,'voice':VOICE,'rate':RATE,'text':beat[4]},ensure_ascii=False,indent=2)+'\n');print(f'speech {i+1}/{len(story)}',flush=True)
    await asyncio.gather(*(one(i,b) for i,b in enumerate(story)))
if __name__=='__main__':asyncio.run(main())
