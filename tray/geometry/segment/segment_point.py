from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tray.geometry.basic.point import Point


if TYPE_CHECKING:
    from tray.geometry.final_base.final_path_line import FinalPathLine


@dataclass(frozen=True, slots=True)
class SegmentPoint(Point[int]):
    """
    A point on a given finalized path line; used when splitting a wall into segments.

    `SegmentPoint` extends `Point[int]` by adding a reference to the `FinalPathLine`
    that produced the point. This makes it possible to access the final path line
    from which the segment boundary point came from while being able to use the Point
    class's normal coordinate comparisons and geometry operations.
    """

    # The finalized path line associated with this segment point
    line: FinalPathLine

    def __post_init__(self) -> None:
        """
        Validate the segment point after dataclass initialization.

        Reuses `Point` validation to ensure both coordinates are non-negative.
        """
        Point.__post_init__(self)

    @property
    def to_point(self) -> Point:
        """
        Return this segment point as a plain `Point[int]`.

        The returned point contains the same `x` and `y` coordinates, but does
        not include the associated `line` reference.

        :return: A plain point with this segment point's coordinates.
        :rtype: Point[int]
        """
        return Point(self.x, self.y)
