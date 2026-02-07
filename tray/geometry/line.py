from __future__ import annotations

import functools
from enum import Enum
from collections.abc import Iterator, Sequence
from typing import Generic, SupportsFloat, TypeVar
from tray.geometry.point import Point

T = TypeVar("T", bound=SupportsFloat)
L = TypeVar("L", bound="Line")


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
    def of_orientation(lines: Sequence[L], orientation: LineOrientation) -> Iterator[L]:
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

    @staticmethod
    def _intervals_overlap(lo1: T, hi1: T, lo2: T, hi2: T) -> bool:
        return not (hi1 <= lo2 or hi2 <= lo1)

    def is_overlapping(self, other: Line[T]) -> bool:
        if self.orientation != other.orientation or not self.is_collinear(other):
            return False
        (line_1_pt_1, line_1_pt_2) = self.normalize
        (line_2_pt_1, line_2_pt_2) = other.normalize
        if self.is_vertical:
            return self._intervals_overlap(line_1_pt_1.y, line_1_pt_2.y, line_2_pt_1.y, line_2_pt_2.y)
        # horizontal
        return self._intervals_overlap(line_1_pt_1.x, line_1_pt_2.x, line_2_pt_1.x, line_2_pt_2.x)

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
        if self.p1 > self.p2:
            return self.p2, self.p1
        return self.p1, self.p2

    def __repr__(self) -> str:
        return f"Line(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r})"

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}, {self.orientation}]"
