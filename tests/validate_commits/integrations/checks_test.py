from __future__ import annotations

from unittest import mock

from validate_commits import application
from validate_commits.integrations import checks
from validate_commits.integrations import configuration


def _mock_author(
    name: str | None = None, email: str | None = None
) -> application.Author:
    author = mock.Mock(spec_set=application.Author)
    # The `name` attribute cannot be set directly.
    author.configure_mock(name=name, email=email)
    return author


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

    def test_author_email_regexp_check(self) -> None:
        config = configuration.Config(
            checks=configuration.Checks(
                author_email=(
                    configuration.Check(
                        pattern=r'@example\.com$',
                        message='Fake email address provided.',
                    ),
                ),
            ),
        )

        custom_checks = checks.get_custom_checks(config)

        assert custom_checks == [
            checks.AuthorEmailRegexpCheck(
                pattern=r'@example\.com$',
                message='Fake email address provided.',
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


class TestAuthorEmailRegexpCheck:
    def test_commit_author_matches(self) -> None:
        commit = mock.Mock(
            spec_set=application.Commit,
            author=_mock_author(email='april.may@example.com'),
            co_authors=[],
        )
        regexp_check = checks.AuthorEmailRegexpCheck(
            pattern=r'@example\.com$',
            message='Fake email address provided.',
        )

        errors = regexp_check(commit)

        assert list(errors) == ['Fake email address provided.']

    def test_co_author_matches(self) -> None:
        commit = mock.Mock(
            spec_set=application.Commit,
            author=_mock_author(email='april.may@example.net'),
            co_authors=[_mock_author(email='andy.skampt@example.com')],
        )
        regexp_check = checks.AuthorEmailRegexpCheck(
            pattern=r'@example\.com$',
            message='Fake email address provided.',
        )

        errors = regexp_check(commit)

        assert list(errors) == ['Fake email address provided.']

    def test_no_matches(self) -> None:
        commit = mock.Mock(
            spec_set=application.Commit,
            author=_mock_author(email='april.may@example.net'),
            co_authors=[],
        )
        regexp_check = checks.AuthorEmailRegexpCheck(
            pattern=r'@example\.com$',
            message='Fake email address provided.',
        )

        errors = regexp_check(commit)

        assert list(errors) == []


class TestAuthorHasEmail:
    def test_no_problems(self) -> None:
        commit = mock.Mock(
            spec_set=application.Commit,
            author=_mock_author(email='april.may@example.com'),
            co_authors=[_mock_author(email='andy.skampt@example.com')],
        )

        errors = checks.author_has_email(commit)

        assert list(errors) == []

    def test_author_has_no_email(self) -> None:
        commit = mock.Mock(
            spec_set=application.Commit,
            author=_mock_author(email=None),
            co_authors=[
                _mock_author(email='andy.skampt@example.com'),
            ],
        )

        errors = checks.author_has_email(commit)

        assert list(errors) == [
            """\
Commit author has no email.

Make sure you have an author email set in your git config, e.g:

    git config user.email "your.name@example.com"
""",
        ]

    def test_co_author_has_no_email(self) -> None:
        commit = mock.Mock(
            spec_set=application.Commit,
            author=mock.Mock(
                spec_set=application.Author, email='april.may@example.com'
            ),
            co_authors=[mock.Mock(spec_set=application.Author, email=None)],
        )

        errors = checks.author_has_email(commit)

        assert list(errors) == [
            """\
Commit co-author has no email.
""",
        ]

    def test_neither_author_has_email(self) -> None:
        commit = mock.Mock(
            spec_set=application.Commit,
            author=mock.Mock(spec_set=application.Author, email=None),
            co_authors=[mock.Mock(spec_set=application.Author, email=None)],
        )

        errors = checks.author_has_email(commit)

        assert list(errors) == [
            """\
Commit author has no email.

Make sure you have an author email set in your git config, e.g:

    git config user.email "your.name@example.com"
""",
            """\
Commit co-author has no email.
""",
        ]


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
