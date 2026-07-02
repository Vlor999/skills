# SKILL.md frontmatter reference

## Base rules

- The file must be named **exactly** `SKILL.md` (case-sensitive).
- Required structure: YAML frontmatter between two `---` lines, followed by markdown content.
- **No field is strictly required**, but `description` is strongly recommended (otherwise Claude has no way to know when to trigger the skill automatically).
- The skill's **directory** name becomes the typed command (`.claude/skills/my-skill/SKILL.md` → `/my-skill`), except for a plugin-root `SKILL.md`, where the `name` field becomes the command name instead.
- Body content: keep it concise (< ~500 lines recommended); content is loaded in full on every invocation and stays in context for the rest of the session.

## Frontmatter fields table

| Field | Required? | Type | Constraints | Purpose | Default |
|---|---|---|---|---|---|
| `name` | No | string | No documented length/character limit | Name shown in the skill listing. Does **not** change the command name (except plugin-root `SKILL.md`, where it becomes the command name) | Directory name |
| `description` | Recommended | string | Max **1536 characters** on its own; if `when_to_use` is also set, the two are concatenated and the combined text must stay under 1536 | What the skill does and when to use it; used by Claude to decide when to invoke it automatically | First paragraph of the markdown body |
| `when_to_use` | No | string | Shares the 1536-character cap with `description` (see above) | Extra context (trigger phrases, example requests), appended to `description` | (none) |
| `argument-hint` | No | string | Free text | Autocomplete hint for expected arguments (e.g. `[issue-number]`) | (none) |
| `arguments` | No | space-separated string, or YAML list | Names must be valid identifiers | Named positional arguments, substituted via `$name` in the content | (none) |
| `disable-model-invocation` | No | boolean | `true` / `false` | `true` = Claude cannot trigger the skill on its own; useful for workflows invoked only via `/name` | `false` |
| `user-invocable` | No | boolean | `true` / `false` | `false` = hidden from the `/` menu; useful for background knowledge the user shouldn't invoke directly | `true` |
| `allowed-tools` | No | space/comma-separated string, or YAML list | Must be valid tool names, can include permission patterns (`Bash(git add *)`) | Tools usable without a permission prompt while this skill is active. Doesn't restrict anything, only adds to existing permissions. For project skills, only applies after workspace trust is accepted | (none) |
| `disallowed-tools` | No | space/comma-separated string, or YAML list | Must be valid tool names | Tools removed from the available pool while this skill is active (useful for autonomous skills). The restriction is lifted on the next message | (none) |
| `model` | No | string | Must match values accepted by `/model`, or `inherit` | Model used while this skill is active. Applies only for the current turn, not persisted | Session model |
| `effort` | No | `low` \| `medium` \| `high` \| `xhigh` \| `max` | Depends on the levels available for the model | Reasoning effort level while this skill is active | Inherited from session |
| `context` | No | string | Must be `fork` if set | `fork` = runs in a forked subagent; the skill's content becomes that subagent's prompt | Inline context |
| `agent` | No | string | Must match an existing subagent type (`Explore`, `Plan`, `general-purpose`, or a custom one in `.claude/agents/`) | Subagent type used if `context: fork` | `general-purpose` |
| `hooks` | No | YAML object (list of hook configs) | Same format as regular hooks | Hooks scoped to this skill's lifecycle | (none) |
| `paths` | No | comma-separated string, or YAML list | Glob patterns | Limits automatic activation of the skill to files matching the patterns | All paths |
| `shell` | No | `bash` \| `powershell` | `powershell` requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` on Windows | Shell used for `` !`command` `` and ` ```! ` blocks in the skill | `bash` |

## Visibility combinations (`disable-model-invocation` × `user-invocable`)

| `disable-model-invocation` | `user-invocable` | Result |
|---|---|---|
| `false` (default) | `true` (default) | Both Claude and the user can invoke the skill |
| `true` | `true` | Only the user can invoke it via `/name` (Claude never triggers it on its own) |
| `false` | `false` | Only Claude can invoke it automatically (absent from the `/` menu) |
| `true` | `false` | No one can invoke it (its description isn't even loaded into context) |

These behaviors can be overridden via `skillOverrides` in `settings.json` (`"on"`, `"name-only"`, `"user-invocable-only"`, `"off"`).

## Scope: personal / project / plugin

| Location | Scope | Notes |
|---|---|---|
| `~/.claude/skills/` | Personal | Available across all projects |
| `.claude/skills/` (in repo) | Project | Available only in that project; `allowed-tools` only takes effect after workspace trust is accepted |
| `plugin/skills/` | Plugin | Namespaced by plugin (`/my-plugin:my-skill`); a plugin-root `SKILL.md` is special (see `name` field) |
| Managed / enterprise | Global | Can override personal and project skills; the `disableSkillShellExecution` policy can disable `` !`command` `` execution |

## Substitutions available in the markdown body

- `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N` — raw positional arguments
- `$name` — named argument declared in `arguments`
- `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}` — skill environment variables
- `` !`command` `` — inline shell execution before the skill is sent to Claude
- ` ```! ` (fenced block) — multi-line shell execution

## Content lifecycle

- **Descriptions** of all skills are always loaded into context (for discovery).
- **Full content** is only loaded on invocation, then stays in context for the rest of the session.
- On auto-compaction, only the first **5000 tokens** of each skill are re-attached; all skills share a combined **25,000-token** budget.
