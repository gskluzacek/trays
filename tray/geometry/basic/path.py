from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, SupportsFloat, TypeVar

from tray.geometry.basic.point import Point

T = TypeVar("T", bound=SupportsFloat)


class Path(Generic[T]):
    def __init__(self, start_point: Point[T] | None = None) -> None:
        self.points: list[Point[T]] = [start_point] if start_point else []

    @property
    def points_as_tuples(self) -> Iterator[tuple[T, T]]:
        return map(lambda pt: (pt.x, pt.y), self.points)

    def add_point(self, point: Point[T]) -> None:
        self.points.append(point)
