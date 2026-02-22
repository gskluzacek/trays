from __future__ import annotations

from tray.geometry.types.tray import JointType
from tray.geometry.basic.line import Line, Point
from tray.geometry.segment.segment_point import SegmentPoint


class FinalPathLine(Line[int]):
    def __init__(self, p1: Point[int], p2: Point[int]):
        super().__init__(p1, p2)
        # TODO: need code to set joint_type
        self.joint_type = JointType.NONE

    def __repr__(self) -> str:
        return f"PathLine(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r}, joint={self.joint_type!r})"

    def __str__(self) -> str:
        return f"{self.p1}, {self.p2}, {self.orientation}, {self.joint_type}"

    @property
    def points_from_line(self) -> tuple[SegmentPoint, SegmentPoint]:
        sl_pt_1, sl_pt_2 = self.normalize
        return SegmentPoint(sl_pt_1.x, sl_pt_1.y, self), SegmentPoint(sl_pt_2.x, sl_pt_2.y, self)
