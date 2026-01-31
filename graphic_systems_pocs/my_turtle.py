"""
Overall purpose The file mixes two small subsystems:

1) A lightweight geometry/path “rendering” model (BasicPoint/BasicPath/SvgPath/SvgGroup) that stores points and prints their coordinates.
2) A simple “turtle” movement model (Turtle/Direction) for stepping a position on a grid by turning and moving.

They are not integrated; they coexist in the same module.


Direction (Enum) Purpose: Represent the turtle’s heading.
Members:
• NORTH, SOUTH, EAST, WEST.
Usage:
• Pass into Turtle(..., direction=Direction.NORTH).
• Internally used by Turtle.left(), Turtle.right(), and Turtle.forward().


Renderer (Protocol) Purpose: A typing contract for any object that can “render” itself given an origin.
Method:
• render(self, origin: BasicPoint): a placeholder protocol method.
Usage:
• SvgGroup stores items typed as Renderer to ensure they have a render method.


BasicPoint Purpose: Represent a 2D point (x, y) and allow simple addition.
Attributes:
• x, y: floats.
Methods:
• __init__(x, y): constructs a point.
• get (property): returns (x, y) tuple.
• __add__(other): returns a new BasicPoint with component-wise addition.
• __str__(): returns string like "[x, y]".
Usage:
p = BasicPoint(10, 20)
q = BasicPoint(5, 5)
r = p + q      # BasicPoint(15, 25)
coords = p.get # (10, 20)
print(p)       # "[10, 20]"


BasicPath Purpose: Store a path relative to an origin, as a list of points.
Attributes:
• origin: BasicPoint base for this path.
• points: list of BasicPoint relative to origin.
Methods:
• __init__(x, y): sets origin and empty points.
• add(x, y): appends a new relative point.
• copy(x, y): makes a new BasicPath with a new origin but shares the same points list.
• render(origin): prints each point’s absolute position by adding origin + self.origin + point.
Usage:
path = BasicPath(10, 10)
path.add(50, 0)
path.add(50, 50)
path.render(BasicPoint(0, 0))
# prints points offset by (10,10)
Notes:
• copy() shares the same points list; changing one path affects the other.


SvgPath Purpose: Manage multiple BasicPath objects as a group, each with its own origin.
Attributes:
• origin: optional BasicPoint offset for the whole group.
• paths: list of BasicPath.
Methods:
• __init__(origin=None): sets group origin.
• new_path(x, y): create a BasicPath and store it.
• copy_path(x, y, path): copy an existing path to a new origin (shares points).
• render(origin): renders each BasicPath with the combined origin.
Usage:
svg_path = SvgPath(BasicPoint(0, 0))
path = svg_path.new_path(10, 10)
path.add(50, 0)
svg_path.copy_path(20, 100, path)
svg_path.render(BasicPoint(0, 0))

SvgGroup Purpose: Aggregate multiple “renderable” items with a shared origin.
Attributes:
• origin: optional BasicPoint offset.
• svg_items: list of Renderer (anything with render()).
Methods:
• add_svg_item(item): add a renderable item.
• render(origin=None): render each item with combined origin.
Usage:
group = SvgGroup(BasicPoint(5, 5))
group.add_svg_item(svg_path)
group.render(BasicPoint(0, 0))

Turtle Purpose: Simulate turtle-style movement with direction and forward steps.
Attributes:
• x, y: current position.
• direction: current heading (Direction).
Methods:
• __init__(x=0, y=0, direction=Direction.EAST): initialize and call start.
• start(x=0, y=0, direction=Direction.EAST): reset position and direction.
• left(): rotate 90° left (N→W→S→E).
• right(): rotate 90° right (N→E→S→W).
• forward(n): move by n along the current direction.
• finish(): placeholder (does nothing).
• left_forward(n): turn left then move.
• right_forard(n): turn right then move (typo in name).
Usage:
t = Turtle(0, 0, Direction.NORTH)
t.forward(10)      # moves "north"
t.right()
t.forward(5)       # moves "east"
Note:
• The movement convention is unusual: north/south adjust x, east/west adjust y. If you expect x=horizontal and y=vertical, this will feel rotated.

main() Purpose: Example usage for SvgPath / BasicPath.
Behavior:
• Builds a square path.
• Copies it to a second origin.
• Calls render (prints absolute coordinates).

"""
from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional, Protocol


class Direction(Enum):
    # Cardinal headings used by Turtle movement/turning.
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class Renderer(Protocol):
    def render(self, origin: BasicPoint):
        """Render the object relative to a given origin point."""


