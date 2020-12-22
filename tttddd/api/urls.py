from fastapi import APIRouter

from .health_check import router as health_check
from .v1 import urls as v1_urls

__all__ = ('router',)

router = APIRouter()
router.include_router(v1_urls.router, prefix='/v1', tags=['v1'])
router.include_router(health_check)
