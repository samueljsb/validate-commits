from __future__ import annotations

import contextlib
from pathlib import Path
from typing import TYPE_CHECKING

import attrs

from validate_commits import cli


if TYPE_CHECKING:
    import git


@attrs.mutable
class GitRepo:
    _repo: git.Repo

    author: str = 'April May <april.may@example.com>'

    def checkout_new_branch(self, name: str) -> None:
        self._repo.create_head(name).checkout()

    def change_file(self, file_name: str) -> None:
        new_file = Path(self._repo.working_dir) / file_name
        new_file.touch()
        self._repo.git.add([new_file])

    def commit(
        self,
        message: str = 'A commit message',
        *,
        author: str | None = None,
        allow_empty: bool = False,
    ) -> str:
        if author is None:
            author = self.author

        self._repo.git.commit(message=message, author=author, allow_empty=allow_empty)
        commit_sha = self._repo.commit().hexsha
        short_sha: str = self._repo.git.rev_parse(commit_sha, short=True)
        return short_sha


@attrs.frozen
class CLI:
    cwd: Path

    def __call__(self, *options: str) -> int:
        with contextlib.chdir(self.cwd):
            return cli.main(options)
