from __future__ import annotations

import sys
import textwrap
from typing import TYPE_CHECKING

import attrs


if TYPE_CHECKING:
    from collections.abc import Collection

    from validate_commits.application import Error


@attrs.frozen
class Reporter:
    base_ref: str

    def report_error(self, error: Error) -> None:
        commit_summary = error.commit.summary
        commit_sha = error.commit.sha

        print(f'error: {commit_sha} ({commit_summary})')  # noqa: T201
        print(textwrap.indent(error.message.rstrip(), '    '))  # noqa: T201

    def report_summary(
        self, *, errors: Collection[Error], commits_checked: int
    ) -> None:
        if errors:
            num_errors = len(errors)
            commits_with_errors = len({error.commit.sha for error in errors})
            print(  # noqa: T201
                f"Found {num_errors} errors in {commits_with_errors} commits between {self.base_ref!r} and 'HEAD' (checked {commits_checked} commits).",
                file=sys.stderr,
            )
        else:
            print(  # noqa: T201
                f"No issues found in {commits_checked} commits between {self.base_ref!r} and 'HEAD'.",
                file=sys.stderr,
            )
