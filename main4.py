from __future__ import annotations

from operator import attrgetter
from itertools import count
from typing import List, Tuple, Dict, Optional

from cyclic_n_tuples import cyclic_n_tuples, fwd_pair, rev_pair


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

    def orientation(self, p2, p3) -> str:
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

        if val > 0:
            # return 'cw'
            return "ccw"  # flip for quadrant 4
        elif val < 0:
            # return 'ccw'
            return "cw"  # flip for quadrant 4
        else:
            return "col"


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

    def direction(self):
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
            return "down" if y_delta > 0 else "up"
        else:
            # the line is going left if the x_delta (run) is positive ( > 0 )
            #   else the line is going down if the x_delta (run) in negative ( < 0 )
            #   the run can never be 0 if the rise is 0
            return "right" if x_delta > 0 else "left"


class Path:
    """
    A simple implementation of a Path class

    A path is ordered list of points that form a polygon.

    in order to be a valid path and therefor a polygon, the path must have a minimum of 3 points
    that is the path must form a triangle (a polygon with 3 sides). A triangle is the polygon with the fewest
    points possible.

    apparently the Path class is not currently used yet, but it does have documentation value in the fact that it
    tells you that the minimum number of points required to form a polygon is 3.
    """
    def __init__(self, start_point: Point):
        self.points = [start_point]

    def add_point(self, point: Point):
        self.points.append(point)


class DimPoint:
    """
    The DimPoint class represents in a single object, the inside, on-center and outside x,y coordinates of a given
    "point" in a path.

    The DimPoint also has other attributes describing it:
        - line_type: reserved (tbd)
        - direction: represents the direction of the point (when taking in consideration of the relative
          location of the next point), which can be: left, right, up or down
        - corner_side: represents if the point lies on inside corner or an outside corner (when taking into
          consideration the relative location of the previous point AND orientation of the path
          [clock wise or counter clock wise])
        - id: a sequential value assigned when creating a new instance of the class, values are assigned sequentially
          and without gaps. this attribute is only for display or debugging purposes and does not serve any
          functional purpose.
        - prev: represents the previous point in the path
        - next: represents the next point in the path

    the prev & next points are initially set to None and then updated when the points are being
    added to the path. that is, you cannot set the prev attribute of a point when there is
    only 1 point on the path. Additionally, the prev point of the first point in the path cannot
    be set until after the last point has been added to the path. Like wise the last point in the
    path cannot be set until we know that no more points will be added to the path (see set_warp
    method of the DimPath class).

    the corner_side is handled similarly to prev and next. It is initially set to None and then updated
    when adding points to the path. It is determined by using a lookup dictionary that takes the inputs
    of: the orientation of the path, the direction of the previous point and the direction of the current
    point. Hence, we cannot determine the corner_side attribute for each point until the next point is
    added, and cannot determine the corner_side of the first point, until after the last point has been
    added (see set_warp method of the DimPath class).

    direction is determined (outside of the DimPoint constructor) by using the current point and next point on the
    path to form a lines object and then calling the direction method of the line object.
    """
    seq = count(1)

    def __init__(
        self,
        direction: str,
        line_type: str,
        outside_pt: Point,
        on_center_pt: Point,
        inside_pt: Point,
        index_pt: IndexPoint,
        copy_id: int = None,
    ):
        self.direction: str = direction
        self.line_type: str = line_type
        self.corner_side: Optional[str] = None
        self.outside_pt: Point = outside_pt
        self.on_center_pt: Point = on_center_pt
        self.inside_pt: Point = inside_pt
        self.index_point: IndexPoint = index_pt
        self.id: int = next(self.seq)
        self.copy_id = copy_id
        self.prev: Optional[DimPoint] = None
        self.next: Optional[DimPoint] = None

    def __str__(self):
        return f"[{self.direction} {self.line_type} {self.outside_pt} {self.on_center_pt} {self.inside_pt}]"

    def outer_line_length(self, other) -> float:
        """
        Calculates the length to use as the outside length of a line adjust for inside corners.

        :param other:   the other point to use in the calculation
        :return:        the calculated length value

        This method takes 2 DimPoint objects as its arguments:
            - self is the first DimPoint object
            - other is the second DimPoint object

        the outer line length needs to be adjusted when the starting or ending or both the starting and ending
        points are on an inside corner.

        we call the first point the current point (curr) and call the second point the next point (next).
        the x, y coordinates of the current point are called curr_x and curr_y respectively, likewise the x, y
            coordinates of the next point are called next_x and next_y
        Together the outside coordinates of the DimPoint objects (curr_x, curr_y & next_x, next_y)
            form the unadjusted line segment.
        The outside x,y coordinates of the DimPoint objects will be used as the "starting point" for the beginning
            and ending points of the line (i.e., the beginning point is: curr_x, curr_y and the ending
            point is: next_x, next_Y) and will be adjusted.
        Hence, initially we will set curr_x, curr_y and next_x, next_y to the outside x y coordinates of
            their respective DimPoint objects
        The method will examine the corner side and direction for each DimPoint object and adjust curr_x,
            curr_y & next_x, next_y coordinates accordingly.
        A corner side can either be an INSIDE corner or an OUTSIDE corner.
        Direction can be: left, right, up or down
        If the corner side is an OUTSIDE corner then we DO NOT adjust the  x, y coordinates
        If the corner side is an INSIDE corner then we DO adjust the x, y coordinates.
        To adjust the coordinates we look at the direction of the DimPoint object.
        If the direction is left or right we adjust the x coordinate.
        If the direction is up or down then we adjust the y coordinate.
        The x or y coordinated is addjust by getting the inside dimension of the DimPoint object and assigning
            curr_x, curr_y, next_x, next_y as appropriate.
        """
        # assign curr_x & curr_y to the outside dimension x & y
        curr_pt = self.get("outside")
        curr_x = curr_pt.x
        curr_y = curr_pt.y

        # assign next_x & next_y to the outside dimension x & y
        next_pt = other.get("outside")
        next_x = next_pt.x
        next_y = next_pt.y

        # check if the current point (i.e., self) is an inside corner
        if self.corner_side == "inside":
            # if the current point is an outside corner we want to adjust it to the corresponding inside coordinates
            curr_pt = self.get("inside")
            # adjust the x coordinate to the inside x coordinate if the direction is left or right
            if self.direction in ("left", "right"):
                curr_x = curr_pt.x
            # adjust the y coordinate to the inside y coordinate if the direction is up or down
            elif self.direction in ("up", "down"):
                curr_y = curr_pt.y
            else:
                raise Exception(f"invalid direction for curr_pt: {self}")

        # check if the next point (i.e., other) is an inside corner
        if other.corner_side == "inside":
            # if the next point is an outside corner we want to adjust it to the corresponding inside coordinates
            next_pt = other.get("inside")
            # adjust the x coordinate to the inside x coordinate if the direction is left or right
            if self.direction in ("left", "right"):
                next_x = next_pt.x
            # adjust the y coordinate to the inside y coordinate if the direction is up or down
            elif self.direction in ("up", "down"):
                next_y = next_pt.y
            else:
                raise Exception(f"invalid direction for next_pt: {other}")

        # define adjusted Point objects based on the adjusted x, y coordinates
        curr_pt = Point(curr_x, curr_y)
        next_pt = Point(next_x, next_y)

        # return the length of the adjusted line segment
        return Line(curr_pt, next_pt).length()

    def get(self, dim: str) -> Point:
        """
        Get the simple point corresponding to the specified dimension.

        :param dim: the dimension of the DimPoint to get, must be either outside, inside or on_center.
        :return: the Point object corresponding to the dimension specified
        """
        if dim == "outside":
            return self.outside_pt
        elif dim == "inside":
            return self.inside_pt
        elif dim == "on_center":
            return self.on_center_pt
        else:
            raise ValueError(f"Invalid dim name: {dim}")

    def dire(self) -> str:
        return self.direction

    def next_dim_pt(self) -> DimPoint:
        return self.next

    def prev_dim_pt(self) -> DimPoint:
        return self.prev

    def get_next_start(self) -> DimPoint:
        # TODO: modify the loop condition to include line type as well as the direction
        temp = self.next_dim_pt()
        while temp.dire() == self.dire():
            temp = temp.next_dim_pt()
        return temp

    def get_prev_end(self) -> DimPoint:
        temp = self.prev_dim_pt()
        while temp.dire() == self.dire():
            temp = temp.prev_dim_pt()
        return temp


