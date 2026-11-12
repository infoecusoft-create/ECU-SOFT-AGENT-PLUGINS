# Architecture

```text
Watcher Eye Agent
       |
       v
PluginHost API
       |
       +---- Registry metadata (JSON; no plugin imports)
       |
       +---- Capability/operation resolver
       |
       +---- Permission and integrity checks
       |
       v
Lazy Plugin Loader
       |
       v
Selected Plugin
       |
       v
Normalized execution result
```

The registry is generated from each plugin's `plugin.json`. Discovery reads
`registry/index.json` only. The selected entry point is imported only at execute
time. V1 uses in-process loading for the trusted demo path; this is not a
security sandbox. Use process isolation before running third-party plugins.
