"""REST registry client with a local JSON snapshot fallback."""
import json,urllib.request
from pathlib import Path
class RegistryClient:
 def __init__(self,base_url,snapshot_path):self.base_url=base_url.rstrip("/");self.snapshot=Path(snapshot_path).expanduser()
 def catalog(self,timeout=5):
  try:
   with urllib.request.urlopen(self.base_url+"/v1/plugins",timeout=timeout) as r:b=r.read()
   self.snapshot.parent.mkdir(parents=True,exist_ok=True);self.snapshot.write_bytes(b);return json.loads(b),"online"
  except OSError:
   if not self.snapshot.exists():raise RuntimeError("Registry is offline and no cache snapshot exists")
   return json.loads(self.snapshot.read_text(encoding="utf-8")),"offline_cache"
