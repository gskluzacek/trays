import pytest
from tray.geometry.point import Point, PathOrientation
from tray.geometry.line import LineOrientation
from tray.geometry.path import Path


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


def test_path_lines_len():
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    path.add_point(Point(0, 10))  # added to make it a rectangle
    path.finalize()
    assert len(path.lines) == 4


def test_path_lines_getitem():
    path = Path()
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    p3 = Point(10, 10)
    p4 = Point(0, 10)
    path.add_point(p1)
    path.add_point(p2)
    path.add_point(p3)
    path.add_point(p4)
    path.finalize()

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


def test_path_lines_iter():
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    path.add_point(Point(0, 10))
    path.finalize()

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
    path.finalize()
    # verify that line orientations are correct for the lines in the path
    assert len(path.lines) == 4
    assert path.lines[0].orientation == LineOrientation.HORZ
    assert path.lines[1].orientation == LineOrientation.VERT
    assert path.lines[2].orientation == LineOrientation.HORZ
    assert path.lines[3].orientation == LineOrientation.VERT


def test_path_horizontal_vertical_properties():
    path = Path()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    path.add_point(Point(0, 10))
    path.finalize()

    horz_lines = list(path.horizontal)
    vert_lines = list(path.vertical)

    assert len(horz_lines) == 2
    assert all(line.is_horizontal for line in horz_lines)
    assert horz_lines[0].p1.coords == (0, 0)
    assert horz_lines[0].p2.coords == (10, 0)
    assert horz_lines[1].p1.coords == (10, 10)
    assert horz_lines[1].p2.coords == (0, 10)

    assert len(vert_lines) == 2
    assert all(line.is_vertical for line in vert_lines)
    assert vert_lines[0].p1.coords == (10, 0)
    assert vert_lines[0].p2.coords == (10, 10)
    assert vert_lines[1].p1.coords == (0, 10)
    assert vert_lines[1].p2.coords == (0, 0)


def test_path_horizontal_vertical_empty():
    path = Path()
    assert list(path.horizontal) == []
    assert list(path.vertical) == []

    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    # finalize() not called yet, path.lines is empty
    assert list(path.horizontal) == []
    assert list(path.vertical) == []

    path.finalize()
    # Path with 2 points has 2 lines (p1->p2 and p2->p1) because of cyclic_n_tuples(offset=0, n=2)
    # Actually let's check what cyclic_n_tuples does.
    horz_lines = list(path.horizontal)
    assert len(horz_lines) == 2
    assert horz_lines[0].p1.coords == (0, 0)
    assert horz_lines[0].p2.coords == (10, 0)
    assert horz_lines[1].p1.coords == (10, 0)
    assert horz_lines[1].p2.coords == (0, 0)
