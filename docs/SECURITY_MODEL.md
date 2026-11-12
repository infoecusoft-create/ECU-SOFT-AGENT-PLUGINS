# Security Model — V1

- Plugins default to `untrusted`.
- Untrusted plugins are blocked unless explicitly opted in.
- Declared permissions must be explicitly approved by the caller.
- Entry-point hashes are checked when a hash is present in the registry.
- Plugin paths are constrained to their declared plugin root.
- The example plugin is read-only.

Limitations:
- In-process Python execution is not a sandbox.
- A plugin can access process privileges once imported.
- SHA-256 does not prove publisher identity.
- V1 does not yet provide OS-level filesystem, network, CPU, or memory isolation.

Do not run unreviewed plugins in a privileged process. Production deployment
must add subprocess/container isolation and a publisher-signature trust model.
