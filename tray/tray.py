from __future__ import annotations

from collections.abc import Iterator
from typing import TypeVar, SupportsFloat
from itertools import combinations


from tray.geometry.point import Point
from tray.geometry.line import Line, LineOrientation, WallType
from tray.geometry.path import Path
from cyclic_n_tuples import cyclic_n_tuples

T = TypeVar("T", bound=SupportsFloat)


class Tray:
    def __init__(self, material_thickness: float, inside_dim_cols: list[float], inside_dim_rows: list[float]):
        self.index_paths: list[Path[int]] = []
        self.index_walls: list[Line[int]] = []

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

    def _classify_index_walls(self, orientation: LineOrientation):
        for wall in Line.of_orientation(self.index_walls, orientation):
            wall_types = []
            wall_type = WallType.NONE

            for path in self.index_paths:
                path_orientation = path.horizontal if orientation == LineOrientation.HORZ else path.vertical

                for line in path_orientation:
                    wall_type = Line.classify_wall(wall, line, orientation)
                    wall_types.append(wall_type)

            if wall_type == WallType.NONE:
                raise ValueError("no wall type found for this wall")
            elif WallType.COMBO in wall_types and WallType.EXTERIOR in wall_types:
                raise ValueError("wall type cannot be both combo and exterior")
            elif sum(v == WallType.EXTERIOR for v in wall_types) > 1:
                raise ValueError("more than one exterior wall type found for this wall")
            else:
                wall_type = max(wall_types)

            print(f"{wall} | wall_type: {wall_type.label}")

    def classify_index_walls(self):
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
            center_to_center_path = Path[float](orientation=index_path.orientation)
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
        index_path = Path[int](index_pt)
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

        if self._is_overlapping_lines(self.index_paths[-1].lines):
            raise ValueError("lines within the base path cannot overlap")

    @staticmethod
    def _is_overlapping_lines(lines: list[Line[T]]) -> bool:
        line_pairs = combinations(lines, 2)
        for line1, line2 in line_pairs:
            if line1.is_overlapping(line2):
                return True
        return False

    def add_wall(self, start_indexes: tuple[int, int], end_indexes: tuple[int, int]) -> None:
        if not self._is_index_within_bounds(*start_indexes) or not self._is_index_within_bounds(*end_indexes):
            raise ValueError(
                "the line's starting and ending index points must be within the bounds of the columns and rows min/max index values"
            )
        index_pt_1 = Point[int](*start_indexes)
        index_pt_2 = Point[int](*end_indexes)
        index_wall = Line[int](index_pt_1, index_pt_2)
        self.index_walls.append(index_wall)

    def finalize_walls(self):
        if self._is_overlapping_lines(self.index_walls):
            raise ValueError("Cannot have overlapping walls")

    def auto_generate_exterior_base_walls(self):
        for index_path in self.index_paths:
            for p1, p2 in cyclic_n_tuples(index_path.points, 2, 0):
                self.add_wall(p1.coords, p2.coords)
