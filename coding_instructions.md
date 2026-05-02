# Code Writing Instructions

Use this guide when implementing new code in this repository.

## 1) Environment and Commands

- Install/update deps with `uv` (example: `uv sync --group dev`).
- Run Python with `uv run python ...`.
- Keep compatibility with Python `3.13` (see [`pyproject.toml`](./pyproject.toml)).

## 2) Implementation Style

- Follow existing typed style: explicit type hints, generics where already used.
- Keep validation near object/method boundaries (raise `ValueError` for invalid geometry/index input).
- Reuse existing primitives before adding new ones:
    - `Point`, `Line`, `Path` in [`tray/geometry/basic/`](./tray/geometry/basic/)
    - typed/final/segment path types in [`tray/geometry/`](./tray/geometry/)
- Prefer small focused methods consistent with `Tray` pipeline structure in [`tray/tray.py`](./tray/tray.py).

## 3) Where to Add New Logic

- Workflow orchestration logic: [`tray/tray.py`](./tray/tray.py)
- Primitive geometric calculations: matching file under [`tray/geometry/basic/`](./tray/geometry/basic/)
- Wall-specific behavior: [`tray/geometry/wall_line.py`](./tray/geometry/wall_line.py)
- Intersection behavior/types: [`tray/geometry/intersection.py`](./tray/geometry/intersection.py), [
  `tray/geometry/types/tray.py`](./tray/geometry/types/tray.py)

## 4) Done Criteria for Code Changes

- Change is minimal and placed in the correct layer.
- Existing contracts are preserved unless intentionally changed and documented.
- Related tests are added/updated (see [Testing Instructions](./testing_instructions.md)).
- Related understanding docs can be cross-checked via [Code Q&A Instructions](./code_questions_instructions.md).