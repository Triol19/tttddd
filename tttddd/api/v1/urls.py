from fastapi import APIRouter

from .endpoints import game, move

__all__ = ('router',)

router = APIRouter()
router.include_router(game.router)
router.include_router(move.router)
