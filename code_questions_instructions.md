# Code Q&A Instructions

Use this guide when answering questions about how the current code works.

## 1) Start From the Runtime Flow

1. Read [`main.py`](./main.py) to identify the expected `Tray` lifecycle.
2. Trace the invoked methods in [`tray/tray.py`](./tray/tray.py):
    - base setup: `start_base` → `extend_base` → `end_base`
    - wall setup: `add_wall` → `finalize_walls` → `classify_index_walls`
    - finalization: `split_path_lines` → `generate_walls_segments` → `generate_intersections`

## 2) Use the Geometry Layer Map

- Point behavior: [`tray/geometry/basic/point.py`](./tray/geometry/basic/point.py)
- Line behavior (orientation, overlap, intersections): [`tray/geometry/basic/line.py`](./tray/geometry/basic/line.py)
- Path containers: [`tray/geometry/basic/path.py`](./tray/geometry/basic/path.py)
- Typed/final paths and segments: [`tray/geometry/base/`](./tray/geometry/base/), [
  `tray/geometry/final_base/`](./tray/geometry/final_base/), [`tray/geometry/segment/`](./tray/geometry/segment/)

## 3) Confirm With Tests

- Primary behavior/regression coverage: [`tests/unit/test_tray.py`](./tests/unit/test_tray.py)
- Geometry behavior coverage: [`tests/unit/test_line.py`](./tests/unit/test_line.py), [
  `tests/unit/test_point.py`](./tests/unit/test_point.py), [
  `tests/unit/test_intersection.py`](./tests/unit/test_intersection.py)
- End-to-end scenario examples: [`tests/integration/test_main_0.py`](./tests/integration/test_main_0.py)

## 4) Reusable Reference Docs

- Generated method analysis: [`generated_walll_segments.md`](./generated_walll_segments.md)
- Class reference summary: [`classes_readme.md`](./classes_readme.md), [
  `classes_attributes_short.md`](./classes_attributes_short.md)
- Related process
  guides: [Architecture](./architecture_instructions.md), [Coding](./coding_instructions.md), [Testing](./testing_instructions.md)