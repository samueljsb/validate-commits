from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Generator

    from validate_commits.application import Commit


def author_has_email(commit: Commit) -> Generator[str]:
    if not commit.author_email:
        yield """\
Commit author has no email.

Make sure you have an author email set in your git config, e.g:

    git config user.email "your.name@example.com"
"""


def commit_is_not_empty(commit: Commit) -> Generator[str]:
    if commit.is_empty:
        yield 'Commit is empty.'


def commit_is_not_fixup(commit: Commit) -> Generator[str]:
    if any(commit.summary.startswith(prefix) for prefix in ('fixup!', '!fixup')):
        yield 'Fixup commit.'
