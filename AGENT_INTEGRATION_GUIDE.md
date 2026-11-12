# ECU SOFT Agent Integration Guide

Version: 0.2.0  
Package: `ECU-SOFT-AGENT-PLUGINS-HYBRID`

This guide explains how an AI agent can discover and call the capabilities shipped in this package. It documents the code in this archive; it does not promise compatibility with every agent product.

## 1. What is included

- `plugin_host.py`: local Python host. It discovers capabilities from `registry/index.json` and lazily loads the selected local plugin.
- `adapters/mcp_server.py`: MCP stdio server. MCP-capable agents can expose its read-only tools to the model.
- `ecusoft_registry/server.py`: read-only HTTP catalog API (metadata discovery only).
- `adapters/rest_client.py`: Python catalog client with a local JSON snapshot fallback.
- `plugins/toyota/toyo_limiter/`: Toyota BIN Inspector. Its registered actions are read-only.

**Important implementation boundary:** the HTTP Registry serves metadata; it does not execute a plugin remotely. The MCP server executes the local plugin through `PluginHost`. The current MCP adapter reads its local `registry/index.json`; it does not automatically download/synchronize a central registry. `RegistryClient` caches catalog metadata only; it is not a remote execution client.

## 2. Requirements

- Python 3.10 or newer.
- For MCP integration: install the optional MCP dependency with `python -m pip install -r requirements-mcp.txt`.
- The agent application must support MCP over stdio, or provide an equivalent custom tool/connector integration.

Run commands from the extracted package root (the directory containing `plugin_host.py`). On Windows, use `py` instead of `python` if that is how Python is installed.

## 3. Validate the package before connecting an agent

```bash
python tools/validate_plugins.py
python tools/build_index.py
python -m unittest discover -s tests -v
```

Start the local catalog API when an HTTP metadata endpoint is needed:

```bash
python -m ecusoft_registry.server
```

Default local address: `http://127.0.0.1:8765`.

Check it:

```bash
curl http://127.0.0.1:8765/health
curl http://127.0.0.1:8765/v1/plugins
curl http://127.0.0.1:8765/v1/capabilities/toyota.inspect_bin
```

Available routes:

| Route | Purpose |
|---|---|
| `GET /health` | API health and schema version |
| `GET /v1/plugins` | Full plugin catalog / metadata |
| `GET /v1/capabilities/{capability_id}` | Find providers for a capability |

These HTTP routes are read-only catalog endpoints. They do not accept a BIN file and do not run a plugin.

## 4. MCP integration (recommended for compatible agents)

### 4.1 Install and smoke-test

```bash
python -m pip install -r requirements-mcp.txt
python adapters/mcp_server.py
```

The second command starts an MCP stdio process and waits for the MCP client. Do not launch it in a normal terminal and expect a human-readable prompt; the agent application owns the stdio protocol. Stop it with Ctrl+C when testing manually.

### 4.2 Register the MCP server in an agent

In the agent's MCP settings, create a **local / stdio** server with:

- Display name: `ECU SOFT`
- Command: the absolute path to the Python executable
- Arguments: the absolute path to `adapters/mcp_server.py`
- Working directory (if supported): the extracted package root
- Environment (optional): `PYTHONUNBUFFERED=1`

Example command/arguments (replace paths with the actual installation paths):

```text
Command: C:\Python312\python.exe
Arguments: C:\ECU-SOFT-AGENT-PLUGINS\repo_snapshot\adapters\mcp_server.py
Working directory: C:\ECU-SOFT-AGENT-PLUGINS\repo_snapshot
```

On Linux/macOS, the equivalent may look like:

```text
Command: /usr/bin/python3
Arguments: /opt/ecu-soft-agent-plugins/adapters/mcp_server.py
Working directory: /opt/ecu-soft-agent-plugins
```

The exact settings-file syntax differs between agent products and versions. Use the agent's own MCP configuration screen/schema; do not paste a configuration example for a different product without adapting it. After saving, restart/reload the agent's MCP connection and confirm that it lists these tools:

- `toyota.identify_vehicle`
- `toyota.inspect_bin`
- `toyota.inspect_speed`
- `toyota.inspect_rpm`
- `toyota.inspect_cutoff`

### 4.3 How the agent should call a tool

The MCP tool input currently contains one required string field: `file_path`.

Example user request to the connected agent:

> Use ECU SOFT `toyota.inspect_bin` on `D:\ECU\vehicle.bin`. Do not modify the file. Report the detected profile, SHA-256 and raw observations, and clearly state any ambiguity.

The agent should select the MCP tool `toyota.inspect_bin` and pass:

```json
{"file_path":"D:\\ECU\\vehicle.bin"}
```

The file path is read by the local process running the MCP server. The BIN must be accessible to that machine/account. If the agent runs remotely or in a container, a host path may not exist there.

## 5. OpenCode integration

If the installed OpenCode version supports local MCP servers, add an MCP server entry through its supported MCP configuration mechanism using the values in section 4.2. Configure the Python executable and script as absolute paths and set the package root as the working directory if the version supports it.

Then:

1. Restart/reload OpenCode so it starts the MCP process.
2. Open the tool list and verify the five `toyota.*` tools are present.
3. Ask OpenCode to run `toyota.identify_vehicle` or `toyota.inspect_bin` with a real local BIN path.
4. Verify that the response identifies the operation as read-only and that the source BIN's hash is unchanged.

OpenCode configuration keys and file locations can vary by release. This archive intentionally does not prescribe an unverified OpenCode JSON schema. Follow the MCP configuration format documented by the exact OpenCode build in use.

## 6. Watcher Eye integration

For a Watcher Eye build with MCP client support:

