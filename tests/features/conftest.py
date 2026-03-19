from __future__ import annotations

from typing import TYPE_CHECKING

import git
import pytest

from tests import helpers


if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def cli(tmp_path: Path) -> helpers.CLI:
    return helpers.CLI(tmp_path)


@pytest.fixture
def git_repo(tmp_path: Path) -> helpers.GitRepo:
    repo = git.Repo.init(tmp_path)
    repo.git.commit(allow_empty=True, message='initial')
    return helpers.GitRepo(repo)
