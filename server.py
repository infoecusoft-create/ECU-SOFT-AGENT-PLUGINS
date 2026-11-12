"""Read-only JSON registry API; metadata only, no remote plugin execution."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import hashlib,json,os
class RegistryHandler(BaseHTTPRequestHandler):
 index_path=Path(__file__).resolve().parents[1]/"registry/index.json"
 def _send(self,status,data,etag=None):
  b=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header("Content-Type","application/json; charset=utf-8");self.send_header("Content-Length",str(len(b)));self.send_header("Cache-Control","public, max-age=60")
  if etag:self.send_header("ETag",etag)
  self.end_headers();self.wfile.write(b)
 def do_GET(self):
  try:d=json.loads(Path(self.index_path).read_text(encoding="utf-8"))
  except Exception as e:return self._send(503,{"error":"catalog_unavailable","detail":str(e)})
  etag='"'+hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()+'"'
  if self.headers.get("If-None-Match")==etag:self.send_response(304);self.send_header("ETag",etag);self.end_headers();return
  if self.path=="/health":return self._send(200,{"status":"ok","schema_version":d.get("schema_version")},etag)
  if self.path in ("/","/v1/plugins"):return self._send(200,d,etag)
  if self.path.startswith("/v1/capabilities/"):
   cap=self.path.rsplit("/",1)[-1];found=[]
   for p in d.get("plugins",[]):
    for c in p.get("capabilities",[]):
     if c.get("id")==cap:found.append({"plugin":{k:p.get(k) for k in ("id","name","version","description")},"capability":c})
   return self._send(200,{"capability":cap,"matches":len(found),"results":found},etag)
  return self._send(404,{"error":"not_found"})
 def log_message(self,*a):pass
def serve(host="127.0.0.1",port=8765):ThreadingHTTPServer((host,port),RegistryHandler).serve_forever()
if __name__=="__main__":serve(os.getenv("ECUSOFT_REGISTRY_HOST","127.0.0.1"),int(os.getenv("ECUSOFT_REGISTRY_PORT","8765")))
