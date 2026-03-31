from __future__ import annotations

from typing import TYPE_CHECKING

from validate_commits.integrations import configuration


if TYPE_CHECKING:
    from pathlib import Path


class TestLoadConfig:
    def test_file_not_found(self, tmp_path: Path) -> None:
        config_file = tmp_path / '.validate-commits-config.toml'

        config = configuration.load_from_file(config_file)

        assert config == configuration.Config(
            checks=configuration.Checks(
                summary=(),
            ),
        )

    def test_empty_file(self, tmp_path: Path) -> None:
        config_file = tmp_path / '.validate-commits-config.toml'
        config_file.write_text('')

        config = configuration.load_from_file(config_file)

        assert config == configuration.Config(
            checks=configuration.Checks(
                summary=(),
            ),
        )

    def test_full_config(self, tmp_path: Path) -> None:
        config_file = tmp_path / '.validate-commits-config.toml'
        config_file.write_text(r"""
[[checks.summary]]
pattern = '\d'
message = "Numbers in commit summary."

[[checks.summary]]
pattern = '\.$'
message = "Ends with a full stop."
""")

        config = configuration.load_from_file(config_file)

        assert config == configuration.Config(
            checks=configuration.Checks(
                summary=(
                    configuration.Check(
                        pattern=r'\d',
                        message='Numbers in commit summary.',
                    ),
                    configuration.Check(
                        pattern=r'\.$',
                        message='Ends with a full stop.',
                    ),
                ),
            ),
        )
