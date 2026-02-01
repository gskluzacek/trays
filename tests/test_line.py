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


def test_line_get_normalized_line_already_normalized():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    line = Line(p1, p2)
    normalized = line.get_normalized_line()
    assert normalized.p1 == p1
    assert normalized.p2 == p2
    assert normalized.orientation == LineOrientation.HORZ


def test_line_get_normalized_line_needs_normalization():
    p1 = Point(10, 0)
    p2 = Point(0, 0)
    line = Line(p1, p2)
    normalized = line.get_normalized_line()
    assert normalized.p1.coords == (0, 0)
    assert normalized.p2.coords == (10, 0)
    assert normalized.orientation == LineOrientation.HORZ
    # Ensure original line is unchanged
    assert line.p1.coords == (10, 0)
    assert line.p2.coords == (0, 0)
