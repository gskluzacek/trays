import pytest
from tray.geometry.basic.point import Point
from tray.geometry.types.geometric import LineOrientation, PathOrientation
from tray.geometry.base.base_path import BasePath


def test_base_path_init_empty():
    path = BasePath()
    assert path.points == []
    assert path.orientation == PathOrientation.NONE


def test_base_path_init_with_start_point():
    p = Point(0, 0)
    path = BasePath(start_point=p)
    assert path.points == [p]
    assert path.orientation == PathOrientation.NONE


def test_base_path_lines_len():
    path = BasePath()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    path.add_point(Point(0, 10))  # added to make it a rectangle
    path.finalize()
    assert len(path.lines) == 4


def test_base_path_lines_getitem():
    path = BasePath()
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


def test_base_path_lines_iter():
    path = BasePath()
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


def test_base_path_set_orientation_ccw():
    # p1=(0,0), p2=(0,10), p3=(10,10) -> val = (10*10) - (0*0) = 100 -> CCW
    path = BasePath()
    path.add_point(Point(0, 0))
    path.add_point(Point(0, 10))
    path.add_point(Point(10, 10))
    path.set_orientation()
    assert path.orientation == PathOrientation.CCW


def test_base_path_set_orientation_cw():
    # p1=(0,0), p2=(10,0), p3=(10,10) -> val = (0*0) - (10*10) = -100 -> CW
    path = BasePath()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(10, 10))
    path.set_orientation()
    assert path.orientation == PathOrientation.CW


def test_base_path_set_orientation_with_collinear_start():
    path = BasePath()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(20, 0))  # collinear
    path.add_point(Point(20, 10))
    path.set_orientation()
    assert path.orientation == PathOrientation.CW


def test_base_path_set_orientation_error_too_few_points():
    path = BasePath()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    with pytest.raises(ValueError, match="could not determine the path's orientation"):
        path.set_orientation()


def test_base_path_set_orientation_error_all_collinear():
    path = BasePath()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.add_point(Point(20, 0))
    with pytest.raises(ValueError, match="could not determine the path's orientation"):
        path.set_orientation()


def test_base_path_finalize():
    path = BasePath()
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    p3 = Point(10, 10)
    p4 = Point(0, 10) # Added to make it a rectangle (orthogonal lines)
    path.add_point(p1)
    path.add_point(p2)
    path.add_point(p3)
    path.add_point(p4)
    path.finalize()

    assert len(path.lines) == 4
    assert path.lines[0].p1 == p1
    assert path.lines[0].p2 == p2
    assert path.lines[1].p1 == p2
    assert path.lines[1].p2 == p3
    assert path.lines[2].p1 == p3
    assert path.lines[2].p2 == p4
    assert path.lines[3].p1 == p4
    assert path.lines[3].p2 == p1


def test_base_path_horizontal_properties():
    path = BasePath()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))  # HORZ
    path.add_point(Point(10, 10)) # VERT
    path.add_point(Point(0, 10))  # HORZ
    # closing line will be (0,10) to (0,0) -> VERT
    path.finalize()

    horz = list(path.horizontal)
    assert len(horz) == 2
    assert all(line.orientation == LineOrientation.HORZ for line in horz)


def test_base_path_vertical_properties():
    path = BasePath()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))  # HORZ
    path.add_point(Point(10, 10)) # VERT
    path.add_point(Point(0, 10))  # HORZ
    # closing line will be (0,10) to (0,0) -> VERT
    path.finalize()

    vert = list(path.vertical)
    assert len(vert) == 2
    assert all(line.orientation == LineOrientation.VERT for line in vert)


def test_base_path_line_repr():
    path = BasePath()
    path.add_point(Point(0, 0))
    path.add_point(Point(10, 0))
    path.finalize()
    line = path.lines[0]
    # PathLine(p1=Point(x=0, y=0), p2=Point(x=10, y=0), type=<LineOrientation.HORZ: 'horizontal'>, breaks=[])
    assert "PathLine" in repr(line)
    assert "breaks=[]" in repr(line)


def test_base_path_horizontal_vertical_empty():
    path = BasePath()
    # No points, or no finalize() -> lines empty
    assert list(path.horizontal) == []
    assert list(path.vertical) == []

    path.add_point(Point(0,0))
    path.add_point(Point(10,0))
    path.finalize()
    assert len(path.lines) == 2


def test_typed_base_path_abstract_instantiation():
    from tray.geometry.typed_base_path import FinalizableTypedBasePath
    class SubPath3(FinalizableTypedBasePath):
        def _make_line(self, p1, p2):
            return super()._make_line(p1, p2)
            
    s3 = SubPath3()
    s3.add_point(Point(0,0))
    s3.add_point(Point(10,0))
    with pytest.raises(NotImplementedError):
        s3.finalize()
