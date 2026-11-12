# ECU SOFT Tools

**Local MCP tools for AI agents · ECU SOFT · Free preview**

The public repository is the **official documentation, capability catalog and MCPB download center** for ECU SOFT Tools. Original engineering source and internal tests live in a separate **private** repository. The downloadable MCPB includes the local execution code intended for end users; it is an inspectable archive.

## Latest local MCP release — v0.3.0

[**Download ECU SOFT Tools v0.3.0 (.mcpb)**](ECU-SOFT-Tools-Local-MCP-v0.3.0.mcpb)

[**Install and usage instructions**](ECU-SOFT-TOOLS-LOCAL-MCP-v0.3.0.md) · [SHA-256 verification](SHA256SUMS-v0.3.0.txt)

The distribution contains **3 local engines and 29 discoverable capabilities**:

| Tool | Capabilities | Functions |
| --- | ---: | --- |
| **IVECO Suite Pro** | 23 | 8 source-defined VCM profiles, speed and fan-temperature inspection, calibration and ABS/EBS checks, Bosch EDC17CV41 and EDC7UC31 DTC and System OFF functions. Nine candidate edits are approval-gated. |
| **Toyota BIN Inspector** | 5 | Read-only identification, BIN metadata, speed, RPM and cut-off observations |
| **Binary Inspector** | 1 | Read-only file metadata and SHA-256 |

**IVECO Suite Pro**: on EDC17CV41 System OFF, the additional **Switches OFF** layer defaults to ON for eligible AdBlue, DPF and EGR requests. An incomplete structural verification blocks saving the candidate. No direct ECU flashing, no source BIN overwrite.

**Catalog-only GitHub access:** Watcher or any compatible MCP agent can discover manifests under plugins/; executable Python engines are included in the MCPB. A new engine version requires an updated MCPB, not a public source-tree checkout. A public manifest alone does not grant execution authorization.

## How to connect

- **Watcher Eye:** Plugins → Add → Install MCPB bundle → Preview → Install → Use in chat
- **Claude Desktop:** On compatible versions, import the MCPB as a local desktop extension
- **Codex CLI / Claude Code / OpenCode:** Extract the MCPB and register the local stdio command using Python and the absolute runtime/mcp_server.py path
- **Ollama:** Needs an MCP-capable agent/front end to connect the local model to these tools
- **ChatGPT Web / Claude Web:** Cannot directly run this local stdio MCPB; there is no public hosted MCP URL

See the **[full guide](ECU-SOFT-TOOLS-LOCAL-MCP-v0.3.0.md)** for exact commands, Windows support and the permission controls.

## Public / private policy

**Public:** README, descriptive plugin.json manifests, user documentation, reviewed distribution bundles and checksums.

**Private:** original Python engineering repositories, source development, proprietary templates, internal tests and release artifacts. Do not commit access tokens or user firmware.

**Safety:** local code execution is off by default and requires explicit per-call approval. Candidate file creation requires a second host-level opt-in, an approved request, and a new output path; it is not a sandbox.

**Transition:** older public Python source paths for Toyota/Binary are temporarily retained so v0.2.x clients do not fail during migration. They are scheduled for removal only after the local bundled v0.3.0 client has been adopted. Historical commits/clones cannot be made private by deleting files.

## بالعربية

**ECU SOFT Tools** بتعرض إمكانيات الأدوات على GitHub العام، وملف **MCPB** قابل للتنزيل. أما السورس الأصلي للإنتاج فهو محفوظ في مستودع **Private**. حزمة MCPB نفسها تحتوي على نسخة تشغيل محلية من الأدوات، وده مقصود. أحدث نسخة v0.3.0 بتضم **IVECO Suite Pro**، وأدوات Toyota وBinary Inspector. التشغيل الفعلي أو تعديل BIN بيحتاج موافقة وصلاحيات إضافية؛ مجرد اكتشاف الأداة لا يعدّل أي ملف.

© ECU SOFT · All rights reserved for proprietary tool engines; public connector components may carry separate licenses.
