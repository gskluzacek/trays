from __future__ import annotations

from enum import Enum
from typing import Generic, SupportsFloat, TypeVar

T = TypeVar("T", bound=SupportsFloat)


class PathOrientation(Enum):
    CW = "clockwise"
    CCW = "counter_clockwise"
    COL = "collinear"
    NONE = "none"


class Point(Generic[T]):
    def __init__(self, x: T, y: T) -> None:
        self.x = x
        self.y = y

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
