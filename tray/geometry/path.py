from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Generic, SupportsFloat, TypeVar
from tray.geometry.point import Point, PathOrientation
from tray.geometry.line import Line
from cyclic_n_tuples import fwd_n_tuple

T = TypeVar("T", bound=SupportsFloat)


class Path(Generic[T]):
    def __init__(
        self,
        start_point: Point[T] | None = None,
        orientation: PathOrientation = PathOrientation.NONE,
    ) -> None:
        self.points: list[Point[T]] = [start_point] if start_point else []
        self.orientation: PathOrientation = orientation
        self.lines: list[Line[T]] = []

    def finalize(self) -> None:
        self.lines = []
        n = len(self.points)
        if n < 2:
            return

        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            self.lines.append(Line(p1, p2))

    @property
    def points_as_tuples(self) -> Iterator[tuple[T, T]]:
        return map(lambda pt: (pt.x, pt.y), self.points)

    def add_point(self, point: Point[T]) -> None:
        self.points.append(point)

    def set_orientation(self) -> None:
        if len(self.points) < 3:
            raise ValueError(
                f"could not determine the path's orientation (clockwise or counter clockwise). please check that you have 3 or more points in your path. Path len: {len(self.points)}"
            )

        orientation = PathOrientation.NONE
        # Note: fwd_n_tuple will yield nothing if len(self.points) < 3,
        # but we already checked that above.
        for pt_1, pt_2, pt_3 in fwd_n_tuple(self.points):
            orientation = pt_1.orientation(pt_2, pt_3)
            if orientation != PathOrientation.COL:
                break

        if orientation == PathOrientation.COL:
            raise ValueError(
                "could not determine the path's orientation (clockwise or counter clockwise). please check that all points in the path are not collinear"
            )

        # This part should be logically unreachable given the checks above,
        # but kept as a safety measure.
        if orientation == PathOrientation.NONE:  # pragma: no cover
            raise ValueError("exhausted path without determining the orientation")

        self.orientation = orientation
