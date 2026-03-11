# delinker

`delinker` recursively replaces symlinks in a directory tree with copies of the files or directories they resolve to.

It keeps scanning until no resolvable symlinks remain. Broken or otherwise unresolved symlinks are left in place and reported to stdout.

The CLI is built with `rich-click`, so `--help` output is rendered with Rich formatting.

## Install

From the GitHub repo:

```bash
pip install git+https://github.com/smprather/delinker.git
```

For local development:

```bash
pip install -e .
```

## Usage

```bash
delinker /path/to/tree
```

You can also run it directly from the repo:

```bash
python delinker.py /path/to/tree
```

Show help:

```bash
delinker --help
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
