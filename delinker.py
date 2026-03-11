#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path

import rich_click as click


CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def find_symlinks(root: Path) -> list[Path]:
    symlinks: list[Path] = []

    for path in root.rglob("*"):
        if path.is_symlink():
            symlinks.append(path)

    return sorted(symlinks, key=lambda path: len(path.parts))


def report_unresolved(link: Path, exc: Exception, destination: Path | None = None) -> None:
    if destination is None or destination == link:
        click.echo(f"Skipping unresolved symlink: {link} ({exc})")
        return

    click.echo(f"Skipping unresolved symlink: {link} (would materialize at {destination}: {exc})")


def materialize_path(
    source: Path,
    destination: Path,
    unresolved_links: set[Path],
    active_dirs: frozenset[Path] = frozenset(),
) -> None:
    try:
        if source.is_symlink():
            source = source.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        if destination not in unresolved_links:
            report_unresolved(source, exc, destination)
            unresolved_links.add(destination)
        return

    if source.is_dir():
        resolved_dir = source.resolve(strict=True)
        if resolved_dir in active_dirs:
            exc = RuntimeError("symlink cycle detected while expanding directories")
            if destination not in unresolved_links:
                report_unresolved(source, exc, destination)
                unresolved_links.add(destination)
            return

        destination.mkdir()
        next_active_dirs = active_dirs | frozenset({resolved_dir})
        for child in source.iterdir():
            materialize_path(child, destination / child.name, unresolved_links, next_active_dirs)
        shutil.copystat(source, destination)
        return

    shutil.copy2(source, destination)


def replace_symlink(link: Path, unresolved_links: set[Path]) -> bool:
    try:
        target = link.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        if link not in unresolved_links:
            report_unresolved(link, exc)
            unresolved_links.add(link)
        return False

    link.unlink()
    materialize_path(target, link, unresolved_links)
    return True


def delink_tree(root: Path) -> tuple[int, int]:
    replaced = 0
    unresolved_links: set[Path] = set()

    while True:
        symlinks = find_symlinks(root)
        if not symlinks:
            break

        replaced_this_round = 0
        pending = [link for link in symlinks if link not in unresolved_links]
        if not pending:
            break

        for link in pending:
            if replace_symlink(link, unresolved_links):
                replaced += 1
                replaced_this_round += 1

        if replaced_this_round == 0:
            break

    return replaced, len(unresolved_links)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path, resolve_path=True),
)
def main(directory: Path) -> None:
    """Replace symlinks under DIRECTORY with copies of their targets."""
    root = directory.resolve(strict=True)
    replaced, unresolved = delink_tree(root)
    click.echo(f"Replaced {replaced} symlink(s)")

    if unresolved:
        click.echo(f"Skipped {unresolved} unresolved symlink(s)")


if __name__ == "__main__":
    main()
