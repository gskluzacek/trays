from __future__ import annotations

import functools
from enum import Enum
from collections.abc import Iterator, Sequence
from typing import Generic, SupportsFloat, TypeVar
from tray.geometry.point import Point

T = TypeVar("T", bound=SupportsFloat)
L = TypeVar("L", bound="Line")


class LineOrientation(Enum):
    VERT = "vertical"
    HORZ = "horizontal"
    NONE = "none"


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

    def is_between(self, point: Point[T]) -> bool:
        line_pt_1, line_pt_2 = self.normalize
        if self.is_horizontal:
            return line_pt_1.x < point.x < line_pt_2.x
        return line_pt_1.y < point.y < line_pt_2.y

    # TODO: after commiting these changes, remove the *_1 versions
    @staticmethod
    def _intervals_overlap_1(lo1: T, hi1: T, lo2: T, hi2: T) -> bool:
        """
        Determines whether two intervals overlap. This static method performs comparison
        to check if one interval lies completely outside the other or if they share
        any overlapping range.

        :param lo1: The lower bound of the first interval
        :type lo1: T
        :param hi1: The upper bound of the first interval
        :type hi1: T
        :param lo2: The lower bound of the second interval
        :type lo2: T
        :param hi2: The upper bound of the second interval
        :type hi2: T
        :return: True if the intervals overlap, otherwise False
        :rtype: bool
        """
        # return not (hi1 <= lo2 or hi2 <= lo1)
        return hi1 > lo2 and hi2 > lo1

    def is_overlapping_1(self, other: Line[T]) -> bool:
        """
        Determines whether the current line overlaps with another line. Overlapping is
        checked only for lines with the same orientation and that are collinear. If the
        lines are vertical, the overlap is checked based on their y-coordinates;
        otherwise, it is checked based on their x-coordinates.

        NOTE: if only the end point touch then the lines are NOT overlapping

        :param other: The line to check for overlap with the current line.
        :type other: Line[T]
        :return: True if the lines overlap, otherwise False.
        :rtype: bool
        """
        if self.orientation != other.orientation or not self.is_collinear(other):
            return False
        line_1_pt_1, line_1_pt_2 = self.normalize
        line_2_pt_1, line_2_pt_2 = other.normalize
        if self.is_vertical:
            return self._intervals_overlap_1(line_1_pt_1.y, line_1_pt_2.y, line_2_pt_1.y, line_2_pt_2.y)
        # horizontal
        return self._intervals_overlap_1(line_1_pt_1.x, line_1_pt_2.x, line_2_pt_1.x, line_2_pt_2.x)

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
