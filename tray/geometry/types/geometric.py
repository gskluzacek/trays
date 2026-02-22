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
