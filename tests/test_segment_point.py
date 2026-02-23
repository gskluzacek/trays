from tray.geometry.basic.point import Point
from tray.geometry.segment.segment_point import SegmentPoint
from tray.geometry.final_base.final_path_line import FinalPathLine


def test_segment_point_init():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    fl = FinalPathLine(p1, p2)
    sp = SegmentPoint(5, 0, fl)
    assert sp.x == 5
    assert sp.y == 0
    assert sp.line == fl


def test_segment_point_to_point():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    fl = FinalPathLine(p1, p2)
    sp = SegmentPoint(5, 0, fl)
    p = sp.to_point
    assert isinstance(p, Point)
    assert not isinstance(p, SegmentPoint)
    assert p.x == 5
    assert p.y == 0
