# Watcher Eye Integration

```python
from plugin_host import PluginHost

host = PluginHost("registry/index.json")
matches = host.discover(
    operation="inspect_binary",
    extension=".bin"
)
```

Execution is explicit and requires untrusted-plugin opt-in for this starter
demo:

```python
host = PluginHost("registry/index.json", allow_untrusted=True)
result = host.execute("inspect_binary", file_path="sample.bin")
```

For production integration, keep `allow_untrusted=False`, review and approve
plugins through a trusted installation workflow, and execute third-party
plugins in a separate restricted process. The current V1 API is local Python;
a future network transport should wrap this API rather than changing plugin
contracts.
