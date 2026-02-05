from __future__ import annotations

import pytest
from unittest.mock import patch

from tray.geometry.point import Point
from tray.geometry.line import Line, LineOrientation, WallType
from tray.tray import Tray


def test_classify_wall_horizontal_interior():
    # Wall is completely separate from path
    wall = Line(Point(0, 0), Point(2, 0))
    path_line = Line(Point(3, 0), Point(5, 0))
    assert Line.classify_wall(wall, path_line, LineOrientation.HORZ) == WallType.INTERIOR

    # Wall is collinear but not overlapping (touching at end)
    wall = Line(Point(0, 0), Point(2, 0))
    path_line = Line(Point(2, 0), Point(4, 0))
    assert Line.classify_wall(wall, path_line, LineOrientation.HORZ) == WallType.INTERIOR

    # Not collinear
    wall = Line(Point(0, 1), Point(2, 1))
    path_line = Line(Point(0, 0), Point(2, 0))
    # WallType.INTERIOR is returned if not collinear
    assert Line.classify_wall(wall, path_line, LineOrientation.HORZ) == WallType.INTERIOR


def test_classify_wall_horizontal_exterior():
    # Wall within path
    wall = Line(Point(1, 0), Point(2, 0))
    path_line = Line(Point(0, 0), Point(3, 0))
    assert Line.classify_wall(wall, path_line, LineOrientation.HORZ) == WallType.EXTERIOR

    # Wall equals path
    wall = Line(Point(0, 0), Point(3, 0))
    path_line = Line(Point(0, 0), Point(3, 0))
    assert Line.classify_wall(wall, path_line, LineOrientation.HORZ) == WallType.EXTERIOR

    # Wall shares one end and is within path
    wall = Line(Point(0, 0), Point(2, 0))
    path_line = Line(Point(0, 0), Point(3, 0))
    assert Line.classify_wall(wall, path_line, LineOrientation.HORZ) == WallType.EXTERIOR


def test_classify_wall_horizontal_combo():
    # Partial overlap
    wall = Line(Point(0, 0), Point(4, 0))
    path_line = Line(Point(2, 0), Point(6, 0))
    assert Line.classify_wall(wall, path_line, LineOrientation.HORZ) == WallType.COMBO

    # Wall contains path
    wall = Line(Point(0, 0), Point(5, 0))
    path_line = Line(Point(1, 0), Point(3, 0))
    assert Line.classify_wall(wall, path_line, LineOrientation.HORZ) == WallType.COMBO


def test_classify_wall_vertical():
    # Exterior
    wall = Line(Point(0, 1), Point(0, 2))
    path_line = Line(Point(0, 0), Point(0, 3))
    assert Line.classify_wall(wall, path_line, LineOrientation.VERT) == WallType.EXTERIOR

    # Interior
    wall = Line(Point(0, 4), Point(0, 5))
    path_line = Line(Point(0, 0), Point(0, 3))
    assert Line.classify_wall(wall, path_line, LineOrientation.VERT) == WallType.INTERIOR

    # Combo
    # shift everything up by 1 to avoid negative coordinates
    wall = Line(Point(0, 0), Point(0, 3))
    path_line = Line(Point(0, 1), Point(0, 4))
    assert Line.classify_wall(wall, path_line, LineOrientation.VERT) == WallType.COMBO


def test_tray_classify_index_walls():
    material_thickness = 5.0
    inside_dim_cols = [100.0, 100.0, 100.0]
    inside_dim_rows = [100.0, 100.0, 100.0]
    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # Path that touches all boundaries:
    # (0,0) -> (3,0) -> (3,3) -> (0,3)
    tray.start_base(0, 0)
    tray.extend_base(3, 0)
    tray.extend_base(3, 3)
    tray.extend_base(0, 3)
    tray.end_base()

    # Add an exterior wall
    tray.add_wall((0, 0), (1, 0))
    # Add an interior wall
    tray.add_wall((1, 1), (2, 1))

    # Path segments for tray2:
    tray2 = Tray(material_thickness, inside_dim_cols, inside_dim_rows)
    tray2.start_base(0, 0)
    tray2.extend_base(3, 0)
    tray2.extend_base(3, 3)
    tray2.extend_base(2, 3)
    tray2.extend_base(2, 1)
    tray2.extend_base(1, 1)
    tray2.extend_base(1, 3)
    tray2.extend_base(0, 3)
    tray2.end_base()

    # Wall (1,1)-(2,1) matches L5 exactly -> EXTERIOR
    tray2.add_wall((1, 1), (2, 1))

    # Wall (0,1)-(3,1) is HORZ. -> COMBO
    tray2.add_wall((0, 1), (3, 1))

    # Wall (0,2)-(1,2) is HORZ. -> INTERIOR
    tray2.add_wall((0, 2), (1, 2))

    # No exception means it passed internal logic. 
    # Individual wall classification is tested in test_classify_index_wall_unit.
    tray2.classify_index_walls()


