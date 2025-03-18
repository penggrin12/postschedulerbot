from __future__ import annotations

from typing import TypeVar


T = TypeVar("T")


def n(x: T | None) -> T:
    return x  # type: ignore
