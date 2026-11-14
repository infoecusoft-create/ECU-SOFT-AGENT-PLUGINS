# ECU SOFT Tools — ChatGPT Usage & Latest-Only Publishing Guide
# دليل استخدام أدوات ECU SOFT داخل ChatGPT وسياسة آخر إصدار فقط

**ECU SOFT repositories ONLY / لمستودعات ECU SOFT فقط**  
**Verified repository cleanup:** 2026-11-14  
**PUBLIC:** https://github.com/infoecusoft-create/ECU-SOFT-AGENT-PLUGINS  
**PRIVATE:** https://github.com/infoecusoft-create/ECU-SOFT-PRIVATE-TOOLS

> This document describes the exact ECU SOFT distribution paths. It is not a generic GitHub/MCP tutorial, and it does **not** change or test Watcher.
>
> هذا الدليل لمستودعَي ECU SOFT الحاليين فقط، ولا يسمح للمُنفذ بتشغيل Watcher أو تعديل إعداداته أو اختبار أدواته.

## 1) قائمة الإصدارات المعتمدة / Approved latest releases

| Component | Where | Current version / Archive | Role |
|---|---|---|---|
| Local desktop MCP bundle | PUBLIC root | [ECU-SOFT-Tools-Local-MCP-v0.4.1.mcpb](ECU-SOFT-Tools-Local-MCP-v0.4.1.mcpb) | General, dynamically extendable stdio MCP host |
| MCP checksum | PUBLIC root | [SHA256SUMS-v0.4.1.txt](SHA256SUMS-v0.4.1.txt) | Verify downloaded bundle |
| VW PCR2.1 EGR V7 | PUBLIC | [plugin.json](plugins/vw/vw_pcr21_egr_v7/plugin.json) — v1.1.0 | Four source-backed actions, including writing |
| VW PCR2.1 DPF V6.23 | PUBLIC | [plugin.json](plugins/vw/vw_pcr21_dpf_v6_23/plugin.json) — v1.1.0 | Four source-backed actions, including writing |
| EGR source package | PRIVATE | distributions/vw_pcr21_egr_v7-1.1.0.zip | Unchanged EGR Python core + adapter |
| DPF source package | PRIVATE | distributions/vw_pcr21_dpf_v6_23-1.1.0.zip | Unchanged DPF Python core + adapter |

