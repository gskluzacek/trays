import pytest
from tray.geometry.point import Point
from tray.geometry.line import Line, LineOrientation


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


def test_line_is_vertical():
    assert Line(Point(0, 0), Point(0, 10)).is_vertical is True
    assert Line(Point(0, 0), Point(10, 0)).is_vertical is False


def test_line_is_horizontal():
    assert Line(Point(0, 0), Point(10, 0)).is_horizontal is True
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


def test_line_is_overlapping():
    # Horizontal
    l1 = Line(Point(0, 0), Point(10, 0))
    l2 = Line(Point(5, 0), Point(15, 0)) # Overlap
    l3 = Line(Point(10, 0), Point(20, 0)) # Touch at endpoint
    l4 = Line(Point(11, 0), Point(20, 0)) # No overlap
    l5 = Line(Point(0, 1), Point(10, 1)) # Different y

    assert l1.is_overlapping(l2) is True
    assert l1.is_overlapping(l3) is True
    assert l1.is_overlapping(l4) is False
    assert l1.is_overlapping(l5) is False

    # Vertical
    v1 = Line(Point(0, 0), Point(0, 10))
    v2 = Line(Point(0, 5), Point(0, 15)) # Overlap
    v3 = Line(Point(0, 10), Point(0, 20)) # Touch at endpoint
    v4 = Line(Point(0, 11), Point(0, 20)) # No overlap
    v5 = Line(Point(1, 0), Point(1, 10)) # Different x

    assert v1.is_overlapping(v2) is True
    assert v1.is_overlapping(v3) is True
    assert v1.is_overlapping(v4) is False
    assert v1.is_overlapping(v5) is False

    # Mixed
    assert l1.is_overlapping(v1) is False