def test_classify_wall_invalid_orientation():
    wall = Line(Point(0, 0), Point(2, 0))
    path_line = Line(Point(3, 0), Point(5, 0))
    with pytest.raises(ValueError, match="orientation must be either vertical or horizontal"):
        Line.classify_wall(wall, path_line, LineOrientation.NONE)


def test_classify_wall_unhandled_collinear_configuration():
    ## the below comments are from Junie - reasoning how to test the case _: "catch all" case if none of the
    ## above cases are true. Which should be theoretically impossible as we have been very careful to test for
    ## every possible interval relation. Might just be more practical to set the code as `# pragma: no cover

    wall = Line(Point(0, 0), Point(2, 0))
    path_line = Line(Point(0, 0), Point(2, 0))

    # To reach the 'case _' in classify_wall, we need col to be True but none of the 'case True if ...' to match.
    # However, 'case True if w1 == p1 and w2 == p2' should match the above points.
    # We can use mocking to force 'is_collinear' to return True, but provide values that don't match any branch.
    # Actually, if we mock the normalize property or the values p1, p2, w1, w2, we can trigger it.

    # Let's try to find a real case first.
    # The match branches for 'case True' cover:
    # 1. w2 <= p1 or w1 >= p2 (disjoint)
    # 2. w1 < p1 < w2 < p2 or p1 < w1 < p2 < w2 (partial overlap)
    # 3. (w1 == p1 and w2 > p2) or (w2 == p2 and w1 < p1) (w contains p, sharing one end)
    # 4. w1 < p1 and w2 > p2 (w contains p, no shared ends)
    # 5. (w1 == p1 and w2 < p2) or (w2 == p2 and w1 > p1) (p contains w, sharing one end)
    # 6. p1 < w1 and w2 < p2 (p contains w, no shared ends)
    # 7. w1 == p1 and w2 == p2 (equal)

    # These should cover ALL possible relations between two intervals [w1, w2] and [p1, p2] where w1 < w2 and p1 < p2.
    # To trigger case _, we can use a mock to return a value that doesn't match.

    with patch.object(Line, "is_collinear", return_value=True):
        # We need to pass horizontal lines so we get into the HORZ block and get w1, w2, p1, p2 as numbers.
        # But we want them to NOT match any case.
        # This is hard because the cases seem exhaustive for numbers.
        # If we make w1 > w2 it might break some assumptions but normalize should prevent that.
        # Wait, if we mock 'normalize' to return something weird?

        # Another way: pass something that isn't a number?
        # But the match is 'case True if ...', if 'col' is True it will check 'if' conditions.
        # If none of the 'if' conditions match, it goes to 'case _'.

        # Let's try to mock the normalize result to be something that fails all 'if' guards.
        # But wait, 'case True' with multiple 'if' guards... if none match it doesn't automatically go to 'case _'
        # unless 'case _' is the next one.

        # Actually, in Python match:
        # case True if cond1: ...
        # case True if cond2: ...
        # case _: ...
        # If col is True but cond1 and cond2 are False, it GOES to case _.

        # So we just need to make all 'if' conditions False while col is True.
        # Since the conditions cover all interval relations, we might need to mock the points to be non-numeric
        # or something that fails all comparisons (though most comparisons are exhaustive).

        # Let's mock 'Line.normalize' to return something that will result in w1, w2, p1, p2 being NaN?
        # No, NaN comparisons usually return False.

        # Need to use PropertyMock for cached_property if we want to mock it on the instance or class level properly
        # but Line.normalize is a cached_property, so it's accessed like an attribute.
        from unittest.mock import PropertyMock

        with patch.object(Line, "normalize", new_callable=PropertyMock) as mock_normalize:
            mock_normalize.side_effect = [(Point(float("nan"), 0), Point(float("nan"), 0)), (Point(0, 0), Point(1, 0))]
            with pytest.raises(ValueError, match="Unhandled collinear configuration"):
                Line.classify_wall(wall, path_line, LineOrientation.HORZ)
