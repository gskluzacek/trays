from __future__ import annotations

from dataclasses import dataclass

from types import NotImplementedType
from typing import Any, Generic, SupportsFloat, TypeVar, TYPE_CHECKING
from contextlib import suppress

from tray.geometry.types.geometric import PathOrientation

if TYPE_CHECKING:
    from tray.geometry.basic.line import Line

T = TypeVar("T", bound=SupportsFloat)


@dataclass(frozen=True, slots=True)
class Point(Generic[T]):
    x: T
    y: T

    def __post_init__(self) -> None:
        if float(self.x) < 0 or float(self.y) < 0:
            raise ValueError(f"x and y must be non-negative (got x={self.x}, y={self.y})")

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    @staticmethod
    def _coerce(other: Any) -> Point[SupportsFloat] | None:
        if isinstance(other, Point):
            return other  # runtime-ok; type parameter may differ

        if isinstance(other, (tuple, list)) and len(other) == 2:
            ox, oy = other
            with suppress(TypeError, ValueError):
                return Point(ox, oy)  # validates coercibility + non-negative

        return None

    def _cmp_key(self) -> tuple[float, float]:
        return float(self.x), float(self.y)

    def __eq__(self, other: object) -> NotImplementedType | bool:
        coerced = self._coerce(other)
        if coerced is None:
            return NotImplemented
        return self._cmp_key() == coerced._cmp_key()

    def __lt__(self, other: object) -> NotImplementedType | bool:
        coerced = self._coerce(other)
        if coerced is None:
            return NotImplemented
        return self._cmp_key() < coerced._cmp_key()

    def __le__(self, other: object) -> NotImplementedType | bool:
        coerced = self._coerce(other)
        if coerced is None:
            return NotImplemented
        return self._cmp_key() <= coerced._cmp_key()

    def __gt__(self, other: object) -> NotImplementedType | bool:
        coerced = self._coerce(other)
        if coerced is None:
            return NotImplemented
        return self._cmp_key() > coerced._cmp_key()

    @property
    def coords(self) -> tuple[T, T]:
        return self.x, self.y

    def orientation(self, p2: Point[T], p3: Point[T]) -> PathOrientation:
        x1, y1 = float(self.x), float(self.y)
        x2, y2 = float(p2.x), float(p2.y)
        x3, y3 = float(p3.x), float(p3.y)

        val = ((y2 - y1) * (x3 - x2)) - ((x2 - x1) * (y3 - y2))

        # y increases downward
        if val > 0:
            return PathOrientation.CCW
        if val < 0:
            return PathOrientation.CW
        return PathOrientation.COL

    def is_orthogonal(self, other: Point[T]) -> bool:
        return (self.y == other.y or self.x == other.x) and self != other

    def is_between(self, line: Line[T]) -> bool:
        line_pt_1, line_pt_2 = line.normalize
        if line.is_horizontal:
            return line_pt_1.x < self.x < line_pt_2.x
        return line_pt_1.y < self.y < line_pt_2.y
