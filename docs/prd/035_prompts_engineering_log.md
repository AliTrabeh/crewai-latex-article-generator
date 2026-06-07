---
id: "035"
title: "Prompts Engineering Log"
group: "11 — Documentation"
priority: medium
---

# Task 035 — Prompts Engineering Log

## Goal

Create `docs/prompts_log.md` documenting the prompt design and iteration history for each CrewAI agent and task. This is a required deliverable in the submission guidelines.

## Files to Create or Modify

- `docs/prompts_log.md` — prompt engineering journal

## Exact Expected Behavior

`docs/prompts_log.md` must contain one entry per agent/task with the following structure:

```markdown
## Agent: ResearcherAgent

### Prompt v1.0 (initial)
**Role:** ...
**Goal:** ...
**Backstory:** ...

**Problem observed:** Too generic; did not focus on academic sources.

### Prompt v1.1 (revised)
**Role:** Academic Researcher
**Goal:** Thoroughly investigate the given topic and gather credible,
up-to-date academic and technical sources.
**Backstory:** You are a meticulous academic researcher...

**Why this works better:** Explicit mention of "academic" constrains
the agent to scholarly sources over blog posts.
```

Repeat for: WriterAgent, ReviewerAgent, LaTeXFormatterAgent, and each Task description.

## Acceptance Criteria

- [ ] At least one entry per agent (4 agents → at least 4 entries).
- [ ] Each entry has at least two prompt versions (initial + revised).
- [ ] Each entry explains why the revision improved the output.
- [ ] File exists at `docs/prompts_log.md`.

## Notes / Constraints

- Fill this log as you iterate on prompts during development — do not fabricate versions post-hoc.
- Include concrete failure examples: "the agent returned blog posts instead of papers" is more useful than "quality was low".
- This file is read by the grader to assess prompt engineering quality.
