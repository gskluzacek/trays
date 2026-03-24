from __future__ import annotations

from enum import Enum


class LineOrientation(Enum):
    VERT = "vertical"
    HORZ = "horizontal"
    NONE = "none"


class PathOrientation(Enum):
    CW = "clockwise"
    CCW = "counter_clockwise"
    COL = "collinear"
    NONE = "none"


class PointLine(Enum):
    P1 = "p1"
    P2 = "p2"
    BETWEEN = "between"
    OUTSIDE = "outside"
    NONE = "none"
