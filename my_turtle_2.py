"""
Here’s a detailed, class-by-class explanation for my_turtle_2.py, including
* what each method does,
* how to use it,
* and the overall purpose of the classes/methods.

Overall Purpose
• The code defines a small “turtle” drawing system that builds geometric paths (as sequences of points), groups them,
and renders them into SVG. The Turtle class is the core for generating paths by moving/turning, while Path, Group,
and View assemble those points into an SVG document. Rendering is handled by Svg (string output) or
Debug (console output).

Class: Renderers (Protocol) — my_turtle_2.py
• Purpose: Define a renderer interface (get_render) that other renderer classes could implement; currently not used elsewhere.
• Method: get_render(self, renderer_type: str)
◦ What it does: Placeholder signature; docstring indicates it’s a stub.
◦ How to use: Implement in a class that claims to be a renderer; no concrete usage in this file.

Class: Debug — my_turtle_2.py
• Purpose: Print readable debug output for paths, groups, and full views.
• Method: render_path(path_obj: Path, path_origin: Point)
◦ What it does: Prints each point of a Path after applying the group’s origin offset.
◦ How to use: Debug.render_path(path, group.origin); used for console inspection.
• Method: render_group(group_obj: Group)
◦ What it does: Prints group boundaries then calls render_path for each path.
◦ How to use: Debug.render_group(group).
• Method: render_view(view_obj: View)
◦ What it does: Prints view boundaries then calls render_group for each group.
◦ How to use: Debug.render_view(view).

Class: Svg — my_turtle_2.py
• Purpose: Convert View/Group/Path objects into SVG XML strings.
• Class attributes:
◦ seq: counter for unique group ids.
◦ xml_str, doc_str, svg_boiler_plate: SVG headers/attributes.
• Method: get_path_cmd(prev: Point, curr: Point)
◦ What it does: Returns an SVG H or V command depending on whether x or y stayed the same. Raises if diagonal.
◦ How to use: Internal; relies on axis-aligned segments.
• Method: render_path(path_obj: Path, path_origin: Point)
◦ What it does: Builds a <path> element with M, then H/V commands, then Z.
◦ How to use: Svg.render_path(path, group.origin); returns SVG string.
• Method: render_group(group_obj: Group)
◦ What it does: Wraps all paths in a <g> element with a unique id.
◦ How to use: Svg.render_group(group); returns SVG string.
• Method: render_view(view_obj: View)
◦ What it does: Creates <svg> with width/height/viewBox derived from view’s max x/y and includes all groups.
◦ How to use: Svg.render_view(view); returns full SVG XML.

Class: Heading (Enum) — my_turtle_2.py
• Purpose: Cardinal headings in degrees.
• Members: NORTH = 90, SOUTH = 270, EAST = 0, WEST = 180.
• Usage: Turtle stores heading as degrees; you pass Heading values into Turtle.set or compare with Heading.<dir>.value.

Class: Direction (Enum) — my_turtle_2.py
• Purpose: Turn directions in degrees.
• Members: LEFT = 90, RIGHT = -90.
• Usage: Turtle.turn(Direction.LEFT).

Class: Point — my_turtle_2.py
• Purpose: Store an (x, y) coordinate with optional attributes.
• Method: __init__(x, y, attribs=None)
◦ What it does: Initializes coordinates and metadata dictionary.
◦ How to use: Point(10, 5) or Point(10, 5, {"svg_cmd": "M"}).
• Method: __str__ / __repr__
◦ What it does: Formats as [x, y].
◦ How to use: Debugging/printing.
• Method: __add__(other: Point)
◦ What it does: Returns a new point at summed coordinates; carries attribs from self.
◦ How to use: abs_point = point + origin.

Class: Path — my_turtle_2.py
• Purpose: Represent a series of Point objects that form a path.
• Method: __init__(points)
◦ What it does: Stores list of points.
◦ How to use: Path(turtle.points) after drawing.
• Methods: min_x, min_y, max_x, max_y
◦ What they do: Return bounds across points.
◦ How to use: Called by Group and View to compute size.

Class: Group — my_turtle_2.py
• Purpose: Combine multiple paths and apply a shared origin offset.
• Method: __init__()
◦ What it does: Starts with origin at (0,0) and empty paths list.
◦ How to use: g = Group().
• Method: add_path(path)
◦ What it does: Adds a Path to the group.
◦ How to use: g.add_path(path).
• Methods: min_x, min_y, max_x, max_y
◦ What they do: Compute group bounds by combining each path’s bounds and origin.
◦ How to use: Internal to View rendering; can be called directly.
• Method: set_origin(x, y)
◦ What it does: Sets origin offset for all paths in the group.
◦ How to use: g.set_origin(0, 10).

Class: View — my_turtle_2.py
• Purpose: Top-level SVG container for multiple groups.
• Method: __init__()
◦ What it does: Initializes empty group list.
◦ How to use: v = View().
• Method: add_group(group)
◦ What it does: Adds a Group to the view.
◦ How to use: v.add_group(g).
• Method: render(render_class, filename)
◦ What it does: Writes rendered output from render_class.render_view(self) to file.
◦ How to use: v.render(Svg, "test.svg") or v.render(Debug, "...") if it had a render_view.
• Methods: min_x, min_y, max_x, max_y
◦ What they do: Compute bounds across all groups.
◦ How to use: Internal by Svg.render_view.

Class: NamedLocation — my_turtle_2.py
• Purpose: Store a named turtle position + heading for later goto.
• Method: __init__(x, y, h, n)
◦ What it does: Records coordinates, heading (as degrees), and name.
◦ How to use: Created internally by Turtle.name.

Class: Turtle — my_turtle_2.py
• Purpose: State-based turtle that records movement as points for path generation.
• Method: __init__()
◦ What it does: Initializes turtle state and storage for points and named locations.
◦ How to use: t = Turtle().
• Method: _add_point(attribs=None)
◦ What it does: Appends current (x, y) as a Point, optionally with metadata.
◦ How to use: Internal.
• Method: set(x=0, y=0, h=Heading.EAST, n="HOME")
◦ What it does: Sets position/heading, creates a named location, adds initial point with svg_cmd: "M".
◦ How to use: t.set(0, 0, Heading.SOUTH, "START").
• Method: name(n)
◦ What it does: Saves current location and heading under a name.
◦ How to use: t.name("P1") before using move_nx/move_ny.
• Property: get
◦ What it does: Returns (x, y, Heading) tuple.
◦ How to use: x, y, h = t.get.
• Properties: get_x, get_y, get_xy, get_h
◦ What they do: Convenience accessors for current position/heading.
◦ How to use: t.get_xy etc.
• Method: length(x, y) / angel(x, y)
◦ What it does: Both raise Exception("not implemented").
◦ How to use: Not usable; likely placeholders.
• Method: goto(n)
◦ What it does: Moves to a named location (via _goto), adds point.
◦ How to use: t.goto("P1").
• Method: home()
◦ What it does: Goes to named location "HOME".
◦ How to use: t.home() after set.
• Method: end()
◦ What it does: Goes to "HOME" with svg_cmd: "Z" to close the path.
◦ How to use: t.end() at the end of a shape.
• Method: _goto(n, attribs=None, x=None, y=None)
◦ What it does: Core method for going to a named location, with optional override x/y, and records a point.
◦ How to use: Internal or advanced usage.
• Method: move_ny(n, ux=0)
◦ What it does: Optionally moves ux forward, then goes to named location n while keeping current x (y from named location).
◦ How to use: t.move_ny("P1", fl) to align y to P1 while continuing columns.
• Method: move_nx(n, uy=0)
◦ What it does: Optionally moves uy forward, then goes to named location n while keeping current y (x from named location).
◦ How to use: t.move_nx("P1", fl) to align x to P1 while continuing rows.
• Method: move(u)
◦ What it does: Moves u units forward based on heading, adds a point.
◦ How to use: t.move(10).
• Method: turn(d, u=0)
◦ What it does: Updates heading by ±90 degrees, optionally moves u.
◦ How to use: t.turn(Direction.LEFT) or t.turn(Direction.RIGHT, 5).

"""
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


