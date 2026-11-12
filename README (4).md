# ECU-SOFT-AGENT-PLUGINS — Hybrid Registry

## Features
- Preserves the locally retrievable V1 host, Toyota read-only inspector, and 22 source profile records.
- Adds a read-only HTTP Registry API, MCP stdio adapter, REST client, and offline snapshot fallback.
- Keeps plugin loading/execution local; the registry distributes metadata only.

## Quick start
```bash
python tools/validate_plugins.py
python tools/build_index.py
python -m unittest discover -s tests -v
python -m ecusoft_registry.server
```
MCP: `pip install -r requirements-mcp.txt`, then run `python adapters/mcp_server.py` from an MCP-capable agent configured for stdio.

## Limits
This build is additive. It is not a full verified Git clone because the GitHub tree/archive endpoint was unavailable. The captured Toyota plugin is read-only. The original Toyota BIN modification source requested for preservation was not present in the reachable tree files. See `docs/HYBRID_REGISTRY.md`.

## Agent integration

See [AGENT_INTEGRATION_GUIDE.md](AGENT_INTEGRATION_GUIDE.md) for step-by-step MCP, OpenCode, Watcher Eye, REST, Python and offline integration instructions. Focused guides are in `docs/agent-integration/`.
