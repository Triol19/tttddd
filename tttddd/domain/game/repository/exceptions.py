from pydantic import PydanticValueError

__all__ = (
    'GameAlreadyFinished',
    'GameNotFound',
)


class GameNotFound(PydanticValueError):
    code = 'game_not_found'
    msg_template = '{game}'

    def __init__(self, *, game: str) -> None:
        super().__init__(game=game)


class GameAlreadyFinished(PydanticValueError):
    code = 'game_finished'
    msg_template = '{game}'

    def __init__(self, *, game: str) -> None:
        super().__init__(game=game)
