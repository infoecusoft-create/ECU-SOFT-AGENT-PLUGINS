# ECU SOFT Tools — Dynamic MCP Toolkit

**Official ECU SOFT distribution, desktop integration and engineering tool catalog.**

## Recommended release — v0.4.0

[Download ECU SOFT Tools MCPB v0.4.0](ECU-SOFT-Tools-Local-MCP-v0.4.0.mcpb) · [SHA-256 checksum](SHA256SUMS-v0.4.0.txt) · [Installation guide](ECU-SOFT-TOOLS-LOCAL-MCP.md)

**Install once; add compatible tools later without rebuilding the MCPB.** Unlike the previous bridge-only versions, v0.4.0 returns each catalog capability as a distinct MCP tool in `tools/list`, alongside six backward-compatible management commands.

The official public catalog currently contains **4 plugins, 30 capabilities**, and the desktop server exposes **36 tools in total**.

### Verified dynamic-update proof

After v0.4.0 was **built and published**, we added `ecusoft.file_sha256` to the GitHub catalog. A fresh extraction of the **exact same, unchanged MCPB archive** discovered it as an additional tool, emitted `notifications/tools/list_changed`, downloaded its verified Python engine from GitHub, and executed it against a temporary fixture with correct SHA-256 and no file mutation. The tool count increased from **35 to 36** without rebuilding the bundle.

The server polls the catalog at five-minute intervals after MCP initialization. A compatible client can force an immediate refresh with `ecusoft_sync`. Some MCP clients process `tools/list_changed` automatically; others may need manual refresh or reconnection, **not an MCPB reinstall**.

## Current public catalog

| Plugin | Capabilities | Desktop execution |
| --- | ---: | --- |
| Toyota BIN Inspector | 5 | Read-only; opt-in |
| Binary Inspector | 1 | Read-only; opt-in |
| IVECO Suite Pro | 23 | 14 read-only actions; 9 candidate-edit actions listed but **disabled** by desktop execution policy |
| ECU SOFT File Integrity | 1 | Read-only SHA-256 inspection; opt-in |

**Discovery and execution are separate.** Publishing a new compatible `plugin.json` registers its capabilities. To execute one, the corresponding versioned Python engine must be available, verified and permitted by the local host.

An arbitrary `.py` file alone is not an MCP interface: the publisher must also provide a unique tool ID, typed inputs, read/write policy, entry point and runnable distribution. The catalog never guesses how to execute unidentified code.

## Installation and compatibility

- **Watcher Eye:** Plugins → Add → Install MCPB → Preview → Install → Use in chat. Reconfigure to v0.4.0 once to gain direct dynamic tools.
- **Desktop MCP clients supporting bundles:** import the `.mcpb` as a local server.
- **Clients with stdio MCP configuration:** extract the archive into a permanent folder and launch `python3 runtime/mcp_server.py`.
- **Model runners without MCP support:** use an MCP-capable agent front end.
- **Browser/cloud agents:** local stdio MCPB cannot be connected directly; the separately planned HTTPS Remote MCP service requires a deployed VPS and authentication.

The MCPB manifest declares `tools_generated: true`; the server declares `tools.listChanged: true`. **Not every desktop host supports dynamic tools.** Hosts that lock tool inventories to a static bundle manifest, including some OS-level MCP registries, may require a different integration mode. Test each actual client instead of assuming universal compatibility.

## Safety and source distribution

Python execution is **disabled by default**. To use a read tool, the operator opts in to local execution, and the host must enforce any user-confirmation prompt. The `approve_code_execution` argument is **not by itself proof of human approval**; secure user consent depends on host policy. Downloaded publisher Python is **not OS-sandboxed**.

Source BIN files must never be overwritten. The current MCPB does not flash ECUs and does not execute the nine IVECO candidate-edit tools.

IVECO and File Integrity use versioned, SHA-256-checked executable archives and minimal public verification loaders. The original IVECO engineering source remains in a separate Private repository. End users can inspect/extract packages they download; no claim of code secrecy is made.

Public GitHub currently provides the dynamic catalog and packages. Anonymous GitHub API limits may temporarily delay refresh or new downloads; the last verified catalog is cached. Future hosting will migrate distribution/execution to the ECU SOFT VPS without changing the product's provider-neutral tool IDs.

## العربية

**الإصدار الموصى به هو v0.4.0.** بتثبته مرة واحدة؛ كل أداة جديدة بملف تعريف ومحرك تنفيذي متوافق تظهر باسمها في قائمة الـMCP من غير ما نعيد بناء الملف. جرّبنا فعليًا إضافة أداة جديدة بعد بناء الإصدار، وظهرت ونفذت على نفس النسخة. حاليًا فيه **30 وظيفة** و**6 أوامر إدارة**.

التنفيذ المحلي مقفول افتراضيًا، وأدوات تعديل ملفات Candidate التسع ما زالت محجوبة. بعض برامج الـDesktop ممكن تحتاج Refresh أو إعادة اتصال لإظهار الأدوات الجديدة، لأن توافق MCP الديناميكي بيختلف حسب البرنامج.

© ECU SOFT
