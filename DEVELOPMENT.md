# Development

## Setup

```bash
uv sync
```

This project uses `uv` to manage the virtual environment and lockfile.

## Run

```bash
uv run delinker --help
uv run delinker /path/to/tree
```

You can also invoke the source file directly:

```bash
uv run python delinker.py /path/to/tree
```

## Validation

There is no automated test suite yet. Validate changes with a temporary directory tree that includes:

- symlinks to files
- symlinks to directories
- nested relative symlinks inside linked directories
- broken symlinks

Syntax-check the module with:

```bash
PYTHONPYCACHEPREFIX=/tmp uv run python -m py_compile delinker.py
```

## Dependency Management

Add or remove dependencies with `uv`, then refresh the lockfile:

```bash
uv add <package>
uv remove <package>
uv lock
```

If dependency metadata changes, commit `pyproject.toml` and `uv.lock` together.
