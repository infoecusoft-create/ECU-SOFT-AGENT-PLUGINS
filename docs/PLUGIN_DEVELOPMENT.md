# Plugin Development

1. Create a uniquely named folder under the appropriate `plugins/` category.
2. Add `plugin.json` with ID, description, operations, capabilities, file types,
   entry point, dependencies, permissions, and safety metadata.
3. Implement `create_plugin()` in the declared entry point.
4. Implement `execute(operation, inputs, context=None)`.
5. Run `python tools/validate_plugins.py`.
6. Run `python tools/build_index.py`.
7. Run `python -m pytest -q`.

Keep plugins focused. Never claim an operation or file format that the code
does not actually support. Do not modify original input files by default.
