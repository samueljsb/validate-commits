from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests import helpers


if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def cli(tmp_path: Path) -> helpers.CLI:
    return helpers.CLI(tmp_path)


@pytest.fixture
def git_repo(tmp_path: Path) -> helpers.GitRepo:
    repo = helpers.new_git_repo(tmp_path)
    return helpers.GitRepo(repo)