def main():
    mt = 5
    be = 15
    fl = 20
    sl = 30
    w = 100
    ns = 4
    nf = 5

    v = View()
    y = base(be, fl, mt, ns, sl, v)
    y = h_wall(be, fl, mt, ns, sl, v, y)
    v_wall(be, fl, mt, ns, sl, v, y)
    v.render(Svg, "test.svg")


def v_wall(be, fl, mt, ns, sl, v, y):
    g = Group()
    t = Turtle()
    draw_v_wall(be, fl, mt, ns, sl, t)
    p = Path(t.points)
    g.add_path(p)
    g.set_origin(0, y)
    v.add_group(g)


def h_wall(be, fl, mt, ns, sl, v, y):
    g = Group()
    t = Turtle()
    draw_h_wall(be, fl, mt, ns, sl, t)
    p = Path(t.points)
    g.add_path(p)
    g.set_origin(0, y)
    v.add_group(g)
    y = v.max_y() + 10
    return y


def base(be, fl, mt, ns, sl, v):
    g = Group()
    t = Turtle()
    draw_base(be, fl, mt, ns, sl, t)
    p = Path(t.points)
    g.add_path(p)
    g.set_origin(0, 0)
    v.add_group(g)
    y = v.max_y() + 10
    return y


def draw_v_wall(be, fl, mt, ns, sl, t):
    t.set(5, 0, Heading.SOUTH)
    v_wall_vert_side(be, fl, mt, ns, sl, t)
    t.turn(Direction.LEFT)
    v_wall_hort_side(be, fl, mt, ns, sl, t)
    t.turn(Direction.LEFT)
    v_wall_vert_side(be, fl, mt, ns, sl, t)
    t.turn(Direction.LEFT)
    t.end()


