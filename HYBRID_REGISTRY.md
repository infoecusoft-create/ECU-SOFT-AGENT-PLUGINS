# Hybrid Universal Registry

The registry is an additive metadata/discovery service. The existing local `PluginHost` continues to load and execute local plugin implementations. The HTTP registry never executes remote code or accepts uploaded files.

- Local HTTP API: `python -m ecusoft_registry.server` (127.0.0.1:8765)
- MCP adapter: install `requirements-mcp.txt`, then run `python adapters/mcp_server.py` over stdio.
- REST routes: `/health`, `/v1/plugins`, `/v1/capabilities/{id}`.
- Offline mode: `RegistryClient` keeps a JSON snapshot and uses it when the server is unavailable.

MCP is the broadest common interface for compatible Agents; REST and Python client cover other integration styles. Agents without tool/connector capability need a product-specific adapter. No implementation can guarantee compatibility with literally every Agent.

Security: catalog is metadata only; downloaded code is not automatically executed; use trusted local packages and OS sandboxing for third-party code. Current PluginHost is not itself an OS sandbox.

Upstream caveat: original repository README states its Toyota plugin is read-only and the checkout is a rebuilt baseline, not a byte-for-byte current upstream clone. This build preserves the Toyota inspector and all 22 profile records captured from the live repository. It does not contain the missing original Toyota editing/calibration source code; do not mistake it for that source.
