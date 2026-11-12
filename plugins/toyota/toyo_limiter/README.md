# Toyota BIN Inspector Plugin

Headless, read-only Toyota BIN identification and inspection extracted from the supplied TOYO LIMITER source.

## Supported capabilities

- `toyota.identify_vehicle`
- `toyota.inspect_bin`
- `toyota.inspect_speed`
- `toyota.inspect_rpm`
- `toyota.inspect_cutoff`

## Python use

```python
from toyota_plugin.tool import execute
result = execute("inspect_bin", {"file_path": "sample.bin"})
```

## Safety boundary

This package does not modify ECU binaries or alter speed, RPM, cut-off, emissions, immobilizer, or other vehicle-control calibrations. It reports source-derived raw bytes and offsets only. Observed values are not validated engineering units or proof of safe compatibility.

## Source fidelity notes

The Toyota profile records are extracted from the supplied `CARS_JSON`. The duplicated source key `hilux_GIN1_3_1` is represented as two explicit conflicting variants so neither record is silently discarded. Conflicting or ambiguous matches are not auto-selected.

No real ECU fixture was supplied; the test suite uses synthetic data and does not claim validation against a real ECU.
