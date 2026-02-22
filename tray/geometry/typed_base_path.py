from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Generic, TypeVar

from cyclic_n_tuples import cyclic_n_tuples

from tray.geometry.basic.path import Path
from tray.geometry.basic.line import Line
from tray.geometry.basic.point import Point
from tray.geometry.types.geometric import LineOrientation

TLine = TypeVar("TLine", bound=Line)


class TypedBasePath(Path[int], Generic[TLine], ABC):
    """
    Base for paths that *have* `lines`, but not necessarily built from `points`.
    Subclasses may populate `self.lines` however they like.
    """

    def __init__(self, start_point: Point[int] | None = None):
        super().__init__(start_point)
        # Path.__init__(self, start_point)
        # NOTE: Path.lines does not get populated until finalize() is called.
        self.lines: list[TLine] = []

    @property
    def horizontal(self) -> Iterator[TLine]:
        return Line.of_orientation(self.lines, LineOrientation.HORZ)

    @property
    def vertical(self) -> Iterator[TLine]:
        return Line.of_orientation(self.lines, LineOrientation.VERT)


class FinalizableTypedBasePath(TypedBasePath[TLine], ABC):
    """
    Adds a standard `finalize()` that constructs `lines` from adjacent `points`
    using a factory hook.
    """

    @abstractmethod
    def _make_line(self, p1: Point[int], p2: Point[int]) -> TLine:
        """Factory hook for creating a path segment line."""
        raise NotImplementedError

    def finalize(self) -> None:
        self.lines = [self._make_line(p1, p2) for p1, p2 in cyclic_n_tuples(self.points, n=2, offset=0)]
