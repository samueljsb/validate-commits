from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from validate_commits import application
from validate_commits.integrations import checks
from validate_commits.integrations import configuration
from validate_commits.integrations import console as console_integration
from validate_commits.integrations import git as git_integration


if TYPE_CHECKING:
    from collections.abc import Sequence


def _build_app(base_ref: str) -> application.App:
    config_file = Path('.validate-commits-config.toml')
    config = configuration.load_from_file(config_file)

    git_commits = git_integration.Commits()

    default_checks = (
        checks.author_has_email,
        checks.commit_is_not_empty,
        checks.commit_is_not_fixup,
    )
    custom_checks = checks.get_custom_checks(config)

    reporter = console_integration.Reporter(base_ref=base_ref)

    return application.App(
        commits=git_commits(base_ref, 'HEAD'),
        checks=(
            *default_checks,
            *custom_checks,
        ),
        report_error=reporter.report_error,
        report_summary=reporter.report_summary,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='validate-commits',
    )
    parser.add_argument(
        '--since', type=str, default='main', help='check commits since this reference'
    )
    args = parser.parse_args(argv)

    base_ref: str = args.since

    app = _build_app(base_ref=base_ref)

    try:
        return app()
    except app.NoCommitsChecked:
        print(f"No commits between {base_ref!r} and 'HEAD'.", file=sys.stderr)  # noqa: T201
        return 1


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
