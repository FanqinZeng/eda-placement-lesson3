"""Export both real voice timelines and all language-specific website links."""
from pathlib import Path
import json
from media_config import media_config
ROOT=Path(__file__).resolve().parents[1];versions={};kinds=None
for lang in ('zh','en'):
    c=media_config(lang);t=json.loads((ROOT/c['timeline']).read_text())
    current=[s['kind'] for s in t['scenes']]
    if kinds is None:kinds=current
    assert current==kinds,'Languages must have the same authored scenes'
    v={k:'media/'+c[k] for k in ['video','captions','poster']}
    v['captions']=f'media/lesson.{lang}.bilingual.vtt'
    v['captionTracks']={mode:f'media/lesson.{lang}.{mode}.vtt' for mode in ['bilingual','zh','en']}
    v.update({'transcript':f'reading/#transcript-{lang}','transcriptDownload':'downloads/'+c['transcript'],'duration':t['duration'],'voice':c['voice'],'label':'中文' if lang=='zh' else 'English','trackLabel':'中英双语','trackLanguage':'mul','chapters':json.loads((ROOT/'site/media'/c['chapters']).read_text()),'scenes':[{k:s[k] for k in ['start','end']} for s in t['scenes']]})
    for k in ['video','captions','poster','transcriptDownload']:assert (ROOT/'site'/v[k]).is_file(),v[k]
    versions[lang]=v
(ROOT/'site/media/versions.json').write_text(json.dumps(versions,ensure_ascii=False,indent=2)+'\n');print('Exported two real voice versions / 25 shared scenes')
