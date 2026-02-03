from __future__ import annotations

import functools
from enum import Enum
from collections.abc import Iterator, Sequence
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

    @staticmethod
    def of_orientation(lines: Sequence[Line[T]], orientation: LineOrientation) -> Iterator[Line[T]]:
        return filter(lambda line: line.orientation == orientation, lines)

    def _set_orientation(self) -> None:
        if self.p1.x == self.p2.x:
            self.orientation = LineOrientation.VERT
        elif self.p1.y == self.p2.y:
            self.orientation = LineOrientation.HORZ
        else:
            raise ValueError("cannot set line orientation for points that are not collinear")

    @property
    def is_vertical(self) -> bool:
        return self.orientation == LineOrientation.VERT

    @property
    def is_horizontal(self) -> bool:
        return self.orientation == LineOrientation.HORZ

    def is_collinear(self, other: Line[T]) -> bool:
        # vertical use case first
        if self.is_vertical:
            # both lines must be vertical
            if other.is_vertical:
                # if x coords are equal then lines are collinear
                return self.p1.x == other.p1.x
            raise ValueError("cannot compare vertical lines with non-vertical lines")
        # horizontal use case second
        # both lines must be horizontal
        if other.is_vertical:
            raise ValueError("cannot compare non-vertical lines with vertical lines")
        # if y coords are equal then lines are collinear
        return self.p1.y == other.p1.y

    @functools.cached_property
    def normalize(self) -> tuple[Point[T], Point[T]]:
        if self.p1.coords > self.p2.coords:
            return self.p2, self.p1
        return self.p1, self.p2

    def __repr__(self) -> str:
        return f"Line(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r})"

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}, {self.orientation}]"
