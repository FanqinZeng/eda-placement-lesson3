"""Offline preview with byte ranges for MP4 seeking. Standard library only.
python3 scripts/serve.py --port 8000
"""
import argparse,functools,re,os
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
class RangeHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.remaining=None;path=Path(self.translate_path(self.path));header=self.headers.get('Range')
        if not header or not path.is_file():return super().send_head()
        size=path.stat().st_size;match=re.fullmatch(r'bytes=(\d*)-(\d*)',header)
        try:
            if not match or not size or not any(match.groups()):raise ValueError()
            a,b=match.groups()
            if a:start=int(a);end=min(int(b),size-1) if b else size-1
            else:start=max(0,size-int(b));end=size-1
            if start<0 or start>=size or end<start:raise ValueError()
        except ValueError:
            self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
        f=path.open('rb');f.seek(start);self.remaining=end-start+1
        self.send_response(206);self.send_header('Content-Type',self.guess_type(str(path)));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(self.remaining));self.end_headers();return f
    def copyfile(self,source,outputfile):
        if self.remaining is None:return super().copyfile(source,outputfile)
        while self.remaining:
            chunk=source.read(min(self.remaining,65536))
            if not chunk:break
            outputfile.write(chunk);self.remaining-=len(chunk)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8000);args=parser.parse_args();site=Path(__file__).resolve().parents[1]/'site'
    server=ThreadingHTTPServer(('127.0.0.1',args.port),functools.partial(RangeHandler,directory=str(site)))
    print(f'Local: http://127.0.0.1:{args.port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()
