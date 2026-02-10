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


def test_point_equality():
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(1, 5)
    p4 = Point(5, 2)

    assert p1 == p2
    assert p1 != p3
    assert p1 != p4

    # Comparison with tuple
    assert p1 == (1, 2)
    assert (1, 2) == p1
    assert p1 != (1, 5)

    # Comparison with incompatible type
    assert p1 != "string"
    assert p1 != (1, 2, 3)  # Incorrect tuple length


def test_point_ordering():
    p1 = Point(1, 2)
    p2 = Point(1, 5)
    p3 = Point(5, 2)

    # Same x, different y
    assert p1 < p2
    assert p2 > p1
    assert p1 <= p2
    assert p2 >= p1

    # Same y, different x
    assert p1 < p3
    assert p3 > p1
    assert p1 <= p3
    assert p3 >= p1

    # Equality ordering
    p1_copy = Point(1, 2)
    assert p1 <= p1_copy
    assert p1 >= p1_copy


# def test_point_invalid_comparison():
#     p1 = Point(1, 2)
#     p2 = Point(5, 5)  # Neither x nor y match
#
#     with pytest.raises(ValueError, match="Unsupported comparison"):
#         _ = p1 == p2
#
#     with pytest.raises(ValueError, match="Unsupported comparison"):
#         _ = p1 < p2
#
#     with pytest.raises(ValueError, match="Unsupported comparison"):
#         _ = p1 <= p2


def test_point_ordering_incompatible_type():
    p1 = Point(1, 2)
    with pytest.raises(TypeError):
        _ = p1 < 10


def test_is_orthogonal():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    p3 = Point(0, 10)
    p4 = Point(10, 10)

    assert p1.is_orthogonal(p2) is True
    assert p1.is_orthogonal(p3) is True
    assert p1.is_orthogonal(p4) is False
    assert p1.is_orthogonal(p1) is False

def test_point_negative_coords_raises():
    with pytest.raises(ValueError, match="x and y must be non-negative"):
        Point(-1, 0)
    with pytest.raises(ValueError, match="x and y must be non-negative"):
        Point(0, -1)

def test_point_le_gt_incompatible_type():
    p1 = Point(1, 2)
    with pytest.raises(TypeError):
        _ = p1 <= 10
    with pytest.raises(TypeError):
        _ = p1 > 10
