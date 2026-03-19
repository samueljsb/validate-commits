from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
import git


if TYPE_CHECKING:
    from collections.abc import Generator


@attrs.frozen
class Commit:
    sha: str

    # Author
    author_name: str
    author_email: str

    # Message
    summary: str

    # Content
    is_empty: bool


def _get_repo() -> git.Repo:
    return git.Repo(search_parent_directories=True)


@attrs.frozen
class Commits:
    _repo: git.Repo = attrs.field(factory=_get_repo)

    def __call__(self, since: str, to: str) -> Generator[Commit]:
        for commit in self._repo.iter_commits(f'{since}...{to}'):
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
                author_name=commit.author.name or '',
                author_email=commit.author.email or '',
                summary=commit_summary,
                is_empty=not bool(changed_files),
            )
