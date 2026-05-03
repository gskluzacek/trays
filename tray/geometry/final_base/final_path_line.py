from __future__ import annotations

from tray.geometry.types.tray import JointType
from tray.geometry.basic.line import Line, Point
from tray.geometry.segment.segment_point import SegmentPoint


class FinalPathLine(Line[int]):
    def __init__(self, p1: Point[int], p2: Point[int]):
        super().__init__(p1, p2)
        # TODO: need code to set joint_type
        self.joint_type = JointType.NONE

    def __repr__(self) -> str:
        return f"FinalPathLine(p1={self.p1!r}, p2={self.p2!r}, orientation={self.orientation!r}, joint={self.joint_type!r})"

    def __str__(self) -> str:
        return f"{self.p1}, {self.p2}, {self.orientation}, {self.joint_type}"

    @property
    def points_from_line(self) -> tuple[SegmentPoint, SegmentPoint]:
        """
        Returns the final path line's two corresponding segment points.

        The points are derived from the normalized segment points associated with the
        final path line. The normalization ensures the points maintain consistent
        representation regardless of the original sequence of input endpoints.

        The SegmentPoint objects returned not only include the stareting and ending points of the
        original final path line, but also include a reference to the FinalPathLine they belong to,

        :return: A tuple containing two `SegmentPoint` objects representing the
                 segment points of the line.
        :rtype: tuple[SegmentPoint, SegmentPoint]
        """
        sl_pt_1, sl_pt_2 = self.normalize
        return SegmentPoint(sl_pt_1.x, sl_pt_1.y, self), SegmentPoint(sl_pt_2.x, sl_pt_2.y, self)
