import pytest
from tray.geometry.basic.point import Point
from tray.geometry.basic.line import Line
from tray.geometry.types.geometric import LineOrientation


def test_line_init_horizontal():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    line = Line(p1, p2)
    assert line.p1 == p1
    assert line.p2 == p2
    assert line.orientation == LineOrientation.HORZ


def test_line_init_vertical():
    p1 = Point(0, 0)
    p2 = Point(0, 10)
    line = Line(p1, p2)
    assert line.p1 == p1
    assert line.p2 == p2
    assert line.orientation == LineOrientation.VERT


def test_line_orientation_error():
    p1 = Point(0, 0)
    p2 = Point(10, 10)  # Diagonal! - Not horizontal or vertical
    with pytest.raises(ValueError, match="cannot set line orientation for points that are not collinear"):
        Line(p1, p2)


def test_line_repr():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    line = Line(p1, p2)
    # Line(p1=Point(x=0, y=0), p2=Point(x=10, y=0), type=<LineOrientation.HORZ: 'horizontal'>)
    expected = f"Line(p1={p1!r}, p2={p2!r}, type={LineOrientation.HORZ!r})"
    assert repr(line) == expected


def test_line_str():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    line = Line(p1, p2)
    # [[0, 0], [10, 0], LineOrientation.HORZ]
    expected = f"[{p1}, {p2}, {LineOrientation.HORZ}]"
    assert str(line) == expected


def test_line_with_floats():
    p1 = Point(1.1, 2.2)
    p2 = Point(1.1, 5.5)
    line = Line(p1, p2)
    assert line.orientation == LineOrientation.VERT


def test_line_normalize_already_normalized():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    line = Line(p1, p2)
    p1_norm, p2_norm = line.normalize
    assert p1_norm == p1
    assert p2_norm == p2


def test_line_normalize_needs_normalization():
    p1 = Point(10, 0)
    p2 = Point(0, 0)
    line = Line(p1, p2)
    p1_norm, p2_norm = line.normalize
    assert p1_norm.coords == (0, 0)
    assert p2_norm.coords == (10, 0)
    # Ensure original line is unchanged
    assert line.p1.coords == (10, 0)
    assert line.p2.coords == (0, 0)


def test_line_of_orientation_horz():
    lines = [
        Line(Point(0, 0), Point(10, 0)),
        Line(Point(0, 0), Point(0, 10)),
        Line(Point(5, 5), Point(15, 5)),
    ]
    horz_lines = list(Line.of_orientation(lines, LineOrientation.HORZ))
    assert len(horz_lines) == 2
    assert all(line.is_horizontal for line in horz_lines)
    assert horz_lines[0].p1.coords == (0, 0)
    assert horz_lines[1].p1.coords == (5, 5)


def test_line_of_orientation_vert():
    lines = [
        Line(Point(0, 0), Point(10, 0)),
        Line(Point(0, 0), Point(0, 10)),
        Line(Point(5, 5), Point(5, 15)),
    ]
    vert_lines = list(Line.of_orientation(lines, LineOrientation.VERT))
    assert len(vert_lines) == 2
    assert all(line.is_vertical for line in vert_lines)
    assert vert_lines[0].p2.coords == (0, 10)
    assert vert_lines[1].p2.coords == (5, 15)


def test_line_of_orientation_none_matching():
    lines = [
        Line(Point(0, 0), Point(10, 0)),
    ]
    vert_lines = list(Line.of_orientation(lines, LineOrientation.VERT))
    assert len(vert_lines) == 0


def test_line_is_vertical_true():
    assert Line(Point(0, 0), Point(0, 10)).is_vertical is True


def test_line_is_vertical_false():
    assert Line(Point(0, 0), Point(10, 0)).is_vertical is False


def test_line_is_horizontal_true():
    assert Line(Point(0, 0), Point(10, 0)).is_horizontal is True


def test_line_is_horizontal_false():
    assert Line(Point(0, 0), Point(0, 10)).is_horizontal is False


def test_line_is_collinear_vertical():
    l1 = Line(Point(0, 0), Point(0, 10))
    l2 = Line(Point(0, 5), Point(0, 15))
    l3 = Line(Point(1, 0), Point(1, 10))

    assert l1.is_collinear(l2) is True
    assert l1.is_collinear(l3) is False


def test_line_is_collinear_horizontal():
    l1 = Line(Point(0, 0), Point(10, 0))
    l2 = Line(Point(5, 0), Point(15, 0))
    l3 = Line(Point(0, 1), Point(10, 1))

    assert l1.is_collinear(l2) is True
    assert l1.is_collinear(l3) is False


