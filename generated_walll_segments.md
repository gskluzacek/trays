# `Tray.generate_walls_segments` — detailed reusable analysis

## Scope and source boundaries

- This analysis is based on source in:
    - `tray/`
    - `cyclic_n_tuples/`
    - `tests/`
- Primary implementation file: `tray/tray.py`

## Entry point behavior

In `tray/tray.py`, `Tray.generate_walls_segments` is:

```python
def generate_walls_segments(self):
    self._generate_walls_segments(LineOrientation.HORZ)
    self._generate_walls_segments(LineOrientation.VERT)
```

### What this means

- It is an orchestrator method.
- It runs segmentation in two passes:
    1. horizontal walls
    2. vertical walls
- It mutates wall objects in place (no return value).

---

## Immediate call graph

1. `Tray.generate_walls_segments()`
2. `Tray._generate_walls_segments(orientation)`
3. `Line.of_orientation(self.index_walls, orientation)`
4. For each wall: `Tray._generate_wall_segments(wall)`
5. Inside `_generate_wall_segments`:
    - selects final-path lines by orientation (`path.horizontal` or `path.vertical`)
    - checks overlap (`path_line.is_overlapping(wall)`)
    - extracts candidate endpoints (`path_line.points_from_line`)
    - filters endpoints to wall extent (`SegmentPoint.is_between(wall)`)
    - sorts breakpoints according to wall direction (`wall.p1 < wall.p2`)
    - determines starting joint parity (`_does_wall_line_start_first` / defaults)
    - pairs adjacent points (`fwd_pair(points)`)
    - appends `SegmentLine`s via `wall.segment_path.add_segment(...)`

---

## `_generate_walls_segments(orientation)`

Implementation pattern:

```python
def _generate_walls_segments(self, orientation: LineOrientation):
    for wall in Line.of_orientation(self.index_walls, orientation):
        self._generate_wall_segments(wall)
```

### Notes

- Delegates all per-wall logic.
- `Line.of_orientation` yields only lines with matching `LineOrientation`.

---

## Core algorithm: `_generate_wall_segments(wall)`

### 1) Gather segment points from overlapping final path lines

Pseudo-flow:

```python
segment_points = []
for path in self.final_index_paths:
    path_lines = path.horizontal if wall.is_horizontal else path.vertical
    for path_line in path_lines:
        if path_line.is_overlapping(wall):
            segment_points.extend(
                pt for pt in path_line.points_from_line if pt.is_between(wall)
            )
```

Interpretation:

- Uses already-split final base paths (`self.final_index_paths` from `split_path_lines`).
- Only compares collinear candidate lines (same orientation list + overlap check).
- Captures endpoints of each overlapping path line that lie on/within wall span.
- Each captured item is a `SegmentPoint` that remembers both:
    - the point
    - the source path line (`.line`), later used for parity logic.

### 2) Order points in wall travel direction

```python
segment_points.sort(reverse=False if wall.p1 < wall.p2 else True)
points = [wall.p1] + [pt.to_point for pt in segment_points] + [wall.p2]
wall.segment_path.points = points
```

Interpretation:

- If wall direction is forward (`p1 < p2`) sort ascending.
- If reverse (`p1 > p2`) sort descending.
- Construct full ordered chain from wall start to wall end.

### 3) Choose starting parity for alternating joint types

```python
if wall.wall_type == WallType.INTERIOR:
    first_joint_type = 0
else:
    first_joint_type = 1

if segment_points:
    path_line_1 = segment_points[0].line
    first_joint_type = 0 if self._does_wall_line_start_first(wall, path_line_1) else 1
```

Interpretation:

- Default offset:
    - `INTERIOR` => `0`
    - otherwise (`EXTERIOR`/`COMBO`) => `1`
- If breakpoints exist, default can be overridden by directional relationship between wall and first source path line.

### 4) Build contiguous segments and assign alternating joint types

```python
joints = [JointType.TS, JointType.FS]
for i, (p1, p2) in enumerate(fwd_pair(points), first_joint_type):
    joint_type = joints[i % 2]
    wall.segment_path.add_segment(p1, p2, joint_type)
```

