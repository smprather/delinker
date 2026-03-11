# AGENTS.md

## Purpose

This repository contains a small single-file Python CLI, `delinker`, that replaces symlinks in a directory tree with copies of their resolved targets.

## Project Shape

- Main implementation: `delinker.py`
- Packaging and dependency metadata: `pyproject.toml`
- Lockfile: `uv.lock`
- Human-facing overview: `README.md`

## Environment

- Use `uv` for dependency and environment management.
- Do not introduce `pip` workflow instructions unless the user explicitly asks for them.
- Prefer `uv run ...` for commands and `uv sync` before validation if dependencies may have changed.

## Common Commands

Sync the environment:

```bash
uv sync
```

Run the CLI:

```bash
uv run delinker --help
uv run delinker /path/to/tree
```

Run the script directly:

```bash
uv run python delinker.py /path/to/tree
```

Update dependencies:

```bash
uv add <package>
uv remove <package>
uv lock
```

## Validation

- There is no formal test suite yet.
- For quick validation, use temporary directories with:
  - file symlinks
  - directory symlinks
  - relative symlinks inside copied directories
  - broken links
- A low-cost syntax check is:

```bash
PYTHONPYCACHEPREFIX=/tmp uv run python -m py_compile delinker.py
```

## Editing Guidance

- Keep the project lightweight. Avoid introducing unnecessary package structure unless there is a clear payoff.
- Preserve the current behavior that broken or unresolved links are reported and left in place.
- If you change dependencies, update both `pyproject.toml` and `uv.lock`.
- If you change CLI behavior, update `README.md` and keep help examples aligned with `rich-click`.
