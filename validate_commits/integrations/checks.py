from __future__ import annotations

import re
from typing import TYPE_CHECKING
from typing import Protocol

import attrs


if TYPE_CHECKING:
    from collections.abc import Generator

    from validate_commits.application import Commit


# Custom checks
# -------------


class _Config(Protocol):
    @property
    def checks(self) -> _ConfigChecks: ...


class _ConfigChecks(Protocol):
    @property
    def summary(self) -> tuple[_RegexpCheck, ...]: ...

    @property
    def author_email(self) -> tuple[_RegexpCheck, ...]: ...


class _RegexpCheck(Protocol):
    @property
    def pattern(self) -> str: ...

    @property
    def message(self) -> str: ...


@attrs.frozen
class SummaryRegexpCheck:
    pattern: str
    message: str

    def __call__(self, commit: Commit) -> Generator[str]:
        if re.search(self.pattern, commit.summary):
            yield self.message


@attrs.frozen
class AuthorEmailRegexpCheck:
    pattern: str
    message: str

    def __call__(self, commit: Commit) -> Generator[str]:
        authors_to_check = (commit.author, *commit.co_authors)
        for author in authors_to_check:
            if author.email and re.search(self.pattern, author.email):
                yield self.message


type CustomCheck = AuthorEmailRegexpCheck | SummaryRegexpCheck


def get_custom_checks(config: _Config) -> list[CustomCheck]:
    checks: list[CustomCheck] = []

    for definition in config.checks.summary:
        checks.append(  # noqa: PERF401
            SummaryRegexpCheck(pattern=definition.pattern, message=definition.message)
        )

    for definition in config.checks.author_email:
        checks.append(  # noqa: PERF401
            AuthorEmailRegexpCheck(
                pattern=definition.pattern, message=definition.message
            )
        )

    return checks


# Built-in checks
# ---------------


def author_has_email(commit: Commit) -> Generator[str]:
    if not commit.author.email:
        yield """\
Commit author has no email.

Make sure you have an author email set in your git config, e.g:

    git config user.email "your.name@example.com"
"""

    for co_author in commit.co_authors:
        if not co_author.email:
            yield """\
Commit co-author has no email.
"""


def commit_is_not_empty(commit: Commit) -> Generator[str]:
    if commit.is_empty:
        yield 'Commit is empty.'


def commit_is_not_fixup(commit: Commit) -> Generator[str]:
    if commit.summary.startswith('fixup!'):
        yield 'Fixup commit.'
