from __future__ import annotations
from tray.geometry.point import Point
from tray.geometry.line import Line, LineOrientation
from tray.geometry.wall_line import WallLine, WallType


def test_wall_line_init():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    wall = WallLine(p1, p2)
    assert wall.p1 == p1
    assert wall.p2 == p2
    assert wall.orientation == LineOrientation.HORZ
    assert wall.wall_type == WallType.NONE


def test_wall_line_init_with_type():
    p1 = Point(0, 0)
    p2 = Point(0, 10)
    wall = WallLine(p1, p2, wall_type=WallType.EXTERIOR)
    assert wall.p1 == p1
    assert wall.p2 == p2
    assert wall.orientation == LineOrientation.VERT
    assert wall.wall_type == WallType.EXTERIOR


def test_wall_line_generics():
    p1 = Point[int](0, 0)
    p2 = Point[int](10, 0)
    wall = WallLine[int](p1, p2)
    assert isinstance(wall.p1.x, int)

    p1_f = Point[float](0.0, 0.0)
    p2_f = Point[float](10.0, 0.0)
    wall_f = WallLine[float](p1_f, p2_f)
    assert isinstance(wall_f.p1.x, float)


def test_wall_line_classify_wall():
    # This is also tested in test_wall_classification.py,
    # but let's add a basic one here to ensure the method works on the class.
    wall = WallLine(Point(0, 0), Point(10, 0))
    path_line = Line(Point(2, 0), Point(8, 0))
    # Wall contains path -> COMBO
    assert wall.classify_wall(path_line, LineOrientation.HORZ) == WallType.COMBO
