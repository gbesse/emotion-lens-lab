import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
from .__main__ import ROOT,example
from .engine import analyze,document,markdown,svg
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*_):pass
    def reply(self,code,data,kind="application/json"):
        content=data if isinstance(data,bytes) else json.dumps(data).encode();self.send_response(code);self.send_header("Content-Type",kind+"; charset=utf-8");self.send_header("Content-Length",str(len(content)));self.send_header("Cache-Control","no-store");self.send_header("X-Content-Type-Options","nosniff");self.end_headers();self.wfile.write(content)
    def do_GET(self):
        url=urlparse(self.path);path=url.path
        if path=="/api/example":
            lang=parse_qs(url.query).get("lang",["en"])[0]
            return self.reply(200,example(lang if lang in ("fr","en","es") else "en"))
        if path in ("/","/app.js","/style.css"):
            file="index.html" if path=="/" else path[1:];return self.reply(200,(ROOT/"web"/file).read_bytes(),{"index.html":"text/html","app.js":"text/javascript","style.css":"text/css"}[file])
        self.reply(404,{"error":"not_found"})
    def do_POST(self):
        if self.path not in ("/api/document","/api/analyze","/api/markdown","/api/svg"):return self.reply(404,{"error":"not_found"})
        if self.headers.get("Origin") not in (None,f"http://127.0.0.1:{self.server.server_port}"):return self.reply(403,{"error":"origin_denied"})
        try:
            size=int(self.headers.get("Content-Length","0"))
            if not 0<size<=500000:raise ValueError("invalid_size")
            data=json.loads(self.rfile.read(size));lang=data.get("lang","en")
            if lang not in ("fr","en","es"):raise ValueError("language")
            if self.path=="/api/document":result={"document":document(data["text"],data["language"],data.get("title","")),"annotations":[]}
            elif self.path=="/api/analyze":result=analyze(data["bundle"])
            elif self.path=="/api/markdown":return self.reply(200,markdown(data["bundle"],lang).encode(),"text/markdown")
            else:return self.reply(200,svg(data["bundle"],lang).encode(),"image/svg+xml")
            self.reply(200,result)
        except (ValueError,TypeError,KeyError):self.reply(400,{"error":"invalid_input","messages":["Entrée non valide","Invalid input","Entrada no válida"]})
def serve(port=8771):ThreadingHTTPServer(("127.0.0.1",port),Handler).serve_forever()
