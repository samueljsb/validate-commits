from __future__ import annotations

import tomllib
from typing import TYPE_CHECKING

import attrs
import cattrs


if TYPE_CHECKING:
    from pathlib import Path


@attrs.frozen
class Check:
    pattern: str
    message: str


@attrs.frozen
class Checks:
    summary: tuple[Check, ...] = ()


@attrs.frozen
class Config:
    checks: Checks = attrs.field(factory=Checks)


def load_from_file(config_file: Path) -> Config:
    try:
        file_content = config_file.read_text()
    except FileNotFoundError:
        return Config()

    data = tomllib.loads(file_content)
    return cattrs.structure(data, Config)
