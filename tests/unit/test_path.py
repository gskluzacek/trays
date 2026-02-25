from tray.geometry.basic.point import Point
from tray.geometry.basic.path import Path


def test_path_init_empty():
    path = Path()
    assert path.points == []


def test_path_init_with_start_point():
    p = Point(0, 0)
    path = Path(start_point=p)
    assert path.points == [p]


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
