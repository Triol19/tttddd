from pydantic import PydanticValueError

__all__ = (
    'WrongMove',
    'WrongOrder',
    'WrongUser',
)


class WrongUser(PydanticValueError):
    code = 'wrong_user'
    msg_template = '{user}'

    def __init__(self, *, user: str) -> None:
        super().__init__(user=user)


class WrongOrder(PydanticValueError):
    code = 'wrong_order'
    msg_template = '{user}'

    def __init__(self, *, user: str) -> None:
        super().__init__(user=user)


class WrongMove(PydanticValueError):
    code = 'wrong_move'
    msg_template = 'X={x}; Y={y}'

    def __init__(self, *, x: int, y: int) -> None:
        super().__init__(x=x, y=y)
