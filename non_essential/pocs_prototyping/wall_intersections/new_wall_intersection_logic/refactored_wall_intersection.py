"""
### What this code is doing (at a high level)

`Wall[T]` represents a line segment between two points (`pt_1`, `pt_2`). The method:

```python
def intersect(self, other: Wall[T]) -> tuple[IntrxnType | None, IntrxnSubtype | None, Point[T] | None]:
```


classifies the intersection between two **axis-aligned** segments under a very specific contract:

- `self` is the **horizontal** segment
- `other` is the **vertical** segment
- endpoints are ordered (`start < end`)
- screen coordinates are “x right, y down”

It returns a triple:

1. **Intersection type**: `CROSS`, `CORNER`, `TEE`, or `None`
2. **Subtype**: which corner (`UPPER_LEFT`, …) or which tee direction (`TOP`, `LEFT`, …), or `NA`/`None`
3. **Intersection point** (a `Point[T]`) or `None`

(From your attachments: `IntrxnType` and `IntrxnSubtype` are `Enum`s of those labels.)

---

### Step-by-step through `intersect`

```python
ih = IntersectHelper(self, other)
ipt = Point(ih.val_vert, ih.val_horz)
```


- `IntersectHelper` is a helper that precomputes the key geometry facts:
  - `ih.val_vert`: the vertical wall’s **x** coordinate (constant for a vertical line)
  - `ih.val_horz`: the horizontal wall’s **y** coordinate (constant for a horizontal line)
  - boolean flags like `ih.outside`, `ih.inside`, `ih.corner`, `ih.tee`
  - plus labels like `ih.corner_type`, `ih.tee_type`

- The potential intersection point of an axis-aligned horizontal and vertical segment is always:
  - **x** = vertical line’s x (`val_vert`)
  - **y** = horizontal line’s y (`val_horz`)
  so `ipt` is the “candidate” intersection point.

---

#### 1) Fast reject: no overlap in projection ranges

```python
if ih.outside:
    return None, None, None
```


This corresponds to: “Does the vertical segment’s `x` fall within the horizontal segment’s `[x1, x2]` range **and** does the horizontal segment’s `y` fall within the vertical segment’s `[y1, y2]` range?”

If either is outside, the segments can’t intersect at all.

---

#### 2) Proper crossing: intersection is strictly inside both segments

```python
if ih.inside:
    return IntrxnType.CROSS, IntrxnSubtype.NA, ipt
```


“Inside” usually means strict inequalities (`start < value < end`) for **both** segments. That excludes endpoint-touching.

So this is the classic “plus sign” intersection: the vertical cuts through the horizontal away from endpoints.

---

#### 3) Corner: they meet exactly at both endpoints

```python
if ih.corner:
    return IntrxnType.CORNER, ih.corner_type, ipt
```


This case means the candidate point `ipt` is simultaneously:
- an endpoint of the horizontal segment **and**
- an endpoint of the vertical segment

`ih.corner_type` then picks which corner label applies (`UPPER_LEFT`, `LOWER_RIGHT`, etc.), using the “y grows downward” convention.

---

#### 4) Tee: endpoint-touch on exactly one segment

```python
if ih.tee:
    return IntrxnType.TEE, ih.tee_type, ipt
```


“Tee” means:
- the intersection lies strictly inside one segment, **but**
- it lands exactly on an endpoint of the other segment

`ih.tee_type` indicates which “arm” is the endpoint: `TOP/BOTTOM` if it’s the vertical’s endpoint, or `LEFT/RIGHT` if it’s the horizontal’s endpoint (depending on how the helper defines it).

---

#### 5) Otherwise: no recognized intersection

```python
return None, None, None
```


This is the “nothing matched” fallback—e.g., parallel segments, or non-axis-aligned inputs, or misordered endpoints, depending on what `IntersectHelper` flags.

---

### Why the method is cleanly structured

- It computes the candidate intersection point once (`ipt`).
- It then classifies into **mutually exclusive** buckets in a sensible priority order:
  1. `outside` (reject early)
  2. `inside` → `CROSS`
  3. `corner`
  4. `tee`
- The return value always has the same shape, which is nice for callers.

---

### The important implied assumptions (a.k.a. “don’t feed it weird stuff”)

Even though `intersect()` itself doesn’t check these, it relies on `IntersectHelper` and your docstring contract:

- `self` must be horizontal and `other` must be vertical (axis-aligned).
- Endpoints must be ordered so “start/end” comparisons make sense.
- Equality checks for endpoints (`==`) can be fragile with floats unless values are exact (even without `NaN`).

If those assumptions hold, the logic reads as a standard, correct classification pipeline for horizontal-vs-vertical segment intersection.

"""

from __future__ import annotations

from typing import SupportsFloat, TypeVar, Generic

from intersection_helper import IntersectHelper, IntrxnType, IntrxnSubtype
from point import Point

T = TypeVar("T", bound=SupportsFloat)


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

    def __init__(self, pt_1: Point[T], pt_2: Point[T]):
        self.pt_1 = pt_1
        self.pt_2 = pt_2

    def intersect(self, other: Wall[T]) -> tuple[IntrxnType | None, IntrxnSubtype | None, Point[T] | None]:
        """
        Determine the intersection type if a given vertical wall intersects with a given horizontal wall.

        self is the horizontal wall.
        other is the vertical wall.
        """
        ih = IntersectHelper(self, other)

        # Fast reject: the lines can only intersect if projected ranges overlap (inclusive).
        if ih.outside:
            return None, None, None

        ipt = Point(ih.val_vert, ih.val_horz)

        # Cross: strictly inside both segments.
        if ih.inside:
            return IntrxnType.CROSS, IntrxnSubtype.NA, ipt

        # Corner: intersection equals an endpoint of both segments.
        if ih.corner:
            return IntrxnType.CORNER, ih.corner_type, ipt

        # Tee: an endpoint of one segment is strictly inside the other.
        if ih.tee:
            return IntrxnType.TEE, ih.tee_type, ipt

        return None, None, None
