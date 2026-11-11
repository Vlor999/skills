# Coding Agent Skills

This repository stores reusable skills for coding agents.

The goal is to keep these skills in one trusted place, then retrieve or copy
them into other repositories when needed. This avoids pulling instructions from
unknown sources and makes it easier to review what an agent is allowed to load.

## Repository Layout

```text
skills/
  caveman/
    SKILL.md
  fill-pr-template/
    SKILL.md
  grilling/
    SKILL.md
  grill-with-docs/
    SKILL.md
    ADR-FORMAT.md
    CONTEXT-FORMAT.md
  handoff/
    SKILL.md
  llm-council/
    SKILL.md
  oss-compliance-audit/
    SKILL.md
    CHECKLIST.md
    REPORT.md
    scripts/
      site-requests.js
  tdd/
    SKILL.md
    deep-modules.md
    interface-design.md
    mocking.md
    refactoring.md
    tests.md
  tutor/
    SKILL.md
    REFERENCE.md
    EXAMPLES.md
  write-a-rule/
    SKILL.md
  write-a-skill/
    SKILL.md
plugins/
  election-radar/
    .claude-plugin/plugin.json
    README.md
    LICENSE
    skills/
      election-radar/
        SKILL.md
        AUTOMATIONS.md
        DATA-FORMAT.md
        PROJECT-RULES.md
        SOURCES.md
        STATE-TEMPLATE.md
        assets/index-template.html
        scripts/*.py
  election-radar-lite/
    .claude-plugin/plugin.json
    README.md, LICENSE, PRIVACY.md, SECURITY.md, TERMS.md
    skills/
      election-radar-lite/
        SKILL.md
        WORKSPACE.md
        PAGE-SPEC.md
        AUTOMATIONS.md
        DATA-FORMAT.md
        PROJECT-RULES.md
        SOURCES.md
        STATE-TEMPLATE.md
.claude-plugin/
  marketplace.json
```

Each skill lives in its own directory. The required entry point is `SKILL.md`.
Some skills also include supporting documentation that is referenced from the
main skill file. Skills distributed as Claude plugins live under `plugins/`,
listed in the repository marketplace (`.claude-plugin/marketplace.json`).

## Available Skills

| Skill | Purpose |
| --- | --- |
| `caveman` | Enables an ultra-compressed communication mode that keeps technical accuracy while reducing filler and token usage. |
| `election-radar` | Sets up a sourced election-watch workspace (archived official documents, state of play, interactive index page, glossary, scheduled sync automations) and serves as the discussion method inside it. |
| `election-radar-lite` | Instructions-only edition of `election-radar` (no bundled scripts or page template), eligible for Anthropic's plugin directory. |
| `fill-pr-template` | Drafts a pull request description from the current branch diff, commits, and repository PR template. |
| `grilling` | Stress-tests a plan or design by asking focused questions until the decision tree is clear. |
| `grill-with-docs` | Stress-tests a plan against project language and documentation, then updates `CONTEXT.md` and ADRs as decisions are made. |
| `handoff` | Writes a compact handoff document so another agent or future session can continue the work. |
| `llm-council` | Runs any decision or tradeoff through a council of 5 independent AI advisors, anonymous peer-review, and chairman synthesis. |
| `oss-compliance-audit` | Audits an open source project (repo, website, shipped binaries, channels) for GDPR/ePrivacy, legal notice, consumer law, trademarks, licenses and notices, security policy, CRA and platform rules, then fixes what the user approves. |
| `tdd` | Guides test-driven development with a red-green-refactor loop and behavior-focused tests. |
| `tutor` | Explains codebase architecture, technological choices (ADRs), mathematical equations, and algorithms, teaches concepts with interactive quizzes, and exports/synchronizes explored knowledge to a Notion workspace. |
| `write-a-rule` | Helps create or edit `.agents/rules/*.md` files with YAML frontmatter, scoped globs, and concise project-specific guidance. |
| `write-a-skill` | Helps create new skills with the expected structure, metadata, and supporting files. |

## Install In Another Repository

From the repository where you want to use the skills, copy either all skills or
one specific skill into `.agents/skills`.

## Prefered option: npx

```bash
npx skills@latest add Vlor999/skills
```
An interface will ask you what you want. You'll be able to pick the ones that makes sense for you

### Option 1: Get All Skills

```bash
mkdir -p .agents/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Vlor999/skills.git /tmp/coding-agent-skills
git -C /tmp/coding-agent-skills sparse-checkout set skills
cp -R /tmp/coding-agent-skills/skills/* .agents/skills/
```

