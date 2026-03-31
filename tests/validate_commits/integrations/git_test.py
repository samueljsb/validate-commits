from __future__ import annotations

from typing import TYPE_CHECKING

from tests import helpers
from validate_commits.integrations import git as git_integration


if TYPE_CHECKING:
    from pathlib import Path


class TestCommits:
    def test_no_commits(self, tmp_path: Path) -> None:
        repo = helpers.new_git_repo(tmp_path)
        git_helper = helpers.GitRepo(repo)
        git_helper.checkout_new_branch('my-branch')

        get_commits = git_integration.Commits(repo)

        commits = list(get_commits(since='main', to='HEAD'))

        assert commits == []

    def test_commits(self, tmp_path: Path) -> None:
        repo = helpers.new_git_repo(tmp_path)
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
        co_authored_sha = git_helper.commit(
            """\
Commit with co-authors

Co-authored-by: Andy Skampt <andy.skampt@example.com>
Co-authored-by: Miranda Beckwith <miranda.beckwith@example.com>
""",
            author='April May <april.may@example.com>',
            allow_empty=True,
        )

        get_commits = git_integration.Commits(repo)

        commits = list(get_commits(since='main', to='HEAD'))

        assert commits == [
            git_integration.Commit(
                sha=co_authored_sha,
                author=git_integration.Author(
                    name='April May',
                    email='april.may@example.com',
                ),
                co_authors=[
                    git_integration.Author(
                        name='Andy Skampt',
                        email='andy.skampt@example.com',
                    ),
                    git_integration.Author(
                        name='Miranda Beckwith',
                        email='miranda.beckwith@example.com',
                    ),
                ],
                summary='Commit with co-authors',
                is_empty=True,
            ),
            git_integration.Commit(
                sha=empty_sha,
                author=git_integration.Author(
                    name='Andy Skampt',
                    email='andy.skampt@example.com',
                ),
                co_authors=[],
                summary='Empty commit',
                is_empty=True,
            ),
            git_integration.Commit(
                sha=first_sha,
                author=git_integration.Author(
                    name='April May',
                    email='april.may@example.com',
                ),
                co_authors=[],
                summary='First commit message',
                is_empty=False,
            ),
        ]

    def test_commits_when_branch_behind_main(self, tmp_path: Path) -> None:
        """
        Unrelated commits are ignored.

        When there are commits on 'main' *after* the current branch diverged,
        they should not be reported.
        """
        repo = helpers.new_git_repo(tmp_path)
        git_helper = helpers.GitRepo(repo)
        # Create a base commit that can be branched from.
        base = git_helper.commit(allow_empty=True)
        # Add another commit on 'main' after the base commit.
        git_helper.commit('This commit should be ignored', allow_empty=True)

        # Create a new branch from the base commit.
        git_helper.checkout_new_branch('my-branch', base=base)
        commit_sha = git_helper.commit(
            'A commit message',
            author='April May <april.may@example.com>',
            allow_empty=True,
        )

        get_commits = git_integration.Commits(repo)

        commits = list(get_commits(since='main', to='HEAD'))

        # Only the commit on 'my-branch' is retrieved.
        assert commits == [
            git_integration.Commit(
                sha=commit_sha,
                author=git_integration.Author(
                    name='April May',
                    email='april.may@example.com',
                ),
                co_authors=[],
                summary='A commit message',
                is_empty=True,
            ),
        ]
