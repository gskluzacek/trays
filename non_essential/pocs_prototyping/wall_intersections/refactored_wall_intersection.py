from __future__ import annotations

from enum import Enum
from functools import total_ordering
from typing import SupportsFloat, TypeAlias, TypeVar, Generic, overload, cast

T = TypeVar("T", bound=SupportsFloat)
PointLike: TypeAlias = "Point[T] | tuple[T, T]"


class PathOrientation(Enum):
    CW = "clockwise"
    CCW = "counter_clockwise"
    COL = "collinear"
    NONE = "none"


@total_ordering
class Point(Generic[T]):
    def __init__(self, x: T, y: T) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    @staticmethod
    def _validate_pair_xy(ax: T, ay: T, bx: T, by: T) -> None:
        # Allowed: identical OR share x OR share y
        # Disallowed: both coordinates differ
        if ax != bx and ay != by:
            raise ValueError("Unsupported comparison: points must be identical or share x or share y.")

    @overload
    @staticmethod
    def _coerce_xy(other: Point[T]) -> tuple[T, T]: ...

    @overload
    @staticmethod
    def _coerce_xy(other: tuple[T, T]) -> tuple[T, T]: ...

    @overload
    @staticmethod
    def _coerce_xy(other: object) -> tuple[T, T] | None: ...

    @staticmethod
    def _coerce_xy(other: object) -> tuple[T, T] | None:
        if isinstance(other, Point):
            return cast(tuple[T, T], (other.x, other.y))
        if isinstance(other, tuple) and len(other) == 2:
            x, y = other
            return cast(tuple[T, T], (x, y))
        return None

    def __eq__(self, other: object) -> bool:
        other_xy = self._coerce_xy(other)
        if other_xy is None:
            return NotImplemented
        ox, oy = other_xy
        self._validate_pair_xy(self.x, self.y, ox, oy)
        return (self.x, self.y) == (ox, oy)

    def __lt__(self, other: object) -> bool:
        other_xy = self._coerce_xy(other)
        if other_xy is None:
            return NotImplemented
        ox, oy = other_xy
        self._validate_pair_xy(self.x, self.y, ox, oy)
        return (self.x, self.y) < (ox, oy)

    @property
    def coords(self) -> tuple[T, T]:
        return self.x, self.y

    def orientation(self, p2: Point[T], p3: Point[T]) -> PathOrientation:
        p1 = self
        x1, y1 = float(p1.x), float(p1.y)
        x2, y2 = float(p2.x), float(p2.y)
        x3, y3 = float(p3.x), float(p3.y)

        val = ((y2 - y1) * (x3 - x2)) - ((x2 - x1) * (y3 - y2))

        # note we are operating in quadrant 4, so we are swapping the values that correspond to cw & ccw
        if val > 0:
            return PathOrientation.CCW
        elif val < 0:
            return PathOrientation.CW
        else:
            return PathOrientation.COL

    def is_orthogonal(self, other: Point[T]) -> bool:
        return (self.y == other.y or self.x == other.x) and self != other


class IntersectionType(Enum):
    CROSS = "cross"
    CORNER = "corner"
    TEE = "tee"
    NONE = "none"


class IntersectionSubType(Enum):
    UPPER_LEFT = "upper-left"
    LOWER_LEFT = "lower-left"
    UPPER_RIGHT = "upper-right"
    LOWER_RIGHT = "lower-right"
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    NONE = "none"
    NA = "N/A"


