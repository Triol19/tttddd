import json
from datetime import date
from enum import Enum
from json import JSONEncoder
from typing import Any, Dict, List, Union
from uuid import UUID

__all__ = (
    'dumps',
    'loads',
)


class ExtendedJSONEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, date):
            return str(obj)
        else:
            return super().default(obj)


def dumps(obj: Union[Dict[Any, Any], List[Any]], **kwargs: Any) -> str:
    kwargs.setdefault('cls', ExtendedJSONEncoder)
    return json.dumps(obj, **kwargs)


loads = json.loads
