from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import base64, json

out = Path(__file__).parent.parent / 'готовое' / 'исследование-v4'
out.mkdir(exist_ok=True)
allowed = {'trevor.jpg', 'aardvark.jpg', 'aardvark-steps.jpg', 'kokoro.jpg', 'knko.jpg', 'mersi.jpg', 'field-hero.jpg', 'field-price.jpg', 'board.jpg'}

class Capture(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1:8846')
        self.send_header('Access-Control-Allow-Methods', 'POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        name = self.path.removeprefix('/')
        size = int(self.headers.get('Content-Length', 0))
        if name not in allowed or size > 5000000 or self.headers.get('Origin') != 'http://127.0.0.1:8846':
            self.send_error(403)
            return
        data = base64.b64decode(json.loads(self.rfile.read(size))['data'], validate=True)
        (out / name).write_bytes(data)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1:8846')
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, *args):
        pass

HTTPServer(('127.0.0.1', 8858), Capture).serve_forever()
