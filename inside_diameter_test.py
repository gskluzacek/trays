from __future__ import annotations

from enum import Enum
from collections.abc import Iterator, Sequence
from typing import Generic, SupportsFloat, TypeVar
from typing import overload

from cyclic_n_tuples import fwd_n_tuple, cyclic_n_tuples

T = TypeVar("T", bound=SupportsFloat)


class PathOrientation(Enum):
    CW = "clockwise"
    CCW = "counter_clockwise"
    COL = "collinear"
    NONE = "none"


class LineOrientation(Enum):
    VERT = "vertical"
    HORZ = "horizontal"
    NONE = "none"

class Point(Generic[T]):
    def __init__(self, x: T, y: T) -> None:
        self.x = x
        self.y = y
        # these private attributes are used at the line level and are accessed via the line's property not the point's property
        self._line_orientation = LineOrientation.NONE

    @property
    def line_orientation(self) -> LineOrientation:
        return self._line_orientation

    @line_orientation.setter
    def line_orientation(self, value: LineOrientation) -> None:
        self._line_orientation = value

    def set_line_orientation(self, other_point: Point) -> None:
        if other_point.x == self.x:
            self.line_orientation = LineOrientation.VERT
        elif other_point.y == self.y:
            self.line_orientation = LineOrientation.HORZ
        else:
            raise ValueError("cannot set line orientation for points that are not collinear")

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    @property
    def coords(self) -> tuple[T, T]:
        return self.x, self.y

    def orientation(self, p2: Point[T], p3: Point[T]) -> PathOrientation:
        p1 = self
        x1, y1 = float(p1.x), float(p1.y)
        x2, y2 = float(p2.x), float(p2.y)
        x3, y3 = float(p3.x), float(p3.y)

        val = ((y2 - y1) * (x3 - x2)) - ((x2 - x1) * (y3 - y2))

        # note we are operating in quadrant 4, so we are swapping the values that correspond to cw & ccw
        if val > 0:
            return PathOrientation.CCW
        elif val < 0:
            return PathOrientation.CW
        else:
            return PathOrientation.COL


class Line(Generic[T]):
    def __init__(self, p1: Point[T], p2: Point[T]) -> None:
        self.p1 = p1
        self.p2 = p2
        if self.orientation == LineOrientation.NONE:
            self.p2.set_line_orientation(self.p1)

    @property
    def orientation(self) -> LineOrientation:
        return self.p2.line_orientation

    def __repr__(self) -> str:
        return f"Line(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r})"

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}, {self.orientation}]"


