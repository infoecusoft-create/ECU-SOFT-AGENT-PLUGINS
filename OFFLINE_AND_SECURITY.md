# Offline mode and security

Local MCP execution reads the local `registry/index.json` and local plugin files, so it can work without internet when dependencies and input files are present. `RegistryClient` caches catalog JSON for offline metadata discovery.

The current build does not automatically synchronize MCP from a cloud registry, verify signed manifests, download plugins, or sandbox Python code at OS level. Load only trusted reviewed plugins, limit file permissions, preserve original BIN files and do not expose the unauthenticated metadata server publicly.
