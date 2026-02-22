from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tray.geometry.basic.point import Point


if TYPE_CHECKING:
    from tray.geometry.final_base.final_path_line import FinalPathLine


@dataclass(frozen=True, slots=True)
class SegmentPoint(Point[int]):
    line: FinalPathLine

    def __post_init__(self) -> None:
        # super().__post_init__()  # keep Point's non-negative validation
        Point.__post_init__(self)

    @property
    def to_point(self) -> Point:
        return Point(self.x, self.y)
