from __future__ import annotations

from enum import Enum
from functools import total_ordering
from typing import SupportsFloat, TypeAlias, TypeVar, Generic, overload, cast

T = TypeVar("T", bound=SupportsFloat)
PointLike: TypeAlias = "Point[T] | tuple[T, T]"


class PathOrientation(Enum):
    CW = "clockwise"
    CCW = "counter_clockwise"
    COL = "collinear"
    NONE = "none"


@total_ordering
class Point(Generic[T]):
    def __init__(self, x: T, y: T) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    @staticmethod
    def _validate_pair_xy(ax: T, ay: T, bx: T, by: T) -> None:
        # Allowed: identical OR share x OR share y
        # Disallowed: both coordinates differ
        if ax != bx and ay != by:
            raise ValueError("Unsupported comparison: points must be identical or share x or share y.")

    @overload
    @staticmethod
    def _coerce_xy(other: Point[T]) -> tuple[T, T]: ...

    @overload
    @staticmethod
    def _coerce_xy(other: tuple[T, T]) -> tuple[T, T]: ...

    @overload
    @staticmethod
    def _coerce_xy(other: object) -> tuple[T, T] | None: ...

    @staticmethod
    def _coerce_xy(other: object) -> tuple[T, T] | None:
        if isinstance(other, Point):
            return cast(tuple[T, T], (other.x, other.y))
        if isinstance(other, tuple) and len(other) == 2:
            x, y = other
            return cast(tuple[T, T], (x, y))
        return None

    def __eq__(self, other: object) -> bool:
        other_xy = self._coerce_xy(other)
        if other_xy is None:
            return NotImplemented
        ox, oy = other_xy
        self._validate_pair_xy(self.x, self.y, ox, oy)
        return (self.x, self.y) == (ox, oy)

    def __lt__(self, other: object) -> bool:
        other_xy = self._coerce_xy(other)
        if other_xy is None:
            return NotImplemented
        ox, oy = other_xy
        self._validate_pair_xy(self.x, self.y, ox, oy)
        return (self.x, self.y) < (ox, oy)

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

    def is_orthogonal(self, other: Point[T]) -> bool:
        return (self.y == other.y or self.x == other.x) and self != other
