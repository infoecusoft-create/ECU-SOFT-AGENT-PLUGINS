# Architecture

- `plugins/**/plugin.json` contains discovery metadata.
- `tools/build_index.py` compiles metadata into `registry/index.json`.
- `PluginHost.discover()` reads only the index and does not import plugin code.
- `PluginHost.execute()` resolves a unique capability and imports its implementation lazily.
- Toyota plugin is read-only and has no file-writing entry points.

This folder is a reconstructed V1-compatible baseline based on the repository structure and README that were publicly visible during preparation. It is not claimed to be a byte-for-byte copy of the upstream GitHub checkout because GitHub could not be cloned from this runtime. Before replacing an existing checkout, compare its current host/schema and merge rather than overwrite.
