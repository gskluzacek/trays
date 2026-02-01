from __future__ import annotations

from enum import Enum
from typing import Generic, SupportsFloat, TypeVar
from tray.geometry.point import Point

T = TypeVar("T", bound=SupportsFloat)


class LineOrientation(Enum):
    VERT = "vertical"
    HORZ = "horizontal"
    NONE = "none"


class Line(Generic[T]):
    def __init__(self, p1: Point[T], p2: Point[T]) -> None:
        self.p1 = p1
        self.p2 = p2
        self.orientation = LineOrientation.NONE
        self._set_orientation()

    def _set_orientation(self) -> None:
        if self.p1.x == self.p2.x:
            self.orientation = LineOrientation.VERT
        elif self.p1.y == self.p2.y:
            self.orientation = LineOrientation.HORZ
        else:
            raise ValueError("cannot set line orientation for points that are not collinear")

    def get_normalized_line(self) -> Line[T]:
        if self.p1.coords > self.p2.coords:
            # need to create new Point so the point p1 that is in the path doesn't get its orientation changed
            p1, p2 = Point(*self.p2.coords), Point(*self.p1.coords)
        else:
            p1, p2 = self.p1, self.p2
        return Line[T](p1, p2)

    def __repr__(self) -> str:
        return f"Line(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r})"

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}, {self.orientation}]"
