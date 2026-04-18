from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pytest

    from tests import helpers


def test_nothing_to_check_if_no_commits(
    git_repo: helpers.GitRepo, cli: helpers.CLI, capsys: pytest.CaptureFixture[str]
) -> None:
    # Create a commit on a base branch.
    git_repo.checkout_new_branch('my-base')
    git_repo.commit(allow_empty=True)

    # Create an empty feature branch.
    git_repo.checkout_new_branch('my-feature')

    ret = cli('--since', 'my-base')

    assert ret == 1

    stdout, stderr = capsys.readouterr()
    assert stdout == ''
    assert (
        stderr
        == """\
No commits between 'my-base' and 'HEAD'.
"""
    )


def test_no_errors_in_one_commit(
    git_repo: helpers.GitRepo,
    cli: helpers.CLI,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Create a commit on a base branch.
    git_repo.checkout_new_branch('my-base')
    git_repo.commit(allow_empty=True)

    # Create a feature branch with one commit.
    git_repo.checkout_new_branch('my-feature')
    git_repo.change_file('a')
    git_repo.commit()

    ret = cli('--since', 'my-base')

    assert ret == 0

    stdout, stderr = capsys.readouterr()
    assert stdout == ''
    assert (
        stderr
        == """\
No issues found in 1 commits between 'my-base' and 'HEAD'.
"""
    )


def test_fixup_commit(
    git_repo: helpers.GitRepo,
    cli: helpers.CLI,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Create a commit on a base branch.
    git_repo.checkout_new_branch('my-base')
    git_repo.commit(allow_empty=True)

    # Create a feature branch with one commit.
    git_repo.checkout_new_branch('my-feature')
    git_repo.change_file('a')
    commit_sha = git_repo.commit(message='fixup! Some other commit')

    ret = cli('--since', 'my-base')

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
Found 1 errors in 1 commits between 'my-base' and 'HEAD' (checked 1 commits).
"""
    )
