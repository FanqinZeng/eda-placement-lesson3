"""Freeze authored Mandarin speech; network required only for missing/changed beats."""
import asyncio,json,hashlib,argparse
from pathlib import Path
import edge_tts
from media_config import media_config
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--lang',choices=['zh','en'],default='zh');ARGS=parser.parse_args()
CFG=media_config(ARGS.lang);VOICE=CFG['voice'];RATE='+0%'
(ROOT/CFG['audio_dir']).mkdir(parents=True,exist_ok=True)
async def main():
    story=json.loads((ROOT/CFG['story']).read_text());sem=asyncio.Semaphore(3)
    async def one(i,beat):
        path=ROOT/CFG['audio_dir']/f'{i:02}.mp3';meta=path.with_suffix('.json');digest=hashlib.sha256((VOICE+RATE+beat[4]).encode()).hexdigest()
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
