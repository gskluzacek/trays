from __future__ import annotations

from tray.geometry.basic.line import Line, Point


class PathLine(Line[int]):
    def __init__(self, p1: Point[int], p2: Point[int]):
        super().__init__(p1, p2)
        self.line_breaks: list[Point[int]] = []

    def __repr__(self) -> str:
        return f"PathLine(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r}, breaks={self.line_breaks!r})"

    def __str__(self) -> str:
        return f"{self.p1}, {self.p2}, {self.orientation}, {self.line_breaks}"

    def add_break(self, break_point: Point[int]):
        """Add a break point to the path"""
        self.line_breaks.append(break_point)
