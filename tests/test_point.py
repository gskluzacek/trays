import pytest
from tray.geometry.point import Point, PathOrientation


def test_point_init():
    p = Point(10, 20)
    assert p.x == 10
    assert p.y == 20


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
    p2 = Point(10, 0)
    p3 = Point(20, 0)
    assert p1.orientation(p2, p3) == PathOrientation.COL


def test_orientation_clockwise():
    # p1=(0,0), p2=(10,0), p3=(10,10) -> val = (0*0) - (10*10) = -100 -> CW
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    p3 = Point(10, 10)
    assert p1.orientation(p2, p3) == PathOrientation.CW


def test_orientation_counter_clockwise():
    # p1=(0,0), p2=(0,10), p3=(10,10) -> val = (10*10) - (0*0) = 100 -> CCW
    p1 = Point(0, 0)
    p2 = Point(0, 10)
    p3 = Point(10, 10)
    assert p1.orientation(p2, p3) == PathOrientation.CCW


def test_point_with_floats():
    p = Point(1.5, 2.5)
    assert p.x == 1.5
    assert p.y == 2.5
    assert p.coords == (1.5, 2.5)