**Policy / السياسة:** Keep only the latest RELEASE FILE for a given product/version line on the active \`main\` branch. Do not remove independent tools merely because their original publication date is older. For every new version: publish the complete verified private archive first; update the matching public \`plugin.json\` with new archive path and SHA-256; verify; then remove superseded release packages and obsolete checksum links. Do not rewrite Git history or force-push.

**تنبيه:** حذف ملف من \`main\` لا يمحوه تلقائيًا من Git history. ويجب ألا يتم مسح أي أداة مختلفة أو أي أرشيف ما زال تعريف عام نشط يشير إليه.

## 2) Architecture / البنية الدقيقة

\`\`\`text
GitHub PUBLIC: ECU-SOFT-AGENT-PLUGINS
  ECU-SOFT-Tools-Local-MCP-v0.4.1.mcpb     # current local stdio bundle
  SHA256SUMS-v0.4.1.txt                    # exact bundle checksum
  CHATGPT_USAGE_AR_EN.md                   # this instruction
  plugins/vw/vw_pcr21_egr_v7/plugin.json   # v1.1.0 metadata
  plugins/vw/vw_pcr21_dpf_v6_23/plugin.json# v1.1.0 metadata
  plugins/...                              # other independent tools

GitHub PRIVATE: ECU-SOFT-PRIVATE-TOOLS
  distributions/vw_pcr21_egr_v7-1.1.0.zip
  distributions/vw_pcr21_dpf_v6_23-1.1.0.zip
  tools/...                                # other independent sources
\`\`\`

A public \`plugin.json\` is metadata and a resolver descriptor; it does **not** itself execute code, download a private ZIP into ChatGPT, expose private GitHub credentials, or attach a generated file. The connected MCP server/runtime must provide those execution and artifact operations.

الـ \`plugin.json\` يُظهر الوظائف للـAgent، لكنه ليس محرك تنفيذ. لا يكفي رفعه على GitHub لتمكين ChatGPT Web من تحميل سورس خاص أو إنشاء مرفق؛ لابد من MCP runtime متصل وقادر على الوصول للحزم والتحقق منها وتشغيلها وإرجاع المخرجات.

## 3) Important distinction: ChatGPT web / ChatGPT desktop / Other desktop MCP hosts

### A. ChatGPT WEB (browser) — current requirement

**You CANNOT paste the GitHub \`plugin.json\` link or upload the \`.mcpb\` as-is and assume a working remote tool.** The current v0.4.1 MCPB is a **local stdio MCP server**. ECU SOFT's public README says its dedicated HTTPS Remote MCP/REST gateway has not yet been deployed.

When an authorized ChatGPT account/workspace has custom MCP-server permissions and ECU SOFT has deployed an authorized remote HTTPS MCP service or Secure MCP Tunnel, use:

1. ChatGPT → **Plugins** → **+** → **Add custom MCP server** (if your account exposes this control).
2. Name: \`ECU SOFT Tools\`. For **Connection**, enter the **actual ECU SOFT HTTPS MCP endpoint** or the authorized Secure MCP Tunnel ID. **Do not invent a URL**; the GitHub repository URL is NOT an MCP endpoint.
3. Select the permitted authentication method. Never paste a GitHub Deploy Key or private-source credentials into the chat or public plugin metadata.
4. Review the server's permissions/security warning and create the plugin.
5. Check **discovered tools**. Verify \`vw_pcr21.egr.apply_off\` and \`vw_pcr21.dpf.apply_off\` are present and allowed for write actions.
6. Install/enable the connected plugin for the chat/workspace. Start a new chat or invoke \`@ECU SOFT Tools\`.
7. Use a safe authorized test file first; verify a real tool result, original hash preservation and downloadable output.

**Permissions caveat:** ChatGPT features and write actions vary by plan and workspace controls. Full custom MCP write/modify support is documented for eligible Business/Enterprise/Edu environments; never claim every plan can do it. Some approved workspace apps require an administrator to **Refresh** their tool/action snapshot after a new \`plugin.json\` release, even if the ECU SOFT catalog has updated automatically.

**الويب:** الرابط المطلوب في إضافة MCP هو عنوان خدمة MCP فعلي، وليس GitHub. لو الخدمة/التونل غير موجودين أو خطة المستخدم لا تدعم Write، اكتب **غير متاح** بوضوح. لا تنسب العطل إلى برنامج Python ولا تُعلن نجاح الربط من مجرد ظهور الاسم.

Official ChatGPT docs:
- https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt
- https://help.openai.com/en/articles/20001256-plugins-in-chatgpt

### B. ChatGPT DESKTOP — local-capable plugin path

ChatGPT's current plugin documentation describes support for **local MCP apps in ChatGPT Desktop** where that feature is available. A separate ChatGPT plugin wrapper or compatible local-app configuration may be required; an \`.mcpb\` from GitHub is **not guaranteed** to be directly importable as a ChatGPT plugin ZIP.

1. Install a compatible ECU SOFT local MCP integration via ChatGPT's supported Desktop/plugin workflow, following its explicit installer/configuration screens.
2. Verify the local runtime is actually running and has the correct Python executable and permissions.
3. Select/mention the installed ECU SOFT plugin in the chat.
4. Confirm its tool list; test \`ecusoft.file_sha256\` on an authorized local file.
5. If needed, refresh/reconnect to discover additional ECU SOFT tools. An independent published capability does not require rebuilding the v0.4.1 bundle, but the client must have updated its catalog and granted its permissions.

If your ChatGPT Desktop build **does not** show a supported local MCP app setup, do not claim that renaming/uploading \`.mcpb\` will fix it. Use a supported MCP-capable desktop agent or wait for the properly hosted ECU SOFT MCP endpoint.

### C. Other supported local stdio MCP clients — existing v0.4.1 path

1. Download only \`ECU-SOFT-Tools-Local-MCP-v0.4.1.mcpb\` from the PUBLIC repo.
2. Verify its SHA-256 against \`SHA256SUMS-v0.4.1.txt\`.
3. Install once in a desktop host that supports MCPB, or extract as ZIP and configure \`python3\` / absolute path to \`runtime/mcp_server.py\` for a stdio MCP client. Python 3.10+ is required by the existing ECU SOFT setup guide.
4. Give appropriate local file-system permissions and operator consent for code execution; standalone Python execution runs with local user permissions and is **not** a Watcher Docker sandbox.
5. Call \`tools/list\`. Additional published tools become discoverable via the ECU SOFT catalog. The local package's documented automatic catalog checks run every five minutes after initialization; some hosts need reconnect, tools refresh, or \`ecusoft_sync\`.
6. This Desktop installation method is **not** the same as connecting a remote ChatGPT Web custom MCP.

Existing ECU SOFT desktop documentation: [ECU-SOFT-TOOLS-LOCAL-MCP.md](ECU-SOFT-TOOLS-LOCAL-MCP.md).

## 4) Exactly how to invoke ECU SOFT tools in a connected ChatGPT chat
## طريقة الاستخدام في محادثة ChatGPT بعد نجاح الربط

**Step 0 — check connection / فحص الاتصال:** Use the chat composer plugin selector or type \`@\` and pick **ECU SOFT Tools** if installed. Ask:

> List the live ECU SOFT MCP tools available in this conversation. Show the exact IDs and read/write modes. Do not simulate tool calls or assume a GitHub file is executable.

**Step 1 — supply input / إدخال الملف:** Attach an authorized ECU BIN/ORI in the chat. Confirm the MCP server actually receives a valid \`file_path\` in its own sandbox/workspace. A path on the user's laptop is NOT automatically accessible to a cloud-connected MCP server.

**Step 2 — inspect / الفحص:**

> Use \`vw_pcr21.egr.inspect\` on the attached BIN. Report source SHA-256, size, detected family and software from the real tool response. Do not modify the original.

For DPF choose \`vw_pcr21.dpf.inspect\`. If the tool reports unsupported family/file, stop instead of guessing.

**Step 3 — preview / المعاينة:**

> Use \`vw_pcr21.egr.preview\` and return the reference match, compatibility details and whether the source ECU Forge engine accepts this exact input. No changes yet.

For DPF, use \`vw_pcr21.dpf.preview\`.

**Step 4 — write / التعديل وإنشاء ملف منفصل:**

> I authorize creating a separate candidate for a supported BIN. Use \`vw_pcr21.egr.apply_off\` with this attached file. Keep the original unchanged, write the result into the permitted results/output folder, and return the candidate as a downloadable attachment with its SHA-256 and source SHA-256. State clearly whether checksum validation is included.

For DPF, use \`vw_pcr21.dpf.apply_off\`. The published input contract is:

\`\`\`json
{
  "file_path": "string (runtime-visible path to uploaded BIN/ORI)",
  "output_path": "string? (new path if host allows)",
  "approved": "boolean? (host permission is still independently required)"
}
\`\`\`

The original source has \`apply_patch_to_file(input_path, output_path)\`; the v1.1.0 adapter exposes this as a separate-file \`apply_off\`. The original source checks reference matching and can reject unsupported binaries. The v1.1.0 public manifests have \`mode: "write"\` and permission \`filesystem.write_output_requires_approval\`.

**Step 5 — verify deliverable / استلام الناتج:** Require all of:
- Actual MCP tool invocation, not a fabricated answer.
- Tool reports success for the requested action and identifies an output file actually created.
- Source SHA-256 and candidate SHA-256; source unchanged.
- Valid downloadable attachment/artifact from the client's file-transfer mechanism, **not merely a path copied into chat text**.
- No unverified statement that the output is ready to flash.
- The original ECU Forge sources state that the checksum is **not corrected**; independent checksum/ECU suitability validation is necessary. Do not bypass emissions regulations.

## 5) Other ECU SOFT tools / باقي أدوات المستودع

The PUBLIC catalog includes independent IVECO, Toyota, binary integrity, binary audit and entropy tools. They must remain available; "latest-only" cleanup applies to superseded releases **of the same product** and must not erase different product IDs. The user may ask:

> Use the connected ECU SOFT plugin to list every available \`iveco.*\`, \`toyota.*\`, \`ecusoft.*\` and \`vw_pcr21.*\` action. For each, show its source-defined mode and input schema.

**Never invent a write action for a read-only plugin, and never suppress an existing, verified write action.**

## 6) Troubleshooting / تشخيص المشاكل

| Observed problem | Exact check / الخطوة |
|---|---|
| Plugin name appears but no tools | Test the actual MCP connection, \`tools/list\`, auth and permissions. GitHub catalog metadata alone is insufficient. |
| \`Persistent account database required\` or similar host message | Host-specific failure; investigate real host runtime/connection, not the ECU source code by default. |
| Only inspect/preview appear | Check the live public \`plugin.json\` version **1.1.0**, that \`apply_off\` exists with \`mode=write\`, the MCP catalog refreshed, and workspace write action permission enabled. |
| New tool not shown after GitHub update | For local v0.4.1 request \`ecusoft_sync\` / reconnect if supported; for ChatGPT managed custom MCP, authorized admins may need to refresh the frozen tool snapshot and enable the new action. |
| Private package missing or SHA mismatch | Check the exact \`private_source.artifact_path\` and SHA-256 in the manifest; require authorized private GitHub access. Do not downgrade to v1.0.0. |
| Preview rejects BIN | The source engine did not verify a supported input; no guessed patch. |
| Write rejected | Distinguish no matching calibration, write permissions/approval, invalid output path, missing artifact transport. Do not bypass authorization. |
| Output path in answer but no attachment | Tool created/returned a path, but the ChatGPT connector did not register a downloadable artifact. A text path is not a file transfer. |
| Checksum unverified | As the original EGR/DPF source states: checksum correction is not included. Treat output as a candidate only. |

## 7) Required handover / نموذج التسليم الإلزامي

The executor must provide:
1. Current PUBLIC repository link and confirmed latest MCPB file + exact SHA-256.
2. PUBLIC active \`plugin.json\` links and versions for all affected tools.
3. PRIVATE exact latest package names, their hashes and proof that public manifest references match.
4. List of removed superseded files **with commit links/IDs**, and explicitly note that Git history remains.
5. Real ChatGPT connection type (Web remote MCP, Desktop local MCP, or other stdio client) and whether that integration was **actually tested**.
6. Actual tools discovered via the connected MCP; include read/write capability modes.
7. For write test, source hash, output hash and verified downloadable artifact (when authorized). Never claim a dry-run or synthetic result is real ECU validation.
8. Statement: **Watcher unchanged**; only GitHub and independent staging were touched.

**STOP / التوقف:** If the executor cannot obtain authenticated ChatGPT MCP access, do not invent a successful ChatGPT test. Hand over the GitHub publishing evidence and document the connection blocker explicitly.

---
ECU SOFT / Ahmed Elsakhawy & Dr. Sayed Mostafa — Controlled distribution instructions.