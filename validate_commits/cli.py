from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Sequence


def main(_: Sequence[str] | None = None) -> int:
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
