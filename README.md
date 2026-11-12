# ECU-SOFT-AGENT-PLUGINS

Universal capability-based plugin registry and lazy-loading execution host for AI agents.

**Goal:** Let Watcher Eye Agent discover the correct tool through metadata rather
than scanning every plugin source file for every task.

## How it works

1. Each plugin declares its identity and capabilities in `plugin.json`.
2. `tools/build_index.py` generates registry indexes from manifests.
3. `PluginHost.discover()` searches metadata without importing plugin code.
4. `PluginHost.execute()` checks policy, then lazy-loads the selected plugin.
5. Results use a consistent response structure.

## Quick start

Requirements: Python 3.10+.

```bash
python tools/validate_plugins.py
python tools/build_index.py
python -m pytest -q
python plugin_host.py --list
python plugin_host.py --discover inspect_binary --extension .bin
```

## Python API

```python
from plugin_host import PluginHost

host = PluginHost("registry/index.json")
matches = host.discover("inspect_binary", ".bin")
print(matches)
```

The included demonstration plugin is deliberately marked `untrusted`.
Review it before enabling it:

```python
host = PluginHost("registry/index.json", allow_untrusted=True)
result = host.execute("inspect_binary", file_path="sample.bin")
```

## Repository structure

- `plugin_host.py`: single-file V1 host and stable initial API.
- `registry/`: generated discovery indexes and schemas.
- `plugins/`: independently packaged plugins.
- `tools/`: validation and index generation.
- `tests/`: automated tests.
- `docs/`: architecture, security, and integration documentation.

## Toyota plugin

The Toyota category is reserved for the real Toyota tool. No Toyota functionality
is fabricated in this release. Integrate the supplied source code and task
description only after reviewing its actual behavior.

## Security notice

This is an extensible V1 foundation, not yet a hardened production sandbox.
In-process plugin execution is unsafe for untrusted third-party code. See
[SECURITY_MODEL.md](docs/SECURITY_MODEL.md).

## License

MIT. See [LICENSE](LICENSE).
