from game.ship import Ship
from game.dot import Dot

from enum import Enum


class CellState(str, Enum):
    MISS = "T"
    HIT = "X"
    UNDEFINED = "O"
    SHIP = "■"


class Board:
    def __init__(self, hid: bool, size: int = 6):
        self.hid = hid
        self.size = size
        self.ships = []

        self.cells: list[list[CellState]] = []
        self._generate_default_cells()

    @property
    def living_ships_count(self) -> int:
        return len([ship for ship in self.ships if ship.hp > 0])

    def out(self, dot: Dot) -> bool:
        return not (dot.x in range(0, self.size - 1) and dot.y in range(0, self.size - 1))

    def add_ship(self, ship: Ship):
        for dot in ship.dots:
            if self.out(dot):
                raise Exception("OUT ERROR")

            if self.get_dot_state(dot) is CellState.SHIP:
                raise Exception("Place is not free")

        for dot in ship.get_border_dots():
            try:
                if self.get_dot_state(dot) == CellState.SHIP:
                    raise Exception("Place is not free")
            except IndexError:
                continue

        for dot in ship.dots:
            self.set_dot_state(dot, CellState.SHIP)
        self.ships.append(ship)

    def shot(self, dot: Dot):
        if self.get_dot_state(dot) not in [CellState.SHIP, CellState.UNDEFINED]:
            raise Exception("You can`t shot in used cells")

        ship = self.get_ship_by_dot(dot)
        new_state = CellState.MISS
        if ship:
            ship.hp -= 1
            if ship.hp <= 0:
                self.contour(ship)

            new_state = CellState.HIT

        self.set_dot_state(dot, new_state)

    def is_still_alive(self) -> bool:
        return self.living_ships_count > 0

    def contour(self, ship: Ship):
        for dot in [dot for dot in ship.get_border_dots() if dot.x >= 0 and dot.y >= 0]:
            self.set_dot_state(dot, CellState.MISS)

    def get_ship_by_dot(self, dot: Dot) -> Ship | None:
        for ship in self.ships:
            if dot in ship.dots:
                return ship
        return None

    def get_dot_state(self, dot: Dot) -> CellState:
        return self.cells[dot.y][dot.x]

    def set_dot_state(self, dot: Dot, state: CellState) -> None:
        self.cells[dot.y][dot.x] = state

    def _generate_default_cells(self, default_state: CellState = CellState.UNDEFINED):
        for x in range(self.size):
            self.cells.append([])
            for y in range(self.size):
                self.cells[x].append(default_state)

    def __str__(self):
        s = ""
        for line_index, line in enumerate(self.cells):
            for dot_index, dot in enumerate(line):
                if dot is CellState.SHIP and self.hid:
                    s += CellState.UNDEFINED + " "
                    continue
                s += dot + " "
            s += "\n"
        return s


