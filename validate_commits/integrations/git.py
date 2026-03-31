from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import git


if TYPE_CHECKING:
    from collections.abc import Generator
    from collections.abc import Sequence


@attrs.frozen
class Commit:
    sha: str

    # Author
    author: Author
    co_authors: Sequence[Author]

    # Message
    summary: str

    # Content
    is_empty: bool


@attrs.frozen
class Author:
    name: str | None
    email: str | None


def _get_repo() -> git.Repo:
    return git.Repo(search_parent_directories=True)


@attrs.frozen
class Commits:
    _repo: git.Repo = attrs.field(factory=_get_repo)

    def __call__(self, since: str, to: str) -> Generator[Commit]:
        for commit in self._repo.iter_commits(f'{since}..{to}'):
            short_sha = self._repo.git.rev_parse(commit.hexsha, short=True)

            if isinstance(commit.summary, bytes):  # pragma: no cover
                commit_summary = commit.summary.decode()
            else:
                commit_summary = commit.summary

            changed_files = self._repo.git.diff_tree(
                commit.hexsha, no_commit_id=True, name_only=True, r=True
            )

            yield Commit(
                sha=short_sha,
                author=Author(
                    name=commit.author.name,
                    email=commit.author.email,
                ),
                co_authors=[
                    Author(
                        name=co_author.name,
                        email=co_author.email,
                    )
                    for co_author in commit.co_authors
                ],
                summary=commit_summary,
                is_empty=not bool(changed_files),
            )
