---
id: 001
title: Initialize todo app constitution
stage: constitution
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: unknown
command: /sp.constitution
labels: ["constitution", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md (created/updated with todo app principles)
tests:
  - (none run)
---

## Prompt

# Todo App Constitution

In-memory Python console Todo App using **spec-driven development**.
Progresses through **basic**, **intermediate**, and **advanced** features for an AI-native workflow.

---

## Core Principles
- **Test-first accuracy** with full validation
- **Clear CLI** for Python developers
- **Reproducible** via specs and **100% test coverage**

---

## Feature Scope

### Basic (MVP)
- Add / delete / update tasks
- View list, mark tasks complete

### Intermediate
- Priorities / tags (high / medium / low, work / home)
- Search / filter / sort (by keyword, status, priority, date)

### Advanced
- Recurring tasks (daily / weekly)
- Due dates with console reminders

---

## Tech Standards
- Python **3.12+**, standard library only (`argparse`, `dataclasses`)
- MVC: **Task model**, in-memory list, console UI
- **PEP 8**, type hints

---

## AI-Native Workflow
- **Spec-driven** via `/speckit`
- AI code generation + human validation
- Iterative phases

---

## Quality Rules
- `unittest` **100% coverage**
- **Immutable models**, no globals
- Input validation, clean errors

---

## Success Metrics
- All features demo via console
- Handles 100+ tasks
- Clean spec history

## Response snapshot

Successfully created the Todo App Constitution (v1.0.0) with:
- 3 core principles: Test-First Accuracy, Clear CLI, Reproducible
- Feature scope across 3 levels: Basic (CRUD), Intermediate (priorities/tags/search), Advanced (recurring/due dates)
- Tech standards: Python 3.12+, standard library only, MVC architecture, PEP 8, type hints
- AI-native workflow: Spec-driven development, AI code generation with human validation, iterative phases
- Quality rules: 100% test coverage with unittest, immutable models, input validation
- Success metrics: Console demo, 100+ tasks, clean spec history

Sync impact report confirms all dependent templates (plan-template.md, spec-template.md, tasks-template.md) remain compatible with no updates required.

## Outcome

- ✅ Impact: Constitution v1.0.0 established, providing foundational governance for Todo App development
- 🧪 Tests: (none run - constitution update)
- 📁 Files: .specify/memory/constitution.md created with full governance document
- 🔁 Next prompts: Consider creating initial feature spec for Todo App MVP
- 🧠 Reflection: Constitution provides clear constraints (Python 3.12+, standard library only, MVC, 100% coverage) that will guide all feature development

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
