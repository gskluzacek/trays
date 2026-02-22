from __future__ import annotations

from typing import Protocol, SupportsFloat, TypeVar

from cyclic_n_tuples import fwd_n_tuple

from tray.geometry.basic.point import Point
from tray.geometry.types.geometric import PathOrientation

T = TypeVar("T", bound=SupportsFloat)


class HasPoints(Protocol[T]):
    points: list[Point[T]]


class PathOrientationMixin:
    """
    Mixin that adds:
      - self.orientation: PathOrientation
      - set_orientation(): determines CW/CCW from self.points

    Requirements:
      - The consuming class must define: self.points: list[Point[T]]
      - The consuming class should be cooperative with super().__init__.
    """

    def __init__(
        self,
        *args,
        orientation: PathOrientation = PathOrientation.NONE,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.orientation: PathOrientation = orientation

    def set_orientation(self: HasPoints[T]) -> None:
        if len(self.points) < 3:
            raise ValueError(
                f"could not determine the path's orientation (clockwise or counter clockwise). please check that you have 3 or more points in your path. Path len: {len(self.points)}"
            )

        orientation = PathOrientation.NONE
        # Note: fwd_n_tuple will yield nothing if len(self.points) < 3,
        # but we already checked that above.
        for pt_1, pt_2, pt_3 in fwd_n_tuple(self.points):
            orientation = pt_1.orientation(pt_2, pt_3)
            if orientation != PathOrientation.COL:
                break

        if orientation == PathOrientation.COL:
            raise ValueError(
                "could not determine the path's orientation (clockwise or counter clockwise). please check that all points in the path are not collinear"
            )

        # This part should be logically unreachable given the checks above,
        # but kept as a safety measure.
        if orientation == PathOrientation.NONE:  # pragma: no cover
            raise ValueError("exhausted path without determining the orientation")

        self.orientation = orientation
