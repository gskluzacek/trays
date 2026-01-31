from __future__ import annotations

from typing import Generic, SupportsFloat, TypeVar
from point import Point, LineOrientation

T = TypeVar("T", bound=SupportsFloat)


class Line(Generic[T]):
    def __init__(self, p1: Point[T], p2: Point[T]) -> None:
        self.p1 = p1
        self.p2 = p2
        if self.orientation == LineOrientation.NONE:
            self.p2.set_line_orientation(self.p1)

    @property
    def orientation(self) -> LineOrientation:
        return self.p2.line_orientation

    def get_normalized_line(self) -> Line[T]:
        if self.p1.coords > self.p2.coords:
            # need to create new Point so the point p1 that is in the path doesn't get its orientation changed
            p1, p2 = Point(*self.p2.coords), Point(*self.p1.coords)
        else:
            p1, p2 = self.p1, self.p2
        return Line(p1, p2)

    def __repr__(self) -> str:
        return f"Line(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r})"

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}, {self.orientation}]"
