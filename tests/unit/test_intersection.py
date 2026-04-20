from tray.geometry.basic.point import Point
from tray.geometry.intersection import Intersection
from tray.geometry.types.tray import IntrxnType


def test_intersection_init_sets_attributes():
    intrxn = Intersection(Point(3, 4), IntrxnType.CROSS)

    assert intrxn.intrxn_pt == Point(3, 4)
    assert intrxn.intrxn_type == IntrxnType.CROSS


def test_intersection_repr():
    intrxn = Intersection(Point(1, 2), IntrxnType.TEE_L)

    assert repr(intrxn) == "Intersection((1, 2), IntrxnType.TEE_L)"


def test_intersection_str():
    intrxn = Intersection(Point(7, 9), IntrxnType.CORNER_RT)

    assert str(intrxn) == "Intersection type IntrxnType.CORNER_RT at (7, 9)"
