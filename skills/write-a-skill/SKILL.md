---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill.
---

# Writing Skills

Full frontmatter field reference (types, constraints, defaults): [REFERENCE.md](REFERENCE.md).

## Process

1. **Gather core requirements** - ask user about:
   - What task/domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?

2. **Draft the skill** - create:
   - SKILL.md with concise instructions, going through the "Frontmatter Decisions" checklist below to pick only the fields this skill needs
   - Additional reference files if content exceeds 500 lines
   - Utility scripts if deterministic operations needed

3. **Review with user** - present draft and ask:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?
   - Do the frontmatter choices still match how you want to use it?

## Frontmatter Decisions

`name` and `description` are the only fields almost every skill needs; everything else is optional and should only be set if a question below applies. See [REFERENCE.md](REFERENCE.md) for exact syntax/constraints of each field. If the user has no opinion, default to omitting the field rather than guessing a value.

| Question | Field to set |
|---|---|
| Should this be usable as a destructive/workflow-specific action that Claude must never trigger on its own? | `disable-model-invocation: true` |
| Is this background knowledge the user should never invoke directly via `/name`? | `user-invocable: false` |
| Does the skill take input typed after `/name`? | `argument-hint`, plus `arguments` (space-separated names, or a YAML list) if there are several distinct named arguments |
| Does it need to run specific tools without prompting, or must it be barred from certain tools for safety? | `allowed-tools` / `disallowed-tools` |
| Does it need a specific model or reasoning effort regardless of session settings? | `model` / `effort` |
| Should it run in a forked subagent instead of inline? | `context: fork` and `agent` |
| Should it only auto-load for files matching certain globs? | `paths` |
| Does it need lifecycle hooks scoped to this skill? | `hooks` |
| Do its inline `` !`command` `` blocks need PowerShell instead of bash? | `shell: powershell` |

## Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

`REFERENCE.md` is a per-skill naming convention, not a shared file — each skill's `REFERENCE.md` covers that skill's own topic.

## SKILL.md Template

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
argument-hint: "[optional-arg]"  # omit if the skill takes no arguments
---

# Skill Name

## Quick start

[Minimal working example]

## Workflows

[Step-by-step processes with checklists for complex tasks]

## Advanced features

[Link to separate files: See [REFERENCE.md](REFERENCE.md)]
```

## Description Requirements

The description is **the only thing your agent sees** when deciding which skill to load. It's surfaced in the system prompt alongside all other installed skills. Your agent reads these descriptions and picks the relevant skill based on the user's request.

**Goal**: Give your agent just enough info to know:

1. What capability this skill provides
2. When/why to trigger it (specific keywords, contexts, file types)

**Format**:

- Max 1536 chars on its own; shared with `when_to_use` if that field is also set (see [REFERENCE.md](REFERENCE.md))
- Write in third person
- First sentence: what it does
- Second sentence: "Use when [specific triggers]"

**Good example**:

```
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

**Bad example**:

```
Helps with documents.
```

The bad example gives your agent no way to distinguish this from other document skills.

## When to Add Scripts

Add utility scripts when:

- Operation is deterministic (validation, formatting)
- Same code would be generated repeatedly
- Errors need explicit handling

Scripts save tokens and improve reliability vs generated code.

## When to Split Files

Split into separate files when:

- SKILL.md exceeds 100 lines
- Content has distinct domains (finance vs sales schemas)
- Advanced features are rarely needed

## Review Checklist

After drafting the new skill, verify:

- [ ] Description includes triggers ("Use when...")
- [ ] SKILL.md under 100 lines (split into reference files per "When to Split Files" if not)
- [ ] Only the frontmatter fields decided in "Frontmatter Decisions" are set — no unused fields left in
- [ ] If SKILL.md and REFERENCE.md both describe the same constraint (e.g. a char limit), the two agree
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples included
- [ ] References one level deep

Note: this guide (`write-a-skill/SKILL.md`) documents the frontmatter spec in depth and is itself longer than 100 lines — the 100-line guideline targets the skills it helps you author, not this meta-skill.