class _LinesView(Sequence[Line]):
    """Dynamic, list-like view over a Path's points that yields Line objects."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def __len__(self) -> int:
        return len(self._path.points)

    @overload
    def __getitem__(self, index: int) -> Line: ...
    @overload
    def __getitem__(self, index: slice) -> list[Line]: ...

    def __getitem__(self, index: int | slice) -> Line | list[Line]:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return [self[i] for i in range(start, stop, step)]

        n = len(self)
        if n == 0:
            raise IndexError("path.lines is empty (no points)")

        i = index % n

        pts = self._path.points
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        # TODO: creating a new Line object, will initialize point p2's line orientation if it is LineOrientation.NONE
        return Line(p1, p2)

    def __iter__(self) -> Iterator[Line]:
        # TODO: iteration will call __getitem__ which will create a new Line object, which will initialize point p2's line orientation if it is LineOrientation.NONE
        for i in range(len(self)):
            yield self[i]


class Path(Generic[T]):
    def __init__(self, start_point: Point[T] | None = None, orientation: PathOrientation = PathOrientation.NONE) -> None:
        self.points: list[Point[T]] = [start_point] if start_point else []
        self.orientation: PathOrientation = orientation

    @property
    def lines(self) -> Sequence[Line]:
        return _LinesView(self)

    def finalize(self) -> None:
        # todo: implement any finalization logic if needed - must have all details within the path to do so
        for line in self.lines:
            pass


    @property
    def points_as_tuples(self) -> Iterator[tuple[T, T]]:
        return map(lambda pt: (pt.x, pt.y), self.points)

    def add_point(self, point: Point[T]) -> None:
        self.points.append(point)

    def set_orientation(self) -> None:
        # Notes:
        #   - it takes at a minimum 3 points to form a polygon
        #   - (at least) 3 of the points must not be collinear
        #       that is 3 collinear points would form a line not a polygon
        #   - that being said, we will try 3 points, incrementally until we get an orientation of non-collinear
        #   - but if all the points in the path do form a straight line (and not a polygon), we could, in theory,
        #       go past the end of the list (out of bounds exception) unless we code for that condition
        #   - and if the path does not contain at least 3 points, the for loop will NOT execute at all

        if len(self.points) < 3:
            raise ValueError(
                f"could not determine the path's orientation (clockwise or counter clockwise). "
                f"please check that you have 3 or more points in your path. Path len: {len(self.points)}"
            )

        orientation = PathOrientation.NONE
        for pt_1, pt_2, pt_3 in fwd_n_tuple(self.points):
            orientation = pt_1.orientation(pt_2, pt_3)
            if orientation != PathOrientation.COL:
                break

        if orientation == PathOrientation.COL:
            raise ValueError(
                "could not determine the path's orientation (clockwise or counter clockwise). "
                "please check that all points in the path are not collinear"
            )

        if orientation == PathOrientation.NONE:
            raise ValueError("exhausted path without determining the orientation")

        self.orientation = orientation


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

    def calc_center_to_center_dims(self):
        self.center_to_center_dim_cols = list(map(
            lambda inside_dim: inside_dim + self.material_thickness,
            self.inside_dim_cols
        ))
        self.center_to_center_dim_rows = list(map(
            lambda inside_dim: inside_dim + self.material_thickness,
            self.inside_dim_rows
        ))

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

    def start_base(self, x_index: int, y_index: int) -> None:
        index_pt = Point[int](x_index, y_index)
        index_path = Path[int](index_pt)
        self.index_paths.append(index_path)

    def extend_base(self, x_index: int, y_index: int) -> None:
        index_path = self.index_paths[-1]
        index_pt = Point[int](x_index, y_index)
        index_path.add_point(index_pt)

    def end_base(self) -> None:
        self.index_paths[-1].set_orientation()
        self.index_paths[-1].finalize()

    def add_wall(self, start_indexes: tuple[int, int], end_indexes: tuple[int, int]) -> None:
        index_pt_1 = Point[int](*start_indexes)
        index_pt_2 = Point[int](*end_indexes)
        index_wall = Line[int](index_pt_1, index_pt_2)
        self.index_walls.append(index_wall)

    def auto_generate_exterior_base_walls(self):
        for index_path in self.index_paths:
            for p1, p2 in cyclic_n_tuples(index_path.points, 2, 0):
                self.add_wall(p1.coords, p2.coords)

def main():
    auto_generate_exterior_base_walls = True
    material_thickness: float = 5
    inside_dim_cols: list[float] = [42.5, 70, 67.5]
    inside_dim_rows: list[float] = [67.5, 117.5]

    tray = Tray(material_thickness, inside_dim_cols, inside_dim_rows)

    # define the polygon for the tray's base
    tray.start_base(0, 0)
    tray.extend_base(3, 0)
    tray.extend_base(3, 2)
    tray.extend_base(0, 2)
    tray.end_base()

    # add lines to represent the walls of the tray (these are the exterior walls)
    if auto_generate_exterior_base_walls:
        tray.auto_generate_exterior_base_walls()
    else:
        tray.add_wall((0, 0), (3, 0))
        tray.add_wall((3, 0), (3, 2))
        tray.add_wall((3, 2), (0, 2))
        tray.add_wall((0, 2), (0, 0))

    # add lines to represent the walls of the tray (these are the interior walls)
    tray.add_wall((1, 0), (1, 2))
    tray.add_wall((0, 1), (3, 1))
    tray.add_wall((2, 1), (2, 2))

    tray.calc_center_to_center_dims()
    tray.calc_center_to_center_points()
    tray.calc_center_to_center_paths()
    tray.calc_center_to_center_walls()

    ...


if __name__ == "__main__":
    main()
