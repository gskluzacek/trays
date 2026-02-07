from __future__ import annotations

from typing import Optional


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Wall:
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

    def __init__(self, pt_1: Point, pt_2: Point):
        self.id = ...
        self.dim_pt = ...
        self.type = ...
        self.super_direction = ...
        self.pt_1 = pt_1
        self.pt_2 = pt_2
        self.inter_walL_list = []

    def intersect(self, other: Wall) -> tuple[Optional[str], Optional[str], Optional[Point]]:
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

        def _outside(start: float, end: float, value: float) -> bool:
            return value < start or value > end

        def _between(start: float, end: float, value: float) -> bool:
            return value > start and value < end

        def _start_end(start: float, end: float, value: float) -> tuple[bool, bool]:
            return value == start, value == end

        # Fast reject: they can only intersect if projected ranges overlap (inclusive).
        if _outside(start_horz, end_horz, val_vert) or _outside(start_vert, end_vert, val_horz):
            return None, None, None

        inside_horz = _between(start_horz, end_horz, val_vert)
        inside_vert = _between(start_vert, end_vert, val_horz)

        # Cross: strictly inside both segments.
        if inside_horz and inside_vert:
            return "cross", None, ipt

        # Corner: intersection equals an endpoint of both segments.
        at_left_end, at_right_end = _start_end(start_horz, end_horz, val_vert)
        at_top_end, at_bottom_end = _start_end(start_vert, end_vert, val_horz)

        corner_map = {
            (True, False, True, False): "upper-left",
            (True, False, False, True): "lower-left",
            (False, True, True, False): "upper-right",
            (False, True, False, True): "lower-right",
        }
        corner_key = (at_left_end, at_right_end, at_top_end, at_bottom_end)
        if corner_key in corner_map:
            return "corner", corner_map[corner_key], ipt

        # Tee: on an endpoint of exactly one segment and strictly inside the other.
        if inside_horz and (at_top_end or at_bottom_end):
            return "tee", ("top" if at_top_end else "bottom"), ipt

        if inside_vert and (at_left_end or at_right_end):
            return "tee", ("left" if at_left_end else "right"), ipt

        return None, None, None
