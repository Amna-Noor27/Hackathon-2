# Tasks: In-Memory Python Todo Console Application

**Input**: Design documents from `/specs/001-todo-cli-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: This project includes automated unit tests to verify CRUD logic.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize `uv` project with `uv init`
- [x] T002 [P] Create `src/` and `tests/` directories
- [x] T003 Configure `ruff` for linting in `pyproject.toml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and base models

- [x] T004 Define `Task` dataclass/model in `src/logic.py`
- [x] T005 Initialize `tasks_db` and `next_id` counter in `src/logic.py`
- [x] T006 Setup base `pytest` configuration in `tests/conftest.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add and List Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement the ability to create tasks and view the entire list.

**Independent Test**: Add 3 tasks via `add_task` and verify `list_tasks` returns all 3 with correct IDs.

### Tests for User Story 1
- [x] T007 [P] [US1] Create unit tests for `add_task` in `tests/test_logic.py`
- [x] T008 [P] [US1] Create unit tests for `list_tasks` in `tests/test_logic.py`

### Implementation for User Story 1
- [x] T009 [US1] Implement `add_task` function in `src/logic.py`
- [x] T010 [US1] Implement `list_tasks` function in `src/logic.py`
- [x] T011 [US1] Implement basic CLI loop with "Add" and "List" in `src/main.py`

**Checkpoint**: MVP Ready - User can manage a list of tasks in the terminal.

---

## Phase 4: User Story 2 - Complete and Delete Tasks (Priority: P2)

**Goal**: Allow users to update task status and remove items.

**Independent Test**: Mark a task as complete and verify status change; delete a task and verify its removal from `list_tasks`.

### Tests for User Story 2
- [x] T012 [P] [US2] Create unit tests for `toggle_task_status` in `tests/test_logic.py`
- [x] T013 [P] [US2] Create unit tests for `delete_task` in `tests/test_logic.py`

### Implementation for User Story 2
- [x] T014 [US2] Implement `toggle_task_status` in `src/logic.py`
- [x] T015 [US2] Implement `delete_task` in `src/logic.py`
- [x] T016 [US2] Add "Complete Task" and "Delete Task" options to CLI menu in `src/main.py`

**Checkpoint**: Task lifecycle management complete.

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Allow descriptive updates to existing tasks.

**Independent Test**: Update a task and verify the new title/description via `list_tasks`.

### Tests for User Story 3
- [x] T017 [P] [US3] Create unit tests for `update_task` in `tests/test_logic.py`

### Implementation for User Story 3
- [x] T018 [US3] Implement `update_task` in `src/logic.py`
- [x] T019 [US3] Add "Update Task" option to CLI menu in `src/main.py`

**Checkpoint**: All CRUD operations implemented.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verification and final UX touches.

- [x] T020 [P] Implement numeric input validation for all CLI prompts in `src/main.py`
- [x] T021 [P] Implement empty description validation in `src/main.py`
- [x] T022 Add "Clear Screen" utility between menu actions for better UX in `src/main.py`
- [ ] T023 Final end-to-end manual validation using `uv run src/main.py`
- [ ] T024 [P] Final documentation update (README.md)

---

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1 & 2**: Prerequisites for everything else.
- **Phase 3 (MVP)**: Must be completed first to have a functional list.
- **Phase 4 & 5**: Can proceed in parallel once Phase 3 is stable.
- **Phase 6**: Final polish after all features are in.

### Parallel Opportunities
- T007, T008 (Tests for US1)
- T012, T013 (Tests for US2)
- T020, T021 (Input validation tasks)
