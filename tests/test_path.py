import pytest
from point import Point, PathOrientation, LineOrientation
from path import Path, _LinesView
from line import Line


def test_path_init_empty():
    path = Path()
    assert path.points == []
    assert path.orientation == PathOrientation.NONE


def test_path_init_with_start_point():
    p = Point(0, 0)
    path = Path(start_point=p)
    assert path.points == [p]
    assert path.orientation == PathOrientation.NONE


def test_path_add_point():
    path = Path()
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    path.add_point(p1)
    path.add_point(p2)
    assert path.points == [p1, p2]


def test_path_points_as_tuples():
    path = Path()
    path.add_point(Point(1, 2))
    path.add_point(Point(10, 2))
    tuples = list(path.points_as_tuples)
    assert tuples == [(1, 2), (10, 2)]


def test_lines_view_len():
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    assert len(path.lines) == 3


def test_lines_view_getitem_int():
    path = Path()
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    p3 = Point(10, 10)
    p4 = Point(0, 10)
    path.add_point(p1)
    path.add_point(p2)
    path.add_point(p3)
    path.add_point(p4)

    line0 = path.lines[0]
    assert line0.p1 == p1
    assert line0.p2 == p2

    line1 = path.lines[1]
    assert line1.p1 == p2
    assert line1.p2 == p3

    line2 = path.lines[2]
    assert line2.p1 == p3
    assert line2.p2 == p4

    line3 = path.lines[3]
    assert line3.p1 == p4
    assert line3.p2 == p1

    # Test modulo wrapping
    line4 = path.lines[4]
    assert line4.p1 == p1
    assert line4.p2 == p2


def test_lines_view_getitem_empty_raises():
    path = Path()
    with pytest.raises(IndexError, match="path.lines is empty"):
        _ = path.lines[0]


def test_lines_view_slice():
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    path.add_point(Point(0, 10))

    lines = path.lines[0:2]
    assert isinstance(lines, list)
    assert len(lines) == 2
    assert lines[0].p1.coords == (0, 0)
    assert lines[1].p1.coords == (10, 0)


def test_lines_view_iter():
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    path.add_point(Point(0, 10))

    lines = list(path.lines)
    assert len(lines) == 4
    assert lines[0].p1.coords == (0, 0)
    assert lines[1].p1.coords == (10, 0)
    assert lines[2].p1.coords == (10, 10)
    assert lines[3].p1.coords == (0, 10)


def test_path_set_orientation_ccw():
    # p1=(0,0), p2=(0,10), p3=(10,10) -> val = (10*10) - (0*0) = 100 -> CCW
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(0, 10))
    path.add_point(Point(10, 10))
    path.set_orientation()
    assert path.orientation == PathOrientation.CCW


def test_path_set_orientation_cw():
    # p1=(0,0), p2=(10,0), p3=(10,10) -> val = (0*0) - (10*10) = -100 -> CW
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    path.set_orientation()
    assert path.orientation == PathOrientation.CW


def test_path_set_orientation_with_collinear_start():
    # First three points are collinear, but next ones determine orientation
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(20, 0))  # Collinear
    path.add_point(Point(20, 10))  # Now it should be CW: (0,0)-(10,0)-(20,0) is COL, (10,0)-(20,0)-(20,10) is CW
    path.set_orientation()
    assert path.orientation == PathOrientation.CW


def test_path_set_orientation_error_too_few_points():
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    with pytest.raises(ValueError, match="please check that you have 3 or more points"):
        path.set_orientation()


def test_path_set_orientation_error_all_collinear():
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(20, 0))
    with pytest.raises(ValueError, match="check that all points in the path are not collinear"):
        path.set_orientation()


def test_path_finalize():
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    path.add_point(Point(0, 10))
    # Finalize currently does nothing but iterate over lines.
    # It shouldn't raise any errors for this rectangle.
    path.finalize()
    # verify that line orientations were set on points (via Line creation in _LinesView)
    assert path.points[1].line_orientation == LineOrientation.HORZ
    assert path.points[2].line_orientation == LineOrientation.VERT
    assert path.points[3].line_orientation == LineOrientation.HORZ
    assert path.points[0].line_orientation == LineOrientation.VERT
