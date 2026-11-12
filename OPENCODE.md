# OpenCode setup

Use this package as a local stdio MCP server only if the installed OpenCode release supports MCP servers. Configure command, script arguments and working directory as documented by that exact release. Use absolute paths and the same Python environment where `requirements-mcp.txt` was installed.

After reloading OpenCode, confirm the five `toyota.*` tools appear, then run a read-only inspection against a test BIN. Configuration keys and file locations vary by release, so this guide does not invent a universal OpenCode JSON schema.
