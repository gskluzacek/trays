from __future__ import annotations

from enum import Enum
from typing import Generic, SupportsFloat, TypeVar

T = TypeVar("T", bound=SupportsFloat)

class PathOrientation(Enum):
    CW = "clockwise"
    CCW = "counter_clockwise"
    COL = "collinear"
    NONE = "none"

class LineOrientation(Enum):
    VERT = "vertical"
    HORZ = "horizontal"
    NONE = "none"

class Point(Generic[T]):
    def __init__(self, x: T, y: T) -> None:
        self.x = x
        self.y = y
        # these private attributes are used at the line level and are accessed via the line's property not the point's property
        self._line_orientation = LineOrientation.NONE

    @property
    def line_orientation(self) -> LineOrientation:
        return self._line_orientation

    @line_orientation.setter
    def line_orientation(self, value: LineOrientation) -> None:
        self._line_orientation = value

    def set_line_orientation(self, other_point: Point) -> None:
        if other_point.x == self.x:
            self.line_orientation = LineOrientation.VERT
        elif other_point.y == self.y:
            self.line_orientation = LineOrientation.HORZ
        else:
            raise ValueError("cannot set line orientation for points that are not collinear")

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    @property
    def coords(self) -> tuple[T, T]:
        return self.x, self.y

    def orientation(self, p2: Point[T], p3: Point[T]) -> PathOrientation:
        p1 = self
        x1, y1 = float(p1.x), float(p1.y)
        x2, y2 = float(p2.x), float(p2.y)
        x3, y3 = float(p3.x), float(p3.y)

        val = ((y2 - y1) * (x3 - x2)) - ((x2 - x1) * (y3 - y2))

        # note we are operating in quadrant 4, so we are swapping the values that correspond to cw & ccw
        if val > 0:
            return PathOrientation.CCW
        elif val < 0:
            return PathOrientation.CW
        else:
            return PathOrientation.COL
