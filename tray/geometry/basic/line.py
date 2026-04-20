from __future__ import annotations

import functools
from collections.abc import Iterator, Sequence
from types import NotImplementedType
from typing import Any, Generic, SupportsFloat, TypeVar
from tray.geometry.basic.point import Point
from tray.geometry.intersection import Intersection
from tray.geometry.types.geometric import LineOrientation, PointLine
from tray.geometry.types.tray import IntrxnType

T = TypeVar("T", bound=SupportsFloat)
L = TypeVar("L", bound="Line")


class Line(Generic[T]):
    def __init__(self, p1: Point[T], p2: Point[T]) -> None:
        self.p1 = p1
        self.p2 = p2
        self.orientation = LineOrientation.NONE
        self._set_orientation()

    @staticmethod
    def of_orientation(lines: Sequence[L], orientation: LineOrientation) -> Iterator[L]:
        return filter(lambda line: line.orientation == orientation, lines)

    def _set_orientation(self) -> None:
        if self.p1.x == self.p2.x:
            self.orientation = LineOrientation.VERT
        elif self.p1.y == self.p2.y:
            self.orientation = LineOrientation.HORZ
        else:
            raise ValueError("cannot set line orientation for points that are not collinear")

    @staticmethod
    def _coerce(other: Any) -> Line[T] | None:
        if isinstance(other, Line):
            return other

        if isinstance(other, (tuple, list)) and len(other) == 2:
            p1 = Point._coerce(other[0])
            p2 = Point._coerce(other[1])
            if p1 and p2:
                try:
                    return Line(p1, p2)
                except ValueError:
                    return None
        return None

    def _cmp_key(self) -> tuple[Point[T], Point[T]]:
        return self.normalize

    def __eq__(self, other: object) -> bool | NotImplementedType:
        coerced = self._coerce(other)
        if coerced is None:
            return NotImplemented
        return self._cmp_key() == coerced._cmp_key()

    def __lt__(self, other: object) -> bool | NotImplementedType:
        coerced = self._coerce(other)
        if coerced is None:
            return NotImplemented
        return self._cmp_key() < coerced._cmp_key()

    def __le__(self, other: object) -> bool | NotImplementedType:
        coerced = self._coerce(other)
        if coerced is None:
            return NotImplemented
        return self._cmp_key() <= coerced._cmp_key()

    def __gt__(self, other: object) -> bool | NotImplementedType:
        coerced = self._coerce(other)
        if coerced is None:
            return NotImplemented
        return self._cmp_key() > coerced._cmp_key()

    def __ge__(self, other: object) -> bool | NotImplementedType:
        coerced = self._coerce(other)
        if coerced is None:
            return NotImplemented
        return self._cmp_key() >= coerced._cmp_key()

    @property
    def is_vertical(self) -> bool:
        return self.orientation == LineOrientation.VERT

    @property
    def is_horizontal(self) -> bool:
        return self.orientation == LineOrientation.HORZ

    @property
    def start_end(self) -> tuple[T, T]:
        """
        Retrieve the start and end coordinates of the line segment based on its orientation.

        This property calculates and returns the endpoints of a line segment after normalization.
        If the line segment is horizontal, it returns the x-coordinates of the start and end points.
        If the line segment is vertical, it returns the y-coordinates of the start and end points.

        :return: The start and end coordinates as a tuple
        :rtype: tuple[T, T]
        """
        p1, p2 = self.normalize
        return (p1.x, p2.x) if self.is_horizontal else (p1.y, p2.y)

    def check_point_on_line(self, pt: Point[T]) -> PointLine:
        """
        Determines the relative position of a given point on a line segment.

        The method evaluates if a point lies outside the segment, at one of its ends,
        or between its ends. The computation depends on whether the line is
        horizontal or vertical and utilizes the coordinates of the point and
        the segment's boundary.

        :param pt: The point to evaluate.
        :type pt: Point[T]
        :return: A value from the PointLine enumeration representing the
            position of the point (OUTSIDE, P1, P2, or BETWEEN) with respect
            to the segment.
        :rtype: PointLine
        """
        i = pt.x if self.is_horizontal else pt.y
        # start_end normalizes the line's points, so we don't do it here
        i1, i2 = self.start_end
        if i < i1 or i > i2:
            return PointLine.OUTSIDE
        elif i == i1:
            return PointLine.P1
        elif i == i2:
            return PointLine.P2
        return PointLine.BETWEEN

    def intersection_point(self, other: Line[int]) -> Point[int]:
        """
        Calculates the intersection point between two lines.

        This method determines the intersection point of the current line instance
        with another line passed as a parameter. It assumes that the lines are
        horizontal and vertical respectively for simplicity.

        Notes:
        * self is the horizontal line and other is the vertical line

        :param other: The other line object with which the intersection point
                      is to be calculated.
        :type other: Line[T]
        :return: The intersection point as a Point object.
        :rtype: Point[T]
        """
        horz_line, vert_line = self, other
        return Point(vert_line.p1.x, horz_line.p1.y)

    def intersect(self, other) -> Intersection | None:
        """
        Determines the type of intersection between two geometric lines.

        The method identifies the intersection point and classifies the intersection type based on relative
        positions of the intersection point and the lines' endpoints. The intersection point may:
        * be OUTSIDE the line
        * be on the LEFT (P1) end point of the line
        * be on the RIGHT (P2) end point of the line
        * be in between the line's endpoints P1 and P2

        Notes:
        * self is the horizontal line and other is the vertical line

        :param other: The second line to compute the intersection with.
        :type other: Line
        :return: A tuple where the first element is the intersection point (or None if there
                 is no intersection) and the second element is the type of intersection.
        :rtype: tuple[Point[T] | None, IntrxnType]
        """
        intrxn_pt = self.intersection_point(other)
        chk_horz = self.check_point_on_line(intrxn_pt)
        chk_vert = other.check_point_on_line(intrxn_pt)

        # if the point is OUTSIDE both lines then it there is not an intersection
        if chk_horz == PointLine.OUTSIDE or chk_vert == PointLine.OUTSIDE:
            return None

        # if the point is at the LEFT (P1) of the horizontal line
        elif chk_horz == PointLine.P1:
            # if the point is at the TOP (P1) of the vertical line
            if chk_vert == PointLine.P1:
                return Intersection(intrxn_pt, IntrxnType.CORNER_LT)
            # if the point is at the BOTTOM (P2) of the vertical line
            elif chk_vert == PointLine.P2:
                return Intersection(intrxn_pt, IntrxnType.CORNER_LB)
            # else the point is BETWEEN the vertical line's P1 & P2
            else:
                return Intersection(intrxn_pt, IntrxnType.TEE_L)

        # if the point is on the RIGHT (P2) of the horizontal line
        elif chk_horz == PointLine.P2:
            # if the point is at the TOP (P1) of the vertical line
            if chk_vert == PointLine.P1:
                return Intersection(intrxn_pt, IntrxnType.CORNER_RT)
            # if the point is at the BOTTOM (P2) of the vertical line
            elif chk_vert == PointLine.P2:
                return Intersection(intrxn_pt, IntrxnType.CORNER_RB)
            # else the point is BETWEEN the vertical line's P1 & P2
            else:
                return Intersection(intrxn_pt, IntrxnType.TEE_R)

        # else the point is BETWEEN the horizontal line's P1 & P2
        else:
            # if the point is at the TOP (P1) of the vertical line
            if chk_vert == PointLine.P1:
                return Intersection(intrxn_pt, IntrxnType.TEE_T)
            # if the point is at the BOTTOM (P2) of the vertical line
            elif chk_vert == PointLine.P2:
                return Intersection(intrxn_pt, IntrxnType.TEE_B)
            # else the point is BETWEEN the vertical line's P1 & P2
            else:
                return Intersection(intrxn_pt, IntrxnType.CROSS)

    def point_from_line(self, value: T) -> Point[T]:
        """
        Generate a point on the line using the specified value. If the line is horizontal,
        the point's x-coordinate will be set to the provided value. Otherwise, the line is
        vertical, and the y-coordinate will be set to the given value.

        :param value: The value to replace either the x-coordinate (if the line is vertical)
                      or the y-coordinate (if the line is horizontal) in order to generate
                      the point.
        :type value: T
        :return: A new point on the line based on the provided value.
        :rtype: Point[T]
        """
        return Point(value, self.p1.y) if self.is_horizontal else Point(self.p1.x, value)

    def wall_inside_path(self, other: Line[T]) -> list[Point[T]]:
        # return a list of points from the wall-line that are inside the path-line
        # this list could be empty, have just one point, or have two points
        # additionally, the wall-line points must be strictly inside the path-line
        # if the points are only touching each other, they are not inside
        # self is the wall-line and other is the path-line
        # start_end will take care of the normalization of the points and checking the orientation
        # the 2 lines must be the collinear (and the same orientation)

        if not self.is_collinear(other):
            raise ValueError("cannot determine endpoints of wall line that are inside path line if lines are not collinear")

        w1, w2 = self.start_end
        p1, p2 = other.start_end

        return [self.point_from_line(w) for w in (w1, w2) if p1 < w < p2]

    #
    # moved to Point class to make usage more intuitive
    #
    # def is_between(self, point: Point[T]) -> bool:
    #     line_pt_1, line_pt_2 = self.normalize
    #     if self.is_horizontal:
    #         return line_pt_1.x < point.x < line_pt_2.x
    #     return line_pt_1.y < point.y < line_pt_2.y
    #

    @staticmethod
    def _intervals_overlap(line_1: Line[T], line_2: Line[T]) -> bool:
        """
        Determines if two line intervals overlap based on their alignment (vertical or
        horizontal). This method is designed to operate based on the principle that
        overlapping intervals must share a common range in one dimensional space
        (either in x-axis or y-axis depending on their alignment).

        NOTE: sharing a single point is not considered overlapping.

        :param line_1: The first line segment being compared.
        :type line_1: Line[T]
        :param line_2: The second line segment being compared.
        :type line_2: Line[T]
        :return: True if the two lines overlap in their respective alignment,
            otherwise False.
        :rtype: bool
        """
        if line_1.is_vertical:
            return line_1.p2.y > line_2.p1.y and line_2.p2.y > line_1.p1.y
        return line_1.p2.x > line_2.p1.x and line_2.p2.x > line_1.p1.x

    def is_overlapping(self, other: Line[T]) -> bool:
        """
        Checks if two lines overlap in their respective alignment.

        The method determines if two lines are overlapping based on their
        orientation and collinearity. If either the orientations differ or
        they are not collinear, the lines are considered non-overlapping.
        Otherwise, it evaluates whether the intervals of the two normalized
        lines overlap.

        :param other: The other line to compare with.
        :type other: Line[T]
        :return: True if the lines overlap, otherwise False.
        :rtype: bool
        """
        if self.orientation != other.orientation or not self.is_collinear(other):
            return False
        line_1, line_2 = Line(*self.normalize), Line(*other.normalize)
        return self._intervals_overlap(line_1, line_2)

    def is_collinear(self, other: Line[T]) -> bool:
        # vertical use case first
        if self.is_vertical:
            # both lines must be vertical
            if other.is_vertical:
                # if x coords are equal then lines are collinear
                return self.p1.x == other.p1.x
            raise ValueError("cannot compare vertical lines with non-vertical lines")
        # horizontal use case second
        # both lines must be horizontal
        if other.is_vertical:
            raise ValueError("cannot compare non-vertical lines with vertical lines")
        # if y coords are equal then lines are collinear
        return self.p1.y == other.p1.y

    @functools.cached_property
    def normalize(self) -> tuple[Point[T], Point[T]]:
        if self.p1 > self.p2:
            return self.p2, self.p1
        return self.p1, self.p2

    def __repr__(self) -> str:
        return f"Line(p1={self.p1!r}, p2={self.p2!r}, type={self.orientation!r})"

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}, {self.orientation}]"
