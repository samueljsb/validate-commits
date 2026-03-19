from __future__ import annotations

from typing import TYPE_CHECKING

import git

from tests import helpers
from validate_commits.integrations import git as git_integration


if TYPE_CHECKING:
    from pathlib import Path


def git_repo(path: Path) -> git.Repo:
    repo = git.Repo.init(path, initial_branch='main')
    repo.git.commit(allow_empty=True, message='initial')
    return repo


class TestCommits:
    def test_no_commits(self, tmp_path: Path) -> None:
        repo = git_repo(tmp_path)
        git_helper = helpers.GitRepo(repo)
        git_helper.checkout_new_branch('my-branch')

        get_commits = git_integration.Commits(repo)

        commits = list(get_commits(since='main', to='HEAD'))

        assert commits == []

    def test_commits(self, tmp_path: Path) -> None:
        repo = git_repo(tmp_path)
        git_helper = helpers.GitRepo(repo)
        git_helper.checkout_new_branch('my-branch')
        git_helper.change_file('a')
        first_sha = git_helper.commit(
            'First commit message', author='April May <april.may@example.com>'
        )
        empty_sha = git_helper.commit(
            'Empty commit',
            author='Andy Skampt <andy.skampt@example.com>',
            allow_empty=True,
        )

        get_commits = git_integration.Commits(repo)

        commits = list(get_commits(since='main', to='HEAD'))

        assert commits == [
            git_integration.Commit(
                sha=empty_sha,
                author_name='Andy Skampt',
                author_email='andy.skampt@example.com',
                summary='Empty commit',
                is_empty=True,
            ),
            git_integration.Commit(
                sha=first_sha,
                author_name='April May',
                author_email='april.may@example.com',
                summary='First commit message',
                is_empty=False,
            ),
        ]
