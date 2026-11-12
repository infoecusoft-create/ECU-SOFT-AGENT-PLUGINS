# Contributing

1. Add a plugin under `plugins/<category>/<plugin_id>/`.
2. Add a `plugin.json` conforming to `registry/schemas/plugin.schema.json`.
3. Keep imports side-effect free.
4. Add tests.
5. Run validation, index generation and the complete test suite.
6. Do not claim real ECU compatibility without test fixtures and documented validation.
