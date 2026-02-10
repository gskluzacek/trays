from __future__ import annotations

from typing import TypeVar, SupportsFloat
from tray.geometry.line import Line, LineOrientation, Point

T = TypeVar("T", bound=SupportsFloat)


class PathLine(Line[T]):
    def __init__(self, p1: Point[T], p2: Point[T]):
        super().__init__(p1, p2)
        self.path_breaks: list[T] = []

    def __repr__(self) -> str:
        return f"PathLine(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r}, breaks={self.path_breaks!r})"

    def __str__(self) -> str:
        return f"{self.p1}, {self.p2}, {self.orientation}, {self.path_breaks}"

    def add_break(self, break_point: T):
        """Add a break point to the path"""
        self.path_breaks.append(break_point)
