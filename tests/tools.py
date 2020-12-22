from typing import Any
from unittest.mock import Mock

import funcy

__all__ = (
    'first',
)


def first(mock_method: Mock) -> Any:
    return funcy.first(mock_method.call_args.args)
