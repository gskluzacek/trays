import pytest
from tray.geometry.point import Point, LineOrientation
from tray.geometry.line import Line


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


def test_line_init_none_already_set():
    # TODO: this test kind of exposes a flaw in the implementation, a line that is not horizontal or vertical can
    #  be created and the edit bypassed by manually setting the p2's line_orientation to something not equal to NONE
    p1 = Point(0, 0)
    p2 = Point(10, 10)  # Diagonal! - Not horizontal or vertical
    p2.line_orientation = LineOrientation.HORZ

    # If set_line_orientation was triggered, it would raise ValueError
    # because (0,0) and (10,10) are not collinear.
    # By providing non-collinear points but setting orientation != NONE,
    # we prove it's not triggered.
    line = Line(p1, p2)

    assert line.orientation == LineOrientation.HORZ


def test_line_init_none_already_set_incorrect():
    p1 = Point(0, 0)
    p2 = Point(10, 0)  # p1 & p2 form a horizontal line
    p2.line_orientation = LineOrientation.VERT

    # we, on purpose, manually set the line orientation to the incorrect value of vertical for a horizontal line
    # if set_line_orientation is triggered when creating the line (and it should not be since line_orientation
    # does not equal NONE), it will update the orientation to horizontal.
    line = Line(p1, p2)

    # validate that the orientation is still (incorrectly set to) vertical
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
