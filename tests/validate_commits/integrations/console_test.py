from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

from validate_commits.application import Commit
from validate_commits.application import Error
from validate_commits.integrations import console


if TYPE_CHECKING:
    import pytest


class TestReportError:
    def test_report_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        error = Error(
            commit=mock.Mock(
                spec_set=Commit,
                sha='abc123',
                summary='Make some changes to some files',
            ),
            message='Something is wrong with this commit.',
        )

        console.report_error(error)

        stdout, stderr = capsys.readouterr()
        assert (
            stdout
            == """\
error: abc123 (Make some changes to some files)
    Something is wrong with this commit.
"""
        )
        assert stderr == ''


class TestReportSummary:
    def test_no_errors(self, capsys: pytest.CaptureFixture[str]) -> None:
        console.report_summary(errors=(), commits_checked=4)

        stdout, stderr = capsys.readouterr()
        assert stdout == ''
        assert (
            stderr
            == """\
No issues found in 4 commits between 'main' and 'HEAD'.
"""
        )

    def test_errors(self, capsys: pytest.CaptureFixture[str]) -> None:
        console.report_summary(
            errors=(
                Error(commit=mock.Mock(spec_set=Commit, sha='abc123'), message=''),
                Error(commit=mock.Mock(spec_set=Commit, sha='abc123'), message=''),
                Error(commit=mock.Mock(spec_set=Commit, sha='def456'), message=''),
            ),
            commits_checked=4,
        )

        stdout, stderr = capsys.readouterr()
        assert stdout == ''
        assert (
            stderr
            == """\
Found 3 errors in 2 commits between 'main' and 'HEAD' (checked 4 commits).
"""
        )
