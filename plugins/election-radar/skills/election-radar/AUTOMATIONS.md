# The two automations

Fill every `{{...}}` from `radar.config.json`, then translate the prompt into the workspace language before creating the task (the task's reports are read by the user). Each prompt is self-contained: a scheduled run starts with no memory of this conversation.

Order matters: **local sync** archives new documents first, **page update** then turns them into figures about 30 minutes later.

Names: `{{title}}: local sync` and `{{title}}: daily update`, or their translation.

---

## 1. Local sync (default {{local_sync_time}}, {{timezone}})

```text
You maintain the election workspace "{{title}}" ({{election}} {{year}}, {{country}}), language {{lang}}.
Workspace folder: {{root}}. Rules and file formats: radar.config.json, the skill election-radar
(SKILL.md, SOURCES.md, DATA-FORMAT.md). Write everything the user reads in {{lang}}.

1. Read radar.config.json, sources.json and "{{state_file}}".
2. Search for documents published since the last run (date in sources.json): new or updated
   platforms and programme documents of each candidate in _data/candidates.json, new candidates
   declaring, new official poll notices (primary source in SOURCES.md for {{country}}), new official
   budget or economic figures.
3. Archive each new official document with scripts/fetch_source.py into the right folder
   (candidate folder, polls folder, context folder), with its own document date.
   Never use a banned domain. Never delete or overwrite an archived file.
4. Update "{{state_file}}": the "What changed" section with today's date and one line per new
   document (link + local path), and any line of the state of play that is now outdated.
5. Do not edit _data/*.json and do not touch the page: the daily update does that.
6. Report in {{lang}}, five lines max: what was archived, what was searched and not found.
   If nothing is new, say so in one line.
```

---

## 2. Daily update (default {{page_update_time}}, {{timezone}})

```text
You maintain the election workspace "{{title}}" ({{election}} {{year}}, {{country}}), language {{lang}}.
Workspace folder: {{root}}. Live page: {{page_url}} (collection "site", documents "dataset",
"candidates" and "glossary"). Rules and formats: the skill election-radar (SKILL.md, SOURCES.md, DATA-FORMAT.md).
Write everything the user reads in {{lang}}.

1. Read _data/dataset.json, _data/candidates.json and the documents archived since meta.checkedAt
   (sources.json).
2. Polls: for each pollster, check the primary source for a newer wave. Replace its entry with the
   new wave (all scenarios, runoffs if any). Never estimate a missing number.
3. Candidates: update declaration status, programme status and documents, key proposals, each
   with its source and document date. When a proposal changes the picture, rewrite that
   candidate's analysis (idea, feasibility, dynamics) with the same grid as the others.
4. Context: update a figure only when its official source publishes a newer one.
5. Set meta.checkedAt to today; set meta.updated to today only if a figure changed. Add one
   changelog line per change, naming the source. If nothing changed, add nothing.
6. Glossary: if a change introduces a technical term not yet in _data/glossary.json, add it with
   scripts/glossary.py (sourced definition, --related candidate, no --question). Never edit the
   questions recorded from the user's conversations.
7. Run scripts/validate_data.py (must end with 0 error) then scripts/render_index.py.
8. If the page URL is set: write the three documents with the Artifact tool (write_db batch,
   collection "site", documents "dataset", "candidates", "glossary"). Do not republish the page.
9. Report in {{lang}}, five lines max: what changed (including new glossary terms), with sources;
   or "nothing new" in one line.
```

---

## Creating them

- **Cowork**: scheduled tasks, one per prompt, daily at the given time, with access to the workspace folder.
- **Claude Code**: a routine or `/schedule` per prompt, run from the workspace folder with this skill installed.
- **Elsewhere**: cron or a CI schedule calling `claude -p "<prompt>"` from the workspace folder.

If the scheduler cannot reach the Artifact tool, the daily update still refreshes the local `index.html`; tell the user the published page will only change when the update runs where the tool exists.
