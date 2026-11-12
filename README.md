# ECU SOFT — Agent Plugins

**Official ECU SOFT Python tools for local AI agents.**

### ECU SOFT Tools · Local MCP v0.2.1 (Free Preview)

[**Download local MCPB**](ECU-SOFT-Tools-Local-MCP-v0.2.1.mcpb) · [**Complete install guide (English + عربي)**](ECU-SOFT-TOOLS-LOCAL-MCP.md) · [SHA-256 verification](SHA256SUMS.txt)

ECU SOFT Tools is a **local Python MCP stdio server** that lets agents discover a growing catalog of ECU SOFT Python capabilities from this repository. The server itself runs **on the user's computer**, not in the cloud. GitHub access is used for outbound catalog synchronization and approved source downloads; cached metadata is available offline.

**Compatible installation paths:**
- **Watcher Eye:** Plugins → Add → Install MCPB bundle → Preview → Install → Use in chat. **Tested**.
- **Claude Desktop:** Settings → Desktop app → Extensions → Advanced settings → Install Extension…; select the `.mcpb`.
- **ChatGPT Desktop:** register the extracted `runtime/mcp_server.py` as a **local STDIO MCP server**, on supported desktop versions.
- **Codex CLI:** `codex mcp add ecusoft -- python3 /absolute/path/to/runtime/mcp_server.py`.
- **Claude Code:** `claude mcp add --transport stdio --scope user ecusoft -- python3 /absolute/path/to/runtime/mcp_server.py`.
- **OpenCode:** add a `type: "local"` MCP entry using `["python3", "/absolute/path/to/runtime/mcp_server.py"]`.
- **Ollama:** use an MCP-capable **agent/front end** (e.g. OpenCode with an Ollama model). Ollama alone is not the MCP client.

**Not supported:** ChatGPT Web or Claude Web running this local `.mcpb` directly; no hosted HTTPS MCP endpoint is shipped.

**Current catalog:** 2 Python plugins, 6 read-only capabilities (binary metadata plus Toyota ECU BIN inspection), with dynamic additions from GitHub. The MCP server exposes `ecusoft_list_tools`, `ecusoft_get_tool`, `ecusoft_sync`, `ecusoft_run_local` and two optional, separately configured GitHub Actions functions.

**Safety:** downloaded Python execution is **disabled by default** and requires explicit permission per call if later enabled. Local Python code execution is **not a sandbox**. The package is currently **free**, without subscription billing.

For prerequisites, exact setup instructions, Windows paths, diagnostics, privacy and limitations, **read the [complete local MCP guide](ECU-SOFT-TOOLS-LOCAL-MCP.md)**.

---

## Repository documentation

- [Agent integration guide](AGENT_INTEGRATION_GUIDE.md)
- [MCP reference](MCP.md)
- [OpenCode setup](OPENCODE.md)
- [Watcher Eye setup](WATCHER_EYE.md)
- [REST discovery and Python host](REST_AND_PYTHON.md)
- [Offline mode and security](OFFLINE_AND_SECURITY.md)
- [Contributor documentation](CONTRIBUTING.md)

**Publisher:** ECU SOFT · Local-first AI tools.
