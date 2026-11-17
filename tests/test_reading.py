import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_reading import render_markdown,build_page
class ReadingTests(unittest.TestCase):
    def test_notes_are_semantic_html_with_tables_lists_and_code(self):
        html=render_markdown('# 标题\n\n说明 **半周长** 和 `x<y`。\n\n1. 第一项\n2. 第二项\n\n| Pin | x |\n|---|---:|\n| A | 2 |\n\n```python\nprint("<script>")\n```')
        for fragment in ['<h2','<strong>半周长</strong>','<code>x&lt;y</code>','<ol>','<table>','<th>Pin</th>','&lt;script&gt;']:self.assertIn(fragment,html)
        self.assertNotIn('<script>',html)
    def test_full_source_contents_are_available_without_javascript(self):
        html=build_page()
        for anchor in ['exercise','reference','data','notes','transcript-zh','transcript-en','reproduce']:self.assertIn('id="'+anchor+'"',html)
        for snippet in ['def bbox(pins):','def evaluate(pins,hub=None):','只走横向和竖向','Horizontal plus vertical','python3 scripts/serve.py']:self.assertIn(snippet,html)
        self.assertIn('<pre',html);self.assertIn('code-copy',html)
        self.assertNotIn('<iframe',html)
if __name__=='__main__':unittest.main()
