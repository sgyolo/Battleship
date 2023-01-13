from game.dot import Dot

class Ship:
    def __init__(self, start_dot: Dot, length: int, is_horizontal: bool):
        self.start_dot = start_dot
        self.length = self.hp = length
        self.is_horizontal = is_horizontal

    @property
    def dots(self) -> list[Dot]:
        return list(self._get_dots_generator)

    def get_border_dots(self) -> list[Dot]:
        dots = set()
        for dot in self.dots:
            dots.add(Dot(dot.x + 1, dot.y))
            dots.add(Dot(dot.x - 1, dot.y))
            dots.add(Dot(dot.x, dot.y + 1))
            dots.add(Dot(dot.x, dot.y - 1))

            dots.add(Dot(dot.x - 1, dot.y - 1))
            dots.add(Dot(dot.x - 1, dot.y + 1))
            dots.add(Dot(dot.x + 1, dot.y + 1))
            dots.add(Dot(dot.x + 1, dot.y - 1))


        return [dot for dot in dots if dot not in self.dots]

    @property
    def _get_dots_generator(self):
        if self.is_horizontal:
            for i in range(self.start_dot.x, self.start_dot.x + self.length):
                yield Dot(i, self.start_dot.y)
        else:
            for i in range(self.start_dot.y, self.start_dot.y + self.length):
                yield Dot(self.start_dot.x, i)

