"""
```python
class IntersectHelper:
```


`IntersectHelper` is a small “precompute and classify” helper for figuring out **how a horizontal wall segment** intersects a **vertical wall segment** (if at all). It computes a bunch of boolean flags once in `__init__`, then exposes convenient properties like `outside`, `inside`, `corner`, `tee`, plus subtype getters (`corner_type`, `tee_type`).

---

## 1) The `corner_map`: mapping endpoint-hit patterns to a corner subtype

```python
corner_map: dict[tuple[bool, bool, bool, bool], IntrxnSubtype] = {
    (True, False, True, False): IntrxnSubtype.UPPER_LEFT,
    (True, False, False, True): IntrxnSubtype.LOWER_LEFT,
    (False, True, True, False): IntrxnSubtype.UPPER_RIGHT,
    (False, True, False, True): IntrxnSubtype.LOWER_RIGHT,
}
```


This dictionary maps a 4-tuple of booleans to which **corner** intersection you have.

The key is:

```
(at_left_end, at_right_end, at_top_end, at_bottom_end)
```


Meaning:

- `at_left_end`: intersection x equals horizontal segment’s left endpoint x
- `at_right_end`: intersection x equals horizontal segment’s right endpoint x
- `at_top_end`: intersection y equals vertical segment’s top endpoint y
- `at_bottom_end`: intersection y equals vertical segment’s bottom endpoint y

If you hit an endpoint on *both* segments simultaneously, you’re at a corner, and this map tells you which one.

---

## 2) `__init__`: normalize the geometry into scalars + booleans

```python
def __init__(self, horz_wall: Wall[T], vert_wall: Wall[T]) -> None:
    self.horz_wall = horz_wall
    self.vert_wall = vert_wall
```


You pass in a **horizontal** wall and a **vertical** wall. The helper then extracts the single constant coordinate for each:

### Extract constant coordinates and ranges

```python
self.val_horz = self.horz_wall.pt_1.y
self.start_horz = self.horz_wall.pt_1.x
self.end_horz = self.horz_wall.pt_2.x
```


For a horizontal segment:

- `val_horz` is the constant y value of the entire segment
- `[start_horz, end_horz]` is its x-range

```python
self.val_vert = self.vert_wall.pt_1.x
self.start_vert = self.vert_wall.pt_1.y
self.end_vert = self.vert_wall.pt_2.y
```


For a vertical segment:

- `val_vert` is the constant x value
- `[start_vert, end_vert]` is its y-range

### Compute “strictly inside” checks

```python
self.inside_horz = self._between(self.start_horz, self.end_horz, self.val_vert)
self.inside_vert = self._between(self.start_vert, self.end_vert, self.val_horz)
```


Interpretation:

- The intersection point candidate is `(x=val_vert, y=val_horz)` (where the infinite lines cross).
- `inside_horz` asks: is `val_vert` strictly between the horizontal segment’s x endpoints?
- `inside_vert` asks: is `val_horz` strictly between the vertical segment’s y endpoints?

Because `_between` uses strict inequality (`>` and `<`), endpoint touches are *not* considered “inside”.

### Compute endpoint equality checks

```python
self.at_left_end, self.at_right_end = self._start_end(self.start_horz, self.end_horz, self.val_vert)
self.at_top_end, self.at_bottom_end = self._start_end(self.start_vert, self.end_vert, self.val_horz)
```


`_start_end(start, end, value)` returns a pair:

- `value == start`
- `value == end`

So:

- `at_left_end`/`at_right_end`: whether the intersection x equals the horizontal’s left/right endpoint x
- `at_top_end`/`at_bottom_end`: whether the intersection y equals the vertical’s top/bottom endpoint y

### Build the “corner key”

```python
self.corner_key = (
    self.at_left_end,
    self.at_right_end,
    self.at_top_end,
    self.at_bottom_end,
)
self._tee_type = IntrxnSubtype.NONE
```


This `corner_key` is exactly what `corner_map` uses to classify corner subtypes.

`_tee_type` is a cached result: it’s updated when you call the `tee` property.

---

## 3) Static helpers: `_outside`, `_between`, `_start_end`

```python
@staticmethod
def _outside(start: T, end: T, value: T) -> bool:
    return value < start or value > end
```


“Outside inclusive bounds” (outside `[start, end]`).

```python
@staticmethod
def _between(start: T, end: T, value: T) -> bool:
    return value > start and value < end
```


“Strictly inside” (inside `(start, end)`), not counting endpoints.

```python
@staticmethod
def _start_end(start: T, end: T, value: T) -> tuple[bool, bool]:
    return value == start, value == end
```


Exact endpoint hits.

---

## 4) Properties that classify the intersection

### `outside`: fast rejection test

```python
@property
def outside(self) -> bool:
    return (
        self._outside(self.start_horz, self.end_horz, self.val_vert) or
        self._outside(self.start_vert, self.end_vert, self.val_horz)
    )
```


This checks whether the candidate intersection point `(val_vert, val_horz)` lies outside either segment’s bounding range:

- vertical line’s x (`val_vert`) must be within the horizontal segment’s x-range
- horizontal line’s y (`val_horz`) must be within the vertical segment’s y-range

If either is outside, the segments **cannot** intersect.

### `inside`: proper “cross” intersection (not at endpoints)

```python
@property
def inside(self) -> bool:
    return self.inside_horz and self.inside_vert
```


True only if the intersection point is strictly inside both segments → a clean “crossing”.

### `corner` and `corner_type`: endpoint-on-both classification

```python
@property
def corner(self) -> bool:
    return self.corner_key in self.corner_map

@property
def corner_type(self) -> IntrxnSubtype:
    return self.corner_map[self.corner_key]
```


If the intersection hits an endpoint of the horizontal segment *and* an endpoint of the vertical segment, you get a corner subtype (upper-left, lower-right, etc.) via the lookup.

Note: `corner_type` assumes `corner` is true; otherwise it will raise `KeyError`.

### `tee` and `tee_type`: endpoint-on-one-but-inside-the-other

```python
@property
def tee(self) -> bool:
    if self.inside_horz and (self.at_top_end or self.at_bottom_end):
        self._tee_type = IntrxnSubtype.TOP if self.at_top_end else IntrxnSubtype.BOTTOM
        return True
    elif self.inside_vert and (self.at_left_end or self.at_right_end):
        self._tee_type = IntrxnSubtype.LEFT if self.at_left_end else IntrxnSubtype.RIGHT
        return True
    return False
```


A “tee” happens when:

- The intersection is **strictly inside** one segment, but exactly on an **endpoint** of the other segment.

This code checks two cases:

1) Intersection is inside the horizontal segment and hits the **top/bottom endpoint** of the vertical segment → tee subtype is `TOP` or `BOTTOM`.

2) Intersection is inside the vertical segment and hits the **left/right endpoint** of the horizontal segment → tee subtype is `LEFT` or `RIGHT`.

`tee_type` returns whatever `tee` last set:

```python
@property
def tee_type(self) -> IntrxnSubtype:
    return self._tee_type
```


One subtlety: `tee_type` is only meaningful after `tee` has been evaluated (otherwise it stays `NONE`). It’s like a little stateful classifier: “call `tee` to compute, then read `tee_type`”.

---

## 5) Putting it together (mental model)

- The candidate intersection point of an axis-aligned horizontal and vertical line is always:
  - `x = vert_wall.pt_1.x`
  - `y = horz_wall.pt_1.y`

This helper decides which bucket that point falls into:

- **`outside`** → no intersection possible
- **`inside`** → cross intersection (strictly inside both)
- **`corner`** → touches endpoints of both (use `corner_type`)
- **`tee`** → endpoint of exactly one + inside the other (use `tee_type`)
- otherwise → aligned in a way that doesn’t produce an intersection under these rules (e.g., touching neither inside nor endpoints)

If you want, I can sketch a tiny truth table showing which flags are expected for cross vs corner vs tee, to make the classification feel even more “mechanical.”

--------------------------------------------------------------------------------------

## Tiny truth table / decision grid for `IntersectHelper`

Think of the candidate intersection point as:

- `x_i = val_vert` (vertical wall’s constant `x`)
- `y_i = val_horz` (horizontal wall’s constant `y`)

And these booleans mean:

- `inside_horz`: `start_horz < x_i < end_horz`
- `inside_vert`: `start_vert < y_i < end_vert`
- `at_left_end`: `x_i == start_horz`
- `at_right_end`: `x_i == end_horz`
- `at_top_end`: `y_i == start_vert`
- `at_bottom_end`: `y_i == end_vert`

### 1) Fast reject: **no intersection**

| Condition | Meaning |
|---|---|
| `outside == True` | `x_i` is outside the horizontal segment’s x-range **or** `y_i` is outside the vertical segment’s y-range → cannot intersect |

So you typically check this first.

---

### 2) Proper “cross” intersection (strictly inside both)

| Case | `inside_horz` | `inside_vert` | Any `at_*_end`? | Result |
|---|---:|---:|---:|---|
| CROSS | True | True | No (all False) | `inside == True` (a “cross”) |

Because `_between` is strict, if you’re “inside” you’re *not* at an endpoint.

---

### 3) Corner intersection (endpoint on both segments)

Corner means: the intersection point is on an endpoint of the horizontal **and** on an endpoint of the vertical.

That corresponds exactly to `corner_key` being in `corner_map`:

| Corner subtype | `at_left_end` | `at_right_end` | `at_top_end` | `at_bottom_end` | Notes |
|---|---:|---:|---:|---:|---|
| `UPPER_LEFT` | True | False | True | False | left end of horizontal + top end of vertical |
| `LOWER_LEFT` | True | False | False | True | left + bottom |
| `UPPER_RIGHT` | False | True | True | False | right + top |
| `LOWER_RIGHT` | False | True | False | True | right + bottom |

Also true at corners:

- `inside_horz == False` (because `x_i` equals start/end, not strictly between)
- `inside_vert == False` (because `y_i` equals start/end)

So corners are “endpoint touch on both sides,” not a cross.

---

### 4) Tee intersection (endpoint on exactly one segment)

A tee means: strictly inside one segment, but exactly on an endpoint of the other.

There are two orientations checked:

#### Tee where the **vertical** ends on the horizontal (top/bottom tee)
| Case | `inside_horz` | `at_top_end` / `at_bottom_end` | `inside_vert` | Tee subtype set |
|---|---:|---:|---:|---|
| TEE (vertical endpoint) | True | True | False (because endpoint) | `TOP` if `at_top_end` else `BOTTOM` |

#### Tee where the **horizontal** ends on the vertical (left/right tee)
| Case | `inside_vert` | `at_left_end` / `at_right_end` | `inside_horz` | Tee subtype set |
|---|---:|---:|---:|---|
| TEE (horizontal endpoint) | True | True | False (because endpoint) | `LEFT` if `at_left_end` else `RIGHT` |

So, summarized:

- Tee ⇒ one “inside_*” is `True`, the other is `False` *because it’s at an endpoint*.

---

## A compact decision order (how you’d typically reason about it)

```python
# Pseudocode / mental flow
if outside:
    # no intersection
elif inside:
    # cross
elif corner:
    # corner_type tells which corner
elif tee:
    # tee_type tells TOP/BOTTOM/LEFT/RIGHT
else:
    # none (e.g., exactly aligned in a non-intersecting way under these rules)
```


If you want, I can also draw a little ASCII diagram for each subtype (UPPER_LEFT, TOP tee, etc.) showing which endpoint is being hit.


"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, SupportsFloat, TypeVar

if TYPE_CHECKING:
    from refactored_wall_intersection import Wall


T = TypeVar("T", bound=SupportsFloat)


class IntrxnType(Enum):
    CROSS = "cross"
    CORNER = "corner"
    TEE = "tee"
    NONE = "none"


class IntrxnSubtype(Enum):
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


class IntersectHelper:
    corner_map: dict[tuple[bool, bool, bool, bool], IntrxnSubtype] = {
        (True, False, True, False): IntrxnSubtype.UPPER_LEFT,
        (True, False, False, True): IntrxnSubtype.LOWER_LEFT,
        (False, True, True, False): IntrxnSubtype.UPPER_RIGHT,
        (False, True, False, True): IntrxnSubtype.LOWER_RIGHT,
    }

    def __init__(self, horz_wall: Wall[T], vert_wall: Wall[T]) -> None:
        self.horz_wall = horz_wall
        self.vert_wall = vert_wall

        self.val_horz = self.horz_wall.pt_1.y
        self.start_horz = self.horz_wall.pt_1.x
        self.end_horz = self.horz_wall.pt_2.x

        self.val_vert = self.vert_wall.pt_1.x
        self.start_vert = self.vert_wall.pt_1.y
        self.end_vert = self.vert_wall.pt_2.y

        self.inside_horz = self._between(self.start_horz, self.end_horz, self.val_vert)
        self.inside_vert = self._between(self.start_vert, self.end_vert, self.val_horz)

        self.at_left_end, self.at_right_end = self._start_end(self.start_horz, self.end_horz, self.val_vert)
        self.at_top_end, self.at_bottom_end = self._start_end(self.start_vert, self.end_vert, self.val_horz)

        self.corner_key: tuple[bool, bool, bool, bool] = (
            self.at_left_end,
            self.at_right_end,
            self.at_top_end,
            self.at_bottom_end,
        )

        self._tee_type = IntrxnSubtype.NONE

    @staticmethod
    def _outside(start: T, end: T, value: T) -> bool:
        return value < start or value > end

    @staticmethod
    def _between(start: T, end: T, value: T) -> bool:
        return value > start and value < end  # noqa

    @staticmethod
    def _start_end(start: T, end: T, value: T) -> tuple[bool, bool]:
        return value == start, value == end

    @property
    def outside(self) -> bool:
        """
        Determines if the value is outside the specified bounds.

        This property evaluates whether the provided horizontal and vertical values
        fall outside their respective ranges as defined by the start and end positions.

        :return: A boolean value indicating if the value is outside the specified bounds.
        :rtype: bool

        ----
        outside docstring is misleading / overly broad
            The outside property says “provided horizontal and vertical values fall outside their respective ranges”, but it actually checks:
            whether vertical wall’s x is outside horizontal segment’s [start_horz, end_horz]
            OR whether horizontal wall’s y is outside vertical segment’s [start_vert, end_vert]
            That’s specifically “the candidate intersection point is outside either segment projection”, not “values are outside bounds” in a general sense.
        """
        # fmt: off
        return (
                self._outside(self.start_horz, self.end_horz, self.val_vert) or
                self._outside(self.start_vert, self.end_vert, self.val_horz)
        )
        # fmt: on

    @property
    def inside(self) -> bool:
        return self.inside_horz and self.inside_vert

    @property
    def corner(self) -> bool:
        return self.corner_key in self.corner_map

    @property
    def corner_type(self) -> IntrxnSubtype:
        return self.corner_map[self.corner_key]

    @property
    def tee(self) -> bool:
        """
        Checks for the "tee" intersection type based on current state conditions.

        This property evaluates if the current object state represents a "tee"
        intersection, which occurs when horizontal or vertical alignment conditions
        are met in conjunction with endpoint specifications. Depending on the specific
        conditions, the intersection subtype (e.g., TOP, BOTTOM, LEFT, RIGHT) is set
        internally. Returns `True` if the "tee" condition is satisfied, otherwise
        returns `False`.

        :return: True if the current state represents a "tee" intersection condition,
            otherwise False.
        :rtype: bool
        """
        if self.inside_horz and (self.at_top_end or self.at_bottom_end):
            self._tee_type = IntrxnSubtype.TOP if self.at_top_end else IntrxnSubtype.BOTTOM
            return True
        elif self.inside_vert and (self.at_left_end or self.at_right_end):
            self._tee_type = IntrxnSubtype.LEFT if self.at_left_end else IntrxnSubtype.RIGHT
            return True
        return False

    @property
    def tee_type(self) -> IntrxnSubtype:
        return self._tee_type
