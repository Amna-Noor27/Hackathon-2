# Research: In-Memory Python Todo Console Application

**Feature**: [In-Memory Python Todo Console Application](../spec.md)
**Date**: 2026-01-01

## Decision 1: Project Management with UV
- **Decision**: Use `uv` for dependency management and running the application.
- **Rationale**: User explicitly requested `uv`. It provides extremely fast dependency resolution and a clean interface for Python projects.
- **Alternatives considered**: `pip`, `poetry`, `pipenv` (all rejected per constraint).

## Decision 2: In-Memory Storage Structure
- **Decision**: Use a Python `list` of `dict` objects to store tasks.
- **Rationale**: Simple, fulfills the "in-memory" and "simplicity" constraints. Lists preserve order which is helpful for display, and dicts allow easy mapping of task attributes.
- **Alternatives considered**:
  - `dict` of `dict`s (Keyed by ID): Faster lookups by ID, but requires extra management for display order.
  - `dataclasses`: Better for type hinting and structured data, but might add slight complexity over simple dicts for a Phase 1 MVP. Will stick to modular functions and clean logic.

## Decision 3: CLI Control Loop
- **Decision**: Use an infinite `while` loop with `input()` and a dispatch table or `match` statement.
- **Rationale**: Python 3.10+ `match` statement provides a clean way to handle menu options. `try-except` blocks will wrap ID lookups and numeric conversions.
- **Alternatives considered**: `cmd` module (might be over-engineering for this simple menu).

## Decision 4: Architecture
- **Decision**: Functional decomposition. Separate file/module structure where storage logic is isolated from terminal I/O.
- **Rationale**: Aligns with Principle VI (Architecture & Validation) from the Constitution.