def test_line_is_collinear_mixed_raises():
    l_vert = Line(Point(0, 0), Point(0, 10))
    l_horz = Line(Point(0, 0), Point(10, 0))

    with pytest.raises(ValueError, match="cannot compare vertical lines with non-vertical lines"):
        l_vert.is_collinear(l_horz)

    with pytest.raises(ValueError, match="cannot compare non-vertical lines with vertical lines"):
        l_horz.is_collinear(l_vert)


def test_line_of_orientation_empty():
    lines = []
    horz_lines = list(Line.of_orientation(lines, LineOrientation.HORZ))
    assert len(horz_lines) == 0


def test_line_is_overlapping_horizontal_overlap():
    l1 = Line(Point(0, 0), Point(10, 0))
    l2 = Line(Point(5, 0), Point(15, 0))
    assert l1.is_overlapping(l2) is True


def test_line_is_overlapping_horizontal_touch():
    l1 = Line(Point(0, 0), Point(10, 0))
    l3 = Line(Point(10, 0), Point(20, 0))
    assert l1.is_overlapping(l3) is False


def test_line_is_overlapping_horizontal_no_overlap():
    l1 = Line(Point(0, 0), Point(10, 0))
    l4 = Line(Point(11, 0), Point(20, 0))
    assert l1.is_overlapping(l4) is False


def test_line_is_overlapping_horizontal_different_y():
    l1 = Line(Point(0, 0), Point(10, 0))
    l5 = Line(Point(0, 1), Point(10, 1))
    assert l1.is_overlapping(l5) is False


def test_line_is_overlapping_vertical_overlap():
    v1 = Line(Point(0, 0), Point(0, 10))
    v2 = Line(Point(0, 5), Point(0, 15))
    assert v1.is_overlapping(v2) is True


def test_line_is_overlapping_vertical_touch():
    v1 = Line(Point(0, 0), Point(0, 10))
    v3 = Line(Point(0, 10), Point(0, 20))
    assert v1.is_overlapping(v3) is False


def test_line_is_overlapping_vertical_no_overlap():
    v1 = Line(Point(0, 0), Point(0, 10))
    v4 = Line(Point(0, 11), Point(0, 20))
    assert v1.is_overlapping(v4) is False


def test_line_is_overlapping_vertical_different_x():
    v1 = Line(Point(0, 0), Point(0, 10))
    v5 = Line(Point(1, 0), Point(1, 10))
    assert v1.is_overlapping(v5) is False


def test_line_is_overlapping_mixed():
    l1 = Line(Point(0, 0), Point(10, 0))
    v1 = Line(Point(0, 0), Point(0, 10))
    assert l1.is_overlapping(v1) is False


def test_line_wall_inside_path_not_collinear_raises():
    l1 = Line(Point(0, 0), Point(10, 0))
    l2 = Line(Point(0, 1), Point(10, 1))
    with pytest.raises(
        ValueError, match="cannot determine endpoints of wall line that are inside path line if lines are not collinear"
    ):
        l1.wall_inside_path(l2)


def test_line_equality():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    l1 = Line(p1, p2)
    l2 = Line(p1, p2)
    l3 = Line(p2, p1)  # Same segment, different order
    l4 = Line(Point(0, 1), Point(10, 1))

    assert l1 == l2
    assert l1 == l3
    assert l1 != l4
    assert l1 == ((0, 0), (10, 0))
    assert l1 == [Point(0, 0), Point(10, 0)]
    assert l1 != "not a line"


def test_line_comparison():
    l1 = Line(Point(0, 0), Point(10, 0))
    l2 = Line(Point(0, 1), Point(10, 1))
    l3 = Line(Point(1, 0), Point(11, 0))

    # Based on normalized points: ((0, 0), (10, 0)) < ((0, 1), (10, 1))
    assert l1 < l2
    assert l1 <= l2
    assert l2 > l1
    assert l2 >= l1

    # Based on normalized points: ((0, 0), (10, 0)) < ((1, 0), (11, 0))
    assert l1 < l3
    assert l1 <= l3
    assert l3 > l1
    assert l3 >= l1

    # Comparison with coerced types
    assert l1 < ((0, 1), (10, 1))
    assert l1 <= ((0, 0), (10, 0))


def test_line_comparison_unsupported_type():
    l1 = Line(Point(0, 0), Point(10, 0))
    with pytest.raises(TypeError):
        _ = l1 < 5
