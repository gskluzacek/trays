from __future__ import annotations

from enum import Enum


class Orientation(Enum):
    CW = "clockwise"
    CCW = "counter_clockwise"
    COL = "collinear"


class Direction(Enum):
    N = "north"
    S = "south"
    E = "east"
    W = "west"


class Point:
    """
    A basic Point class having X and Y coordinates.

    Additionally, 3 consecutive points on a path are said to have a given orientation based on their
    relative location to one another. The 3 points could be going in a clock wise orientation, a
    counter clock wise orientation or neither (i.e., the 3 points form 2 lines that are collinear).
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({str(self.x).zfill(4)}, {str(self.y).zfill(4)})"

    def __repr__(self):
        return str(self)

    def orientation(self, p2: Point, p3: Point) -> Orientation:
        """
        Calculates the orientation of 3 ordered points (on a path).

        :param p2:  the 2nd point in the list of 3 ordered points
        :param p3:  the 3rd point in the list of 3 ordered points
        :return:    the orientation of the 3 ordered points

        self is the 1st point in the list of 3 ordered points

        the 3 ordered points are used to form 2 lines
            - line 1: p1, p2
            - line 2: p2, p3

        depending on the relative "direction" of each line, the orientation is determined.
        in this case direction is actual the slope of a line. That is: rise over run, where rise is defined as
        y2 - y1 and run is defined as x2 - x1 --> (y2 - y1) / (x2 - x1).

        if we calculate the slope of line 1 and line 2, then compare those slopes we can say:
        - if the slope of line 1 is GREATER than the slope of line 2 then the two lines (and therefor the 3 points)
          have a clock wise orientation
        - if the slope of line 2 is greater (i.e., the slope of line 1 is LESS than the slope of line 2) then the
          two lines have a counter clock wise orientation
        - if the slope of lines 1 and 2 are equal, the orientation cannot be determined from these 3 points as the
          line are collinear.

        refer to the Geeks For Geeks article below for details on the calculation used
        https://www.geeksforgeeks.org/orientation-3-ordered-points/
        see also
        https://tutorialspoint.dev/algorithm/geometric-algorithms/orientation-3-ordered-points
        """
        p1 = self
        val = ((p2.y - p1.y) * (p3.x - p2.x)) - ((p2.x - p1.x) * (p3.y - p2.y))

        # note we are operating in quadrant 4, so we are swapping the values that correspond to cw & ccw
        if val > 0:
            return Orientation.CCW
        elif val < 0:
            return Orientation.CW
        else:
            return Orientation.COL


class Line:
    """
    A very simple implementation of a Line Class

    In this implementation of the line class the line can only be horizontal or vertical
    The line can never be diagonal.

    This restriction is primarily due to the fact that the laser cutter cannot create bevel cuts and all cuts
    produced by the laser cutter are 90 degrees. We are not talking about the angle of the horizontal lines cut
    out by the laser cutter but rather vertical lines cut into the material, i.e., the angle between the material
    being cut and the head of the laser cutter itself. And that this ange is limited to exactly 90 degrees.
    """
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"[{self.p1.x}, {self.p1.y} - {self.p2.x}, {self.p2.y}]"

    def delta(self):
        """
        Returns the rise and run of a Line object
        :return: tuple of 2 items: (rise, run)

        rise and run are the 2 components used to calculate the slop of a line
        rise is: y2 - y1
        run is: x2 - x1
        slope is: rise / run akd (y2-y1)/(x2-x1)
        """
        y_delta = self.p2.y - self.p1.y  # aka rise
        x_delta = self.p2.x - self.p1.x  # aka run
        return y_delta, x_delta

    def length(self):
        """
        Determine the length of a line.

        :return: a value greater than 0 representing the length of the line

        Note: In our simple world, the line must be either vertical or horizontal and NOT diagonal.
        """
        # because the lines that we are working with are either horizontal or vertical and
        # never diagonal, that means that one of the two variables (x_delta & y_delta) will
        # be zero and the other will be non-zero - so we can just return the absolute value
        # of the sum of the two values (as we want length to only be positive).
        y_delta, x_delta = self.delta()

        # the order of the points used to define a line are not important and that is why we
        # are using the absolute values here
        return abs(y_delta + x_delta)

    def direction(self) -> Direction:
        """
        Determine the direction of a line.

        :return: the direction of the line: left, right, up or down.

        Note: In our simple world, the line must be either vertical (up or down) or horizontal (left or right)
        and NOT diagonal.
        """
        y_delta, x_delta = self.delta()

        # use case x_delta (run) is 0 and y_delta (rise) is non-zero
        if not x_delta:
            # the line is going up if the y_delta (rise) is positive ( > 0 )
            #   else the line is going down if the y_delta (rise) in negative ( < 0 )
            #   the rise can never be 0 if the run is 0
            return Direction.S if y_delta > 0 else Direction.N
        else:
            # the line is going left if the x_delta (run) is positive ( > 0 )
            #   else the line is going down if the x_delta (run) in negative ( < 0 )
            #   the run can never be 0 if the rise is 0
            return Direction.E if x_delta > 0 else Direction.W
