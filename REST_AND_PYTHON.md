# REST discovery and Python execution

Start the metadata catalog with `python -m ecusoft_registry.server`. The API exposes `GET /health`, `GET /v1/plugins`, and `GET /v1/capabilities/{id}`. It does not execute plugins.

For local execution from Python, import `PluginHost` from `plugin_host.py` and call `discover()` / `execute()` as shown in the root integration guide. The `RegistryClient` class fetches and caches catalog metadata; it is not a remote execution API.
