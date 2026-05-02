# Test Writing Instructions

Use this guide when writing tests for existing or new behavior.

## 1) Framework and Commands

- Use `pytest`.
- Run tests via `uv`:
    - all tests: `uv run pytest`
    - unit tests: `uv run pytest tests/unit`
    - integration tests: `uv run pytest tests/integration`
- Do not assume `pytest-cov` is installed.

## 2) Placement Rules

- Keep tests in `tests/unit/` or `tests/integration/` based on scope.
- Keep all unit tests for a given Python class in the same file.
    - Example: `Tray` tests are centralized in [`tests/unit/test_tray.py`](./tests/unit/test_tray.py).

## 3) What to Cover

- Happy path behavior and key outputs.
- Validation errors (`ValueError`) for invalid geometry/index inputs.
- Orientation/overlap/intersection edge cases in geometry primitives.
- End-to-end lifecycle interactions for major pipeline changes (see [
  `tests/integration/test_main_0.py`](./tests/integration/test_main_0.py)).

## 4) Existing Examples to Mirror

- Orchestration and regression coverage: [`tests/unit/test_tray.py`](./tests/unit/test_tray.py)
- Primitive geometry coverage: [`tests/unit/test_line.py`](./tests/unit/test_line.py), [
  `tests/unit/test_point.py`](./tests/unit/test_point.py)
- Intersection-specific checks: [`tests/unit/test_intersection.py`](./tests/unit/test_intersection.py)

See
also: [Code Q&A](./code_questions_instructions.md), [Architecture](./architecture_instructions.md), [Coding](./coding_instructions.md).