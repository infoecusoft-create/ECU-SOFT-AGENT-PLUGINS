# ECU SOFT Tools — Local MCP Setup (v0.4.1)

**Current desktop package:** [ECU-SOFT-Tools-Local-MCP-v0.4.1.mcpb](ECU-SOFT-Tools-Local-MCP-v0.4.1.mcpb)  
**Integrity:** [SHA256SUMS-v0.4.1.txt](SHA256SUMS-v0.4.1.txt)  
**Repository:** https://github.com/infoecusoft-create/ECU-SOFT-AGENT-PLUGINS

ECU SOFT Tools provides a local, dynamically extensible MCP server. It exposes one independently callable MCP tool for each registered capability in the GitHub catalog. You install the desktop bundle once and new compatible capabilities are discovered by synchronization rather than adding another bundle per tool.

## Requirements

- Python 3.10 or newer installed on the device that runs the MCP server.
- A Desktop AI agent with stdio MCP support or compatible MCPB extension support.
- Outbound internet to access the public GitHub catalog and download newly published engine packages. Previously verified/cached tools can be available offline.
- Explicit operator permission for local publisher-code execution.

**This is a local stdio MCP server, not a public HTTPS Remote MCP URL.** A VPS-based remote MCP endpoint is a separate deployment.

## Watcher — already built in

ECU SOFT Tools comes installed as a **built-in Watcher plugin**. Do not manually add another ECU SOFT MCPB or create a duplicate connection.

Watcher built-in **v0.4.1** exposes compatible tools through the ordinary provider tool catalog, supports read/write modes, and runs publisher code in a disposable Docker container.

- Conversation source files are mounted read-only.
- The output location for write operations is a separate per-operation folder, under `outputs/ecusoft/`, mounted at `/results` in the container.
- The provider receives candidate file paths and SHA-256 digests in the tool result.
- No direct ECU flashing. Invalid or unsupported ECU profiles do not generate candidates.

When a new plugin manifest appears, the built-in catalog refreshes. The active provider may need the next tool catalog refresh to see it.

## Other compatible desktop agents

Some Desktop apps support importing an MCPB directly through their extension or local MCP settings. Import the `.mcpb` package once, follow the app's confirmation prompts, and verify that the ECU SOFT tools appear.

If the host only supports explicit stdio commands, extract the MCPB (it is ZIP-format) into a persistent directory:

```bash
mkdir -p ~/ecu-soft-tools
python3 -m zipfile -e ECU-SOFT-Tools-Local-MCP-v0.4.1.mcpb ~/ecu-soft-tools
```

Then register a local MCP server with executable `python3` and argument:

```text
/absolute/path/to/ecu-soft-tools/runtime/mcp_server.py
```

On Windows, use a suitable Python executable such as `python.exe` with the absolute Windows path to the extracted `runtime\mcp_server.py` file. Follow the host application's own MCP setup instructions—support and exact menus differ between vendors.

A model runner that does not implement MCP directly needs an MCP-capable agent frontend.

## Discovering new tools

The server responds to the standard MCP `tools/list` call. Each plugin capability from `plugins/**/plugin.json` appears by its unique tool ID (for example, `iveco.list_supported_systems` or `ecusoft.file_sha256`).

The original six `ecusoft_*` management commands remain for backward compatibility:

- `ecusoft_list_tools`, `ecusoft_get_tool`, `ecusoft_sync`
- `ecusoft_run_local`, `ecusoft_run_github`, `ecusoft_remote_result`

The optional GitHub Actions commands require separately configured GitHub workflow credentials. Local execution does not depend on them.

The server checks the GitHub catalog every five minutes after MCP initialization. Call `ecusoft_sync` to check immediately. Compatible hosts receive `notifications/tools/list_changed`; other hosts may need **Refresh tools** or **Reconnect**. No MCPB reinstall is needed merely because a new compatible tool was added.

A standalone Python file does not automatically become a safe, callable tool: each plugin needs a valid `plugin.json` with an ID, entry point, typed input schema, operation mode, and verified executable distribution.

## Reading and editing files

The Desktop MCPB v0.4.1 supports both `read` and `write` capability modes. New live example: ecusoft.file_audit_report is a separately published write capability that reads an input file and writes a SHA-256/size JSON report to a new output file. Watcher discovered it automatically and generated an artifact without source edits or another MCPB install.

For candidate creation with the IVECO tool, a typical call requires:

```json
{
  "file_path": "/absolute/path/to/original.bin",
  "speed_kmh": 120,
  "approved": true,
  "output_path": "/absolute/path/to/new_candidate.bin",
  "approve_code_execution": true
}
```

This example describes parameters, **not a request to modify a real vehicle**. The particular operation succeeds only on a compatible, verified software profile. The candidate must be a new file; the original must not be overwritten.

Local execution is disabled by default until enabled in the host settings. The host should enforce actual user approval for each sensitive call. Boolean inputs alone are not proof of consent. **Standalone desktop Python execution is not sandboxed at operating-system level** and runs with the local user's permissions.

Watcher is different: it includes the isolated Docker filesystem routing described above. The standalone Desktop MCPB does not gain the Watcher sandbox automatically.

## Verification and troubleshooting

After installation, ask the agent to list all ECU SOFT tool IDs. The current catalog has **6 plugins, 32 capabilities and 38 MCP commands** (including the management commands).

If a tool is missing, request `ecusoft_sync`; inspect the server logs for any GitHub rate limit, stale cache, Python invocation or package verification error. Some clients need a manual catalog refresh. An unsupported binary profile may correctly reject a requested Candidate operation.

Use a **synthetic test file** to check file creation before working with any genuine ECU dump. Check the candidate size, checksum, output path and the original source digest.

## بالعربي

- **Watcher:** ECU SOFT موجودة فيه كإضافة Built-in أساسية. مش محتاج تثبيت MCPB أو توصيلها مرة تانية.
- **أي Desktop Agent متوافق:** حمّل v0.4.1 وثبّته مرة واحدة، وبعد كده الأدوات الجديدة تتسجل عن طريق تحديث الفهرس.
- **الوظائف:** القراءة والتعديل مدعومان. أدوات IVECO الـ23 بتظهر للـProvider، والتسع وظائف الخاصة بالتعديل ممكن تنشئ Candidate مع ملف BIN متوافق.
- **الملف الأصلي:** لا يتم استبداله. Watcher يحفظ النتيجة في `outputs/ecusoft/` داخل مساحة المحادثة.
- **المزامنة:** عند بعض البرامج تحتاج Refresh أو Reconnect لإظهار أداة جديدة، من غير إعادة تثبيت.
- **الأونلاين:** Remote MCP عبر HTTPS يحتاج تشغيل بوابة VPS منفصلة؛ مش موجود كعنوان عام لحد دلوقتي.

© ECU SOFT — v0.4.1


### Verified general output attachments

The independently published ecusoft.byte_entropy_report tool was discovered and downloaded automatically by Watcher. Its output JSON appeared in the normal authenticated artifact list, and download returned exact bytes in the isolated integration test. Original input remained unchanged. Prior chat replies containing only old output paths are not retroactively converted into attachments; new executions produce native downloadable files.
