from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Generic, SupportsFloat, TypeVar, overload

from tray.geometry.point import Point, PathOrientation
from tray.geometry.line import Line
from cyclic_n_tuples import fwd_n_tuple

T = TypeVar("T", bound=SupportsFloat)


class _LinesView(Sequence[Line]):
    """Dynamic, list-like view over a Path's points that yields Line objects."""

    def __init__(self, path: Path, normalize_ind: bool = False) -> None:
        self._path = path
        self._normalize_ind = normalize_ind

    def __len__(self) -> int:
        return len(self._path.points)

    @overload
    def __getitem__(self, index: int) -> Line: ...
    @overload
    def __getitem__(self, index: slice) -> list[Line]: ...

    def __getitem__(self, index: int | slice) -> Line | list[Line]:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return [self[i] for i in range(start, stop, step)]

        n = len(self)
        if n == 0:
            raise IndexError("path.lines is empty (no points)")

        i = index % n

        pts = self._path.points
        p1 = pts[i]
        p2 = pts[(i + 1) % n]

        if self._normalize_ind:
            if p1.coords > p2.coords:
                # need to create new Point so the point p1 that is in the path doesn't get its orientation changed
                p1, p2 = Point(*p2.coords), Point(*p1.coords)

        # TODO: creating a new Line object, will initialize point p2's line orientation if it is LineOrientation.NONE
        return Line(p1, p2)

    def __iter__(self) -> Iterator[Line]:
        # TODO: iteration will call __getitem__ which will create a new Line object, which will initialize point p2's line orientation if it is LineOrientation.NONE
        for i in range(len(self)):
            yield self[i]


class Path(Generic[T]):
    def __init__(
        self,
        start_point: Point[T] | None = None,
        orientation: PathOrientation = PathOrientation.NONE,
    ) -> None:
        self.points: list[Point[T]] = [start_point] if start_point else []
        self.orientation: PathOrientation = orientation

    @property
    def lines(self) -> Sequence[Line]:
        return _LinesView(self)

    @property
    def lines_normalized(self) -> Sequence[Line]:
        return _LinesView(self, True)

    def finalize(self) -> None:
        # todo: implement any finalization logic if needed - must have all details within the path to do so
        for _ in self.lines:
            pass

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
        for pt_1, pt_2, pt_3 in fwd_n_tuple(self.points):
            orientation = pt_1.orientation(pt_2, pt_3)
            if orientation != PathOrientation.COL:
                break

        if orientation == PathOrientation.COL:
            raise ValueError(
                "could not determine the path's orientation (clockwise or counter clockwise). please check that all points in the path are not collinear"
            )

        if orientation == PathOrientation.NONE:
            raise ValueError("exhausted path without determining the orientation")

        self.orientation = orientation
