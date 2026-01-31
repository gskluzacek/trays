from __future__ import annotations

from itertools import count

from enum import Enum
from typing import Tuple, List, Optional, Dict, Any, Protocol

from cyclic_n_tuples import fwd_pair

class Renderers(Protocol):
    def get_render(self, renderer_type: str):
        """bob was here"""


class Debug:
    @classmethod
    def render_path(cls, path_obj: Path, path_origin: Point):
        print("\t\tpath element beginning xml...")
        for i, point in enumerate(path_obj.points):
            abs_point = point + path_origin
            print(f"\t\t\t{i}: {abs_point}")
        print("\t\tpath element ending xml...")

    @classmethod
    def render_group(cls, group_obj: Group):
        print("\tgroup element beginning xml...")
        for path in group_obj.paths:
            cls.render_path(path, group_obj.origin)
        print("\tgroup element ending xml...")

    @classmethod
    def render_view(cls, view_obj: View):
        print("svg file beginning xml...")
        for group in view_obj.groups:
            cls.render_group(group)
        print("svg file ending xml...")


class Svg:
    seq = count(1)
    xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
    doc_str = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
    svg_boiler_plate = (
        'style="fill-rule:evenodd;clip-rule:evenodd" '
        'version="1.1" '
        'xml:space="preserve" '
        'xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:serif="http://www.serif.com/"'
    )


    @classmethod
    def get_path_cmd(cls, prev: Point, curr: Point):
        if curr.y == prev.y:
            return f"H {curr.x}"
        elif curr.x == prev.x:
            return f"V {curr.y}"
        else:
            raise ValueError(
                f"only path commands where either current x equal previous x or current y equal previous y "
                f"are supported. Current: {curr}; Previous: {prev}"
            )

    @classmethod
    def render_path(cls, path_obj: Path, path_origin: Point):
        first_pt = path_obj.points[0] + path_origin
        cmds = [f"M {first_pt.x} {first_pt.y}"]
        for i, (prev_pt, curr_pt) in enumerate(fwd_pair(path_obj.points), 1):
            prev_abs_pt = prev_pt + path_origin
            curr_abs_pt = curr_pt + path_origin
            cmds.append(cls.get_path_cmd(prev_abs_pt, curr_abs_pt))
        cmds.append("Z")
        data = " ".join(cmds)
        path_elm = f'<path d="{data}" style="fill:none;fill-rule:nonzero;stroke-width:2;stroke:rgb(0,0,0)"/>'
        return path_elm

    @classmethod
    def render_group(cls, group_obj: Group):
        group = [f'<g id="p-{next(cls.seq)}">']
        for path in group_obj.paths:
            path_elm = cls.render_path(path, group_obj.origin)
            group.append(f"\t\t{path_elm}")
        group.append("\t</g>")
        group_elm = "\n".join(group)
        return group_elm

    @classmethod
    def render_view(cls, view_obj: View):
        max_y = view_obj.max_y()
        max_x = view_obj.max_x()
        view = [
            f'<svg width="{max_x}mm" height="{max_y}mm" '
            f'viewBox="0 0 {max_x} {max_y}" '
            f'{cls.svg_boiler_plate}>'
        ]
        for group in view_obj.groups:
            group_elm = cls.render_group(group)
            view.append(f"\t{group_elm}")
        view.append("</svg>")
        view_elm = "\n".join(view)
        return f"{cls.xml_str}\n{cls.doc_str}\n{view_elm}\n"


class Heading(Enum):
    NORTH = 90
    SOUTH = 270
    EAST = 0
    WEST = 180


class Direction(Enum):
    LEFT = 90
    RIGHT = -90


class Point:
    def __init__(self, x: float, y: float, attribs: Dict[str, Any] = None):
        self.x = x
        self.y = y
        self.attribs = attribs or {}

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    def __repr__(self):
        return str(self)

    def __add__(self, other: Point):
        total = Point(
            self.x + other.x,
            self.y + other.y,
            self.attribs
        )
        return total


class Path:
    def __init__(self, points: List[Point]):
        self.points = points

    def min_x(self):
        return min(pt.x for pt in self.points)

    def min_y(self):
        return min(pt.y for pt in self.points)

    def max_x(self):
        return max(pt.x for pt in self.points)

    def max_y(self):
        return max(pt.y for pt in self.points)


