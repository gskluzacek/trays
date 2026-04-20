# trays

`trays` is a Python project for modeling compartment trays (for laser-cut builds) from indexed base paths and wall
definitions.

> Project status: work in progress.

## Overview

The current codebase centers on the `Tray` model in `tray/tray.py`, where you:

1. define material thickness and inside dimensions (columns/rows),
2. define a base path using index coordinates,
3. add interior/exterior walls,
4. finalize geometry and generate wall/intersection data.

Legacy notes in `README_old.md` explain the original modeling approach in detail; this README keeps the operational
setup for the current repository state.

## Requirements

- Python `>=3.13` (from `pyproject.toml`)
- `uv` package manager / runner (project includes `uv.lock`)

Optional dev tools are managed through the `dev` dependency group:

- `pytest`
- `coverage`
- `ruff`

## Setup

From the repository root:

```bash
uv sync --group dev
```

This installs the project environment with test/lint tooling.

## Run

Primary runnable entry point:

- `main.py`

Run it with:

```bash
uv run python main.py
```

There is also a legacy/prototype script at `main_5/main5.py`.

```bash
uv run python main_5/main5.py
```

## Scripts

No packaged CLI scripts are currently declared in `pyproject.toml` (`[project.scripts]` is not defined).

Use direct `uv run python ...` commands for now.

- TODO: decide whether to expose an installable CLI entry point (for example `trays = ...`) and add it under
  `[project.scripts]`.

## Environment Variables

No required runtime environment variables were found in the main project package (`tray/`) or test suite.

- TODO: if future features require config via environment variables, document them here (`NAME`, required/optional,
  default, example).

## Tests

The repository uses `pytest` and configures test discovery in `pyproject.toml`:

- `testpaths = ["tests"]`

Run all tests:

```bash
uv run pytest
```

Run unit tests only:

```bash
uv run pytest tests/unit
```

Run integration tests only:

```bash
uv run pytest tests/integration
```

Run coverage:

```bash
uv run coverage run -m pytest
uv run coverage report -m
```

## Project Structure

```text
.
├── main.py                     # Current primary runnable example
├── pyproject.toml              # Project metadata, Python requirement, pytest/ruff config
├── uv.lock                     # Locked dependency state for uv
├── tray/
│   ├── tray.py                 # Core Tray orchestration
│   └── geometry/               # Geometry primitives, base/final/segment/intersection logic
├── tests/
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── README_old.md               # Historical README and early design narrative
└── LICENSE
```

Note: `non_essential/` contains prototypes and exploratory assets that are not part of the core runtime path.

## Legacy Modeling Notes (Condensed)

The original project concept (documented in `README_old.md`) defines a tray in three steps:

1. overall parameters (material thickness, dimensions, tab/finger settings),
2. base polygon path in index-space coordinates,
3. wall definitions in the same index-space.

This conceptual model is still reflected in current APIs (`start_base`, `extend_base`, `end_base`, `add_wall`).

## License

This project is licensed under **The Unlicense** (public domain dedication).

See `LICENSE` for the full text.