def v_wall_hort_side(be, fl, mt, ns, sl, t):
    t.move(be).name("p1")
    t.turn(Direction.LEFT, mt).turn(Direction.RIGHT).name("p2")
    for i in range(ns):
        t.move_ny("p1", fl)
        t.move_ny("p2", sl)
    t.move_ny("p1", fl)
    t.move(be)


def v_wall_vert_side(be, fl, mt, ns, sl, t):
    t.move(mt).move(be).name("p1")
    t.turn(Direction.RIGHT, mt).turn(Direction.LEFT).name("p2")
    for i in range(ns):
        t.move_nx("p1", fl)
        t.move_nx("p2", sl)
    t.move_nx("p1", fl)
    t.move(be).move(mt)


def draw_h_wall(be, fl, mt, ns, sl, t):
    t.set(0, 0, Heading.SOUTH)
    h_wall_vert_side(be, fl, mt, ns, sl, t)
    t.turn(Direction.LEFT)
    h_wall_hort_side(be, fl, mt, ns, sl, t)
    t.turn(Direction.LEFT)
    h_wall_vert_side(be, fl, mt, ns, sl, t)
    t.turn(Direction.LEFT)
    t.end()


def h_wall_hort_side(be, fl, mt, ns, sl, t):
    t.move(mt).move(be).name("p1")
    t.turn(Direction.LEFT, mt).turn(Direction.RIGHT).name("p2")
    for i in range(ns):
        t.move_ny("p1", fl)
        t.move_ny("p2", sl)
    t.move_ny("p1", fl)
    t.move(be).move(mt)


def h_wall_vert_side(be, fl, mt, ns, sl, t):
    t.move(mt).move(be).name("p1")
    t.turn(Direction.LEFT, mt).turn(Direction.RIGHT).name("p2")
    for i in range(ns):
        t.move_nx("p1", fl)
        t.move_nx("p2", sl)
    t.move_nx("p1", fl)
    t.move(be).move(mt)


def draw_base(be, fl, mt, ns, sl, t):
    t.set(mt, mt, Heading.SOUTH)
    base_vert_side(be, fl, mt, ns, sl, t)
    t.turn(Direction.LEFT)
    base_hort_side(be, fl, mt, ns, sl, t)
    t.turn(Direction.LEFT)
    base_vert_side(be, fl, mt, ns, sl, t)
    t.turn(Direction.LEFT)
    base_hort_side(be, fl, mt, ns, sl, t)
    t.end()


def base_hort_side(be, fl, mt, ns, sl, t):
    t.move(be).name("p1")
    t.turn(Direction.RIGHT, mt).turn(Direction.LEFT).name("p2")
    for i in range(ns):
        t.move_ny("p1", fl)
        t.move_ny("p2", sl)
    t.move_ny("p1", fl)
    t.move(be)


def base_vert_side(be, fl, mt, ns, sl, t):
    t.move(be).name("p1")
    t.turn(Direction.RIGHT, mt).turn(Direction.LEFT).name("p2")
    for i in range(ns):
        t.move_nx("p1", fl)
        t.move_nx("p2", sl)
    t.move_nx("p1", fl)
    t.move(be)


def main_1():
    mt = 3
    fl = 6
    sl = 13
    be = 6
    d = 50
    nf = 5
    ns = 4

    t = Turtle()
    t.set(0, 0, h=Heading.SOUTH).move(d)

    draw_bottom(t, mt, be, fl, sl, ns)      # h --> EAST

    fl = 6
    sl = 11
    nf = 3
    ns = 2
    be = 5

    draw_right_side(be, fl, mt, ns, sl, t)

    # t.turn(Direction.LEFT)
    # t.move(d)
    t.end()

    p = Path(t.points)
    g = Group()
    g.add_path(p)
    g.set_origin(0, 0)
    v = View()
    v.add_group(g)
    v.render(Svg, "test.svg")


def draw_right_side(be, fl, mt, ns, sl, t):
    t.turn(Direction.LEFT).move(be)  # h --> NORTH
    t.name("R-FINGER")

    t.turn(Direction.LEFT).move(mt)  # h --> WEST
    t.turn(Direction.RIGHT)  # h --> NORTH
    t.name("R-SPACE")

    for i in range(ns):
        t.move_nx("R-FINGER", fl)
        t.move_nx("R-SPACE", sl)

    t.move_nx("R-FINGER", fl)
    t.move(be)


def draw_bottom(t, mt, be, fl, sl, ns):
    t.turn(Direction.LEFT).move(mt).move(be)  # h --> EAST
    t.name('SPACE')

    t.turn(Direction.RIGHT).move(mt)  # h --> SOUTH
    t.turn(Direction.LEFT)  # h --> EAST
    t.name('FINGER')

    for i in range(ns):
        t.move_ny("SPACE", fl)
        t.move_ny("FINGER", sl)

    t.move_ny("SPACE", fl)  # h --> EAST
    t.move(be).move(mt)


if __name__ == "__main__":
    main()
