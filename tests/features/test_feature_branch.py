from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pytest

    from tests import helpers


def test_nothing_to_check_if_no_commits(
    git_repo: helpers.GitRepo, cli: helpers.CLI, capsys: pytest.CaptureFixture[str]
) -> None:
    git_repo.checkout_new_branch('my-feature')

    ret = cli()

    assert ret == 1

    stdout, stderr = capsys.readouterr()
    assert stdout == ''
    assert (
        stderr
        == """\
No commits between 'main' and 'HEAD'.
"""
    )


def test_no_errors_in_one_commit(
    git_repo: helpers.GitRepo,
    cli: helpers.CLI,
    capsys: pytest.CaptureFixture[str],
) -> None:
    git_repo.checkout_new_branch('my-feature')

    git_repo.change_file('a')
    git_repo.commit()

    ret = cli()

    assert ret == 0

    stdout, stderr = capsys.readouterr()
    assert stdout == ''
    assert (
        stderr
        == """\
No issues found in 1 commits between 'main' and 'HEAD'.
"""
    )


def test_commit_with_missing_required_information(
    git_repo: helpers.GitRepo,
    cli: helpers.CLI,
    capsys: pytest.CaptureFixture[str],
) -> None:
    git_repo.checkout_new_branch('my-feature')

    commit_sha = git_repo.commit(
        message='A bad commit', author='Andy Skampt <>', allow_empty=True
    )

    ret = cli()

    assert ret == 1

    stdout, stderr = capsys.readouterr()
    assert (
        stdout
        == f"""\
error: {commit_sha} (A bad commit)
    Commit author 'Andy Skampt' has no email.

    Make sure you have an author email set in your git config, e.g:

        git config user.email "your.name@example.com"
error: {commit_sha} (A bad commit)
    Commit is empty.
"""
    )
    assert (
        stderr
        == """\
Found 2 errors in 1 commits between 'main' and 'HEAD' (checked 1 commits).
"""
    )


def test_fixup_commit(
    git_repo: helpers.GitRepo,
    cli: helpers.CLI,
    capsys: pytest.CaptureFixture[str],
) -> None:
    git_repo.checkout_new_branch('my-feature')

    git_repo.change_file('a')
    commit_sha = git_repo.commit(message='fixup! Some other commit')

    ret = cli()

    assert ret == 1

    stdout, stderr = capsys.readouterr()
    assert (
        stdout
        == f"""\
error: {commit_sha} (fixup! Some other commit)
    Fixup commit.
"""
    )
    assert (
        stderr
        == """\
Found 1 errors in 1 commits between 'main' and 'HEAD' (checked 1 commits).
"""
    )
