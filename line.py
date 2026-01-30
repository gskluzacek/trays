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

    def __repr__(self) -> str:
        return f"Line(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r})"

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}, {self.orientation}]"
