from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional, Protocol


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class Renderer(Protocol):
    def render(self, origin: BasicPoint):
        """bob was here"""


class BasicPoint:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def get(self):
        return self.x, self.y

    def __add__(self, other: BasicPoint):
        total = BasicPoint(
            self.x + other.x,
            self.y + other.y
        )
        return total

    def __str__(self):
        return f"[{self.x}, {self.y}]"


class BasicPath:
    def __init__(self, x: float, y: float):
        self.origin: BasicPoint = BasicPoint(x, y)
        self.points: List[BasicPoint] = []

    def add(self, x: float, y: float):
        self.points.append(BasicPoint(x, y))

    def copy(self, x: float, y: float):
        new_path = BasicPath(x, y)
        new_path.points = self.points
        return new_path

    def render(self, origin: BasicPoint):
        origin = origin +  self.origin
        for i, point in enumerate(self.points, 1):
            print(f"{i}: {point + origin}")


class SvgPath:
    def __init__(self, origin: Optional[BasicPoint] = None):
        self.origin = origin
        self.paths: List[BasicPath] = []

    def new_path(self, x: float, y: float):
        path = BasicPath(x, y)
        self.paths.append(path)
        return path

    def copy_path(self, x: float, y: float, path: BasicPath):
        new_path = path.copy(x, y)
        self.paths.append(new_path)

    def render(self, origin: BasicPoint):
        origin = origin +  self.origin
        for path in self.paths:
            path.render(origin)


class SvgGroup:
    def __init__(self, origin: Optional[BasicPoint] = None):
        self.origin = origin
        self.svg_items: List[Renderer] = []

    def add_svg_item(self, item: Renderer):
        self.svg_items.append(item)

    def render(self, origin: Optional[BasicPoint] = None):
        origin = origin or BasicPoint(0,0)
        origin += self.origin
        for svg_item in self.svg_items:
            svg_item.render(origin)


def main():
    svg_path = SvgPath(BasicPoint(0, 0))

    path = svg_path.new_path(10, 10)
    path.add(50, 0)
    path.add(50, 50)
    path.add(0, 50)
    path.add(0, 0)

    svg_path.copy_path(20,100, path)

    svg_path.render(BasicPoint(0,0))


class Turtle:
    def __init__(self, x: float = 0, y: float = 0, direction = Direction.EAST):
        self.x = self.y = self.direction = None
        self.start(x, y, direction)

    def start(self, x: float = 0, y: float = 0, direction = Direction.EAST):
        self.x = x
        self.y = y
        self.direction = direction

    def left(self):
        if self.direction is Direction.NORTH:
            self.direction = Direction.WEST
        elif self.direction is Direction.SOUTH:
            self.direction = Direction.EAST
        elif self.direction is Direction.EAST:
            self.direction = Direction.NORTH
        else:
            self.direction = Direction.SOUTH

    def right(self):
        if self.direction is Direction.NORTH:
            self.direction = Direction.EAST
        elif self.direction is Direction.SOUTH:
            self.direction = Direction.WEST
        elif self.direction is Direction.EAST:
            self.direction = Direction.SOUTH
        else:
            self.direction = Direction.NORTH

    def forward(self, n: float):
        if self.direction is Direction.NORTH:
            self.x -= n
        elif self.direction is Direction.SOUTH:
            self.x += n
        elif self.direction is Direction.EAST:
            self.y += n
        else:
            self.y -= n

    def finish(self):
        pass

    def left_forward(self, n: float):
        self.left()
        self.forward(n)

    def right_forard(self, n: float):
        self.right()
        self.forward(n)


if __name__ == "__main__":
    main()
