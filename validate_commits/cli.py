from __future__ import annotations

import argparse
import sys
from typing import TYPE_CHECKING

from validate_commits import application
from validate_commits.integrations import checks
from validate_commits.integrations import console as console_integration
from validate_commits.integrations import git as git_integration


if TYPE_CHECKING:
    from collections.abc import Sequence


def _build_app() -> application.App:
    git_commits = git_integration.Commits()

    default_checks = (
        checks.author_has_email,
        checks.commit_is_not_empty,
        checks.commit_is_not_fixup,
    )

    return application.App(
        commits=git_commits('main', 'HEAD'),
        checks=default_checks,
        report_error=console_integration.report_error,
        report_summary=console_integration.report_summary,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='validate-commits',
    )
    _ = parser.parse_args(argv)

    app = _build_app()

    try:
        return app()
    except app.NoCommitsChecked:
        print("No commits between 'main' and 'HEAD'.", file=sys.stderr)  # noqa: T201
        return 1


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