### Option 2: Get One Skill

Replace `tdd` with the skill you want:

```bash
mkdir -p .agents/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Vlor999/skills.git /tmp/coding-agent-skills
git -C /tmp/coding-agent-skills sparse-checkout set skills/tdd
cp -R /tmp/coding-agent-skills/skills/tdd .agents/skills/
```

### Option 3: Short `npx` Command

If you prefer an `npx` style command, you can use `degit` to copy a single
skill directory:

```bash
mkdir -p .agents/skills
npx degit Vlor999/skills/skills/tdd .agents/skills/tdd
```

Replace `tdd` with any available skill name.

## Use A Skill

Ask your coding agent to use the skill by name:

```text
Use the tdd skill to implement this feature test-first.
```

Or:

```text
Use grilling to challenge this design before we implement it.
```

If your agent supports a global skills directory, you can copy these skills
there instead of copying them into each project. Keep the full skill directory,
not only `SKILL.md`, because some skills depend on sibling reference files.

## Using `election-radar` In Claude Desktop

`election-radar` needs four things: local files and a shell (archive, scripts),
web search, the Artifact tool (live page) and a scheduler (two daily
automations). Claude Desktop in **Cowork** mode provides all four, so that is
the recommended setup.

1. **Install the skill.** Either install the plugin from this repository's
   marketplace (`claude plugin marketplace add Vlor999/skills`, then
   `claude plugin install election-radar@vlor999-skills`), or zip the
   `plugins/election-radar/skills/election-radar/` folder (the folder itself at
   the root of the zip) and upload it in *Settings → Capabilities → Skills*.
   Enable code execution and web search in the same settings.
2. **Init in Cowork.** Open a Cowork session, give it access to the folder that
   will hold the workspace (default `~/Desktop/<Election> <Year>`), and ask for
   it in plain words, e.g. *"Set up a radar for the 2027 French presidential
   election, in French"*. The skill asks for the missing parameters in one
   message, builds the folder, publishes the page and creates the automations.
3. **Automations.** In Cowork they become two scheduled tasks: *local sync*
   (default 07:15) then *page update* (default 07:45). Scheduled tasks only run
   while the computer is awake and Claude Desktop is open, so pick times when
   that is the case.
4. **Discuss.** Two options:
   - **In Cowork, on the workspace folder (recommended).** Claude reads the
     up-to-date state of play and `_data/`, and can archive new sources and
     grow the glossary on disk.
   - **In a Claude Project.** Paste the generated instructions file
     (`instructions-projet.md` / `project-instructions.md`) into the project
     instructions and add the state-of-play file (`00 - …md`) as a project
     file. Project files are static copies: re-upload the state of play after
     the automations change it, and expect glossary or archive updates to be
     limited to what the session can write.
5. **Live page.** The published artifact reads its data from its database,
   which the *page update* task rewrites each morning, so the link stays the
   same and never needs republishing. The local `index.html` in the folder
   works offline as a fallback.

## Security Model

Treat skills as executable instructions for an agent. Before installing or
copying a skill into another repository, review:

- `SKILL.md`
- Any referenced files in the same skill directory
- Any scripts or assets bundled with the skill

This repository is intended to be the reviewed source of truth. Prefer copying
skills from here instead of downloading random prompts or instructions directly
into project repositories.

Recommended practices:

- Keep skills small and readable.
- Avoid hidden behavior or unnecessary scripts.
- Prefer plain Markdown instructions unless a deterministic helper script is
  truly useful.
- Review changes in pull requests before using updated skills in sensitive
  repositories.
- Copy only the skills a repository needs.

## Creating A New Skill

Use `write-a-skill` to create new skills and `write-a-rule` to create or update repository rule files under `.agents/rules/`.

At minimum, create:

```text
skills/my-skill/
  SKILL.md
```

`SKILL.md` should start with front matter:

```md
---
name: my-skill
description: Brief description of what the skill does. Use when the user asks for specific trigger cases.
---
```

Keep the description clear and specific. It is what the agent sees when
deciding whether to load the skill.

## Updating Skills

When changing a skill:

1. Edit the skill in `skills/<skill-name>/`.
2. Keep supporting files next to the skill that uses them.
3. Review the diff carefully, especially instructions that allow file edits,
   shell commands, network access, or credentials.
4. Copy the updated skill into any repositories that should use the new version.

## Notes

This repository does not install skills automatically. It is a source repository
for reviewed skill definitions that can be copied into coding-agent
environments.
