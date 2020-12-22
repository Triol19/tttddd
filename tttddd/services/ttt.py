# type: ignore
from typing import List

from tttddd.domain.move import Move, WrongMove


class TTT:
    def __init__(
            self,
            moves: List[Move],
            size: int,
            x: int,
            y: int,
    ) -> None:
        self.__moves = moves
        self.__size = size
        self.__x = x
        self.__y = y

        self.__board = None

    @staticmethod
    def _tac_or_toe(index: int) -> int:
        return 1 if index else 0

    def validate_and_move(self) -> None:
        index = 0
        self.__board = [
            [None for _ in range(self.__size)] for _ in range(self.__size)
        ]

        for index, move in enumerate(self.__moves):
            self.__board[move.x][move.y] = self._tac_or_toe(index)

        try:
            if self.__board[self.__x][self.__y] is not None:
                raise WrongMove(x=self.__x, y=self.__x)
        except IndexError:
            raise WrongMove(x=self.__x, y=self.__x)
        self.__board[self.__x][self.__y] = self._tac_or_toe(index + 1)

    def is_finished(self) -> bool:
        transpositions = [
            self.__board,
            zip(*self.__board),
        ]
        winner_combinations = [
            '000',
            '111',
        ]

        for transposition in transpositions:
            for row in transposition:
                for combination in winner_combinations:
                    if combination in ''.join(map(str, row)):
                        return True
        return False