class Wall(Generic[T]):
    """
    if...
    1. the origin is in the upper left of the screen, i.e., x grows larger as you move to the right and y grows larger as you move down
    2. we never have NaN floats
    3. start < end always

    is `Wall.intersect` written correctly?


    Yes — **given your three assumptions**, `Wall.intersect()` is logically consistent for **axis-aligned** walls where:

    - `self` is **horizontal** with `pt_1.y == pt_2.y` and `pt_1.x < pt_2.x`
    - `other` is **vertical** with `pt_1.x == pt_2.x` and `pt_1.y < pt_2.y`
    - screen coords are **x right, y down**

    ### Why it’s correct under those assumptions

    - **Fast reject**:
    ```python
    value < start or value > end
    ```

      correctly rejects when the vertical wall’s x is outside the horizontal segment’s x-range, or the horizontal wall’s y is outside the vertical segment’s y-range. This is the standard inclusive range overlap test for axis-aligned segments.

    - **Cross vs endpoint-touch**:
      - `"cross"` is returned only when the intersection lies **strictly inside** both segments (`start < value < end`). Good.
      - Endpoint touches are excluded from `"cross"` and handled later as `"corner"` or `"tee"`. Good.

    - **Corner labeling matches “y grows downward”**:
      - Since `start_vert = vert.pt_1.y` and `start_vert < end_vert`, `start_vert` is the **top** endpoint (smaller y), and `end_vert` is the **bottom** endpoint (larger y).
      - Your mapping:
        - `(left end, top end)` → `"upper-left"`
        - `(left end, bottom end)` → `"lower-left"`
        - etc.

      That’s consistent with screen coordinates.

    - **Tee cases are correctly partitioned**:
      - If the intersection is strictly inside the horizontal segment and at the vertical’s endpoint → `"tee"` with `"top"`/`"bottom"`.
      - If strictly inside the vertical and at the horizontal’s endpoint → `"tee"` with `"left"`/`"right"`.
      - If it’s neither cross, corner, nor tee, it returns no intersection.

    ### The only “gotchas” (outside your assumptions)
    If any of these can happen, the method can misclassify:

    1. **Non-axis-aligned walls** (not perfectly horizontal/vertical).
    2. **Endpoints not ordered** (if `pt_1` isn’t guaranteed to be the “start”, i.e., `pt_1.x < pt_2.x` for horizontal and `pt_1.y < pt_2.y` for vertical).
    3. **Float equality precision**: it uses `==` to detect endpoint hits. Even without `NaN`, tiny rounding differences can make a true endpoint-touch fail the `==` checks.

    But **with your stated constraints**, the logic and the corner/tee labeling are correct.
    """

    corner_map: dict[tuple[bool, bool, bool, bool], IntersectionSubType] = {
        (True, False, True, False): IntersectionSubType.UPPER_LEFT,
        (True, False, False, True): IntersectionSubType.LOWER_LEFT,
        (False, True, True, False): IntersectionSubType.UPPER_RIGHT,
        (False, True, False, True): IntersectionSubType.LOWER_RIGHT,
    }

    def __init__(self, pt_1: Point[T], pt_2: Point[T]):
        self.id = ...
        self.dim_pt = ...
        self.type = ...
        self.super_direction = ...
        self.pt_1 = pt_1
        self.pt_2 = pt_2
        self.inter_walL_list = []

    def intersect(
        self, other: Wall[T]
    ) -> tuple[
        IntersectionType | None,
        IntersectionSubType | None,
        Point[T] | None,
    ]:
        """
        Determine the intersection type if a given vertical wall intersects with a given horizontal wall.

        self is the horizontal wall.
        other is the vertical wall.
        """
        horz = self
        val_horz = horz.pt_1.y
        start_horz = horz.pt_1.x
        end_horz = horz.pt_2.x

        vert = other
        val_vert = vert.pt_1.x
        start_vert = vert.pt_1.y
        end_vert = vert.pt_2.y

        ipt = Point(val_vert, val_horz)

        def _outside(start: T, end: T, value: T) -> bool:
            return value < start or value > end

        def _between(start: T, end: T, value: T) -> bool:
            return value > start and value < end  # noqa

        def _start_end(start: T, end: T, value: T) -> tuple[bool, bool]:
            return value == start, value == end

        # Fast reject: they can only intersect if projected ranges overlap (inclusive).
        # fmt: off
        if (
                _outside(start_horz, end_horz, val_vert) or
                _outside(start_vert, end_vert, val_horz)
        ):
            return None, None, None
        # fmt: on

        inside_horz = _between(start_horz, end_horz, val_vert)
        inside_vert = _between(start_vert, end_vert, val_horz)

        # Cross: strictly inside both segments.
        if inside_horz and inside_vert:
            return IntersectionType.CROSS, IntersectionSubType.NA, ipt

        # Corner: intersection equals an endpoint of both segments.
        at_left_end, at_right_end = _start_end(start_horz, end_horz, val_vert)
        at_top_end, at_bottom_end = _start_end(start_vert, end_vert, val_horz)

        corner_key: tuple[bool, bool, bool, bool] = (
            at_left_end,
            at_right_end,
            at_top_end,
            at_bottom_end,
        )
        if corner_key in self.corner_map:
            return (
                IntersectionType.CORNER,
                self.corner_map[corner_key],
                ipt,
            )

        # Tee: on an endpoint of exactly one segment and strictly inside the other.
        if inside_horz and (at_top_end or at_bottom_end):
            return (
                IntersectionType.TEE,
                (IntersectionSubType.TOP if at_top_end else IntersectionSubType.BOTTOM),
                ipt,
            )

        if inside_vert and (at_left_end or at_right_end):
            return (
                IntersectionType.TEE,
                (IntersectionSubType.LEFT if at_left_end else IntersectionSubType.RIGHT),
                ipt,
            )

        return None, None, None
