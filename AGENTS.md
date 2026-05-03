# AGENTS

This file is a compact index for AI-assisted work in this repository.

## Session Startup Requirement

- When starting a new chat, first review [`./.junie/AGENTS.md`](./.junie/AGENTS.md).
- Treat `.junie/AGENTS.md` as the session-specific instruction source before using this root guide.

## Instruction Topics

- [Code Q&A Instructions](./code_questions_instructions.md)
- [Architecture Proposal Instructions](./architecture_instructions.md)
- [Code Writing Instructions](./coding_instructions.md)
- [Test Writing Instructions](./testing_instructions.md)

## Core Project Anchors

- Entrypoint example: [`main.py`](./main.py)
- Main orchestration model: [`tray/tray.py`](./tray/tray.py)
- Geometry primitives: [`tray/geometry/basic/`](./tray/geometry/basic/)
- Wall/intersection behavior: [`tray/geometry/wall_line.py`](./tray/geometry/wall_line.py), [
  `tray/geometry/intersection.py`](./tray/geometry/intersection.py)
- Utility iterators: [`cyclic_n_tuples/__init__.py`](./cyclic_n_tuples/__init__.py)
- Unit tests: [`tests/unit/`](./tests/unit/)
- Integration tests: [`tests/integration/`](./tests/integration/)

## Working Conventions

- Use `uv` for dependency management and command execution.
- Use `pytest` for tests.
- Do not rely on `pytest-cov`.
- Keep style compatible with Python `3.13`.
- Keep unit tests for a given Python class in the same test file.

For implementation/test details, follow the topic files listed above.