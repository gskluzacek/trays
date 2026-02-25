from tray.geometry.basic.point import Point
from tray.geometry.segment.segment_path import SegmentPath
from tray.geometry.segment.segment_line import SegmentLine
from tray.geometry.types.tray import JointType


def test_segment_path_init():
    sp = SegmentPath()
    assert len(sp.lines) == 0
    assert sp.points == []


def test_segment_path_add_segment():
    sp = SegmentPath()
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    sp.add_segment(p1, p2, JointType.TS)
    assert len(sp.lines) == 1
    assert isinstance(sp.lines[0], SegmentLine)
    assert sp.lines[0].joint_type == JointType.TS
