from typing import cast

from fastapi import FastAPI
from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
    ValidationError,
)
from sqlalchemy.orm import Session
from starlette.types import ASGIApp

from tttddd.api.urls import router
from tttddd.core.conf import settings
from tttddd.core.database import AsyncDBEngine
from tttddd.core.error import (
    http_exception_handler,
    internal_server_error_handler,
    request_validation_error_handler,
    validation_error_handler,
)
from tttddd.core.exception import InternalServerError
from tttddd.injector import injector

__all__ = ('create_app',)


def create_app() -> ASGIApp:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        root_path='/',
        on_startup=[
            injector.get(AsyncDBEngine).connect,
        ],
        on_shutdown=[
            injector.get(AsyncDBEngine).disconnect,
            injector.get(Session).close
        ],
    )

    app.include_router(router)
    app.add_exception_handler(
        InternalServerError,
        internal_server_error_handler,
    )
    app.add_exception_handler(
        RequestValidationError,
        request_validation_error_handler,
    )
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)

    return cast(ASGIApp, app)