class DimPath:
    """
    A DimPath instance is an order sequence of DimPoint objects.

    This class provides a add convenience method that both creates a DimPoint object (calculating the required DimPoint
    attributes) and adds the point to the DimPath's list of points.

    It also provides a set_wrap method that closes or finalizes an instance of the DimPath class, by updating certain
    attributes of the first and last DimPoint objects contained in the DimPath.

    After set_wrap has been called, no more points should be added to the path. We do not currently guard against
    this, so it is up to the developer to ensure that they do not do this.

    the final method of the DimPath class, uses a dictionary to look up the corner_side value for a given DimPoint.
    The corner_side value can either be inside or outside and is based on the orientation of the DimPath (clock wise
    or counter clock wise), the direction (left, right, up or down) of the current point and the direction of
    the previous point.
    """
    corner_side: Dict[str, Dict[str, Dict[str, str]]] = {
        "cw": {
            "left": {"up": "outside", "down": "inside"},
            "right": {"up": "inside", "down": "outside"},
            "up": {"left": "inside", "right": "outside"},
            "down": {"left": "outside", "right": "inside"},
        },
        "ccw": {
            "left": {"up": "inside", "down": "outside"},
            "right": {"up": "outside", "down": "inside"},
            "up": {"left": "outside", "right": "inside"},
            "down": {"left": "inside", "right": "outside"},
        },
    }

    def __init__(self, path_ori: str):
        """
        Creates an empty DimPath object with the specified orientation.

        :param path_ori: path orientation, either: cw (clock wise) or ccw (counter clock wise)

        The Path orientation is determined after all the IndexPoints for given IndexPath have been added and
        the Base class's end_path method has been called

        The path is created empty from the Base class's cal_dim_paths() method and points are added to the
        Dim Path by calling DimPath.add from the same.

        a corresponding DimPath is created for each IndexPath

        for each IndexPoints of an IndexPath a DimPoint is created as follows
        - the previous and next IndexPoints are retrieved
        - the AVG coordinates are retrieved for the Prev, Curr & Next IndexPoints (from the corresponding
          AggregatePoint objects - AggregatePoint objects are calculated from the material width, column
          widths & rows heights and have min xy, avg xy and max xy coordinates)
        - line objects are created from prev AVG coord, curr AVG coord (prev line) and from curr AVG coord,
          next AVG coord (next line)
        - the previous direction and current directions are retrieved for the prev_line & next_line objects
          (left, right, up, down).
        - from the path orientation, prev_line_direction and next_line_direction the "point numbers" for the
          outside dimensional point and inside dimensional point are determined. for each combination of
          orientation, prev direction and next direction a point number (1 thru 8) is looked up.
        - the outside point number and inside point number are then used to get xy coordinates for the outside xy
          coordinate and inside xy coordinate. A point number corresponds to a specific set of x-min, y-min, x-avg,
          y-avg, x-max, y-max pairs
        - the outside xy coordinate, inside xy coordinate along with the on-center (curr AVG aggregate point) xy
          coordinate and curr_direction and line_type (reserved / TBD) and then passed to the DimPath.add method.
        """
        self.path_ori = path_ori
        self.path_points: List[DimPoint] = []

    def get_corner_side(self, prev_dim_pt: DimPoint, curr_dim_pt: DimPoint) -> str:
        """
        Calculate the Corner Side for a given Previous and Current DimPoint objects.

        :param prev_dim_pt:     the previous point
        :param curr_dim_pt:     the current point
        :return:                the corner side: inside-corner or outside-corner

        the direction of the previous and current points is retrieved and along with the path's orientation, the
        corner side is then looked up. Each combination of orientation (clock wise or counter clock wise), previous
        direction (up, down, left, right) and current direction corresponds to the current point's corner side.
        Either the point lines on an inside corner of a polygon or on an outside corner of a polygon.
        """
        return self.corner_side[self.path_ori][prev_dim_pt.dire()][curr_dim_pt.dire()]

    def add(
        self,
        direction: str,
        line_type: str,
        outside_pt: Point,
        on_center_pt: Point,
        inside_pt: Point,
        index_point: IndexPoint,
        copy_id: int = None,
    ) -> DimPoint:
        """
        Create and add a new DimPoint to the DimPath.

        :param direction:       the direction (left, right, up, down) of the current point to the next point
        :param line_type:       the line type, reserved, TBD
        :param outside_pt:      the xy Point object for the outside point
        :param on_center_pt:    the xy Point object for the on-center point
        :param inside_pt:       the xy Point object for the inside point
        :param index_point:     the index_point used to generate the dim point
        :param copy_id:         if we are adding a point that came from another point, we use the copy_id to track the
                                original point
        :return:                Nothing

        if the point being added, is the 2nd or more point, then
            - the corner side of the current point is determined and set by using the current point and the
              previous point.
            - additionally, the current points previous point is set and the previous points next point is set.
        """
        # create the new point
        new_point = DimPoint(direction, line_type, outside_pt, on_center_pt, inside_pt, index_point, copy_id)

        # if there is at least one other point in the list
        if self.path_points:
            # get the prev point
            prev_point = self.path_points[-1]
            # if the lines are not collinear (i.e., have the same direction)
            if new_point.direction != prev_point.direction:
                # set the corner side
                new_point.corner_side = self.get_corner_side(prev_point, new_point)
            # set tne previous point's next point and set the current point's previous point
            prev_point.next = new_point
            new_point.prev = prev_point
        # add the new point to the path
        self.path_points.append(new_point)
        return new_point

    def set_wrap(self) -> None:
        """
        Finalizes the path by connecting the first and last points' prev & next.

        :return:    nothing

        Call the set_wrap method after the last point has been added to the DimPath object.
        After calling set_wrap, you should not add additional points to the path!

        The method will
        - set the previous point for the first point in the path to the last point in the path
        - set the next point for the last point in the path to the first point it the path
        - if the first and last points are not collinear, then it will also set the corner side for
          first point in the path
        """
        # get the first and last points in the path
        first_point = self.path_points[0]
        last_point = self.path_points[-1]
        # if the points are not collinear
        if first_point.direction != last_point.direction:
            # set the corner side of the first point
            first_point.corner_side = self.get_corner_side(last_point, first_point)
        # set the last point's next to the fisrt point and the first point's prev to the last point
        last_point.next = first_point
        first_point.prev = last_point


