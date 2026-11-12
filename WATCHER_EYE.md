# Watcher Eye setup

If the installed Watcher Eye build has an MCP client, add `ECU SOFT` as a local stdio MCP server. Use the absolute Python executable, `adapters/mcp_server.py` path and package root as working directory. Refresh discovery and verify the five `toyota.*` tools before use.

If MCP client support is not implemented in that Watcher Eye build, integrate `PluginHost` directly from Python (see `../../AGENT_INTEGRATION_GUIDE.md`, section 8) or build a reviewed adapter. Do not label it MCP integration until an MCP connection and tool call have actually passed.
