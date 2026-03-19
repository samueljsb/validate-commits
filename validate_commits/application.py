from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Protocol

import attrs


if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable
    from collections.abc import Sequence


class Commit(Protocol):
    @property
    def sha(self) -> str: ...

    @property
    def author_name(self) -> str: ...

    @property
    def author_email(self) -> str: ...

    @property
    def summary(self) -> str: ...

    @property
    def is_empty(self) -> bool: ...


@attrs.frozen
class Error:
    commit: Commit
    message: str


@attrs.frozen
class App:
    commits: Iterable[Commit]
    checks: Sequence[Check]
    report_error: Callable[[Error], None]
    report_summary: SummaryReport

    class Check(Protocol):
        def __call__(self, commit: Commit) -> Iterable[str]: ...

    class SummaryReport(Protocol):
        def __call__(self, *, commits_checked: int, errors: list[Error]) -> None: ...

    class NoCommitsChecked(Exception):
        pass

    def __call__(self) -> int:
        commits_checked = 0
        errors: list[Error] = []
        for commit in self.commits:
            for check in self.checks:
                for error_msg in check(commit):
                    error = Error(commit, error_msg)
                    self.report_error(error)
                    errors.append(error)
            commits_checked += 1

        if not commits_checked:
            raise self.NoCommitsChecked

        self.report_summary(errors=errors, commits_checked=commits_checked)

        return 1 if errors else 0