1. Add a new local MCP connection named `ECU SOFT`.
2. Set its transport to stdio.
3. Set the executable, script arguments, and working directory as in section 4.2.
4. Grant the MCP process read access only to the intended ECU input folder where the operating system allows it.
5. Refresh tool discovery and confirm the five `toyota.*` capabilities appear.
6. Route Toyota identification/inspection requests to these tools; do not ask the language model to invent offsets or profile matches.

If Watcher Eye does not yet implement an MCP client, create a product-specific adapter that invokes the local `PluginHost` API shown in section 8. Do not describe the integration as MCP-connected until an actual MCP client connection and tool call have been tested.

## 7. REST / HTTP discovery for agents without MCP

The catalog API can help an agent discover available plugins and capability descriptions:

```http
GET http://127.0.0.1:8765/v1/plugins
GET http://127.0.0.1:8765/v1/capabilities/toyota.inspect_bin
```

An agent that only supports HTTP can use these endpoints for discovery. **The current package does not provide an HTTP endpoint to execute Toyota tools.** To execute locally, the agent needs a trusted local bridge/adapter that calls `PluginHost`, or it should use MCP if supported.

Do not expose the catalog server to the public internet as an execution service; it is metadata-only and has no authentication layer in this build. Keep it bound to localhost unless you add an authenticated, reviewed deployment layer.

## 8. Direct Python SDK-style integration

The current stable programmatic interface is `PluginHost` (there is not yet a separately packaged/published pip SDK).

```python
from pathlib import Path
from plugin_host import PluginHost

package_root = Path(r"C:\ECU-SOFT-AGENT-PLUGINS\repo_snapshot")
host = PluginHost(package_root / "registry" / "index.json")

# Discover capability metadata
matches = host.discover("toyota.inspect_bin")
print(matches)

# Execute the local read-only capability
result = host.execute(
    "toyota.inspect_bin",
    file_path=r"D:\ECU\vehicle.bin",
)
print(result)
```

Run this script with the package root as the working directory, or add that root to `PYTHONPATH`. Treat the returned dictionary as untrusted tool output and validate it before using it in automated decisions.

Other registered capability IDs are:

```text
toyota.identify_vehicle
toyota.inspect_bin
toyota.inspect_speed
toyota.inspect_rpm
toyota.inspect_cutoff
```

## 9. Offline behavior and central registry bootstrap

- Local MCP calls use the local `registry/index.json` and local plugin files. They can work without internet as long as Python, dependencies, the package and the input BIN are available.
- The HTTP catalog server also serves the local index file.
- `RegistryClient` can download `/v1/plugins` and save a JSON snapshot, then return that snapshot when the HTTP server is unavailable.

Example:

```python
from adapters.rest_client import RegistryClient

client = RegistryClient(
    base_url="http://127.0.0.1:8765",
    snapshot_path="~/.ecusoft/registry-cache.json",
)
catalog, source = client.catalog()
print("catalog source:", source)  # online or offline_cache
print("plugins:", [p["id"] for p in catalog.get("plugins", [])])
```

For a future centrally hosted registry, configure its fixed base URL once in the agent/adapter settings. Users should not need to paste individual GitHub repository URLs for every tool lookup. This archive does **not** yet implement automatic cloud bootstrap, signed catalog verification, automatic plugin downloads, or synchronization of the MCP server's local index from a remote registry. Those require a separately deployed registry and additional implementation/security review.

## 10. Security and safe operation

- Current Toyota capabilities are read-only; they inspect files and return observations.
- Do not grant write access to ECU files for this plugin.
- Keep original BIN files immutable and work on copies for any future editing workflow.
- `PluginHost` is a Python loader, **not an operating-system sandbox**. Only load plugins from a trusted, reviewed package.
- The current catalog does not provide cryptographic signatures or authenticated distribution. A checksum alone detects accidental changes but does not establish publisher identity.
- Restrict file access at OS level and do not expose the local registry server publicly without authentication, TLS and a security review.
- Never treat model-generated interpretations as verified calibration values. Preserve raw bytes, offsets and ambiguity in reports.

## 11. Current scope and upstream preservation note

This archive is an additive reconstructed baseline, not a byte-for-byte clone of the live GitHub repository. It includes the captured Toyota read-only inspector and its 22 profile records. It does not contain the original Toyota BIN modification/tuning source that was not available in the captured source tree. Do not use this package as a replacement for that missing editing source, and do not claim it modifies Toyota BIN files.

## 12. Troubleshooting

| Symptom | Check |
|---|---|
| Agent does not list ECU SOFT tools | Confirm MCP support, correct stdio transport, absolute Python/script paths, working directory and MCP dependency installation. Reload the MCP connection. |
| `No module named mcp` | Run `python -m pip install -r requirements-mcp.txt` using the same Python executable configured in the agent. |
| Plugin directory not found | Keep the package directory structure intact; do not move `plugin_host.py` away from `plugins/` and `registry/`. |
| BIN path not found | Ensure the path is visible to the account/process running MCP; container paths differ from host paths. |
| Registry API unavailable | Start `python -m ecusoft_registry.server`; check port 8765 and `GET /health`. |
| REST client reports no offline snapshot | Connect once to the catalog API to create the configured cache file, or provide a valid catalog snapshot. |

## 13. Verification checklist

- [ ] `python tools/validate_plugins.py` completes successfully.
- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] HTTP `/health` returns `status: ok`.
- [ ] The agent lists all five Toyota tools through MCP.
- [ ] A real BIN inspection succeeds on a test copy.
- [ ] The original BIN SHA-256 before and after inspection is identical.
- [ ] No claim of remote execution, universal-agent compatibility or Toyota BIN modification is made unless separately implemented and tested.
