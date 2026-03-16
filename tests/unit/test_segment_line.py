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


def test_segment_line_repr():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    jt = JointType.TS
    sl = SegmentLine(p1, p2, jt)
    expected = "SegmentLine(p1=(0, 0), p2=(10, 0), orientation=LineOrientation.HORZ, joint_type=JointType.TS)"
    assert repr(sl) == expected


def test_segment_line_str():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    jt = JointType.TS
    sl = SegmentLine(p1, p2, jt)
    expected = "[(0, 0), (10, 0), LineOrientation.HORZ, JointType.TS]"
    assert str(sl) == expected
