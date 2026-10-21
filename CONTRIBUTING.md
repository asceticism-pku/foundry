# Contributing to Foundry

Build Foundry using the [installation instructions](README.md#installation), then install the development tools from the Foundry directory:

```bash
python -m pip install -r requirements/lint.txt
pre-commit install
```

## Checks

```bash
pre-commit run --all-files
python -m pytest tests/
```

The hook configuration covers Ruff, clang-format, Markdown, workflow syntax, SPDX headers, and commit sign-off. GPU tests require CUDA and the dependencies specified by each test.

## Pull requests

Describe the behavior change, include focused tests, and update affected configuration or documentation. Preserve SPDX headers and license information. Report bugs with a reproducer, dependency versions, and traceback.
