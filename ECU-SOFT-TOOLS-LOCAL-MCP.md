# ECU SOFT Tools — Local MCP v0.2.1

**Free preview · Local Python MCP · Windows, Linux and macOS**

Official repository: https://github.com/infoecusoft-create/ECU-SOFT-AGENT-PLUGINS

**Download:** [ECU-SOFT-Tools-Local-MCP-v0.2.1.mcpb](ECU-SOFT-Tools-Local-MCP-v0.2.1.mcpb)

## What does it do?

ECU SOFT Tools is a locally launched MCP server for AI agents. It discovers tools from the official GitHub repository and exposes their metadata, inputs and read-only execution methods. At release: 2 Python plugins and 6 capabilities (binary metadata and Toyota BIN analysis). The GitHub catalog can grow without replacing the MCP server.

**IMPORTANT: this is local stdio MCP, not a hosted cloud connector.** Your agent launches Python on the user's own computer. There is no HTTPS remote MCP server URL. Live catalog refresh needs outbound Internet to GitHub; offline fallback metadata is bundled. Files are not uploaded merely by listing tools.

Six MCP functions: `ecusoft_list_tools`, `ecusoft_get_tool`, `ecusoft_sync`, `ecusoft_run_local`, `ecusoft_run_github` and `ecusoft_remote_result`. The optional GitHub Actions functions require a separately configured workflow and credentials; they are **not enabled by default** and are not needed for local use.

**Security:** `allow_local_execution=false` by default. Catalog lookup and sync work without executing downloaded Python. Running downloaded code requires opting in and approving the individual tool. This is **not an OS sandbox**. Review third-party code and file access permissions before enabling execution.

## Requirements

- Python 3.10+ (`python3` on Linux/macOS; `python` on Windows).
- Local desktop agent with **MCP stdio** support.
- Internet to refresh catalog (cached/seed catalog usable offline).

## Installation by application

### Watcher Eye — verified

1. Download the `.mcpb` file without extracting.
2. **Plugins → Add → Install MCPB bundle → Choose File → Preview**.
3. Keep **Allow local Python tool execution = false** at first.
4. **Install → Use in chat** next to ECU SOFT Tools.
5. Ask: "Call ecusoft_list_tools and show catalog.source, catalog.commit, any warning, and all tool IDs. Do not run Python tools."

Actual Watcher test confirmed local MCP tool invocation and GitHub live catalog sync after the v0.2.1 fix.

### Claude Desktop — custom desktop extension

**Settings → Desktop app → Manage (Extensions) → Advanced settings → Install Extension…** and select the `.mcpb` file. Review and approve local execution; restart if tools don't appear. This is **not** the remote connectors URL screen.

Official instructions: https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop

### Other stdio agents: extract the MCPB first

The MCPB is a ZIP-format bundle. Extract it once to a permanent location:

```bash
mkdir -p ~/ecu-soft-tools
python3 -m zipfile -e ECU-SOFT-Tools-Local-MCP-v0.2.1.mcpb ~/ecu-soft-tools
```

Local MCP command:

```bash
python3 /absolute/path/to/ecu-soft-tools/runtime/mcp_server.py
```

The agent (MCP client) starts the process; it is not an ordinary interactive Python chat.

**ChatGPT Desktop** (supported desktop setup): Settings → MCP servers → Add server → **STDIO**. Set command `python3` and argument to the absolute `runtime/mcp_server.py` path; save and restart, inspect `/mcp`. **ChatGPT Web/mobile cannot directly run this local MCPB.**

Docs: https://learn.chatgpt.com/docs/extend/mcp

**Codex CLI:**

```bash
codex mcp add ecusoft -- python3 /absolute/path/to/ecu-soft-tools/runtime/mcp_server.py
codex mcp list
```

Equivalent `~/.codex/config.toml`:

```toml
[mcp_servers.ecusoft]
command = "python3"
args = ["/absolute/path/to/ecu-soft-tools/runtime/mcp_server.py"]
```

**Claude Code:**

```bash
claude mcp add --transport stdio --scope user ecusoft -- python3 /absolute/path/to/ecu-soft-tools/runtime/mcp_server.py
```

Use `/mcp` in Claude Code to inspect it. See https://support.claude.com/en/articles/14554922-claude-code-user-faq

**OpenCode:** add to `opencode.json`, then restart:

```json
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
```

Official docs: https://opencode.ai/docs/mcp-servers/

**Ollama / local LLMs:** Ollama is a **model runner**, not the MCP client that installs this extension. Use an MCP-capable agent such as OpenCode configured with an Ollama model, then register ECU SOFT as local MCP there. `ollama run` alone does not expose these tools. Open WebUI may need an stdio-to-HTTP adapter: https://docs.openwebui.com/features/extensibility/mcp/

**Windows:** substitute `python` for `python3` and an absolute Windows path, e.g. `C:\ECUSoft\ecu-soft-tools\runtime\mcp_server.py`. The MCPB manifest includes a Windows Python command override.

## Verify and troubleshoot

Ask the model to invoke `ecusoft_list_tools`; inspect `catalog.source`. `github-manifests` means the live GitHub catalog was successfully loaded; `offline`/`seed` means cached data and may include a warning. At time of publication there are 2 indexed plugins with 6 capabilities, but the number may grow.

A successful installation alone does not prove live GitHub sync. If tools are missing, inspect your agent's MCP server log, check the Python executable/path, and restart the agent. Do not switch a local stdio command into a remote MCP URL field.

The product is **free preview** now; subscriptions are not enabled. Execution stays on the user's device by default; optional GitHub Actions (if separately set up) is a distinct remote mode.

## دليل الاستخدام بالعربية

**ECU SOFT Tools خادم MCP بيشتغل محليًا على جهازك، مش على سيرفر سحابي.** بيتصل بـGitHub لتحديث قائمة الأدوات، لكن تنفيذ Python المحلي مقفول افتراضيًا لحد موافقة المستخدم.

- **Watcher:** Plugins → Add → Install MCPB bundle → Preview → Install → Use in chat.
- **Claude Desktop:** Settings → Desktop app → Extensions → Advanced settings → Install Extension… ثم اختار ملف `.mcpb`.
- **ChatGPT Desktop / Codex / Claude Code / OpenCode:** فك الحزمة في مجلد ثابت واربط `python3 /absolute/path/runtime/mcp_server.py` بصفة **local stdio MCP**.
- **Ollama:** لازم Agent يدعم MCP ويشغّل موديل Ollama، مش Ollama وحده.
- **ChatGPT Web أو Claude Web:** مش بيشغّلوا هذا الخادم المحلي مباشرة.
- **أول اختبار:** اطلب `ecusoft_list_tools` وتأكد من `catalog.source`؛ ما تشغّلش ملفات BIN في اختبار التثبيت.

© ECU SOFT · v0.2.1
