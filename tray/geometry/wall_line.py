from __future__ import annotations

from enum import IntEnum
from typing import TypeVar, SupportsFloat
from tray.geometry.line import Line, LineOrientation, Point

T = TypeVar("T", bound=SupportsFloat)


class WallType(IntEnum):
    def __new__(cls, value: int, label: str):
        obj = int.__new__(cls, value)  # create the enum member as an int
        obj._value_ = value
        obj._label_ = label
        return obj

    NONE = (0, "none")
    INTERIOR = (1, "interior")
    EXTERIOR = (2, "exterior")
    COMBO = (3, "combo")

    @property
    def label(self) -> str:
        return self._label_


class WallLine(Line[T]):
    def __init__(self, p1: Point[T], p2: Point[T], wall_type: WallType = WallType.NONE) -> None:
        super().__init__(p1, p2)
        self.wall_type: WallType = wall_type

    def classify_wall(self, path_line: Line[T], orientation: LineOrientation) -> WallType:
        (w1, w2) = self.normalize
        (p1, p2) = path_line.normalize

        if orientation == LineOrientation.HORZ:
            w1, w2 = w1.x, w2.x
            p1, p2 = p1.x, p2.x
        elif orientation == LineOrientation.VERT:
            w1, w2 = w1.y, w2.y
            p1, p2 = p1.y, p2.y
        else:
            raise ValueError("orientation must be either vertical or horizontal")

        col = self.is_collinear(path_line)

        match col:
            case False:
                return WallType.INTERIOR

            # w completely below p OR completely above p (including touching at endpoints)
            case True if (w2 <= p1) or (w1 >= p2):
                return WallType.INTERIOR

            # partial overlap on one side -> "combo"
            case True if (w1 < p1 < w2 < p2) or (p1 < w1 < p2 < w2):
                return WallType.COMBO

            case True if (w1 == p1 and w2 > p2) or (w2 == p2 and w1 < p1):
                return WallType.COMBO

            case True if w1 < p1 and w2 > p2:
                return WallType.COMBO

            # w within p or equal -> "exterior" per your original mapping
            case True if (w1 == p1 and w2 < p2) or (w2 == p2 and w1 > p1):
                return WallType.EXTERIOR

            case True if p1 < w1 and w2 < p2:
                return WallType.EXTERIOR

            case True if w1 == p1 and w2 == p2:
                return WallType.EXTERIOR

            case _:
                raise ValueError("Unhandled collinear configuration")
