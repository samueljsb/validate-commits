from __future__ import annotations

from unittest import mock

import pytest

from validate_commits import application
from validate_commits.application import Author
from validate_commits.application import Commit
from validate_commits.application import Error


class TestApp:
    def test_no_commits(self) -> None:
        report_error = mock.Mock()
        report_summary = mock.Mock()
        app = application.App(
            commits=(),
            checks=(mock.Mock(spec_set=application.App.Check),),
            report_error=report_error,
            report_summary=report_summary,
        )

        with pytest.raises(app.NoCommitsChecked):
            app()

        assert not report_error.called
        assert not report_summary.called

    def test_no_errors(self) -> None:
        commit = mock.Mock(spec_set=Commit)
        report_error = mock.Mock()
        report_summary = mock.Mock(spec_set=application.App.SummaryReport)
        app = application.App(
            commits=(commit,),
            checks=(mock.Mock(spec_set=application.App.Check, return_value=()),),
            report_error=report_error,
            report_summary=report_summary,
        )

        app()

        assert not report_error.called
        assert report_summary.call_args_list == [
            mock.call(commits_checked=1, errors=[])
        ]

    def test_reports_errors(self) -> None:
        commit = mock.Mock(
            spec_set=Commit,
            sha='abc123',
            summary='Change a thing',
            author=mock.Mock(spec_set=Author, email='april.may@example.com'),
        )
        report_error = mock.Mock()
        report_summary = mock.Mock(spec_set=application.App.SummaryReport)
        app = application.App(
            commits=(commit,),
            checks=(
                mock.Mock(
                    spec_set=application.App.Check,
                    return_value=['Something is wrong'],
                ),
            ),
            report_error=report_error,
            report_summary=report_summary,
        )

        app()

        assert report_error.call_args_list == [
            mock.call(Error(commit=commit, message='Something is wrong'))
        ]
        assert report_summary.call_args_list == [
            mock.call(
                commits_checked=1,
                errors=[Error(commit=commit, message='Something is wrong')],
            )
        ]
