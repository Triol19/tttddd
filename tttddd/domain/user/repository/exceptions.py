from pydantic import PydanticValueError

__all__ = (
    'UserNotFound',
)


class UserNotFound(PydanticValueError):
    code = 'user_not_found'
    msg_template = '{user}'

    def __init__(self, *, user: str) -> None:
        super().__init__(user=user)
