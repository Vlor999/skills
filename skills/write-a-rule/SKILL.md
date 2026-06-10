---
name: write-a-rule
description: Create or edit Markdown rule files under `.agents/rules/` with YAML frontmatter, scoped globs, and concise actionable guidance. Use when the user asks to write a rule, create a rule.md file, add repository rules, document agent rules, or update `.agents/rules/` instructions.
---

# Writing Rule Files

## Overview

Rule files live in `.agents/rules/` and use Markdown with YAML frontmatter. Create rules that are short, concrete, and scoped to the files or workflows they govern.

## Workflow

1. Identify whether the rule is global or file-scoped.
2. Choose a clear filename under `.agents/rules/`, usually kebab-case plus `.md`.
3. Write YAML frontmatter with `description`, optional `globs`, and `alwaysApply`.
4. Write the rule body in Markdown with imperative, project-specific instructions.
5. Keep examples focused on file layout, naming, command conventions, or other details that remove ambiguity.

## Frontmatter

Use this structure for scoped rules:

```md
---
description: Short description of what the rule covers
globs:
  - "**/*.py"
alwaysApply: false
---
```

Use this structure for global repository rules:

```md
---
description: General repository instructions
alwaysApply: true
---
```

Fields:

- `description`: Summarize what the rule covers.
- `globs`: Add only when the rule applies to specific files or directories.
- `alwaysApply`: Use `true` for global project rules and `false` for scoped rules.

## Writing Guidelines

- Keep rules concise and actionable.
- Use imperative language: "Use pytest", "Avoid broad exceptions", "Keep changes focused".
- Prefer project-specific conventions over generic advice.
- Group related guidance under clear headings.
- Avoid long explanations unless an example makes the rule clearer.
- Do not use `globs` for rules that apply to the whole repository.

## Template

```md
---
description: Short description
globs:
  - "path/or/pattern/**"
alwaysApply: false
---

# Rule title

## Section name

- First rule.
- Second rule.
- Third rule.
```

## Example

```md
---
description: Testing conventions for Python code
globs:
  - "**/*.py"
  - "tests/**/*.py"
alwaysApply: false
---

# Testing conventions

- Use pytest.
- Add or update tests for every behavior change.
- Prefer testing observable behavior over implementation details.

## Test layout

- Use a mirrored test structure: the test tree should mirror the source tree.
```
