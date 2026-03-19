from __future__ import annotations

from unittest import mock

import pytest

from validate_commits import application
from validate_commits.integrations import checks


class TestCommitIsNotFixup:
    def test_no_problem(self) -> None:
        commit = mock.Mock(spec_set=application.Commit, summary='Make some changes')

        errors = checks.commit_is_not_fixup(commit)

        assert list(errors) == []

    @pytest.mark.parametrize(
        'summary',
        [
            'fixup! Some other commit',
            '!fixup Some other commit',
        ],
    )
    def test_fixup_commit(self, summary: str) -> None:
        commit = mock.Mock(spec_set=application.Commit, summary=summary)

        errors = checks.commit_is_not_fixup(commit)

        assert list(errors) == ['Fixup commit.']
