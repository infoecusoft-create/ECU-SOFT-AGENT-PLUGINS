import json,tempfile,unittest,threading,urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer
from ecusoft_registry.server import RegistryHandler
class ApiTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name)/"index.json";p.write_text(json.dumps({"schema_version":1,"plugins":[{"id":"p","capabilities":[{"id":"p.read","mode":"read"}]}]}));RegistryHandler.index_path=p;self.s=ThreadingHTTPServer(("127.0.0.1",0),RegistryHandler);threading.Thread(target=self.s.serve_forever,daemon=True).start();self.base=f"http://127.0.0.1:{self.s.server_port}"
 def tearDown(self):self.s.shutdown();self.s.server_close();self.tmp.cleanup()
 def test_health_and_catalog(self):self.assertEqual(json.loads(urllib.request.urlopen(self.base+"/health").read())["status"],"ok");self.assertEqual(len(json.loads(urllib.request.urlopen(self.base+"/v1/plugins").read())["plugins"]),1)
 def test_capability_lookup(self):self.assertEqual(json.loads(urllib.request.urlopen(self.base+"/v1/capabilities/p.read").read())["matches"],1)
if __name__=="__main__":unittest.main()
