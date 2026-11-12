# ECU SOFT Tools — Local MCP

**Official ECU SOFT public catalog and MCP installer.**

## Recommended working distribution: v0.2.1 (dynamic)

[Download ECU SOFT Tools MCPB v0.2.1](ECU-SOFT-Tools-Local-MCP-v0.2.1.mcpb) · [Installation guide](ECU-SOFT-TOOLS-LOCAL-MCP.md) · [SHA-256](SHA256SUMS.txt)

**The original rule remains: install the MCPB once.** It refreshes capability definitions from the official GitHub catalog. For tools whose executable sources are available through its configured downloader, the client fetches and verifies each tool as needed. Adding a compatible public tool does not require rebuilding the MCPB.

**IMPORTANT CORRECTION (2026-11-13): v0.3.0 is NOT the recommended release.** Its bundled-engine design accidentally made new executable tools depend on upgrading the MCPB, contrary to the original dynamic-update requirement. Do not migrate to v0.3.0 based on the former instructions. Existing users of the dynamic MCPB should not replace their installation for this release.

## Current tool catalog

- **Toyota BIN Inspector:** 5 read-only catalog capabilities; source currently available through the original public downloader.
- **Binary Inspector:** 1 read-only catalog capability; source currently available through the original public downloader.
- **IVECO Suite Pro:** 23 capabilities (14 inspection; 9 candidate-edit), with 8 source-defined VCM families and Bosch EDC17CV41/EDC7UC31 detection and analysis functions. Its manifest is listed publicly, but **the original private IVECO executable engine is not available for automatic download by v0.2.1**. Catalog discovery does **not** yet mean it can be executed. Do not promise automatic private-tool execution until an authorized distribution method is explicitly approved and tested.

**Do not confuse discovery and execution.** A manifest can appear immediately after GitHub sync while its source distribution still needs configuration. Neither the number of tools in the list nor catalog sync alone proves execution.

## Connect locally

- **Watcher Eye:** Plugins → Add → Install MCPB bundle → Preview → Install → Use in chat.
- **Compatible Claude Desktop extensions:** import the MCPB as a local extension.
- **Codex, Claude Code, OpenCode, and compatible stdio clients:** extract the MCPB into a permanent folder and register its `runtime/mcp_server.py` command with Python.
- **Ollama:** requires an MCP-compatible agent/front end; Ollama alone is a model runner.
- **ChatGPT Web / Claude Web:** cannot directly execute this local stdio MCPB.

[Full instructions](ECU-SOFT-TOOLS-LOCAL-MCP.md).

## Public catalog / private sources

The **public repository** is intended for documentation, tool manifests and the user-downloadable MCPB. The separate **private source repository** stores original engineering source. Older Toyota/Binary Python files are **still present on the public branch** because v0.2.1 dynamically downloads them. Deleting these files without a compatible source-distribution path would break existing users. Keeping sources private while supporting download-and-run of newly added tools still requires a deliberately approved executable distribution mechanism.

A user-downloadable MCPB or tool package may contain code; users who receive it can inspect it. The project does **not** claim to prevent extraction of code given to users.

### Security

Execution of downloaded Python requires host permission and per-call approval; this is **not an OS sandbox**. Candidate files must never overwrite the original BIN. No ECU flashing is implemented by the MCPB.

**Status:** Dynamic v0.2.1 remains the recommended engine. v0.3.0 is an experimental superseded bundle retained for traceability, not a required upgrade.

## بالعربية

**التصحيح:** الإصدار الموصى به حاليًا هو **MCPB v0.2.1 الديناميكي**. تثبّته مرة واحدة ويحدّث كتالوج الأدوات تلقائيًا من GitHub. نشر v0.3.0 كمحرك ثابت كان تغييرًا غير مطلوب؛ **لا تحدّث إلى v0.3.0** لهذا السبب.

أدوات Toyota وBinary القديمة عندها سورس متاح للتنزيل حسب التصميم الأصلي. تعريف **IVECO Suite Pro** ظهر في الكتالوج، لكن تشغيل سورسها الخاص تلقائيًا **ليس جاهزًا**. هنحافظ على الفصل بين Public وPrivate، وما نغيّرش طريقة التوزيع من غير قرار صريح.

© ECU SOFT
