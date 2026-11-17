import functools,sys,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from http.server import ThreadingHTTPServer
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from serve import RangeHandler
class RangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.content=bytes(range(200));Path(cls.temp.name,'film.mp4').write_bytes(cls.content)
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(RangeHandler,directory=cls.temp.name));cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.url=f'http://127.0.0.1:{cls.server.server_port}/film.mp4'
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.temp.cleanup()
    def test_prefix_middle_suffix_and_head(self):
        for header,want in [('bytes=0-31',self.content[:32]),('bytes=100-150',self.content[100:151]),('bytes=-16',self.content[-16:])]:
            with self.subTest(header=header),urllib.request.urlopen(urllib.request.Request(self.url,headers={'Range':header})) as r:self.assertEqual(r.status,206);self.assertEqual(r.read(),want);self.assertEqual(int(r.headers['Content-Length']),len(want))
        with urllib.request.urlopen(urllib.request.Request(self.url,method='HEAD',headers={'Range':'bytes=0-31'})) as r:self.assertEqual(r.status,206);self.assertEqual(r.read(),b'');self.assertEqual(r.headers['Content-Range'],'bytes 0-31/200')
    def test_invalid_ranges(self):
        for header in ['bytes=999-','bytes=10-2','bytes=-0','bytes=-','bytes=0-1,4-5']:
            with self.subTest(header=header),self.assertRaises(urllib.error.HTTPError) as caught:urllib.request.urlopen(urllib.request.Request(self.url,headers={'Range':header}))
            self.assertEqual(caught.exception.code,416)
if __name__=='__main__':unittest.main()
