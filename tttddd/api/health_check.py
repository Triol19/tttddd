import asyncio

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import StatementError
from sqlalchemy.orm.session import Session

from tttddd.injector import injector

router = APIRouter()


async def db_connection_exists() -> bool:
    session = injector.get(Session)

    try:
        session.execute('SELECT 1')
    except StatementError:
        return False

    return True


@router.get('/health_check')
async def health_check() -> JSONResponse:
    if not all(await asyncio.gather(
        db_connection_exists(),
    )):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JSONResponse(status_code=status.HTTP_200_OK)
