# ECU-SOFT-AGENT-PLUGINS

Capability-based plugin registry and lazy-loading execution host for AI agents.

## Included in this rebuilt package

- `plugin_host.py`: metadata discovery and lazy execution.
- `plugins/`: independent plugin packages.
- `registry/index.json`: generated capability index.
- `registry/schemas/`: manifest schema.
- `tools/`: plugin validation and index generation.
- `tests/`: host and Toyota inspection tests.
- `docs/`: architecture and security notes.

## Toyota plugin

The Toyota plugin is extracted from the supplied TOYO LIMITER source and retains the source-derived Toyota profile catalogue (22 records including the duplicate-key variants). It supports vehicle/profile identification and read-only inspection of Speed, RPM and CUT OFF data regions.

**It intentionally does not implement binary modification of vehicle-control calibrations.** No speed limiter, RPM limiter or cut-off values are changed, and no output BIN is written.

## Quick start

```bash
python tools/validate_plugins.py
python tools/build_index.py
python -m unittest discover -s tests -v
python examples/discover_toyota.py
```

## Execute a capability

```python
from plugin_host import PluginHost
host = PluginHost()
result = host.execute("toyota.inspect_bin", file_path="sample.bin")
print(result)
```

## Important upstream note

This ZIP is a rebuilt, self-contained baseline following the known upstream repository layout and documented V1 behavior. It is not a verified byte-for-byte clone of the latest GitHub branch. The GitHub checkout was unreachable from the build runtime, so compare/merge the included host and schema with the live upstream repository before replacing it.
