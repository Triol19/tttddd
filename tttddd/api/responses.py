from typing import Any

from fastapi import responses

from tttddd.core.json import dumps

__all__ = ('JSONResponse',)


class JSONResponse(responses.JSONResponse):
    def render(self, content: Any) -> bytes:
        return dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
