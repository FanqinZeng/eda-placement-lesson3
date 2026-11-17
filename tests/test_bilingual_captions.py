import unittest,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CaptionsTests(unittest.TestCase):
    def test_translations_cover_every_spoken_sentence_on_both_timelines(self):
        rows=json.loads((ROOT/'video/bilingual-alignment.json').read_text())
        for lang in ('zh','en'):
            story=json.loads((ROOT/('video/story.json' if lang=='zh' else 'video/story.en.json')).read_text())
            normal=lambda x:re.sub(r'\s+','',x)
            for i,beat in enumerate(story):
                self.assertEqual(normal(''.join(r[lang] for r in rows if r['scene']==i)),normal(beat[4]))
            previous=0
            for row in rows:
                t=row['timing'][lang];self.assertLess(t['start'],t['end']);self.assertGreaterEqual(t['start']+.001,previous);previous=t['end']
            text=(ROOT/f'site/media/lesson.{lang}.bilingual.vtt').read_text()
            for cue in text.split('\n\n')[1:]:
                if '-->' not in cue:continue
                self.assertRegex(cue,r'[\u4e00-\u9fff]');self.assertRegex(cue,r'[A-Za-z]')
if __name__=='__main__':unittest.main()
