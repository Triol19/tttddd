from collections import defaultdict
from typing import Any, Dict, List, Tuple, Union

from fastapi import HTTPException, Request, status
from fastapi.exception_handlers import (
    http_exception_handler as default_http_exception_handler,
)
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse
from funcy import first, last, rest

from .exception import InternalServerError

__all__ = (
    'extract_type',
    'loc',
    'http_exception_handler',
    'request_validation_error_handler',
    'validation_error_handler',
    'internal_server_error_handler',
)


error_place_to_field: Dict[str, str] = defaultdict(
    lambda: 'fields',
    header='headers',
    cookie='cookies',
)


def extract_type(exc: Exception) -> str:
    return exc.__class__.__name__.upper()


def loc(seq: Tuple[Union[str, int], ...]) -> str:
    #  remove from seq items like __root__ for root_validator
    seq = tuple(filter(lambda x: not str(x).startswith('_'), seq))
    return '.'.join(map(str, rest(seq)))


def error_place(seq: Tuple[str, ...]) -> str:
    return error_place_to_field[first(seq)]


async def http_exception_handler(
        request: Request, exc: HTTPException,
) -> JSONResponse:
    if 300 > exc.status_code >= 200:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return await default_http_exception_handler(request, exc)


async def request_validation_error_handler(
        _: Request,
        exc: RequestValidationError
) -> JSONResponse:
    return validation_errors_processing(exc.errors(), via_request=True)


async def validation_error_handler(
        _: Request,
        exc: ValidationError,
) -> JSONResponse:
    return validation_errors_processing(exc.errors(), via_request=False)


def validation_errors_processing(
        errors: List[Dict[str, Any]],
        via_request: bool,
) -> JSONResponse:
    details: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    content = {
        'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'error': {
            'message': 'VALUE_ERROR',
            'type': 'VALIDATION_ERROR',
            'details': details,
        }
    }

    for error in errors:
        details[error_place(error['loc'])].append(
            {
                'name': loc(error['loc']) if via_request else error['loc'][0],
                'reason': {
                    'type': last(error['type'].split('.')).upper(),
                    'message': error['msg'],
                }
            }
        )

    return JSONResponse(
        content=content,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def internal_server_error_handler(
        _: Request,
        exc: InternalServerError
) -> JSONResponse:
    content = {
        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'error': {
            'message': 'INTERNAL_SERVER_ERROR',
            'type': extract_type(exc),
            'details': {'error': str(exc)},
        }
    }

    return JSONResponse(
        content=content,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
