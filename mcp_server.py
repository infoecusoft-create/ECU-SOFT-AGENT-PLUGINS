"""Optional MCP stdio adapter. Requires pip install -r requirements-mcp.txt."""
from pathlib import Path
import json
INDEX=Path(__file__).resolve().parents[1]/"registry/index.json"
def capabilities_from_index(index):
 out=[]
 for p in index.get("plugins",[]):
  for c in p.get("capabilities",[]):out.append({"name":c["id"],"description":c.get("description",p.get("description","")),"inputSchema":{"type":"object","properties":{k:{"type":"string"} for k in c.get("input",{})},"required":list(c.get("input",{}))},"plugin_id":p["id"],"mode":c.get("mode","read")})
 return out
def run_stdio():
 try:from mcp.server.fastmcp import FastMCP
 except ImportError as e:raise SystemExit("Install MCP support: pip install -r requirements-mcp.txt") from e
 from plugin_host import PluginHost
 h=PluginHost();app=FastMCP("ECU SOFT Universal Registry")
 for item in capabilities_from_index(json.loads(INDEX.read_text(encoding="utf-8"))):
  if item["mode"]!="read":continue
  def bind(cap):
   def tool(file_path:str):return h.execute(cap,file_path=file_path)
   return tool
  app.tool(name=item["name"],description=item["description"])(bind(item["name"]))
 app.run(transport="stdio")
if __name__=="__main__":run_stdio()
