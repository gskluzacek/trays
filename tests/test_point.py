import pytest
from point import Point, PathOrientation, LineOrientation

def test_point_init():
    p = Point(10, 20)
    assert p.x == 10
    assert p.y == 20
    assert p.line_orientation == LineOrientation.NONE

def test_point_line_orientation_setter():
    p = Point(0, 0)
    p.line_orientation = LineOrientation.VERT
    assert p.line_orientation == LineOrientation.VERT
    p.line_orientation = LineOrientation.HORZ
    assert p.line_orientation == LineOrientation.HORZ

def test_set_line_orientation_vertical():
    p1 = Point(10, 20)
    p2 = Point(10, 30)
    p1.set_line_orientation(p2)
    assert p1.line_orientation == LineOrientation.VERT

def test_set_line_orientation_horizontal():
    p1 = Point(10, 20)
    p2 = Point(30, 20)
    p1.set_line_orientation(p2)
    assert p1.line_orientation == LineOrientation.HORZ

def test_set_line_orientation_error():
    p1 = Point(10, 20)
    p2 = Point(30, 40)
    with pytest.raises(ValueError, match="cannot set line orientation for points that are not collinear"):
        p1.set_line_orientation(p2)

def test_point_repr():
    p = Point(1, 2)
    assert repr(p) == "Point(x=1, y=2)"

def test_point_str():
    p = Point(1, 2)
    assert str(p) == "[1, 2]"

def test_point_coords():
    p = Point(5, 15)
    assert p.coords == (5, 15)

def test_orientation_collinear():
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    p3 = Point(2, 2)
    assert p1.orientation(p2, p3) == PathOrientation.COL

def test_orientation_clockwise():
    # In quadrant 4 (y increases downwards), or standard Cartesian?
    # val = ((y2 - y1) * (x3 - x2)) - ((x2 - x1) * (y3 - y2))
    # If val < 0, it's CW.
    # p1=(0,0), p2=(1,0), p3=(1,1)
    # y1=0, x1=0; y2=0, x2=1; y3=1, x3=1
    # val = ((0 - 0) * (1 - 1)) - ((1 - 0) * (1 - 0))
    # val = (0 * 0) - (1 * 1) = -1
    # Should be CW.
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    p3 = Point(1, 1)
    assert p1.orientation(p2, p3) == PathOrientation.CW

def test_orientation_counter_clockwise():
    # p1=(0,0), p2=(1,1), p3=(1,0)
    # y1=0, x1=0; y2=1, x2=1; y3=0, x3=1
    # val = ((1 - 0) * (1 - 1)) - ((1 - 0) * (0 - 1))
    # val = (1 * 0) - (1 * -1) = 1
    # Should be CCW.
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    p3 = Point(1, 0)
    assert p1.orientation(p2, p3) == PathOrientation.CCW

def test_point_with_floats():
    p = Point(1.5, 2.5)
    assert p.x == 1.5
    assert p.y == 2.5
    assert p.coords == (1.5, 2.5)
