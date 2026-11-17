import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from media_config import media_config
class MediaConfigTests(unittest.TestCase):
    def test_language_outputs_are_separate_and_chinese_stays_compatible(self):
        zh,en=media_config('zh'),media_config('en')
        self.assertEqual(zh['chapters'],'chapters.json');self.assertEqual(zh['poster'],'poster.jpg')
        self.assertEqual(en['chapters'],'chapters.en.json');self.assertEqual(en['video'],'lesson.en.mp4')
        self.assertEqual(zh['audio_dir'],'video/audio');self.assertEqual(en['audio_dir'],'video/audio/en')
        self.assertTrue(zh['voice'].startswith('zh-'));self.assertTrue(en['voice'].startswith('en-'))
    def test_unknown_language_rejected(self):
        with self.assertRaises(ValueError):media_config('fr')
if __name__=='__main__':unittest.main()
