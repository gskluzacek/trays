from __future__ import annotations

from tray.geometry.basic.line import Line, Point
from tray.geometry.types.tray import JointType


class SegmentLine(Line[int]):
    def __init__(self, p1: Point[int], p2: Point[int], joint_type: JointType):
        super().__init__(p1, p2)
        self.joint_type = joint_type
