from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pathlib import Path

    import pytest

    from tests import helpers


def test_commit_summary_regexp(
    tmp_path: Path,
    git_repo: helpers.GitRepo,
    cli: helpers.CLI,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_file = tmp_path / '.validate-commits-config.toml'
    config_file.write_text(r"""
[[checks.summary]]
pattern = '\d'
message = "Numbers in commit summary."
""")

    git_repo.checkout_new_branch('my-feature')
    git_repo.change_file('a')
    commit_sha = git_repo.commit('There is 1 change in this commit')

    ret = cli()

    assert ret == 1

    stdout, stderr = capsys.readouterr()
    assert (
        stdout
        == f"""\
error: {commit_sha} (There is 1 change in this commit)
    Numbers in commit summary.
"""
    )
    assert (
        stderr
        == """\
Found 1 errors in 1 commits between 'main' and 'HEAD' (checked 1 commits).
"""
    )


def test_author_email_regexp(
    tmp_path: Path,
    git_repo: helpers.GitRepo,
    cli: helpers.CLI,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_file = tmp_path / '.validate-commits-config.toml'
    config_file.write_text(r"""
[[checks.author_email]]
pattern = '@example\.com$'
message = "Fake email address provided."
""")

    git_repo.checkout_new_branch('my-feature')
    git_repo.change_file('a')
    commit_sha = git_repo.commit(
        message='A commit', author='April May <april.may@example.com>'
    )

    ret = cli()

    assert ret == 1

    stdout, stderr = capsys.readouterr()
    assert (
        stdout
        == f"""\
error: {commit_sha} (A commit)
    Fake email address provided.
"""
    )
    assert (
        stderr
        == """\
Found 1 errors in 1 commits between 'main' and 'HEAD' (checked 1 commits).
"""
    )
