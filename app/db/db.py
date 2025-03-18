from __future__ import annotations

from piccolo.engine.sqlite import SQLiteEngine

__all__: list[str] = ["db"]


db = SQLiteEngine()
