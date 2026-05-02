from __future__ import annotations

from collections.abc import Iterator
from typing import TypeVar, SupportsFloat
from itertools import combinations, product

from cyclic_n_tuples import cyclic_n_tuples, fwd_pair
from tray.geometry.final_base.final_path_line import FinalPathLine

from tray.geometry.types.tray import WallType, JointType, IntrxnType
from tray.geometry.types.geometric import LineOrientation
from tray.geometry.basic.point import Point
from tray.geometry.basic.line import Line
from tray.geometry.basic.path import Path
from tray.geometry.segment.segment_point import SegmentPoint
from tray.geometry.wall_line import WallLine
from tray.geometry.base.base_path import BasePath
from tray.geometry.final_base.final_base_path import FinalBasePath

T = TypeVar("T", bound=SupportsFloat)


class Tray:
    def __init__(self, material_thickness: float, inside_dim_cols: list[float], inside_dim_rows: list[float]):
        self.index_paths: list[BasePath] = []
        self.final_index_paths: list[FinalBasePath] = []
        self.index_walls: list[WallLine] = []

        self.material_thickness: float = material_thickness

        self.inside_dim_cols: list[float] = inside_dim_cols
        self.inside_dim_rows: list[float] = inside_dim_rows

        self.center_to_center_dim_cols: list[float] = []
        self.center_to_center_dim_rows: list[float] = []

        self.center_to_center_points: list[list[Point[float]]] = []

        self.center_to_center_paths: list[Path[float]] = []
        self.center_to_center_walls: list[Line[float]] = []

    @property
    def ndx_walls_as_tuples(self) -> Iterator[tuple[T, T, T, T]]:
        return map(lambda wall: (wall.p1.x, wall.p1.y, wall.p2.x, wall.p2.y), self.index_walls)

    def _classify_index_wall(self, wall: WallLine) -> WallType:
        wall_types = []
        # wall_segments = []
        wall_type = WallType.NONE

        for path in self.index_paths:
            path_orientation = path.horizontal if wall.orientation == LineOrientation.HORZ else path.vertical

            for line in path_orientation:
                wall_type = wall.classify_wall(line)
                wall_types.append(wall_type)
                # print(f"{wall} to {line} <-- {wall_type.name}")

                if wall_type == WallType.COMBO or wall_type == WallType.EXTERIOR:
                    for point in wall.wall_inside_path(line):
                        line.add_break(point)

                # if wall_type == WallType.COMBO:
                #     ...
                # wall_segment = wall.path_inside_wall(line)
                # wall_segments.append(wall_segment)

        if wall_type == WallType.NONE:
            raise ValueError("no wall type found for this wall")
        elif WallType.COMBO in wall_types and WallType.EXTERIOR in wall_types:
            raise ValueError("wall type cannot be both combo and exterior")
        elif sum(v == WallType.EXTERIOR for v in wall_types) > 1:
            raise ValueError("more than one exterior wall type found for this wall")
        else:
            wall_type = max(wall_types)

        return wall_type

    def _classify_index_walls(self, orientation: LineOrientation):
        for wall in Line.of_orientation(self.index_walls, orientation):
            wall_type = self._classify_index_wall(wall)
            wall.wall_type = wall_type

    def classify_index_walls(self):
        # assigns wall_type to each wall: EXTERIOR, INTERIOR, or COMBO
        # additionally, it determines the breaks in path lines (and adds them to the path line) when wall_type is COMBO or EXTERIOR
        self._classify_index_walls(LineOrientation.HORZ)
        self._classify_index_walls(LineOrientation.VERT)

    def calc_center_to_center_dims(self):
        self.center_to_center_dim_cols = list(
            map(lambda inside_dim: inside_dim + self.material_thickness, self.inside_dim_cols)
        )
        self.center_to_center_dim_rows = list(
            map(lambda inside_dim: inside_dim + self.material_thickness, self.inside_dim_rows)
        )

    def calc_center_to_center_points(self):
        material_adjustment = self.material_thickness / 2.0

        center_point_x_coords = [material_adjustment]
        for i, inside_dim in enumerate(self.center_to_center_dim_cols):
            center_point_x_coords.append(center_point_x_coords[i] + inside_dim)

        center_point_y_coords = [material_adjustment]
        for i, inside_dim in enumerate(self.center_to_center_dim_rows):
            center_point_y_coords.append(center_point_y_coords[i] + inside_dim)

        for center_point_y in center_point_y_coords:
            row_of_center_to_center_points: list[Point[float]] = []
            for center_point_x in center_point_x_coords:
                row_of_center_to_center_points.append(Point[float](center_point_x, center_point_y))
            self.center_to_center_points.append(row_of_center_to_center_points)

    def calc_center_to_center_paths(self):
        for index_path in self.index_paths:
            center_to_center_path = Path[float]()
            for ndx_px, ndx_py in index_path.points_as_tuples:
                center_to_center_path.add_point(self.center_to_center_points[ndx_py][ndx_px])
            self.center_to_center_paths.append(center_to_center_path)

    def calc_center_to_center_walls(self):
        for p1x, p1y, p2x, p2y in self.ndx_walls_as_tuples:
            p1 = self.center_to_center_points[p1y][p1x]
            p2 = self.center_to_center_points[p2y][p2x]
            self.center_to_center_walls.append(Line[float](p1, p2))

    def _is_index_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x <= len(self.inside_dim_cols) and 0 <= y <= len(self.inside_dim_rows)

    def start_base(self, x_index: int, y_index: int) -> None:
        if not self._is_index_within_bounds(x_index, y_index):
            raise ValueError(
                "the index starting point must be within the bounds of the columns and rows min/max index values"
            )

        index_pt = Point[int](x_index, y_index)
        index_path = BasePath(index_pt)
        self.index_paths.append(index_path)

    def extend_base(self, x_index: int, y_index: int) -> None:
        if not self._is_index_within_bounds(x_index, y_index):
            raise ValueError(
                "the index point being added must be within the bounds of the columns and rows min/max index values"
            )

        index_path = self.index_paths[-1]
        prev_index_pt = index_path.points[-1]
        prev_index_pt_x, prev_index_pt_y = prev_index_pt.coords

        if x_index == prev_index_pt_x and y_index == prev_index_pt_y:
            raise ValueError("cannot add the same point twice to the base path")

        index_pt = Point[int](x_index, y_index)

        if not index_pt.is_orthogonal(prev_index_pt):
            raise ValueError(
                "the point being added must have either the same x or y coordinate (but not both) as the previous point"
            )

        index_path.add_point(index_pt)

    def end_base(self) -> None:
        if len(self.index_paths[-1].points) < 4:
            raise ValueError("the number of points in the base path must be at least 4")

        if len(self.index_paths[-1].points) % 2 == 1:
            raise ValueError("the number of points in the base path must be even")

        x_coords = [point.x for point in self.index_paths[-1].points]
        y_coords = [point.y for point in self.index_paths[-1].points]
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        if min_x != 0 or max_x != len(self.inside_dim_cols) or min_y != 0 or max_y != len(self.inside_dim_rows):
            raise ValueError(
                "the base path must have points on the boundaries of: x=0, y=0, x=max_x_index and y=max_y_index"
            )

        self.index_paths[-1].set_orientation()
        self.index_paths[-1].finalize()

        for prev_line, curr_line in cyclic_n_tuples(self.index_paths[-1].lines, n=2, offset=0):
            if curr_line.orientation == prev_line.orientation:
                raise ValueError("consecutive lines in the base path cannot have the same orientation")

        self._validate_for_overlapping_lines(self.index_paths[-1].lines)

    @staticmethod
    def _validate_for_overlapping_lines(lines: list[Line[T]]) -> None:
        line_pairs = combinations(lines, 2)
        for line1, line2 in line_pairs:
            if line1.is_overlapping(line2):
                raise ValueError(f"lines cannot overlap - Line 1: {line1}, Line 2: {line2} ")

    def add_wall(self, start_indexes: tuple[int, int], end_indexes: tuple[int, int]) -> None:
        if not self._is_index_within_bounds(*start_indexes) or not self._is_index_within_bounds(*end_indexes):
            raise ValueError(
                "the line's starting and ending index points must be within the bounds of the columns and rows min/max index values"
            )
        index_pt_1 = Point[int](*start_indexes)
        index_pt_2 = Point[int](*end_indexes)
        index_wall = WallLine(index_pt_1, index_pt_2)
        self.index_walls.append(index_wall)

    def finalize_walls(self):
        # make sure that the walls specified do not overlap with one another
        self._validate_for_overlapping_lines(self.index_walls)

    def auto_generate_exterior_base_walls(self):
        for index_path in self.index_paths:
            for p1, p2 in cyclic_n_tuples(index_path.points, 2, 0):
                self.add_wall(p1.coords, p2.coords)

    def split_path_lines(self):
        # using the line_breaks, as determined by _classify_index_wall(), generate the final path points/lines
        for index_path in self.index_paths:
            new_path = FinalBasePath()
            for line in index_path.lines:
                new_path.add_point(line.p1)
                for path_break in sorted(line.line_breaks, reverse=line.p1 > line.p2):
                    new_path.add_point(path_break)
            new_path.set_orientation()
            new_path.finalize()
            self.final_index_paths.append(new_path)

    @staticmethod
    def _does_wall_line_start_first(line1: WallLine, line2: FinalPathLine) -> bool:
        """
        Determines if the wall line starts/ends before/after the final path line based on their
        normalized positions and alignment.

        NOTE: if the wall's direction is bottom/right to top/left then what we normally think of as the start
        of the wall-line & path-line is P2 after normalization. Additionally, `before` also becomes `after` in
        this case, essentially flipping the logic. but we are still checking if the wall-line starts first.

        IMPORTANT: The Wall Line and Path Line need to be collinear and (partially) overlapping to
        have a chance of returning True.

        :param line1: The wall line to compare.
        :type line1: WallLine
        :param line2: The final path line to compare.
        :type line2: FinalPathLine
        :return: 1) True if the wall's direction is top/left to bottom/right and the wall line starts before
            the final path line or 2) True if the wall's direction is bottom/right to top/left and the wall line
            ends after the final path line.
        :rtype: bool
        """
        line1_p1, line1_p2 = line1.normalize
        line2_p1, line2_p2 = line2.normalize
        if line1.is_horizontal:
            return (line1_p1.x < line2_p1.x) if line1.p1 < line1.p2 else (line1_p2.x > line2_p2.x)
        return (line1_p1.y < line2_p1.y) if line1.p1 < line1.p2 else (line1_p2.y > line2_p2.y)

    def _generate_wall_segments(self, wall: WallLine):
        segment_points: list[SegmentPoint] = []
        for path in self.final_index_paths:
            path_lines = path.horizontal if wall.is_horizontal else path.vertical

            for path_line in path_lines:
                # note is_overlapping already checks if the lines are collinear, so no need to check here
                if path_line.is_overlapping(wall):
                    # we check both P1 and P2 of path_line to see if they are between wall's points
                    # points_from_line - calls normalize on the points (probably not necessary as we sort the segment points)
                    segment_points.extend([pt for pt in path_line.points_from_line if pt.is_between(wall)])

        # we reverse the order of the sort if the wall line is bottom/right to top/left versus top/left to bottom/right
        segment_points.sort(reverse=False if wall.p1 < wall.p2 else True)
        points = [wall.p1] + [pt.to_point for pt in segment_points] + [wall.p2]
        wall.segment_path.points = points

        if wall.wall_type == WallType.INTERIOR:
            first_joint_type = 0
        else:
            # TODO: are there any other conditions that we need to check to determine if an empty
            #  segment_points list with a COMBO/EXTERIOR wall-line should have a 1st joint type of 1 or 0?
            first_joint_type = 1
        if segment_points:
            path_line_1 = segment_points[0].line
            first_joint_type = 0 if self._does_wall_line_start_first(wall, path_line_1) else 1

        joints = [JointType.TS, JointType.FS]
        for i, (p1, p2) in enumerate(fwd_pair(points), first_joint_type):
            joint_type = joints[i % 2]
            wall.segment_path.add_segment(p1, p2, joint_type)

    def _generate_walls_segments(self, orientation: LineOrientation):
        for wall in Line.of_orientation(self.index_walls, orientation):
            self._generate_wall_segments(wall)

    def generate_walls_segments(self):
        self._generate_walls_segments(LineOrientation.HORZ)
        self._generate_walls_segments(LineOrientation.VERT)

    def generate_intersections(self):
        walls_horz = Line.of_orientation(self.index_walls, LineOrientation.HORZ)
        walls_vert = Line.of_orientation(self.index_walls, LineOrientation.VERT)

        # only walls need to know about corner and tee intersections
        # walls (top) and segments need to know about cross intersections
        # in other words walls need to know about all intersection types, but segements only
        # need to know about cross intersections

        # when a cross intersection is found between two walls, we have to find the corresponding segments
        # the intersection can be in the middle of one segment or on the end points of two segments (P1 on
        #   one and P2 on the other)

        for wall_horz, wall_vert in product(walls_horz, walls_vert):
            # print(f"checking intersection between: ({wall_horz.p1, wall_horz.p2}) and ({wall_vert.p1, wall_vert.p2})")
            intrxn = wall_horz.intersect(wall_vert)
            if intrxn:
                # print(f"    {intrxn}")
                wall_horz.intersections.append(intrxn)
                wall_vert.intersections.append(intrxn)
                if intrxn.intrxn_type == IntrxnType.CROSS:
                    wall_horz.determine_segments_with_intrxn(intrxn)
                    wall_vert.determine_segments_with_intrxn(intrxn)
