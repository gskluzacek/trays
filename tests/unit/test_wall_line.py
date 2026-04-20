from __future__ import annotations
import pytest
from tray.geometry.basic.point import Point
from tray.geometry.base.path_line import PathLine
from tray.geometry.types.tray import WallType
from tray.geometry.types.geometric import LineOrientation
from tray.geometry.types.geometric import PointLine
from tray.geometry.types.tray import IntrxnType, JointType
from tray.geometry.intersection import Intersection
from tray.geometry.wall_line import WallLine


def test_wall_line_init():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    wall = WallLine(p1, p2)
    assert wall.p1 == p1
    assert wall.p2 == p2
    assert wall.orientation == LineOrientation.HORZ
    assert wall.wall_type == WallType.NONE
    assert wall.intersections == []


def test_wall_line_init_with_type():
    p1 = Point(0, 0)
    p2 = Point(0, 10)
    wall = WallLine(p1, p2, wall_type=WallType.EXTERIOR)
    assert wall.p1 == p1
    assert wall.p2 == p2
    assert wall.orientation == LineOrientation.VERT
    assert wall.wall_type == WallType.EXTERIOR


def test_wall_line_generics_int():
    p1 = Point[int](0, 0)
    p2 = Point[int](10, 0)
    wall = WallLine(p1, p2)
    assert isinstance(wall.p1.x, int)


def test_wall_line_classify_wall():
    # This is also tested in test_wall_classification.py,
    # but let's add a basic one here to ensure the method works on the class.
    wall = WallLine(Point(0, 0), Point(10, 0))
    path_line = PathLine(Point(2, 0), Point(8, 0))
    # Wall contains path -> COMBO
    assert wall.classify_wall(path_line) == WallType.COMBO


def test_wall_line_repr():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    wall = WallLine(p1, p2, wall_type=WallType.INTERIOR)
    expected = f"Line(p1={p1!r}, p2={p2!r}, type={wall.orientation!r}, wall_type={WallType.INTERIOR!r}, segment_path=[])"
    assert repr(wall) == expected


def test_classify_wall_horizontal_interior_disjoint():
    # Wall is completely separate from path
    wall = WallLine(Point(0, 0), Point(2, 0))
    path_line = PathLine(Point(3, 0), Point(5, 0))
    assert wall.classify_wall(path_line) == WallType.INTERIOR


def test_classify_wall_horizontal_interior_touching():
    # Wall is collinear but not overlapping (touching at end)
    wall = WallLine(Point(0, 0), Point(2, 0))
    path_line = PathLine(Point(2, 0), Point(4, 0))
    assert wall.classify_wall(path_line) == WallType.INTERIOR


def test_classify_wall_horizontal_interior_not_collinear():
    # Not collinear
    wall = WallLine(Point(0, 1), Point(2, 1))
    path_line = PathLine(Point(0, 0), Point(2, 0))
    # WallType.INTERIOR is returned if not collinear
    assert wall.classify_wall(path_line) == WallType.INTERIOR


def test_classify_wall_horizontal_exterior_within():
    # Wall within path
    wall = WallLine(Point(1, 0), Point(2, 0))
    path_line = PathLine(Point(0, 0), Point(3, 0))
    assert wall.classify_wall(path_line) == WallType.EXTERIOR


def test_classify_wall_horizontal_exterior_equal():
    # Wall equals path
    wall = WallLine(Point(0, 0), Point(3, 0))
    path_line = PathLine(Point(0, 0), Point(3, 0))
    assert wall.classify_wall(path_line) == WallType.EXTERIOR


def test_classify_wall_horizontal_exterior_share_end():
    # Wall shares one end and is within path
    wall = WallLine(Point(0, 0), Point(2, 0))
    path_line = PathLine(Point(0, 0), Point(3, 0))
    assert wall.classify_wall(path_line) == WallType.EXTERIOR


def test_classify_wall_horizontal_combo_partial_overlap():
    # Partial overlap
    wall = WallLine(Point(0, 0), Point(4, 0))
    path_line = PathLine(Point(2, 0), Point(6, 0))
    assert wall.classify_wall(path_line) == WallType.COMBO


def test_classify_wall_horizontal_combo_contains():
    # Wall contains path
    wall = WallLine(Point(0, 0), Point(5, 0))
    path_line = PathLine(Point(1, 0), Point(3, 0))
    assert wall.classify_wall(path_line) == WallType.COMBO


def test_classify_wall_vertical_exterior():
    # Exterior
    wall = WallLine(Point(0, 1), Point(0, 2))
    path_line = PathLine(Point(0, 0), Point(0, 3))
    assert wall.classify_wall(path_line) == WallType.EXTERIOR


def test_classify_wall_vertical_interior():
    # Interior
    wall = WallLine(Point(0, 4), Point(0, 5))
    path_line = PathLine(Point(0, 0), Point(0, 3))
    assert wall.classify_wall(path_line) == WallType.INTERIOR


def test_classify_wall_vertical_combo():
    # Combo
    # shift everything up by 1 to avoid negative coordinates
    wall = WallLine(Point(0, 0), Point(0, 3))
    path_line = PathLine(Point(0, 1), Point(0, 4))
    assert wall.classify_wall(path_line) == WallType.COMBO


def test_classify_wall_unhandled_collinear_configuration():
    from unittest.mock import patch, PropertyMock

    wall = WallLine(Point(0, 0), Point(2, 0))
    path_line = PathLine(Point(0, 0), Point(2, 0))

    with patch.object(WallLine, "is_collinear", return_value=True):
        with patch.object(WallLine, "normalize", new_callable=PropertyMock) as mock_normalize:
            mock_normalize.side_effect = [(Point(float("nan"), 0), Point(float("nan"), 0)), (Point(0, 0), Point(1, 0))]
            with pytest.raises(ValueError, match="Unhandled collinear configuration"):
                wall.classify_wall(path_line)


def test_determine_segments_with_intrxn_adds_intersection_for_point_on_segment():
    wall = WallLine(Point(0, 0), Point(10, 0))
    wall.segment_path.add_segment(Point(0, 0), Point(5, 0), JointType.NONE)
    wall.segment_path.add_segment(Point(5, 0), Point(10, 0), JointType.NONE)
    intrxn = Intersection(Point(5, 0), IntrxnType.CROSS)

    wall.determine_segments_with_intrxn(intrxn)

    first_intersections = wall.segment_path.lines[0].intersections
    second_intersections = wall.segment_path.lines[1].intersections
    assert len(first_intersections) == 1
    assert len(second_intersections) == 1
    assert first_intersections[0].pt_chk == PointLine.P2
    assert second_intersections[0].pt_chk == PointLine.P1
    assert first_intersections[0].intrxn is intrxn
    assert second_intersections[0].intrxn is intrxn


def test_determine_segments_with_intrxn_skips_point_outside_segments():
    wall = WallLine(Point(0, 0), Point(10, 0))
    wall.segment_path.add_segment(Point(0, 0), Point(5, 0), JointType.NONE)
    wall.segment_path.add_segment(Point(5, 0), Point(10, 0), JointType.NONE)
    intrxn = Intersection(Point(11, 0), IntrxnType.CROSS)

    wall.determine_segments_with_intrxn(intrxn)

    assert wall.segment_path.lines[0].intersections == []
    assert wall.segment_path.lines[1].intersections == []
