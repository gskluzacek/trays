from __future__ import annotations

from tray.geometry.types.tray import WallType
from tray.geometry.basic.line import Line, Point
from tray.geometry.base.path_line import PathLine
from tray.geometry.segment.segment_path import SegmentPath


class WallLine(Line[int]):
    def __init__(self, p1: Point[int], p2: Point[int], wall_type: WallType = WallType.NONE) -> None:
        super().__init__(p1, p2)
        self.wall_type: WallType = wall_type
        self.segment_path: SegmentPath = SegmentPath()

    def __repr__(self) -> str:
        return f"Line(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r}, wall_type={self.wall_type!r})"

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}, {self.orientation}, {self.wall_type.label}]"

    def classify_wall(self, path_line: PathLine) -> WallType:
        w1_val, w2_val = self.start_end
        p1_val, p2_val = path_line.start_end

        col = self.is_collinear(path_line)

        match col:
            case False:
                return WallType.INTERIOR

            # w is A) completely below/left p OR B) completely above/right p (including touching at endpoints)
            case True if (w2_val <= p1_val) or (w1_val >= p2_val):
                return WallType.INTERIOR

            # partial overlap on one side -> "combo"
            case True if (w1_val < p1_val < w2_val < p2_val) or (p1_val < w1_val < p2_val < w2_val):
                return WallType.COMBO

            case True if (w1_val == p1_val and w2_val > p2_val) or (w2_val == p2_val and w1_val < p1_val):
                return WallType.COMBO

            case True if w1_val < p1_val and w2_val > p2_val:
                return WallType.COMBO

            # w within p or equal -> "exterior" per your original mapping
            case True if (w1_val == p1_val and w2_val < p2_val) or (w2_val == p2_val and w1_val > p1_val):
                return WallType.EXTERIOR

            case True if p1_val < w1_val and w2_val < p2_val:
                return WallType.EXTERIOR

            case True if w1_val == p1_val and w2_val == p2_val:
                return WallType.EXTERIOR

            case _:
                raise ValueError("Unhandled collinear configuration")
