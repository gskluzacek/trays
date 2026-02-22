import pytest
from tray.geometry.basic.point import Point
from tray.geometry.basic.path import PathOrientation


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


def test_point_equality_equal():
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    assert p1 == p2


def test_point_equality_not_equal_y():
    p1 = Point(1, 2)
    p3 = Point(1, 5)
    assert p1 != p3


def test_point_equality_not_equal_x():
    p1 = Point(1, 2)
    p4 = Point(5, 2)
    assert p1 != p4


def test_point_equality_with_tuple():
    p1 = Point(1, 2)
    assert p1 == (1, 2)


def test_point_equality_with_tuple_reverse():
    p1 = Point(1, 2)
    assert (1, 2) == p1


def test_point_equality_with_different_tuple():
    p1 = Point(1, 2)
    assert p1 != (1, 5)


def test_point_equality_with_incompatible_type():
    p1 = Point(1, 2)
    assert p1 != "string"


def test_point_equality_with_incorrect_tuple_length():
    p1 = Point(1, 2)
    assert p1 != (1, 2, 3)


def test_point_ordering_same_x_different_y():
    p1 = Point(1, 2)
    p2 = Point(1, 5)
    assert p1 < p2
    assert p2 > p1
    assert p1 <= p2
    assert p2 >= p1


def test_point_ordering_same_y_different_x():
    p1 = Point(1, 2)
    p3 = Point(5, 2)
    assert p1 < p3
    assert p3 > p1
    assert p1 <= p3
    assert p3 >= p1


def test_point_ordering_equality():
    p1 = Point(1, 2)
    p1_copy = Point(1, 2)
    assert p1 <= p1_copy
    assert p1 >= p1_copy


def test_point_ordering_incompatible_type():
    p1 = Point(1, 2)
    with pytest.raises(TypeError):
        _ = p1 < 10


def test_is_orthogonal_x_axis():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    assert p1.is_orthogonal(p2) is True


def test_is_orthogonal_y_axis():
    p1 = Point(0, 0)
    p3 = Point(0, 10)
    assert p1.is_orthogonal(p3) is True


def test_is_orthogonal_diagonal():
    p1 = Point(0, 0)
    p4 = Point(10, 10)
    assert p1.is_orthogonal(p4) is False


def test_is_orthogonal_same_point():
    p1 = Point(0, 0)
    assert p1.is_orthogonal(p1) is False


def test_point_negative_x_raises():
    with pytest.raises(ValueError, match="x and y must be non-negative"):
        Point(-1, 0)


def test_point_negative_y_raises():
    with pytest.raises(ValueError, match="x and y must be non-negative"):
        Point(0, -1)


def test_point_le_incompatible_type():
    p1 = Point(1, 2)
    with pytest.raises(TypeError):
        _ = p1 <= 10


def test_point_gt_incompatible_type():
    p1 = Point(1, 2)
    with pytest.raises(TypeError):
        _ = p1 > 10