Interpretation:

- `fwd_pair` yields adjacent point pairs `(p0,p1), (p1,p2), ...`.
- Enumeration starts at parity offset (`0` or `1`).
- Alternation rule:
    - even index -> `JointType.TS` (`tab-slot`)
    - odd index -> `JointType.FS` (`finger-space`)
- `add_segment` creates `SegmentLine(p1, p2, joint_type)` and appends it.

---

## Direction-sensitive helper: `_does_wall_line_start_first`

Signature:

```python
def _does_wall_line_start_first(line1: WallLine, line2: FinalPathLine) -> bool:
```

Purpose:

- Compare normalized extents of wall vs path line and answer whether the wall starts first,
  while correctly handling reversed wall direction.

Logic summary:

- Obtain normalized endpoints from both lines (`line.normalize`).
- Horizontal:
    - if wall is forward (`line1.p1 < line1.p2`): compare normalized starts (`line1_p1.x < line2_p1.x`)
    - if wall is reverse: compare normalized ends (`line1_p2.x > line2_p2.x`)
- Vertical: same pattern using `y`.

Why this matters:

- For reverse-direction walls, “start-before” semantics flip to an end-based comparison.
- This controls initial TS/FS alternation parity.

---

## Called functions/types and their role

### `Line.of_orientation(...)` (`tray/geometry/basic/line.py`)

- Filters line sequence by orientation.
- Used in per-orientation wall pass.

### `Line.is_overlapping(...)` (`tray/geometry/basic/line.py`)

- Determines collinear overlap.
- Gate for whether a path line contributes breakpoint endpoints.

### `points_from_line` (line/path-line property)

- Produces endpoint `SegmentPoint`s for a line.
- Preserves source line reference on each point.

### `SegmentPoint.is_between(wall)` (`tray/geometry/segment/segment_point.py`)

- Checks if the point lies within wall bounds.

### `SegmentPoint.to_point`

- Converts segment-point wrapper to plain geometric `Point`.

### `fwd_pair(seq)` (`cyclic_n_tuples/__init__.py`)

- Returns consecutive forward pairs from ordered points.

### `SegmentPath.add_segment(...)` (`tray/geometry/segment/segment_path.py`)

- Appends a `SegmentLine` with `joint_type` to wall segment path.

### `JointType` and `WallType` (`tray/geometry/types/tray.py`)

- `JointType.TS` / `JointType.FS` are alternating joint labels.
- `WallType.INTERIOR/EXTERIOR/COMBO` influences initial parity.

---

## Preconditions (important for correctness)

`generate_walls_segments` assumes prior pipeline stages were run:

- walls exist in `self.index_walls`
- wall types already assigned by `classify_index_walls()`
- final split paths prepared by `split_path_lines()`

If not, segmentation can still execute but will produce low-fidelity or incorrect segmentation/parity behavior.

---

## Observable postconditions

For each wall:

- `wall.segment_path.points` becomes ordered [start, breakpoints..., end]
- `wall.segment_path.lines` contains contiguous `SegmentLine`s over those points
- each segment has alternating `TS/FS` according to computed starting parity

Method returns `None`; effects are in-place mutations on wall objects.

---

## Test-backed expectations from `tests/unit/test_tray.py`

- `test_tray_generate_walls_segments_interior`
    - interior wall starts with `JointType.TS`.

- `test_tray_generate_walls_segments_with_no_segments`
    - exterior walls in that setup start with `JointType.FS` fallback parity.

- `test_tray_generate_walls_segments_combo_start_first`
    - exercises combo/exterior and overlap split behavior.

- `test_does_wall_line_start_first_bottom_right_to_top_left`
    - validates reversed-direction comparison logic for horizontal and vertical walls.

---

## Practical one-line summary

`generate_walls_segments` converts each wall from a single line into an ordered, direction-aware sequence of
joinery-labeled subsegments (`TS`/`FS`) using overlap with already-split final base-path geometry.