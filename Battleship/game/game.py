import time

from game.board import Board
from game.dot import Dot
from game.player import User, AI, Player
from game.ship import Ship

from random import randint, choice

SHIP_SIZES = (3, 2, 2, 1, 1, 1)
ATTEMPTS_LIMIT = 600


class Game:
    def __init__(self):
        self.user_board = self.random_board(False)
        self.ai_board = self.random_board(True)

        self.ai = AI("AI", self.ai_board, self.user_board)
        self.user = User("User", self.user_board, self.ai_board)

        self.players = [self.ai, self.user]

    @staticmethod
    def random_board(hid: bool) -> Board:
        def try_generate():
            board = Board(hid)
            for size in SHIP_SIZES:
                tries = 0
                while tries < ATTEMPTS_LIMIT:
                    try:
                        board.add_ship(
                            Ship(Dot(randint(0, board.size), randint(0, board.size)), size, choice([True, False])))
                        break
                    except:
                        tries += 1
                else:
                    return
            return board

        gen = None
        while gen is None:
            gen = try_generate()
        return gen

    def greet(self):
        name = input("Введите своё имя:\n")

        if len(name) == 0:
            print(":(")
        else:
            print("Привет,", name)
            self.user.name = name
        time.sleep(0.3)

        print(
            """
        ===== BATTLESHIP =====
        ======= ПРАВИЛА ======
        1. Запрещено ходить в
        одни и те же клетки.
        2. Пример ввода клетки:
        2 1 - значит, ход будет
        осуществлятся во второй
        ряд и первый столбец. 
        """
        )

        input("Готов?")

    def _make_move(self, player: Player):

        if self.may_end_game(player):
            return True

        self.print_boards()
        print(self.may_end_game(player))
        if player.move():
            player.notify("Вы можете совершить ещё ход")
            print(f"{player.name} совершает ещё ход")
            self.print_boards()
            return self._make_move(player)
        return self.may_end_game(player)




    def may_end_game(self, player: Player):
        print(player.enemy_board.is_still_alive())
        return not player.enemy_board.is_still_alive()


    def print_boards(self):
        print(self.user, self.ai, sep="\n\n")

    def try_to_congratulate_player(self, player: Player):
        print(player.enemy_board.living_ships_count, "ЛОДКИ КОРАБЛЯ ВРАГА", player.name)
        if self.may_end_game(player):
            player.notify("поздравляем с победой")
            print(f"Игрок {player.name} победил")
            return True
        return False

    def loop(self):
        def move(player):
            if self.try_to_congratulate_player(player):
                return
            self.print_boards()
            print(player.enemy_board.living_ships_count)
            print(f"{player.name} ходит...")
            player.notify("Ваш ход")
            return player.move()



        while True:
            for player in self.players:
                self.print_boards()

                next_move = True
                while next_move:
                    next_move = move(player)
                    if next_move is None:
                        return


                player.notify("Вы сделали ход")
                print(f"{player.name} сделал ход!")

    def start(self):
        self.greet()
        self.loop()
