# delinker

`delinker` recursively replaces symlinks in a directory tree with copies of the files or directories they resolve to.

It keeps scanning until no resolvable symlinks remain. Broken or otherwise unresolved symlinks are left in place and reported to stdout.

The CLI is built with `rich-click`, so `--help` output is rendered with Rich formatting.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Use With uv

Run from a cloned checkout without manually activating a virtualenv:

```bash
uv sync
uv run delinker --help
uv run delinker /path/to/tree
```

Run the script entrypoint directly through `uv`:

```bash
uv run python delinker.py /path/to/tree
```

## Install As a Tool

Install from GitHub as a standalone CLI:

```bash
uv tool install git+https://github.com/smprather/delinker.git
```

Upgrade an existing tool install:

```bash
uv tool install --upgrade git+https://github.com/smprather/delinker.git
```

## Development

```bash
uv sync
uv run delinker --help
```

## Usage

```bash
delinker /path/to/tree
```

From the repo with `uv`:

```bash
uv run delinker /path/to/tree
```

Show help:

```bash
uv run delinker --help
```

## Behavior

- Replaces symlinks to files with copied files.
- Replaces symlinks to directories by materializing the target directory contents.
- Handles nested symlinks recursively until there are no more resolvable links.
- Preserves broken or unresolved links, but reports each one once.
- Guards against directory-expansion cycles and reports them as unresolved.

## Example

Before:

```text
work/
  file-link -> /data/source.txt
  dir-link -> /data/assets
  broken-link -> missing-target
```

After running `delinker work`:

```text
work/
  file-link
  dir-link/
    ...
  broken-link -> missing-target
```

## Notes

`delinker` modifies the target tree in place. Run it on a copy first if you need a reversible workflow.

See [DEVELOPMENT.md](/home/myles/delinker/DEVELOPMENT.md) for contributor workflow details and [AGENTS.md](/home/myles/delinker/AGENTS.md) for repo-specific guidance for coding agents.
