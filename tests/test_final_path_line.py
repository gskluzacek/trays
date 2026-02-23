from tray.geometry.basic.point import Point
from tray.geometry.segment.segment_point import SegmentPoint
from tray.geometry.final_base.final_path_line import FinalPathLine
from tray.geometry.final_base.final_base_path import FinalBasePath


def test_final_base_path_init():
    p = Point(0, 0)
    fbp = FinalBasePath(p)
    assert fbp.points == [p]


def test_final_base_path_make_line():
    fbp = FinalBasePath()
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    line = fbp._make_line(p1, p2)
    assert isinstance(line, FinalPathLine)
    assert line.p1 == p1
    assert line.p2 == p2


def test_final_path_line_points_from_line():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    fl = FinalPathLine(p1, p2)
    pts = fl.points_from_line
    assert len(pts) == 2
    assert isinstance(pts[0], SegmentPoint)
    assert isinstance(pts[1], SegmentPoint)
    assert pts[0].line == fl
    assert pts[1].line == fl
    # Normalized order
    assert pts[0].coords == (0, 0)
    assert pts[1].coords == (10, 0)


def test_final_path_line_repr():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    fl = FinalPathLine(p1, p2)
    # PathLine(p1=Point(x=0, y=0), p2=Point(x=10, y=0), type=<LineOrientation.HORZ: 'horizontal'>, joint=<JointType.NONE: 'none'>)
    expected_repr = f"PathLine(p1={p1!r}, p2={p2!r}, type={fl.orientation!r}, joint={fl.joint_type!r})"
    assert repr(fl) == expected_repr


def test_final_path_line_str():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    fl = FinalPathLine(p1, p2)
    expected_str = f"{p1}, {p2}, {fl.orientation}, {fl.joint_type}"
    assert str(fl) == expected_str