class AggregatePoint:
    """
    The AggregatePoint class is used to transition the input values for column widths and row heights into
    a raw set of x y coordinates which contain min, avg and max coordinates that take the material thickness
    into consideration.
    """
    def __init__(
        self,
        x_min: float,
        y_min: float,
        x_avg: float,
        y_avg: float,
        x_max: float,
        y_max: float,
    ):
        """
        Create Aggregate Point.

        :param x_min:  x1
        :param y_min:  y1
        :param x_avg:  x2
        :param y_avg:  y2
        :param x_max:  x3
        :param y_max:  y3
        """
        self.x1, self.y1 = x_min, y_min
        self.x2, self.y2 = x_avg, y_avg
        self.x3, self.y3 = x_max, y_max

    def __str__(self):
        return f"[[min {self.x1}, {self.y1}], [avg {self.x2}, {self.y2}], [max {self.x3}, {self.y3}]]"

    def __repr__(self):
        return str(self)

    def avg(self) -> Point:
        """
        Get the Point object for the average point of the Aggregate Point object.

        :return: a Point object that is the x, y coordinates representing an average of the min & max coordinate values
        """
        return Point(self.x2, self.y2)

    def get(self, pt_nbr: int) -> Point:
        """
        Get the x, y coordinates corresponding to the given point number.

        :param pt_nbr:  integer value 1 through 8
        :return:        real x, y point obj for given point number

        the x, y coordinates returned are based on the point number passed in
            pt nbr 1:       x_min, y_min
            pt nbr 2:       x_avg, y_min
            pt nbr 3:       x_max, y_max
            pt nbr 4:       x_min, y_avg
            pt nbr 5:       x_max, y_avg
            pt nbr 6:       x_min, y_max
            pt nbr 7:       x_avg, y_max
            pt nbr 8:       x_max, y_max

        notes:
            variables x1 & y1 correspond to x_min & y_min
            variables x3 & y3 correspond to x_max & y_max
            variables x2 & y2 correspond to x_avg & y_avg (the average of the max and min values)
        """
        if pt_nbr == 1:
            return Point(self.x1, self.y1)
        elif pt_nbr == 2:
            return Point(self.x2, self.y1)
        elif pt_nbr == 3:
            return Point(self.x3, self.y1)
        elif pt_nbr == 4:
            return Point(self.x1, self.y2)
        elif pt_nbr == 5:
            return Point(self.x3, self.y2)
        elif pt_nbr == 6:
            return Point(self.x1, self.y3)
        elif pt_nbr == 7:
            return Point(self.x2, self.y3)
        elif pt_nbr == 8:
            return Point(self.x3, self.y3)


class IndexPoint:
    """
    the IndexPoint class is a column (x) and row (y) position into the 2 dimensional AggregatePoint array
    where the columns and rows have simple widths & heights. The use of IndexPoint allows us to describe
    a polygon's path using simple column and row integer indices instead of actual decimal x, y coordinates.
    """

    def __init__(self, x_index: int, y_index: int, line_type: Optional[str] = None, dim_pt: DimPoint = None):
        self.line_type = line_type
        self.x_index = x_index
        self.y_index = y_index
        self.dim_point: Optional[DimPoint] = dim_pt

    def __str__(self) -> str:
        return f"[{self.x_index}, {self.y_index}]"

    def __repr__(self) -> str:
        return str(self)

    @property
    def gxy(self) -> Tuple[int, int]:
        return self.x_index, self.y_index


class IndexPath:
    def __init__(self, start_point: IndexPoint = None, orientation: str = None):
        self.orientation = orientation
        self.index_points: List[IndexPoint] = [start_point] if start_point else []

    def add_point(self, point: IndexPoint) -> None:
        self.index_points.append(point)


class IndexWall:
    def __init__(self, start_pt: IndexPoint, end_pt: IndexPoint, wall_type: str):
        self.start_pt = start_pt
        self.end_pt = end_pt
        self.wall_type = wall_type

    def __str__(self):
        return f"{self.start_pt} {self.end_pt} | {self.start_pt.dim_point} {self.end_pt.dim_point}"


class Intersection:
    def __init__(self, intrxn: Point, x_type: str, x_subtype: str):
        self.intrxn = intrxn
        self.x_type = x_type
        self.x_subtype = x_subtype
        self.xpt_sort = (intrxn.x, intrxn.y)


class BaseSlot:
    def __init__(self, bslot_type):
        self.type: str = bslot_type     # horz or vert
        self._intersections: List[Intersection] = []
        self.sorted = False

    @property
    def intersections(self):
        if not self.sorted:
            self._sort()
        return self._intersections

    def add(self, intrxn_pt: Point, x_type: str, x_subtype: str):
        intrxn = Intersection(intrxn_pt, x_type, x_subtype)
        self._intersections.append(intrxn)

    def _sort(self):
        self.sorted = True
        self._intersections.sort(key=attrgetter('xpt_sort'))


class Wall:
    seq = count(1)
    def __init__(self, pt_1: Point, pt_2: Point, w_type=None):
        """
        Define a Wall Object.

        :param pt_1:        Point object defining the beginning of the wall
        :param pt_2:        Point object defining the ending of the wall
        :param w_type:      type of wall: finger joint, tab slot

        other attributes:
        - super_direction:  vertical or horizontal
        - inter_wall_list:  list of IntersectionToWall objects that the wall contains

        the method will determine the super direction by comparing the 2 x coordinates
            and the 2 y coordinates.
        additionally, the method will ensure that the pt_1 attribute contains the Point
            object that has the smaller x coordinate if it is a horizontal wall or
            the smaller y coordinate if it is a vertical wall. Swapping pt_1 and pt_2
            if necessary.
        """
        self.id = next(self.seq)
        self.type = w_type
        t1, t2 = pt_1, pt_2
        # check if the line is horizontal or vertical. If both x coords are equal then vertical
        if pt_1.x == pt_2.x:
            spr_dir = "vert"
            # make sure pt_1 is the point with the smaller y coordinate
            if pt_1.y > pt_2.y:
                pt_2, pt_1 = pt_1, pt_2
        # else if both y coords are equal then horizontal
        elif pt_1.y == pt_2.y:
            spr_dir = "horz"
            # make sure pt_1 is the point with the smaller x coordinate
            if pt_1.x > pt_2.x:
                pt_2, pt_1 = pt_1, pt_2
        else:
            raise ValueError(
                f"the line must be horizontal or vertical - given points ({t1.x}, {t1.y}) and ({t2.x}, {t2.y})."
            )
        self.super_direction = spr_dir
        self.pt_1 = pt_1
        self.pt_2 = pt_2
        self.inter_walL_list = []

    def __str__(self):
        return f"WALL #{self.id} - pt1: {self.pt_1} pt2: {self.pt_2} : {self.super_direction}"

    def intersect(self, other: Wall) -> Tuple[Optional[str], Optional[str], Optional[Point]]:
        """
        Determine the intersection type if a given vertical wall intersects with a given horizontal wall.

        :param other:   the vertical wall
        :return:        the type of intersection: corner, cross, tee or None if the 2 walls do not intersect

        self is the horizontal wall.
        """
        horz = self
        horz_y = horz.pt_1.y
        vert = other
        vert_x = vert.pt_1.x
        intersection_point = Point(vert_x, horz_y)
        # cross intersection
        if vert.pt_1.y < horz_y < vert.pt_2.y and horz.pt_1.x < vert_x < horz.pt_2.x:
            return "cross", None, intersection_point
        # corner intersection
        elif horz.pt_1.x == vert.pt_1.x and horz.pt_1.y == vert.pt_1.y:
            return "corner", "upper-left", intersection_point
        elif horz.pt_1.x == vert.pt_2.x and horz.pt_1.y == vert.pt_2.y:
            return "corner", "lower-left", intersection_point
        elif horz.pt_2.x == vert.pt_1.x and horz.pt_2.y == vert.pt_1.y:
            return "corner", "upper-right", intersection_point
        elif horz.pt_2.x == vert.pt_2.x and horz.pt_2.y == vert.pt_2.y:
            return "corner", "lower-right", intersection_point
        # tee intersection
        elif vert.pt_1.y == horz_y and horz.pt_1.x < vert_x < horz.pt_2.x:
            return "tee", "top", intersection_point
        elif vert.pt_2.y == horz_y and horz.pt_1.x < vert_x < horz.pt_2.x:
            return "tee", "bottom", intersection_point
        elif horz.pt_1.x == vert_x and vert.pt_1.y < horz_y < vert.pt_2.y:
            return "tee", "left", intersection_point
        elif horz.pt_2.x == vert_x and vert.pt_1.y < horz_y < vert.pt_2.y:
            return "tee", "right", intersection_point
        # walls do not intersect
        else:
            return None, None, None


