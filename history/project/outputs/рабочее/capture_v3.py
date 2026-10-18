from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
import base64,json
out=Path(__file__).parent.parent/'готовое'/'проверка';out.mkdir(exist_ok=True)
allowed={'desktop-v3.jpg','mobile-v3.jpg','tasks-v3.jpg','tracks-v3.jpg','week-v3.jpg','camp-v3.jpg','calendar-v3.jpg','reviews-v3.jpg','team-v3.jpg','price-v3.jpg','qa-v3.json'}
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
