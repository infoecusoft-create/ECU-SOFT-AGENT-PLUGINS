# ECU SOFT Tools — Local MCP

**Official ECU SOFT public catalog and MCP installer.**

## Recommended working distribution: v0.2.1 (dynamic)

[Download ECU SOFT Tools MCPB v0.2.1](ECU-SOFT-Tools-Local-MCP-v0.2.1.mcpb) · [Installation guide](ECU-SOFT-TOOLS-LOCAL-MCP.md) · [SHA-256](SHA256SUMS.txt)

**The original rule remains: install the MCPB once.** It refreshes capability definitions from the official GitHub catalog. For tools whose executable sources are available through its configured downloader, the client fetches and verifies each tool as needed. Adding a compatible public tool does not require rebuilding the MCPB.


## Current tool catalog

- **Toyota BIN Inspector:** 5 read-only catalog capabilities; source currently available through the original public downloader.
- **Binary Inspector:** 1 read-only catalog capability; source currently available through the original public downloader.
- **IVECO Suite Pro:** 23 catalog capabilities (14 inspection and 9 candidate-edit). The 14 read actions now download and run through the unchanged dynamic MCPB using a SHA-256-verified binary archive and minimal loader. The nine candidate-edit actions remain blocked by the v0.2.1 execution policy, pending a separate explicitly approved write-permission implementation.

**Do not confuse discovery and execution.** A manifest can appear immediately after GitHub sync while its source distribution still needs configuration. Neither the number of tools in the list nor catalog sync alone proves execution.

## Connect locally

- **Watcher Eye:** Plugins → Add → Install MCPB bundle → Preview → Install → Use in chat.
- **Compatible Claude Desktop extensions:** import the MCPB as a local extension.
- **Codex, Claude Code, OpenCode, and compatible stdio clients:** extract the MCPB into a permanent folder and register its `runtime/mcp_server.py` command with Python.
- **Ollama:** requires an MCP-compatible agent/front end; Ollama alone is a model runner.
- **ChatGPT Web / Claude Web:** cannot directly execute this local stdio MCPB.

[Full instructions](ECU-SOFT-TOOLS-LOCAL-MCP.md).

## Public catalog / private sources

The **public repository** is intended for documentation, tool manifests and the user-downloadable MCPB. The separate **private source repository** stores original engineering source. Older Toyota/Binary Python files are **still present on the public branch** because v0.2.1 dynamically downloads them. Deleting these files without a compatible source-distribution path would break existing users. IVECO now demonstrates the approved dynamic distribution pattern: a minimal public verification adapter plus a versioned, hash-pinned binary archive; the original engineering source remains in the private repository. The distributed archive can be extracted by recipients and is not represented as secret.

A user-downloadable MCPB or tool package may contain code; users who receive it can inspect it. The project does **not** claim to prevent extraction of code given to users.

### Security

Execution of downloaded Python requires host permission and per-call approval; this is **not an OS sandbox**. Candidate files must never overwrite the original BIN. No ECU flashing is implemented by the MCPB.


## بالعربية

**الإصدار الموصى به حاليًا هو MCPB v0.2.1 الديناميكي.** ثبّته مرة واحدة، ويقدر يحدّث كتالوج الأدوات من GitHub. اكتشاف أداة جديدة لا يضمن تشغيلها من غير وجود مصدر تنفيذي متاح.

أدوات Toyota وBinary متاحة للتنزيل والتنفيذ وفق صلاحيات المضيف. **IVECO Suite Pro اشتغلت فعلًا** من محرك مضغوط ومثبت البصمة ومن غير تحديث الـMCPB: الـ14 وظيفة فحص متاحة، لكن وظائف إنشاء ملفات Candidate التسع ما زالت محجوبة بسياسة التنفيذ الحالية. التشغيل يتطلب موافقة المستخدم وتفعيل السماح بالتنفيذ المحلي. السورس الأصلي محفوظ في المستودع الخاص.

© ECU SOFT
