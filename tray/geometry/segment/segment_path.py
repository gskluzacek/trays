from tray.geometry.basic.point import Point
from tray.geometry.typed_base_path import TypedBasePath
from tray.geometry.segment.segment_line import SegmentLine
from tray.geometry.types.tray import JointType


class SegmentPath(TypedBasePath[SegmentLine]):
    def __init__(self, start_point: Point[int] | None = None):
        super().__init__(start_point)

    def add_segment(self, p1: Point[int], p2: Point[int], joint_type: JointType) -> None:
        self.lines.append(SegmentLine(p1, p2, joint_type))
