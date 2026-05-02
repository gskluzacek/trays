# Architecture Proposal Instructions

Use this guide when proposing new architectural solutions for new requirements.

## 1) Preserve Current Domain Boundaries

- Keep orchestration in [`tray/tray.py`](./tray/tray.py) (`Tray` should coordinate, not duplicate primitive logic).
- Keep geometry rules in the geometry layer (`tray/geometry/**`).
- Keep sequence/chunk iteration helpers in [`cyclic_n_tuples/__init__.py`](./cyclic_n_tuples/__init__.py).

## 2) Respect Existing Invariants

- Geometry is axis-aligned and orthogonal (non-orthogonal lines are rejected).
- Index-space modeling is transformed into center-to-center coordinates.
- Validation is explicit and eager (`ValueError` on invalid states).
- Wall classification and segmentation are separate phases before intersection processing.

## 3) Proposal Pattern

1. State where the requirement belongs: `Tray` orchestration vs geometry primitive vs utility layer.
2. Define new/changed invariant(s) and failure modes.
3. Identify touch points in code and tests:
    - implementation files in `tray/`
    - unit tests in `tests/unit/`
    - integration tests in `tests/integration/`
4. Prefer minimal extension of current types/enums over parallel ad-hoc structures.

## 4) Quality Gates for Architecture Suggestions

- Include backward-compatibility impact (public constructor/method contracts).
- Include test impact (what existing tests may break, what new tests are needed).
- Include data-flow impact through the existing lifecycle in [`main.py`](./main.py).

See
also: [Code Q&A](./code_questions_instructions.md), [Coding](./coding_instructions.md), [Testing](./testing_instructions.md).