class Base:
    """
    The Base class represents the dimensions of the base of the tray. It uses a path of points to
    describe the polygon shape will form the base of the tray.
    """
    # direction_dims is a dictionary used to look up the outer, inner tuple pair for a given
    #   combination of path orientation, prev_direction and current direction
    direction_dims: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = {
        "cw": {
            "left": {"left": (7, 2), "up": (6, 3), "down": (8, 1)},
            "right": {"right": (2, 7), "up": (1, 8), "down": (3, 6)},
            "up": {"left": (6, 3), "right": (1, 8), "up": (4, 5)},
            "down": {"left": (8, 1), "right": (3, 6), "down": (5, 4)},
        },
        "ccw": {
            "left": {"left": (2, 7), "up": (3, 6), "down": (1, 8)},
            "right": {"right": (7, 2), "up": (8, 1), "down": (6, 3)},
            "up": {"left": (3, 6), "right": (8, 1), "up": (5, 4)},
            "down": {"left": (1, 8), "right": (6, 3), "down": (4, 5)},
        },
    }

    def __init__(
        self,
        mat_thick: float,
        fngr_len: float,
        spc_len: float,
        min_be_len: float,
        col_widths: List[float],
        row_heights: List[float],
        max_tbslt_bt_xs: int,
        min_tbslt_len: int,
        wall_tbslt_dist: float,
        depth: float,
    ):
        """
        Create a Base object

        :param mat_thick:       material thickness
        :param fngr_len:        finger length - the width of a finger joint
        :param spc_len:         space length - the width of a space within a finger joint
        :param min_be_len:      minimum beginning / ending length - the minimal width of the space that come before
                                and after the finger/space joint
        :param col_widths:      list of column widths to use to calculate the base dimensions (aggregate points)
        :param row_heights:     list of row heights to use to calculate the base dimensions (aggregate points)
        :param depth:           how high the walls are...
        """
        self.max_tbslt_bt_xs = max_tbslt_bt_xs
        self.min_tbslt_len = min_tbslt_len
        self.wall_tbslt_dist = wall_tbslt_dist

        self.index_paths: List[IndexPath] = []
        self.dim_paths: List[DimPath] = []

        self.norm_index_paths: List[IndexPath] = []
        self.norm_dim_paths: List[DimPath] = []

        self.index_walls: List[IndexWall] = []
        self.base_slots: List[BaseSlot] = []

        self.mat_thick = mat_thick
        self.fngr_len = fngr_len
        self.spc_len = spc_len
        self.min_be_len = min_be_len
        self.depth_outer = depth

        self.col_widths = col_widths
        self.nbr_cols = len(self.col_widths)
        self.width = sum(self.col_widths)

        self.row_heights = row_heights
        self.nbr_rows = len(self.row_heights)
        self.height = sum(self.row_heights)

        self.agg_coords: List[List[AggregatePoint]] = []

        # self.calc_coords()

    def get_avg_agg_point(self, index_point: IndexPoint) -> Point:
        """
        Returns the AVG point from the AggregatePoint corresponding to the specified IndexPoint

        :param index_point:     the index point to get the AVG aggregate x,y coordinate values
        :return:                the Point object for the AVG coordinate of the AggregatePoint

        IndexPoint objects represent the column (x) and row (y) position within the 2D AggregatePoint grid
        """
        return self.agg_coords[index_point.x_index][index_point.y_index].avg()

    def get_dims_from_agg_points(
        self, index_point: IndexPoint, outside: int, inside: int
    ) -> Tuple[Point, Point]:
        """
        Returns the inside and outside dimensions (x, y coords) points for a given index point and point numbers.

        :param index_point:     index point corresponding to the aggregate point you wish to get the
                                inside and outside dimensional points for
        :param outside:         point number to get for the outside dimensional point
        :param inside:          point number to get for the inside dimensional point
        :return:                the x, y coordinates (outside, inside) corresponding to the point numbers specified

        the agg_pt.get() method takes a point number and returns real point object based on that as follows
            pt nbr 1:       x_min, y_min
            pt nbr 2:       x_avg, y_min
            pt nbr 3:       x_max, y_max
            pt nbr 4:       x_min, y_avg
            pt nbr 5:       x_max, y_avg
            pt nbr 6:       x_min, y_max
            pt nbr 7:       x_avg, y_max
            pt nbr 8:       x_max, y_max
        """
        # get the aggregate point corresponding to the index point passed in
        agg_pt = self.agg_coords[index_point.x_index][index_point.y_index]

        # get the outside & inside dimensional coordinates based on the point numbers (1 - 4) passed in
        outside_pt = agg_pt.get(outside)
        inside_pt = agg_pt.get(inside)

        return outside_pt, inside_pt

    def calc_agg_coords(self):
        # calc the ratio to adjust the column widths by
        #   total_mat_thickness = (nbr_of_cols + 1) * mat_thick
        #   total_inside_dim_cols_widths = total_of_all_columns - total_mat_thickness
        #   ratio = total_inside_dim_cols_widths / total_of_all_columns
        col_ratio = (self.width - ((self.nbr_cols + 1) * self.mat_thick)) / self.width

        # calc adjusted columns (i.e., inside dim width)
        col_id_widths = [col * col_ratio for col in self.col_widths]

        # calc the column offsets by accumulating
        #   the adj col widths
        #   plus the mat_thickness
        col_offset = 0
        col_offsets = [col_offset]
        for col_id_width in col_id_widths:
            col_offset += col_id_width + self.mat_thick
            col_offsets.append(col_offset)

        # do the same for the rows...

        row_ratio = (self.height - ((self.nbr_rows + 1) * self.mat_thick)) / self.height
        row_id_heights = [row * row_ratio for row in self.row_heights]
        row_offset = 0
        row_offsets = [row_offset]
        for row_id_height in row_id_heights:
            row_offset += row_id_height + self.mat_thick
            row_offsets.append(row_offset)

        for col in col_offsets:
            x_min = col
            x_max = col + self.mat_thick
            x_avg = (x_min + x_max) / 2.0
            row_of_agg_points = []
            for row in row_offsets:
                y_min = row
                y_max = row + self.mat_thick
                y_avg = (y_min + y_max) / 2.0
                row_of_agg_points.append(
                    AggregatePoint(x_min, y_min, x_avg, y_avg, x_max, y_max)
                )
            self.agg_coords.append(row_of_agg_points)

    def calc_dim_paths(self):
        # TODO: !!! see if we could refactor the bulk of the functionality (i.e., the code in the for loop)
        #   in this method into the DimPath add() method. This would allow the add method to be more independent
        #   and more usable by other functions (if necessary). That is if we needed to create DimPath objects from
        #   other lists than just the list used to hold the BASE object's points.
        for i_path in self.index_paths:

            # determine the orientation for the path by using the first 3 points of the path
            path_ori = i_path.orientation

            # loop over each point in the `modified` path
            dim_path = DimPath(path_ori)
            for prev_i_point, curr_i_point, next_i_point in cyclic_n_tuples(i_path.index_points, 3, -1):

                # get the avg aggregate (on center) point for the p, c & n ndx pts
                prev_pt = self.get_avg_agg_point(prev_i_point)
                curr_pt = self.get_avg_agg_point(curr_i_point)
                next_pt = self.get_avg_agg_point(next_i_point)

                # generate the previous and current lines from the p, c & n ndx pts
                prev_ln = Line(prev_pt, curr_pt)
                curr_ln = Line(curr_pt, next_pt)

                # get the line directions (going left, right, up or down)
                prev_dire = prev_ln.direction()
                curr_dire = curr_ln.direction()

                # determine outside & inside dimensional points based on the:
                #   previous line direction
                #   current line direction
                #   and path orientation
                outside_pt_nbr, inside_pt_nbr = Base.dim(prev_dire, curr_dire, path_ori)
                outside_dim, inside_dim = self.get_dims_from_agg_points(
                    curr_i_point, outside_pt_nbr, inside_pt_nbr
                )
                new_dim_point = dim_path.add(
                    direction=curr_dire,
                    line_type=curr_i_point.line_type,
                    outside_pt=outside_dim,
                    on_center_pt=curr_pt,
                    inside_pt=inside_dim,
                    index_point=curr_i_point,
                )
                curr_i_point.dim_point = new_dim_point
            dim_path.set_wrap()
            self.dim_paths.append(dim_path)

    def orientation(self, i_path):
        # notes:
        #   - it takes at a minimum 3 points to form a polygon
        #   - (at least) 3 of the points must not be collinear
        #       that is 3 collinear points would form a line not a polygon
        #   - that being said, we will try 3 points, incrementally until we get an orientation of non-collinear
        #   - but if all the points in the path do form a straight line (and not a polygon) we could, in theory
        #       go past the end of the list (out of bounds exception) unless we code for that condition
        #   - and if the path does not contain at least 3 points, the for loop will NOT execute at all

        if len(i_path.index_points) < 3:
            raise ValueError(
                f"could not determine the path's orientation (clock wise or counter clock wise). "
                f"please check that you have 3 or more points in your path. Path len: {len(i_path.index_points)}"
            )

        path_ori = None
        for i in range(len(i_path.index_points) - 2):
            i_pt_1 = i_path.index_points[i]
            pt_1 = self.get_avg_agg_point(i_pt_1)
            i_pt_2 = i_path.index_points[i + 1]
            pt_2 = self.get_avg_agg_point(i_pt_2)
            i_pt_3 = i_path.index_points[i + 2]
            pt_3 = self.get_avg_agg_point(i_pt_3)
            path_ori = pt_1.orientation(pt_2, pt_3)
            if path_ori != "col":
                break

        if path_ori == "col":
            raise ValueError(
                "could not determine the path's orientation (clock wise or counter clock wise). "
                "please check that all points in the path are not collinear"
            )
        if path_ori is None:
            raise ValueError("exhausted path without determining the orientation")

        return path_ori

    def calc_min(self, tot_len: float) -> (int, int, float):
        """
        Calculates the number of fingers, spaces & beginning / ending length for finger joint edges.

        :param tot_len:     the total length of the edge - outside diameter
        :return:            a tuple of:
                            number of fingers in the finger joint edge
                            number of spaces in the finger joint edge
                            the calculated beginning / ending length
        """
        # TODO: look at where we're using integer division
        #   and see how we could maybe introduce a fractional precision
        #   into the calculation

        # TODO: is the use case of 1 finger and 0 spaces valid?
        max_fs = tot_len - ((self.mat_thick + self.min_be_len) * 2)
        n1 = max_fs + self.spc_len
        n2 = self.fngr_len + self.spc_len
        nbr_of_fngrs = int(n1 // n2)
        nbr_of_spcs = nbr_of_fngrs - 1
        tot_fngr_len = nbr_of_fngrs * self.fngr_len
        tot_spc_len = nbr_of_spcs * self.spc_len
        be_len = self.min_be_len + ((max_fs - tot_fngr_len - tot_spc_len) / 2)

        return nbr_of_fngrs, nbr_of_spcs, be_len

    def normalize_paths(self):
        for dim_path in self.dim_paths:
            starting_point = None
            norm_index_path = IndexPath(orientation=dim_path.path_ori)
            norm_dim_path = DimPath(dim_path.path_ori)
            curr_point = dim_path.path_points[0].get_prev_end().next_dim_pt()

            while curr_point != starting_point:
                if not starting_point:
                    starting_point = curr_point

                dim_pt = norm_dim_path.add(
                    direction=curr_point.direction,
                    line_type=curr_point.line_type,
                    outside_pt=curr_point.outside_pt,
                    on_center_pt=curr_point.on_center_pt,
                    inside_pt=curr_point.inside_pt,
                    index_point=curr_point.index_point,
                    copy_id=curr_point.id
                )
                curr_i_pt = curr_point.index_point
                index_pt = IndexPoint(
                    x_index=curr_i_pt.x_index,
                    y_index=curr_i_pt.y_index,
                    line_type=curr_i_pt.line_type,
                    dim_pt=dim_pt,
                )
                norm_index_path.add_point(index_pt)
                curr_point = curr_point.get_next_start()

            norm_dim_path.set_wrap()
            self.norm_index_paths.append(norm_index_path)
            self.norm_dim_paths.append(norm_dim_path)

            # TODO: link between the dim_point and the index_point
            # TODO: normalize the index_points too

    def gen_svg_inner_walls(self):
        extra_space = 20
        horz_os = extra_space
        vert_os = self.height + extra_space
        inc_vos = self.depth_outer + self.mat_thick + extra_space

        vtab_len = (self.depth_outer - (3 * self.wall_tbslt_dist)) / 2
        y_side_a = vert_os + self.depth_outer
        x_side_1_b = horz_os
        x_side_1_a = horz_os + self.mat_thick
        cross_slot_len = self.depth_outer / 2

        svg_paths = []
        for bslot in self.base_slots:
            svg_cmds = []
            c_to_c_len = Line(bslot.intersections[0].intrxn, bslot.intersections[-1].intrxn).length()

            # y_side_a gets initialized before the outer for loop and gets incremented
            #   at the end of the outer for loop
            y_side_b = y_side_a - self.wall_tbslt_dist
            y_side_c = y_side_b - vtab_len
            y_side_d = y_side_c - self.wall_tbslt_dist
            y_side_e = y_side_d - vtab_len
            y_side_f = y_side_e - self.wall_tbslt_dist
            # x_side_1_a and x_side_1_b are constant values set before the outer for loop
            x_side_2_a = horz_os + c_to_c_len
            x_side_2_b = horz_os + c_to_c_len + self.mat_thick
            y_bottom_a = y_side_a
            y_bottom_b = y_bottom_a + self.mat_thick
            x_bottom = x_side_1_a
            x_top = x_side_2_a

            # side 2
            svg_cmds.append(f"M {x_side_2_a} {y_side_a}")
            svg_cmds.append(f"V {y_side_b}")
            svg_cmds.append(f"H {x_side_2_b}")
            svg_cmds.append(f"V {y_side_c}")
            svg_cmds.append(f"H {x_side_2_a}")
            svg_cmds.append(f"V {y_side_d}")
            svg_cmds.append(f"H {x_side_2_b}")
            svg_cmds.append(f"V {y_side_e}")
            svg_cmds.append(f"H {x_side_2_a}")
            svg_cmds.append(f"V {y_side_f}")

            # top
            for intrxn_1, intrxn_2 in rev_pair(bslot.intersections[1:]):
                span_len = Line(intrxn_1.intrxn, intrxn_2.intrxn).length()
                x_top -= span_len
                if intrxn_1.x_type == "cross" and bslot.type == "vert":
                    svg_cmds.append(f"    H {x_top + self.mat_thick}")
                    svg_cmds.append(f"V {y_side_f + cross_slot_len}")
                    svg_cmds.append(f"H {x_top}")
                    svg_cmds.append(f"V {y_side_f}    ")
                else:
                    svg_cmds.append(f"H {x_top}")


            # side 1
            svg_cmds.append(f"H {x_side_1_a}")
            svg_cmds.append(f"V {y_side_e}")
            svg_cmds.append(f"H {x_side_1_b}")
            svg_cmds.append(f"V {y_side_d}")
            svg_cmds.append(f"H {x_side_1_a}")
            svg_cmds.append(f"V {y_side_c}")
            svg_cmds.append(f"H {x_side_1_b}")
            svg_cmds.append(f"V {y_side_b}")
            svg_cmds.append(f"H {x_side_1_a}")
            svg_cmds.append(f"V {y_side_a}")

            # bottom
            for intrxn_1, intrxn_2 in fwd_pair(bslot.intersections):
                tbslt_len, n = self.calc_tbslt_len(intrxn_1.intrxn, intrxn_2.intrxn)
                span_len = Line(intrxn_1.intrxn, intrxn_2.intrxn).length()
                x_bottom_a = x_bottom + self.wall_tbslt_dist
                x_bottom_b = x_bottom_a + tbslt_len

                if intrxn_1.x_type == "cross" and bslot.type == "horz":
                    x_cross_a = x_bottom - self.mat_thick
                    x_cross_b = x_cross_a + self.mat_thick
                    y_cross = y_bottom_a - cross_slot_len
                    svg_cmds.append(f"H {x_cross_a}")
                    svg_cmds.append(f"V {y_cross}")
                    svg_cmds.append(f"H {x_cross_b}")
                    svg_cmds.append(f"V {y_bottom_a}")

                for i in range(n):
                    svg_cmds.append(f"H {x_bottom_a}")
                    svg_cmds.append(f"V {y_bottom_b}")
                    svg_cmds.append(f"H {x_bottom_b}")
                    svg_cmds.append(f"V {y_bottom_a}")
                    x_bottom_a = x_bottom_b + (self.wall_tbslt_dist * 2) + self.mat_thick
                    x_bottom_b = x_bottom_a + tbslt_len
                x_bottom += span_len
            svg_cmds.append("Z")

            # slots for Tee intersections
            x_slot =  x_side_1_a
            for intrxn_1, intrxn_2 in fwd_pair(bslot.intersections[:-1]):
                span_len = Line(intrxn_1.intrxn, intrxn_2.intrxn).length()
                x_slot += span_len
                if intrxn_2.x_type == "tee":
                    # bottom slot
                    svg_cmds.append(f"M {x_slot} {y_side_b}")
                    svg_cmds.append(f"H {x_slot - self.mat_thick}")
                    svg_cmds.append(f"V {y_side_c}")
                    svg_cmds.append(f"H {x_slot}")
                    svg_cmds.append("Z")
                    # top slot
                    svg_cmds.append(f"M {x_slot} {y_side_d}")
                    svg_cmds.append(f"H {x_slot - self.mat_thick}")
                    svg_cmds.append(f"V {y_side_e}")
                    svg_cmds.append(f"H {x_slot}")
                    svg_cmds.append("Z")

            svg_path = " ".join(svg_cmds)
            svg_paths.append(svg_path)

            y_side_a += inc_vos

        inner_walls = "\n".join(svg_paths)
        print(inner_walls)

    def gen_svg_base_slots(self):
        svg_paths = []
        half_mt = self.mat_thick * 0.5
        first_dist = half_mt + self.wall_tbslt_dist
        norm_dist = self.mat_thick + (2 * self.wall_tbslt_dist)
        # print(f"### mat think: {self.mat_thick}, wall slot dist: {self.wall_tbslt_dist}")
        for bslot in self.base_slots:
            for intrxn_1, intrxn_2 in fwd_pair(bslot.intersections):
                tbslt_len, n = self.calc_tbslt_len(intrxn_1.intrxn, intrxn_2.intrxn)
                if bslot.type == "horz":
                    x1 = intrxn_1.intrxn.x + first_dist
                    x2 = x1 + tbslt_len
                    y1 = intrxn_1.intrxn.y - half_mt
                    y2 = y1 + self.mat_thick
                else:
                    x1 = intrxn_1.intrxn.x + half_mt
                    x2 = x1 - self.mat_thick
                    y1 = intrxn_1.intrxn.y + first_dist
                    y2 = y1 + tbslt_len

                for i in range(n):
                    svg_cmds = []
                    svg_cmds.append(f"M {x1} {y1}")
                    if bslot.type == "horz":
                        svg_cmds.append(f"H {x2}")
                        svg_cmds.append(f"V {y2}")
                        svg_cmds.append(f"H {x1}")
                        x1 = x2 + norm_dist
                        x2 = x1 + tbslt_len
                    else:
                        svg_cmds.append(f"V {y2}")
                        svg_cmds.append(f"H {x2}")
                        svg_cmds.append(f"V {y1}")
                        y1 = y2 + norm_dist
                        y2 = y1 + tbslt_len
                    svg_cmds.append(f"Z")
                    svg_path = " ".join(svg_cmds)
                    svg_paths.append(svg_path)

        svg_slots = "\n".join(svg_paths)
        print(svg_slots)

    def gen_svg_base_path(self, i: int = 0):
        # TODO: we probably need different logic for base parts versus side walls parts
        # TODO: add logic to handle different kinds of line types (fingered / smooth)
        # TODO: for base parts do we need logic to determine the type of corner and then calculate the #f/s & be differently?

        # TODO: analysis of consecutive collinear lines with the same type
        #   do we group them together into 1 line

        # print("=" * 100)
        # print(f"\tfinger length:         {self.fngr_len}")
        # print(f"\tspace length:          {self.spc_len}")
        # print(f"\tmaterial thickness:    {self.mat_thick}")
        # print(f"\tminimum beg / end len: {self.min_be_len}")

        # TODO: make this loop over all dim_paths
        norm_dim_path = self.norm_dim_paths[i]
        # print("-" * 100)
        # print(f"\tpath orientation: {norm_dim_path.path_ori}")
        # print("-" * 100)

        curr_dim_pt = norm_dim_path.path_points[0]

        inside_point = curr_dim_pt.get("inside")
        # PATH CMD: MOVE TO 1st point on the path
        # TODO: will we need special logic to determine inside/outside corner & adjust x,y values?
        path_cmds = [f"M {inside_point.x} {inside_point.y}"]

        for ctr, curr_dim_pt in enumerate(norm_dim_path.path_points, 1):
            next_dim_pt = curr_dim_pt.get_next_start()

            # begin processing of the current line(curr_dim_pt, next_dim_point)
            curr_corner_side = curr_dim_pt.corner_side
            next_corner_side = next_dim_pt.corner_side

            # print(
            #     f"*** [{ctr}] processing ***\n"
            #     f"\tCURR: #{curr_dim_pt.id} {curr_dim_pt.get('outside')} {curr_dim_pt.dire()} >>> {curr_corner_side} <<<\n"
            #     f"\tinside: {curr_dim_pt.get('inside')}\n"
            #     f"\tNEXT: #{next_dim_pt.id} {next_dim_pt.get('outside')} {next_dim_pt.dire()} >>> {next_corner_side} <<<\n"
            #     f"\tinside: {next_dim_pt.get('inside')}"
            # )

            o_len = curr_dim_pt.outer_line_length(next_dim_pt)
            nbr_of_fngrs, nbr_of_spcs, be_len = self.calc_min(tot_len=o_len)

            # print(
            #     f"\tlength: {o_len}, number of fingers: {nbr_of_fngrs}, "
            #     f"number of spaces: {nbr_of_spcs}, beg / end length: {be_len}"
            # )

            if curr_dim_pt.dire() == "right":
                dir_coord = curr_dim_pt.get("inside").x
                mult = 1
                dir1 = "H"
                dir2 = "V"
                fp1_coord = curr_dim_pt.get("outside").y
                fp2_coord = curr_dim_pt.get("inside").y
            elif curr_dim_pt.dire() == "left":
                dir_coord = curr_dim_pt.get("inside").x
                mult = -1
                dir1 = "H"
                dir2 = "V"
                fp1_coord = curr_dim_pt.get("outside").y
                fp2_coord = curr_dim_pt.get("inside").y
            elif curr_dim_pt.dire() == "down":
                dir_coord = curr_dim_pt.get("inside").y
                mult = 1
                dir1 = "V"
                dir2 = "H"
                fp1_coord = curr_dim_pt.get("outside").x
                fp2_coord = curr_dim_pt.get("inside").x
            else:
                dir_coord = curr_dim_pt.get("inside").y
                mult = -1
                dir1 = "V"
                dir2 = "H"
                fp1_coord = curr_dim_pt.get("outside").x
                fp2_coord = curr_dim_pt.get("inside").x

            # path_cmds.append("\n\n")
            if curr_corner_side == "inside":
                dir_coord += mult * self.mat_thick
                # path_cmds.append(f"<<< {dir1} {dir_coord} <<<")
                path_cmds.append(f"{dir1} {dir_coord}")

            # create PATH for beginning BEG-END
            # PATH CMD: go-to the dir_cord adjusted for the beg-end length
            dir_coord += mult * be_len
            path_cmds.append(f"{dir1} {dir_coord}")

            # create PATH for N number of FINGER-SPACE pairs
            for _ in range(nbr_of_spcs):
                # PATH CMD: go-to finger point outside
                path_cmds.append(f"{dir2} {fp1_coord}")
                # PATH CMD: go to the dir_cord adjusted for the finger length
                dir_coord += mult * self.fngr_len
                path_cmds.append(f"{dir1} {dir_coord}")
                # PATH CMD: go to finger point inside
                path_cmds.append(f"{dir2} {fp2_coord}")
                # PATH CMD: go to the dir_cord adjusted for the space length
                dir_coord += mult * self.spc_len
                path_cmds.append(f"{dir1} {dir_coord}")

            # create PATH for last FINGER
            # PATH CMD: go-to finger point outside
            path_cmds.append(f"{dir2} {fp1_coord}")
            # PATH CMD: go to the dir_cord adjusted for the finger length
            dir_coord += mult * self.fngr_len
            path_cmds.append(f"{dir1} {dir_coord}")
            # PATH CMD: go to finger point inside
            path_cmds.append(f"{dir2} {fp2_coord}")

            # create PATH for beginning BEG-END
            # PATH CMD: go-to the dir_cord adjusted for the beg-end length
            dir_coord += mult * be_len
            path_cmds.append(f"{dir1} {dir_coord}")

            if next_corner_side == "inside":
                dir_coord += mult * self.mat_thick
                # path_cmds.append(f">>> {dir1} {dir_coord} >>>")
                path_cmds.append(f"{dir1} {dir_coord}")

        path_cmds.append("Z")
        svg_path = " ".join(path_cmds)
        print(svg_path)


    def gen_svg_path_raw(self, i: int = 0, dim: str = "outside"):
        dim_path = self.dim_paths[i]

        # the first point on the path is used for the Move To command
        move_to_dim = dim_path.path_points[0]
        point = move_to_dim.get(dim)
        svg_path_list = [f"M {point.x} {point.y}"]

        # the direction of the first point is used to determine if a horizontal line
        #   or a vertical line should be drawn when consuming the second point
        prev_dire = move_to_dim.direction

        # since we have already processed the first point in the move to command,
        #   start with the 2nd point in the for loop
        for dim_point in dim_path.path_points[1:]:
            point = dim_point.get(dim)
            if prev_dire in ["left", "right"]:
                svg_path_list.append(f"H {point.x}")
            else:
                svg_path_list.append(f"V {point.y}")
            prev_dire = dim_point.direction

        svg_path_list.append("Z")
        return " ".join(svg_path_list)

    def start_path(self, x_index: int, y_index: int, line_type: str = "finger"):
        point = IndexPoint(x_index, y_index, line_type)
        path = IndexPath(point)
        self.index_paths.append(path)

    def extend_path(self, x_index, y_index, line_type: str = "finger"):
        path = self.index_paths[-1]
        point = IndexPoint(x_index, y_index, line_type)
        path.add_point(point)

    def end_path(self):
        path = self.index_paths[-1]
        path.orientation = self.orientation(path)

    def add_wall(self, start: Tuple[int, int], end: Tuple[int, int], wall_type: str = "tab_slot"):
        p1 = IndexPoint(*start)
        p2 = IndexPoint(*end)
        wall = IndexWall(p1, p2, wall_type)
        self.index_walls.append(wall)

    def add_base_wall(self, start: IndexPoint, end: IndexPoint, wall_type: str = "finger"):
        wall = IndexWall(start, end, wall_type)
        self.index_walls.append(wall)


    @classmethod
    def dim(cls, dire1, dire2, ori) -> Tuple[int, int]:
        """
        Determines the Outer & Inner point numbers corresponding to the given inputs.

        :param dire1: the direction of the first line (left, right, up down)
        :param dire2: the direction of the second line
        :param ori:   the orientation of the polygon formed by the lines of the path (clock wise, counter clock wise, collinear)
        :return:      a tuple of (outer dim point number, inner dim point number)

        Note: a point number is an integer value from 1 to 8.
        point numbers correspond to a given x (min, avg, max) and y (min, avg, max) pair
            pt nbr 1:       x_min, y_min
            pt nbr 2:       x_avg, y_min
            pt nbr 3:       x_max, y_max
            pt nbr 4:       x_min, y_avg
            pt nbr 5:       x_max, y_avg
            pt nbr 6:       x_min, y_max
            pt nbr 7:       x_avg, y_max
            pt nbr 8:       x_max, y_max
        """
        return cls.direction_dims[ori][dire1][dire2]

    def create_path_walls(self):
        for norm_index_path in self.norm_index_paths:
            for curr_pt, next_pt in cyclic_n_tuples(norm_index_path.index_points, 2, 0):
                self.add_base_wall(curr_pt, next_pt, "finger")

    def proc_walls(self):
        # print("-" * 100)
        walls_horz = []
        walls_vert = []

        for index_wall in self.index_walls:
            start_avg_pt = self.get_avg_agg_point(index_wall.start_pt)
            end_avg_pt = self.get_avg_agg_point(index_wall.end_pt)
            wall = Wall(start_avg_pt, end_avg_pt, index_wall.wall_type)
            if wall.super_direction == "horz":
                walls_horz.append(wall)
            else:
                walls_vert.append(wall)
            # print(f"{wall} -- {index_wall.start_pt} {index_wall.end_pt}")

        bslots = {}
        for wall_h in walls_horz:
            for wall_v in walls_vert:
                x_type, x_subtype, x_point = wall_h.intersect(wall_v)
                # print(f"horz #{wall_h.id} vert #{wall_v.id} : intersection {x_type}, {x_subtype}, {x_point}")
                if x_type:
                    # TODO: the code below handles only interior walls (i.e., wall type is tab slot)
                    #   we still need to exterior wall (wall type is finger)
                    if wall_h.type == "tab_slot":
                        bslots.setdefault(wall_h.id, BaseSlot('horz')).add(x_point, x_type, x_subtype)
                        # print("added to horz base slot")
                    if wall_v.type == "tab_slot":
                        bslots.setdefault(wall_v.id, BaseSlot('vert')).add(x_point, x_type, x_subtype)
                        # print("added to vert base slot")

        for val in bslots.values():
            self.base_slots.append(val)

        print("-" * 100)

    def calc_tbslt_len(self, oc_pt1: Point, oc_pt2: Point) -> Tuple[float, int]:
        tbslt_len = n = -1
        span_len = Line(oc_pt1, oc_pt2).length()
        tot_spc_len = (2 * self.wall_tbslt_dist) + self.mat_thick
        # print(f">> pt1: {oc_pt1} {oc_pt2} span len {span_len} - 2wts+mt: {tot_spc_len}")
        for n in range(self.max_tbslt_bt_xs, 0, -1):
            tbslt_len = (span_len - (n * tot_spc_len)) / n
            # print(f"   nbr of slots {n} of length {tbslt_len}")
            if tbslt_len >= self.min_tbslt_len:
                # print(f"   meets min slot len of {self.min_tbslt_len}")
                break
        # print(f">> final: {n} slots of {tbslt_len}")
        return tbslt_len, n

def main():
    #
    # create the appropriate base for the desired polygon use case
    #

    # base = Test.base_1()
    base = Test.base_2()

    #
    # add the polygon for the use case
    #

    # Test.super_all_collinear_poly(base)
    # Test.complex_poly(base)
    # Test.simple_ccw(base)
    # Test.simple_cw(base)
    # two_path(base)
    # collinear_rr(base)
    # collinear_ll(base)
    # collinear_uu1(base)
    # collinear_uu2(base)
    # collinear_dd(base)
    # Test.collinear_all(base)
    Test.one_inner(base)

    #
    # do the calculations
    #

    base.calc_dim_paths()
    base.normalize_paths()
    base.create_path_walls()

    base.proc_walls()


    # base.gen_svg_path()
    base.gen_svg_base_path()
    base.gen_svg_base_slots()
    base.gen_svg_inner_walls()

    # svg_path = base.gen_svg_path_raw(0)
    # print(svg_path)
    # svg_path = base.gen_svg_path_raw(0, "inside")
    # print(svg_path)
    # svg_path = base.gen_svg_path_raw(0, "on_center")
    # print(svg_path)
    # svg_path = base.gen_svg_path(1)
    # print(svg_path)
    print("\n\nDONE")

class Test:
    @staticmethod
    def base_1():
        # this base has non-symmetric col & row layout
        #   5 cols x 4 rows
        base = Base(
            mat_thick=3,
            fngr_len=20.0,
            spc_len=10.0,
            min_be_len=10.0,
            col_widths=[50, 50, 50, 50, 100],
            row_heights=[125, 50, 100, 25],
            min_tbslt_len=50,
            max_tbslt_bt_xs=2,
            wall_tbslt_dist=10,
            depth=50,

        )
        base.calc_agg_coords()
        return base

    @staticmethod
    def base_2():
        # this base has a symmetric 10 x 10 layout
        base = Base(
            mat_thick=10,
            fngr_len=30.0,
            spc_len=60.0,
            min_be_len=10.0,
            col_widths=[100] * 10,
            row_heights=[100] * 10,
            min_tbslt_len=75,
            max_tbslt_bt_xs=6,
            wall_tbslt_dist=20,
            depth=150,
        )
        base.calc_agg_coords()
        return base

    @staticmethod
    def one_inner(base):
        # clock wise
        base.start_path(2, 2)
        base.extend_path(8, 2)
        base.extend_path(8, 8)
        base.extend_path(5, 8)
        base.extend_path(5, 5)
        base.extend_path(2, 5)
        base.end_path()

        base.add_wall((2, 3), (8, 3))
        base.add_wall((7, 2), (7, 8))

    @staticmethod
    def collinear_rr(base):
        # clock wise
        base.start_path(0, 0)  # upper left
        base.extend_path(2, 0)  # upper middle ???
        base.extend_path(5, 0)  # upper right
        base.extend_path(5, 4)  # lower right
        base.extend_path(0, 4)  # lower left
        base.end_path()

    @staticmethod
    def super_all_collinear_poly(base):
        base.start_path(3, 1)       # 1     right
        base.extend_path(6, 1)      # 2     right
        base.extend_path(8, 1)      # 3     down
        base.extend_path(8, 3)      # 4     down
        base.extend_path(8, 5)      # 5     down
        base.extend_path(8, 7)      # 6     left
        base.extend_path(6, 7)      # 7     left
        base.extend_path(3, 7)      # 8     left
        base.extend_path(1, 7)      # 9     up
        base.extend_path(1, 5)      # 10    up
        base.extend_path(1, 3)      # 11    up
        base.extend_path(1, 1)      # 12    right
        base.end_path()

    @staticmethod
    def collinear_ll(base):
        # clock wise
        base.start_path(0, 0)  # upper left
        base.extend_path(5, 0)  # upper right
        base.extend_path(5, 4)  # lower right
        base.extend_path(3, 4)  # lower middle ???
        base.extend_path(0, 4)  # lower left
        base.end_path()

    @staticmethod
    def collinear_uu1(base):
        # counter clock wise
        base.start_path(5, 2)
        base.extend_path(5, 0)
        base.extend_path(0, 0)
        base.extend_path(0, 4)
        base.extend_path(5, 4)
        base.end_path()

    @staticmethod
    def collinear_uu2(base):
        # counter clock wise
        base.start_path(0, 0)
        base.extend_path(0, 4)
        base.extend_path(5, 4)
        base.extend_path(5, 2)
        base.extend_path(5, 0)
        base.end_path()

    @staticmethod
    def collinear_dd(base):
        # counter clock wise
        base.start_path(0, 0)
        base.extend_path(0, 2)
        base.extend_path(0, 4)
        base.extend_path(5, 4)
        base.extend_path(5, 0)
        base.end_path()

    @staticmethod
    def collinear_all(base):
        # counter clock wise
        base.start_path(0, 0)
        base.extend_path(0, 2)  #
        base.extend_path(0, 4)
        base.extend_path(2, 4)  #
        base.extend_path(5, 4)
        base.extend_path(5, 2)  #
        base.extend_path(5, 0)
        base.extend_path(3, 0)  #
        base.end_path()

    @staticmethod
    def simple_ccw(base):
        # columns:          5   [0 to 4]
        # rows:             4   [0 to 3]
        # vertical walls:   6   [0 to 5]
        # horizontal walls: 5   [0 to 4]

        # counter clock wise
        base.start_path(0, 4)  # lower left
        base.extend_path(5, 4)  # lower right
        base.extend_path(5, 0)  # upper right
        base.extend_path(0, 0)  # upper left
        base.end_path()

    @staticmethod
    def simple_cw(base):
        # clock wise
        base.start_path(0, 4)  # lower left
        base.extend_path(0, 0)  # upper left
        base.extend_path(5, 0)  # upper right
        base.extend_path(5, 4)  # lower right
        base.end_path()

    @staticmethod
    def two_path(base):
        # clock wise
        base.start_path(0, 4)  # upper left
        base.extend_path(0, 0)  # lower left
        base.extend_path(5, 0)  # upper right
        base.extend_path(5, 4)  # lower right
        base.end_path()

        base.start_path(2, 1)
        base.extend_path(4, 1)
        base.extend_path(4, 3)
        base.extend_path(2, 3)
        # base.end_path()

    @staticmethod
    def complex_poly(base):
        base.start_path(0, 10)
        base.extend_path(1, 10)
        base.extend_path(1, 8)
        base.extend_path(3, 8)
        base.extend_path(3, 9)
        base.extend_path(2, 9)
        base.extend_path(2, 10)
        base.extend_path(10, 10)
        base.extend_path(10, 7)
        base.extend_path(8, 7)
        base.extend_path(8, 4)
        base.extend_path(10, 4)
        base.extend_path(10, 2)
        base.extend_path(8, 2)
        base.extend_path(8, 0)
        base.extend_path(3, 0)
        base.extend_path(3, 1)
        base.extend_path(4, 1)
        base.extend_path(4, 3)
        base.extend_path(2, 3)
        base.extend_path(2, 0)
        base.extend_path(0, 0)
        base.extend_path(0, 5)
        base.extend_path(5, 5)
        base.extend_path(5, 3)
        base.extend_path(6, 3)
        base.extend_path(6, 8)
        base.extend_path(7, 8)
        base.extend_path(7, 9)
        base.extend_path(4, 9)
        base.extend_path(4, 8)
        base.extend_path(5, 8)
        base.extend_path(5, 6)
        base.extend_path(0, 6)
        base.end_path()


if __name__ == "__main__":
    main()
