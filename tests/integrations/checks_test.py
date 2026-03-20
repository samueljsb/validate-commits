from __future__ import annotations

from unittest import mock

from validate_commits import application
from validate_commits.integrations import checks


class TestCommitIsNotFixup:
    def test_no_problem(self) -> None:
        commit = mock.Mock(spec_set=application.Commit, summary='Make some changes')

        errors = checks.commit_is_not_fixup(commit)

        assert list(errors) == []

    def test_fixup_commit(self) -> None:
        commit = mock.Mock(
            spec_set=application.Commit, summary='fixup! Some other commit'
        )

        errors = checks.commit_is_not_fixup(commit)

        assert list(errors) == ['Fixup commit.']
