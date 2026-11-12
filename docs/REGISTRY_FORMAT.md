# Registry Format

`plugin.json` inside each plugin folder is the canonical source of truth.
Run `python tools/build_index.py` to regenerate derived indexes.

- `index.json`: compact discovery records and entry-point metadata.
- `capabilities.json`: capability to plugin-ID mapping.
- `operations.json`: operation to plugin-ID mapping.
- `file_types.json`: extension to plugin-ID mapping.
- `categories.json`: category to plugin-ID mapping.
- `dependencies.json`: declared dependencies.
- `versions.json`: plugin/API compatibility metadata.
- `integrity.json`: SHA-256 entry-point digests.

A SHA-256 digest detects unexpected file changes; it does not establish who
published the plugin or whether the publisher is trustworthy.
