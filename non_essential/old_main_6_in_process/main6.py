from __future__ import annotations

from enum import Enum
# from itertools import count
# from operator import attrgetter
from typing import List, Tuple, Dict, Optional

from basic import Point as BPoint, Line as BLine, Orientation as Ori, Direction as Dir
from cyclic_n_tuples import cyclic_n_tuples, fwd_n_tuple


class LineType(Enum):
    FINGER = "finger_joint"
    TAB_SLOT = "tab_slot_joint"
    SMOOTH = "no_joint"


class IndexPoint:
    """
    the IndexPoint class is a column (x) and row (y) position into the 2 dimensional AggregatePoint array
    where the columns and rows have simple widths & heights. The use of IndexPoint allows us to describe
    a polygon's path using simple column and row integer indices instead of actual decimal x, y coordinates.
    """

    def __init__(self, x_index: int, y_index: int, line_type: Optional[LineType] = None):
        self.line_type = line_type
        self.x_index = x_index
        self.y_index = y_index

    @property
    def gxy(self) -> Tuple[int, int]:
        return self.x_index, self.y_index

    @property
    def pt(self) -> BPoint:
        return BPoint(self.x_index, self.y_index)

    def __str__(self) -> str:
        return f"[{self.x_index}, {self.y_index}]"

    def __repr__(self) -> str:
        return str(self)

    # TODO: add the following methods:
    #   next_point()
    #   prev_point()
    #   get_next_start()
    #   get_prev_end()


class IndexLine:
    def __init__(self, start_pt: IndexPoint, end_pt: IndexPoint, line_type: LineType):
        self.start_pt = start_pt
        self.end_pt = end_pt
        self.line_type = line_type

    def __str__(self):
        return f"{self.start_pt} {self.end_pt}"


class IndexPath:
    def __init__(self, start_point: IndexPoint = None, orientation: Ori = None):
        self.orientation = orientation
        self.index_points: List[IndexPoint] = [start_point] if start_point else []

    def add_point(self, point: IndexPoint) -> None:
        self.index_points.append(point)
        # TODO: modify method to support
        #   prev and next attributes

    def set_orientation(self):
        # notes:
        #   - it takes at a minimum 3 points to form a polygon
        #   - (at least) 3 of the points must not be collinear
        #       that is 3 collinear points would form a line not a polygon
        #   - that being said, we will try 3 points, incrementally until we get an orientation of non-collinear
        #   - but if all the points in the path do form a straight line (and not a polygon) we could, in theory
        #       go past the end of the list (out of bounds exception) unless we code for that condition
        #   - and if the path does not contain at least 3 points, the for loop will NOT execute at all

        if len(self.index_points) < 3:
            raise ValueError(
                f"could not determine the path's orientation (clock wise or counter clock wise). "
                f"please check that you have 3 or more points in your path. Path len: {len(self.index_points)}"
            )

        path_ori: Optional[Ori] = None
        for i_pt_1, i_pt_2, i_pt_3 in fwd_n_tuple(self.index_points):
            path_ori = i_pt_1.pt.orientation(i_pt_2.pt, i_pt_3.pt)
            if path_ori != Ori.COL:
                break

        if path_ori == Ori.COL:
            raise ValueError(
                "could not determine the path's orientation (clock wise or counter clock wise). "
                "please check that all points in the path are not collinear"
            )

        if path_ori is None:
            raise ValueError("exhausted path without determining the orientation")

        self.orientation = path_ori

    # TODO: add the following methods:
    #   set_wrap()

class Base:
    def __init__(self, **kwargs):
        self.index_paths: List[IndexPath] = []
        self.norm_index_paths: List[IndexPath] = []
        self.index_walls: List[IndexLine] = []

    def start_path(self, x_index: int, y_index: int, line_type: LineType = LineType.FINGER):
        point: IndexPoint = IndexPoint(x_index, y_index, line_type)
        path: IndexPath = IndexPath(point)
        self.index_paths.append(path)

    def extend_path(self, x_index, y_index, line_type: LineType = LineType.FINGER):
        path: IndexPath = self.index_paths[-1]
        point: IndexPoint = IndexPoint(x_index, y_index, line_type)
        path.add_point(point)

    def end_path(self):
        self.index_paths[-1].set_orientation()
        # TODO: add logic to normalize the IndexPath here
        self.create_path_lines()

    def create_path_lines(self):
        for norm_index_path in self.norm_index_paths:
            for curr_pt, next_pt in cyclic_n_tuples(norm_index_path.index_points, 2, 0):
                # TODO: we can't hardcode the line_type here, need to determine it from the index point
                self.add_exterior_line(curr_pt, next_pt, LineType.FINGER)

    def add_exterior_line(self, start: IndexPoint, end: IndexPoint, line_type: LineType = LineType.FINGER):
        line = IndexLine(start, end, line_type)
        self.index_walls.append(line)

    def add_interior_line(self, start: Tuple[int, int], end: Tuple[int, int], line_type: LineType = LineType.TAB_SLOT ):
        p1: IndexPoint = IndexPoint(*start)
        p2: IndexPoint = IndexPoint(*end)
        line = IndexLine(p1, p2, line_type)
        self.index_walls.append(line)


def main():
    base = Base(
        mat_thick=5,
        fngr_len=15.0,
        spc_len=25.0,
        min_be_len=6.0,
        col_widths=[47.5, 75, 72.5],
        row_heights=[72.5, 122.5],
        min_tbslt_len=30,
        max_tbslt_bt_xs=2,
        wall_tbslt_dist=5,
        depth=75,
        on_center=True
    )
    base.start_path(0, 0)
    base.extend_path(3, 0)
    base.extend_path(3, 2)
    base.extend_path(0, 2)
    base.end_path()

    base.add_interior_line((1, 0), (1, 2))
    base.add_interior_line((0, 1), (3, 1))
    base.add_interior_line((2, 1), (2, 2))

if __name__ == "__main__":
    main()
