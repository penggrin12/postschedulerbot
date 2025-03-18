from __future__ import annotations

import logging

logger: logging.Logger = logging.getLogger(__name__)


def setup() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
