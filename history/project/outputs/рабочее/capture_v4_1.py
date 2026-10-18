from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
import base64,json
out=Path(__file__).parent.parent/'готовое'/'проверка';out.mkdir(exist_ok=True)
allowed={'desktop-v4-1.jpg','mobile-v4-1.jpg','tasks-v4-1.jpg','tracks-v4-1.jpg','week-v4-1.jpg','camp-v4-1.jpg','calendar-v4-1.jpg','reviews-v4-1.jpg','team-v4-1.jpg','price-v4-1.jpg','qa-v4-1.json','live-v4-1.jpg','mobile-price-v4-1.jpg','alumni-v4-1.jpg'}
class Capture(BaseHTTPRequestHandler):
 def do_OPTIONS(self):
  self.send_response(204);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8846');self.send_header('Access-Control-Allow-Methods','POST,OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type');self.end_headers()
 def do_POST(self):
  name=self.path.removeprefix('/')
  size=int(self.headers.get('Content-Length',0))
  if name not in allowed or size>5000000 or self.headers.get('Origin')!='http://127.0.0.1:8846':self.send_error(403);return
  obj=json.loads(self.rfile.read(size))
  if name.endswith('.jpg'):(out/name).write_bytes(base64.b64decode(obj['data'],validate=True))
  else:(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
  self.send_response(200);self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8846');self.end_headers();self.wfile.write(b'OK')
 def log_message(self,*args):pass
HTTPServer(('127.0.0.1',8858),Capture).serve_forever()
