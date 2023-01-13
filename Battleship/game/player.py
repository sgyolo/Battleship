from abc import ABC, abstractmethod
from game.dot import Dot
from game.board import Board, CellState
from random import randint


class Player(ABC):
    def __init__(self, name: str, board: Board, enemy_board: Board):
        self.name = name
        self.board = board
        self.enemy_board = enemy_board

    @abstractmethod
    def ask(self) -> Dot:
        pass

    @abstractmethod
    def notify(self, message: str) -> None:
        pass

    def move(self) -> bool | None:
        while True:
            try:
                dot = self.ask()
                self.enemy_board.shot(dot)
                if self.enemy_board.get_dot_state(dot) is CellState.HIT:
                    return True
                return False
            except Exception as e:
                self.notify(e)
                continue

    def __str__(self):
        return f'Доска игрока {self.name}\n\n{self.board}'


class AI(Player):
    def ask(self) -> Dot:
        return Dot(randint(0, self.enemy_board.size - 1), randint(0, self.enemy_board.size - 1))

    def notify(self, message: str) -> None:
        pass


class User(Player):
    def ask(self) -> Dot:
        x, y = map(int, input("Введите ваш ход:\n").split())
        x -= 1
        y -= 1

        return Dot(x, y)

    def notify(self, message: str) -> None:
        print(f"{self.name}!\n{message}")