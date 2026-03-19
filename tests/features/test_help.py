from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING
from unittest import mock

import pytest


if TYPE_CHECKING:
    from tests import helpers


def test_help_is_in_readme(
    cli: helpers.CLI, capsys: pytest.CaptureFixture[str]
) -> None:
    with (
        # Patching is required to ensure colours are not used in Python >= 3.14.
        mock.patch.dict(os.environ, {'NO_COLOR': '1'}),  # noqa: TID251
        pytest.raises(SystemExit) as exc_info,
    ):
        cli('--help')

    assert exc_info.value.code == 0

    stdout, _ = capsys.readouterr()
    assert stdout in _read_readme()


def _read_readme() -> str:
    repo_root = Path(__file__).parent.parent.parent
    return (repo_root / 'README.md').read_text()
