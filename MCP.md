# MCP setup

1. Install Python 3.10+.
2. From the package root run `python -m pip install -r requirements-mcp.txt`.
3. Register a local stdio MCP server in the agent:
   - command: absolute Python executable path
   - arguments: absolute path to `adapters/mcp_server.py`
   - working directory: package root, if supported
4. Reload the connection and verify `toyota.identify_vehicle`, `toyota.inspect_bin`, `toyota.inspect_speed`, `toyota.inspect_rpm`, and `toyota.inspect_cutoff` are listed.
5. Call a tool with `{"file_path":"ABSOLUTE_PATH_TO_TEST_BIN"}`.

The MCP process uses the local catalog and local plugin files. It does not fetch or execute remote code.
