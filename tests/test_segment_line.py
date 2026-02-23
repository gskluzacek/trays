from tray.geometry.basic.point import Point
from tray.geometry.segment.segment_line import SegmentLine
from tray.geometry.types.tray import JointType


def test_segment_line_init():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    jt = JointType.TS
    sl = SegmentLine(p1, p2, jt)
    assert sl.p1 == p1
    assert sl.p2 == p2
    assert sl.joint_type == jt
