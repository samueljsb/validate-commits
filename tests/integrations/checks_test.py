from __future__ import annotations

from unittest import mock

from validate_commits import application
from validate_commits.integrations import checks
from validate_commits.integrations import configuration


class TestGetCustomChecks:
    def test_no_custom_checks(self) -> None:
        config = configuration.Config()

        custom_checks = checks.get_custom_checks(config)

        assert custom_checks == []

    def test_sumary_regexp_check(self) -> None:
        config = configuration.Config(
            checks=configuration.Checks(
                summary=(
                    configuration.Check(
                        pattern=r'\d+',
                        message='Commit summary contains numbers',
                    ),
                ),
            ),
        )

        custom_checks = checks.get_custom_checks(config)

        assert custom_checks == [
            checks.SummaryRegexpCheck(
                pattern=r'\d+',
                message='Commit summary contains numbers',
            ),
        ]


class TestSummaryRegexpCheck:
    def test_matches(self) -> None:
        commit = mock.Mock(spec_set=application.Commit, summary='Make 42 changes')
        regexp_check = checks.SummaryRegexpCheck(
            pattern=r'\d+',
            message='Summary contains numbers.',
        )

        errors = regexp_check(commit)

        assert list(errors) == ['Summary contains numbers.']

    def test_no_matches(self) -> None:
        commit = mock.Mock(spec_set=application.Commit, summary='Make some changes')
        regexp_check = checks.SummaryRegexpCheck(
            pattern=r'\d+',
            message='Summary contains numbers.',
        )

        errors = regexp_check(commit)

        assert list(errors) == []


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
