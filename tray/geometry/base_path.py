from typing import SupportsFloat, TypeVar
from collections.abc import Iterator

from cyclic_n_tuples import cyclic_n_tuples

from tray.geometry.path import Path
from tray.geometry.line import Line, LineOrientation
from tray.geometry.path_line import PathLine
from tray.geometry.point import Point

T = TypeVar("T", bound=SupportsFloat)


class BasePath(Path[T]):
    def __init__(self, start_point: Point[T] | None = None):
        super().__init__(start_point)
        # NOTE: Path.lines does not get populated until finalize() is called.
        self.lines: list[PathLine[T]] = []

    def finalize(self) -> None:
        self.lines = []
        for p1, p2 in cyclic_n_tuples(self.points, n=2, offset=0):
            self.lines.append(PathLine(p1, p2))

    @property
    def horizontal(self) -> Iterator[PathLine[T]]:
        return Line.of_orientation(self.lines, LineOrientation.HORZ)

    @property
    def vertical(self) -> Iterator[PathLine[T]]:
        return Line.of_orientation(self.lines, LineOrientation.VERT)
