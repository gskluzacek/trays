from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Sequence, overload


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int
    line_type: str


@dataclass(frozen=True, slots=True)
class Line:
    p1: Point
    p2: Point
    type: str


class _LinesView(Sequence[Line]):
    """A dynamic, list-like view over a Path's points that yields Line objects."""

    def __init__(self, path: "Path") -> None:
        self._path = path

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

        # Support negative indexing like a normal list
        i = index % n

        points = self._path.points
        p1 = points[i]
        p2 = points[(i + 1) % n]
        return Line(p1=p1, p2=p2, type=p2.line_type)

    def __iter__(self) -> Iterator[Line]:
        for i in range(len(self)):
            yield self[i]


@dataclass(slots=True)
class Path:
    points: list[Point]

    @property
    def lines(self) -> Sequence[Line]:
        # Returns a dynamic view (not a precomputed list), so it always reflects self.points.
        return _LinesView(self)


# --- Example usage ---
if __name__ == "__main__":
    path = Path(
        points=[
            Point(0, 0, "A"),
            Point(1, 0, "B"),
            Point(1, 1, "C"),
            Point(0, 1, "D"),
        ]
    )

    first = path.lines[0]   # p1=points[0], p2=points[1], type=points[1].line_type
    third = path.lines[2]   # p1=points[2], p2=points[3], type=points[3].line_type
    last = path.lines[-1]   # p1=points[-1], p2=points[0], type=points[0].line_type

    print(first)
    print(third)
    print(last)
    print(list(path.lines))  # iterable, list-like behavior