class Group:
    def __init__(self):
        self.origin = Point(0, 0)
        self.paths: List[Path] = []

    def add_path(self, path: Path):
        self.paths.append(path)

    def min_x(self):
        return max(path.min_x() for path in self.paths) + self.origin.x

    def min_y(self):
        return max(path.min_y() for path in self.paths) + self.origin.y

    def max_x(self):
        return max(path.max_x() for path in self.paths) + self.origin.x

    def max_y(self):
        return max(path.max_y() for path in self.paths) + self.origin.y

    def set_origin(self, x: float, y: float):
        self.origin = Point(x, y)


class View:
    def __init__(self):
        self.groups: List[Group] = []

    def add_group(self, group: Group):
        self.groups.append(group)

    def render(self, render_class, filename):
        with open(filename, 'w') as svg_fh:
            svg_fh.write(render_class.render_view(self))

    def min_x(self):
        return max(group.min_x() for group in self.groups)

    def min_y(self):
        return max(group.min_y() for group in self.groups)

    def max_x(self):
        return max(group.max_x() for group in self.groups)

    def max_y(self):
        return max(group.max_y() for group in self.groups)


class NamedLocation:
    def __init__(self, x: float, y: float, h: Heading, n: str):
        self.x = x
        self.y = y
        self.h: float = h.value
        self.n = n


class Turtle:
    def __init__(self):
        self.x: Optional[float] = None
        self.y: Optional[float] = None
        self.h: Optional[float] = None
        self.points: List[Point] = []
        self.named_locs: Dict[str, NamedLocation] = {}

    def _add_point(self, attribs: Optional[Dict[str, Any]] = None):
        point = Point(self.x, self.y, attribs)
        self.points.append(point)

    def set(self, x: float = 0, y: float = 0, h: Heading = Heading.EAST, n: str = "HOME"):
        self.x = x
        self.y = y
        self.h = h.value
        self.name(n)
        self._add_point({"svg_cmd": "M"})
        return self

    def name(self, n):
        self.named_locs[n] = NamedLocation(self.x, self.y, Heading(self.h), n)
        return self

    @property
    def get(self) -> (float, float, Heading):
        return self.x, self.y, Heading(self.h)

    @property
    def get_x(self) -> float:
        return  self.x

    @property
    def get_y(self) -> float:
        return self.y

    @property
    def get_xy(self) -> (float, float):
        return self.x, self.y

    @property
    def get_h(self) -> Heading:
        return Heading(self.h)

    def length(self, x: float, y: float):
        raise Exception("not implemented")

    def angel(self, x: float, y: float):
        raise Exception("not implemented")

    def goto(self, n: str):
        self._goto(n)

    def home(self):
        self._goto("HOME")

    def end(self):
        self._goto("HOME", {"svg_cmd": "Z"})

    def _goto(self, n: str, attribs: Optional[Dict[str, Any]] = None, x: float = None, y: float = None):
        named_loc = self.named_locs[n]
        self.x = x or named_loc.x
        self.y = y or named_loc.y
        self.h = named_loc.h
        self._add_point(attribs)

    def move_ny(self, n: str, ux: Optional[float] = 0):
        not ux or self.move(ux)
        self._goto(n, x=self.x)

    def move_nx(self, n: str, uy: Optional[float] = 0):
        not uy or self.move(uy)
        self._goto(n, y=self.y)

    def move(self, u: float):
        if self.h == Heading.NORTH.value:
            self.y -= u
        elif self.h == Heading.SOUTH.value:
            self.y += u
        elif self.h == Heading.EAST.value:
            self.x += u
        elif self.h == Heading.WEST.value:
            self.x -= u
        else:
            raise Exception(f"Turtle's Heading of: {self.h} does not map to one of: NORTH (90), SOUTH (270), EAST (0) or WEST (180)")
        self._add_point()
        return self

    def turn(self, d: Direction, u: float = 0):
        self.h = (self.h + d.value) % 360
        not u or self.move(u)
        return self


def calc_widths(widths: List[float], mt: float) -> List[float]:
    return [width - mt for width in widths]