class BasicPoint:
    # Simple 2D point with basic vector-like addition.
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def get(self):
        # Convenience tuple representation.
        return self.x, self.y

    def __add__(self, other: BasicPoint):
        # Component-wise addition; returns a new point.
        total = BasicPoint(
            self.x + other.x,
            self.y + other.y
        )
        return total

    def __str__(self):
        return f"[{self.x}, {self.y}]"


class BasicPath:
    # Path defined by an origin and a list of relative points.
    def __init__(self, x: float, y: float):
        self.origin: BasicPoint = BasicPoint(x, y)
        self.points: List[BasicPoint] = []

    def add(self, x: float, y: float):
        # Add a point relative to this path's origin.
        self.points.append(BasicPoint(x, y))

    def copy(self, x: float, y: float):
        # Copy path with a new origin; points list is shared.
        new_path = BasicPath(x, y)
        new_path.points = self.points
        return new_path

    def render(self, origin: BasicPoint):
        # Print each point's absolute position using combined origins.
        origin = origin +  self.origin
        for i, point in enumerate(self.points, 1):
            print(f"{i}: {point + origin}")


class SvgPath:
    # Collection of BasicPath items with an optional group origin.
    def __init__(self, origin: Optional[BasicPoint] = None):
        self.origin = origin
        self.paths: List[BasicPath] = []

    def new_path(self, x: float, y: float):
        # Create and register a new path.
        path = BasicPath(x, y)
        self.paths.append(path)
        return path

    def copy_path(self, x: float, y: float, path: BasicPath):
        # Clone an existing path to a new origin.
        new_path = path.copy(x, y)
        self.paths.append(new_path)

    def render(self, origin: BasicPoint):
        # Render all paths relative to the combined origin.
        origin = origin +  self.origin
        for path in self.paths:
            path.render(origin)


class SvgGroup:
    # Group of renderable items with a shared origin.
    def __init__(self, origin: Optional[BasicPoint] = None):
        self.origin = origin
        self.svg_items: List[Renderer] = []

    def add_svg_item(self, item: Renderer):
        # Add any renderable item (must implement render()).
        self.svg_items.append(item)

    def render(self, origin: Optional[BasicPoint] = None):
        # Render items using a default origin if none provided.
        origin = origin or BasicPoint(0,0)
        origin += self.origin
        for svg_item in self.svg_items:
            svg_item.render(origin)


def main():
    # Demo: build a square path, copy it, and print coordinates.
    svg_path = SvgPath(BasicPoint(0, 0))

    path = svg_path.new_path(10, 10)
    path.add(50, 0)
    path.add(50, 50)
    path.add(0, 50)
    path.add(0, 0)

    svg_path.copy_path(20,100, path)

    svg_path.render(BasicPoint(0,0))


class Turtle:
    # Turtle-like cursor that turns and moves on a 2D plane.
    def __init__(self, x: float = 0, y: float = 0, direction = Direction.EAST):
        self.x = self.y = self.direction = None
        self.start(x, y, direction)

    def start(self, x: float = 0, y: float = 0, direction = Direction.EAST):
        # Reset position and direction.
        self.x = x
        self.y = y
        self.direction = direction

    def left(self):
        # Turn 90 degrees left.
        if self.direction is Direction.NORTH:
            self.direction = Direction.WEST
        elif self.direction is Direction.SOUTH:
            self.direction = Direction.EAST
        elif self.direction is Direction.EAST:
            self.direction = Direction.NORTH
        else:
            self.direction = Direction.SOUTH

    def right(self):
        # Turn 90 degrees right.
        if self.direction is Direction.NORTH:
            self.direction = Direction.EAST
        elif self.direction is Direction.SOUTH:
            self.direction = Direction.WEST
        elif self.direction is Direction.EAST:
            self.direction = Direction.SOUTH
        else:
            self.direction = Direction.NORTH

    def forward(self, n: float):
        # Move forward by n in the current direction.
        if self.direction is Direction.NORTH:
            self.x -= n
        elif self.direction is Direction.SOUTH:
            self.x += n
        elif self.direction is Direction.EAST:
            self.y += n
        else:
            self.y -= n

    def finish(self):
        # Placeholder for any teardown/commit logic.
        pass

    def left_forward(self, n: float):
        # Convenience: turn left and move.
        self.left()
        self.forward(n)

    def right_forard(self, n: float):
        # Convenience: turn right and move (note typo in method name).
        self.right()
        self.forward(n)


if __name__ == "__main__":
    main()
