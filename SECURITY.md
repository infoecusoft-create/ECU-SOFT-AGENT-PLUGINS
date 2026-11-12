# Security model

This V1 host is not a hardened sandbox. Plugins execute in-process after lazy import and therefore must be treated as trusted code. Do not load third-party plugins from untrusted sources in a production agent. Use a separate process/container with OS-level isolation for untrusted extensions.

The Toyota plugin is restricted to reading `.bin` files. It does not write or modify ECU binaries, execute shell commands, access the network, or access the Windows registry.
