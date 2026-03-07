from __future__ import annotations

from tray.geometry.basic.line import Line, Point
from tray.geometry.types.tray import JointType


class SegmentLine(Line[int]):
    def __init__(self, p1: Point[int], p2: Point[int], joint_type: JointType):
        super().__init__(p1, p2)
        self.joint_type = joint_type

    def __repr__(self) -> str:
        return f"SegmentLine(p1={self.p1}, p2={self.p2}, orientation={self.orientation}, joint_type={self.joint_type})"

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}, {self.orientation}, {self.joint_type}]"
