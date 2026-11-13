# ECU SOFT Tools — Dynamic MCP Toolkit

Official ECU SOFT distribution hub for local Desktop MCP and the integrated Watcher plugin.

## Recommended desktop release: v0.4.1

[Download MCPB v0.4.1](ECU-SOFT-Tools-Local-MCP-v0.4.1.mcpb) · [SHA-256 checksum](SHA256SUMS-v0.4.1.txt) · [Desktop setup guide](ECU-SOFT-TOOLS-LOCAL-MCP.md)

**Install the Desktop MCPB once.** Compatible new tools appear in `tools/list` after catalog synchronization, without rebuilding or reinstalling the bundle. The server exposes each capability as an independent MCP command, plus six backwards-compatible management commands.

The current public catalog contains **5 plugins, 31 capabilities and 37 MCP tools**.

| Plugin | Capabilities | Executable operations |
| --- | ---: | --- |
| IVECO Suite Pro | 23 | 14 inspections and 9 candidate edits |
| Toyota BIN Inspector | 5 | Publisher-defined read operations |
| Binary Inspector | 1 | Read-only metadata inspection |
| ECU SOFT File Integrity | 1 | Read-only file SHA-256 |
| ECU SOFT File Audit Report | 1 | Create a new JSON checksum report (write) |

### Live post-install proof: November 13, 2026

After v0.4.1 was released, a fifth independent plugin named **ECU SOFT File Audit Report** was added on GitHub. Watcher built-in v0.4.1, with source and MCPB unchanged, began with 35 offline MCP commands and **automatically refreshed to 37** in a clean test account. No explicit sync command was made. The new ecusoft.file_audit_report tool executed inside Docker and created a verified JSON artifact without altering the original synthetic file.

### Verified functionality

- **Dynamic discovery:** After the v0.4.0 MCPB was built, the `ecusoft.file_sha256` tool was published on GitHub. The unmodified installed bundle discovered it and executed it, receiving `notifications/tools/list_changed`, without any reinstall.
- **General read/write dispatch:** In v0.4.1, both `mode=read` and `mode=write` use the manifest-defined Python entry point. The dispatcher is not hard-coded to IVECO. A new tool requires a unique capability ID, `plugin.json`, typed inputs and an available, verifiable engine.
- **Actual candidate creation:** A clean v0.4.1 MCPB install downloaded the public IVECO engine, inspected a synthetic VCM file, generated a new speed Candidate, and verified that the original BIN remained byte-for-byte unchanged.
- **Updates:** Automatic catalog checks run every five minutes after MCP initialization. `ecusoft_sync` forces a refresh. Some hosts handle `tools/list_changed` automatically; other hosts may require reconnecting or refreshing the tool list, **not reinstalling the bundle**.

### Write actions and safety

The nine IVECO candidate-edit operations are **enabled** in v0.4.1. They require a supported software profile and an explicit target for the generated Candidate, not direct programming of an ECU. The publisher's code rejects overwriting the source file.

Standalone desktop execution is disabled by default until the operator enables local Python execution in the host. Individual calls use `approve_code_execution`; IVECO's Candidate output also uses `approved=true` and a new `output_path`. The MCP host should enforce actual user consent—those Boolean parameters alone do not prove consent. **Standalone Python execution is not an OS security sandbox** and inherits the local user's privileges.

### Watcher installation — already built in

**Watcher bundles ECU SOFT Tools as a built-in plugin. You do not manually install or connect a second MCPB.** Watcher built-in v0.4.1 supports general read/write execution and runs the tools in an isolated Docker container with the conversation's source files mounted read-only. Produced files appear in a separate `outputs/ecusoft/` folder, with paths and checksums returned to the provider.

The standalone desktop package and Watcher's built-in integration are separate distribution paths. Neither a GitHub catalog update nor a desktop MCPB upload silently replaces the embedded Watcher runtime.

### Transport and compatibility

This repository distributes **local stdio MCPB** packages. Any Desktop AI host that supports compatible MCP tool registration may use the integration; compatibility cannot be guaranteed for every vendor or client. Browser/cloud AI agents need the separate HTTPS Remote MCP / REST gateway planned for a VPS, which is **not yet publicly deployed**.

Source verification uses pinned GitHub blobs and SHA-256 integrity metadata. The downloadable IVECO executable ZIP-like archive is extractable by recipients; its original authoring repository remains private. GitHub rate limits may temporarily delay synchronization.

## العربية

**الإصدار الموصى به للـDesktop هو v0.4.1.** تثبته مرة واحدة، ويعرض الأدوات الجديدة بشكل ديناميكي عند تحديث الفهرس. وظائف `read` و`write` مدعومة، بما فيها 14 وظيفة فحص و9 وظائف Candidate في IVECO. كل Candidate يُحفظ كملف جديد، من غير تغيير الملف الأصلي.

**في Watcher الإضافة أساسية ومدمجة مع البرنامج**؛ لا تحتاج تثبيت MCPB أو توصيل Plugin ثانية. Watcher v0.4.1 يشغّل الوظائف داخل Docker مع فصل ملفات الإدخال عن ملفات النتائج.

التنفيذ على أجهزة Desktop خارج Watcher يحتاج تفعيل تشغيل Python، والموافقة على التعديل حسب طريقة العميل. بعض الـProviders قد تحتاج Refresh لإظهار الأدوات الجديدة. مسار HTTPS العام ينتظر تجهيز الـVPS.

© ECU SOFT
