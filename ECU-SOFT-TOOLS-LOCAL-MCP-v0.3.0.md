# ECU SOFT Tools — Local MCP v0.3.0

**Local Python MCP/stdio · Windows / Linux / macOS · Free preview**

Public GitHub catalog: https://github.com/infoecusoft-create/ECU-SOFT-AGENT-PLUGINS

## Public catalog, private original source

The public repository contains capability descriptions, setup guides and reviewed downloadable MCPB releases. Original engineering source is stored in the PRIVATE ECU-SOFT-PRIVATE-TOOLS repository.

**The MCPB deliberately contains its own local copies of executable tools**, so users can run them without cloning a public Python source repository. Anyone who downloads the MCPB can inspect its bundled code. This is intentional and does NOT make the private GitHub repository accessible.

Live GitHub synchronization updates only the **public tool manifests**. If a new capability or engine version is announced but is not included in the installed MCPB, update your MCPB before executing it. Existing local engines can work offline using the bundled catalog.

## Included engines and capabilities

- **Binary Inspector:** 1 read-only metadata operation (size and SHA-256).
- **Toyota BIN Inspector:** 5 read-only operations (identification, BIN, speed, RPM, cut-off).
- **IVECO Suite Pro:** 23 operations (14 read-only, 9 candidate edits), based on IVECO Suite Pro 3.6.1.

Total **29 discoverable capabilities**, 20 read-only and 9 candidate-file operations.

IVECO VCM: 8 source-defined families (WP6, WP7, WP8, WP8.55, WP9, WP10 rel61, WP10 rel75, legacy VCM3). Recognized VCM firmware can support speed, fan temperature, calibration, ABS/EBS identification and source-qualified candidate edits. Bosch **EDC17CV41** and **EDC7UC31** support DTC and System OFF operations on validated software variants. EDC7UC31 has a source-defined speed candidate range of 40–160 km/h. In **EDC17CV41**, Switches OFF is enabled by default for explicit System OFF requests involving AdBlue, DPF or EGR. Incomplete extra-layer verification prevents saving a candidate.

These are **source-defined** families and catalog functions, not claims of verified support for every firmware revision. Only authorized and structurally verified firmware can be processed. No vehicle is flashed and no original BIN is overwritten.

## Install and connect

### Watcher Eye
1. Download ECU-SOFT-Tools-Local-MCP-v0.3.0.mcpb.
2. Plugins → Add → Install MCPB bundle → Choose File → Preview.
3. Review the Python command and keep Allow local Python tool execution **false** for the first catalog-only test.
4. Install → Use in chat → ask the agent to call ecusoft_list_tools.
5. Report catalog.source, warnings and the discovered IVECO tool IDs. A v0.2.x installation may require replacement with v0.3.0.

### Claude Desktop
On supported versions: Settings → Desktop app → Extensions → Advanced settings → Install Extension… and select the MCPB. Review any requested local execution permissions.

### Codex CLI, Claude Code, OpenCode and other stdio clients
Extract the MCPB (ZIP-format) to a fixed folder:

~~~bash
mkdir -p ~/ecu-soft-tools
python3 -m zipfile -e ECU-SOFT-Tools-Local-MCP-v0.3.0.mcpb ~/ecu-soft-tools
~~~

Then register the local MCP command: python3 /absolute/path/to/ecu-soft-tools/runtime/mcp_server.py

Codex CLI:

~~~bash
codex mcp add ecusoft -- python3 /absolute/path/to/ecu-soft-tools/runtime/mcp_server.py
~~~

Claude Code:

~~~bash
claude mcp add --transport stdio --scope user ecusoft -- python3 /absolute/path/to/ecu-soft-tools/runtime/mcp_server.py
~~~

OpenCode configuration:

~~~json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "ecusoft": {
      "type": "local",
      "command": ["python3", "/absolute/path/to/ecu-soft-tools/runtime/mcp_server.py"],
      "enabled": true
    }
  }
}
~~~

Windows: use python or absolute python.exe path instead of python3.

**Ollama** runs the model; you still need an MCP-compatible agent using that model (such as OpenCode with an Ollama provider). **ChatGPT Web/Claude Web** cannot directly run a local stdio MCPB. There is no public hosted MCP endpoint.

## Local permission gates

- **Catalog-only:** default. Python code execution disabled.
- **Read and candidate preview execution:** host sets ECUSOFT_ALLOW_LOCAL_EXECUTION=1 AND each execution call includes approve_code_execution=true.
- **Actual candidate file creation:** host also sets ECUSOFT_ALLOW_CANDIDATE_WRITES=1 AND the request explicitly includes approved=true and a NEW output_path. No original overwrite.
- **Not sandboxed:** local Python executes with the operating system account's permissions. Restrict OS access and review code before enabling.
- No license tokens, cloud credentials or private GitHub API keys are in this distribution.

Available MCP tools: ecusoft_list_tools, ecusoft_get_tool, ecusoft_sync, ecusoft_run_local; optional GitHub Actions tools remain disabled unless separately configured.

**Example first test:** "Use ECU SOFT Tools to call ecusoft_list_tools and identify which IVECO VCM families are in the catalog. Do not modify any files."

© ECU SOFT — local engineering toolkit for authorized use.
