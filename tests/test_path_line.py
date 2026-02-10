import pytest
from tray.geometry.path_line import PathLine
from tray.geometry.point import Point
from tray.geometry.line import LineOrientation

def test_path_line_init():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    pl = PathLine(p1, p2)
    assert pl.p1 == p1
    assert pl.p2 == p2
    assert pl.path_breaks == []
    assert pl.orientation == LineOrientation.HORZ

def test_path_line_repr():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    pl = PathLine(p1, p2)
    expected_repr = f"PathLine(p1={p1!r}, p2={p2!r}, type={LineOrientation.HORZ!r}, breaks=[])"
    assert repr(pl) == expected_repr

def test_path_line_str():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    pl = PathLine(p1, p2)
    expected_str = f"{p1}, {p2}, {LineOrientation.HORZ}, []"
    assert str(pl) == expected_str

def test_path_line_add_break():
    p1 = Point(0, 0)
    p2 = Point(10, 0)
    pl = PathLine(p1, p2)
    pl.add_break(5)
    assert pl.path_breaks == [5]
    pl.add_break(7.5)
    assert pl.path_breaks == [5, 7.5]

def test_path_line_inheritance():
    p1 = Point(0, 0)
    p2 = Point(0, 10)
    pl = PathLine(p1, p2)
    assert pl.is_vertical is True
    assert pl.is_horizontal is False
    assert pl.normalize == (p1, p2)
