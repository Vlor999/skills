---
name: election-radar
description: Sets up a sourced election-watch workspace for any country, election and year, in the user's chosen language - a local folder archiving official documents (platforms, poll notices, budget figures) in their original format, a state-of-play page, an interactive index page (candidates on a left-right axis, poll averages, runoffs, candidate cards, budget context), a sourced glossary that grows with every question, and two scheduled automations that keep the archive and the page up to date. Then serves as the working method for discussing the campaign inside that workspace. Use when the user wants to follow, track, monitor, compare or "set up a space/project/radar" for an election, campaign, candidates, polls or platforms (présidentielle, législatives, general election, midterms, Bundestagswahl, elecciones...), even if they don't say "radar", and whenever they ask about candidates or platforms inside a project created by this skill.
---

# Election radar

Two phases. **Init** builds the workspace once. **Discuss** is how you work in it afterwards, every day, in the user's language.

The workspace has three layers, and each answers a different need:

1. **Local folder**: the archive. Official documents in their original format, sorted by candidate, poll notices, context figures, and a manifest of where each file came from. It survives broken links and deleted pages.
2. **State-of-play page** (`00 - …md`): the starting point a human or a future session reads first. Plain Markdown, also uploaded as a project file.
3. **Index page** (`index.html`, optionally published with a live database): the visual overview, rebuilt from `_data/*.json`.
4. **Glossary** (`_data/glossary.json`, rendered as `Glossaire.md` / `Glossary.md` and as a searchable section of the page): every technical term met in the discussion, with a sourced definition and the question it came from. Terms are underlined in the candidate cards and link to their entry.

Plus **two automations**: *local sync* (documents and state of play) runs first, *page update* (figures and live page) runs after it.

## Non-negotiable rules

These hold in both phases. They exist because an election workspace is only useful if the user can trust every line of it, and because it touches people's votes.

- **No figure without a source.** Every percentage, amount, date or quote carries a URL and the date of the document. No source found means no figure, and you say it is missing. Never estimate a poll number, never fill a gap from memory.
- **Primary sources first**: the official poll notice over the article about it, the candidate's own platform over a summary, the statistics office over a news story. See [SOURCES.md](SOURCES.md).
- **Date the document, not just the visit.** An old booklet or last year's counter-budget is labelled with its own date, so it is never presented as the 2027 platform.
- **Same treatment for every candidate**: same sections, same depth, same criteria for feasibility. Partisan media are not used as sources, whatever their side (the banned list is in `radar.config.json`).
- **No voting recommendation.** You analyse ideas, feasibility and dynamics; the user decides.
- **Everything the user reads is in the workspace language** (`lang` in the config): pages, state of play, changelogs, automation reports, discussion. Sources stay in their original language.

## Phase 1: Init

### 1. Check what the environment can do

Say in two lines what you can and cannot set up here, then carry on with what works:

| Capability | Used for | If missing |
|---|---|---|
| Local filesystem + shell | folder, scripts | build the folder in the sandbox and hand it over as a zip |
| Web search / fetch | research | stop: the skill needs it |
| Artifact tool with `db` capability | published page with live data | keep the local `index.html` only |
| Scheduled tasks (Cowork scheduled tasks, Claude Code routines or `/schedule`, cron + `claude -p`) | the two automations | write the prompts to `AUTOMATIONS.md` in the workspace and tell the user where to paste them |

### 2. Get the parameters

Take what the user already said; ask only for the rest, in **one** message (use tappable choices if available):

- country, election type, year (and the vote date if already set)
- language of the workspace (default: the language the user writes in)
- local folder (default: `~/Desktop/<Election> <Year>`)
- sources to refuse beyond the defaults, sources accepted with care
- discussion style: the defaults in [PROJECT-RULES.md](PROJECT-RULES.md) (sourced, sparring partner, idea + feasibility + dynamics, schools of thought). Show them in one line and ask if anything changes.
- times for the two automations and the timezone (default: local sync 07:15, page update 07:45)

Then run:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/init_workspace.py --root "<folder>" --country "<country>" \
  --election "<election>" --year <year> --lang <lang> --tz <tz> --system <two-round|single-round|proportional|other> \
  --ban <domain> [--ban <domain> ...]
```

`--system` decides what the runoff section shows (runoff duels for two-round systems, seat projections otherwise). If you don't know the system yet, find it first (step 3).

### 3. Research, in this order

Each step feeds the next. Keep a running list of what you could not find.

1. **Electoral framework**: official calendar, voting system, candidacy rules (signatures, deposits, deadlines), from the electoral authority.
2. **Field of candidates**: declared candidates, then likely ones that pollsters test. A candidate is "declared" only with a source showing the declaration.
3. **Polls**: for each pollster, its latest wave only, from the primary source listed in SOURCES.md. Record every scenario (hypothesis) separately: candidate lists change between scenarios, and averaging across them is what the page does, not you.
4. **Platforms and documents**: official site, PDFs, budget documents. Download each with `fetch_source.py` (below). Mark status `full`, `partial` or `none`.
5. **Context**: the budget and economic constraint every platform faces (debt, deficit, growth, unemployment, whatever binds in this country), from the statistics office, fiscal council, central bank, IMF or Eurostat. Note the date of each figure. If an independent think tank plans to cost the platforms, record when.

Archive every official document you rely on:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/fetch_source.py --root "<folder>" --url "<url>" \
  --dest "<candidates folder>/<id>" --name "<short-name>" --title "<title>" --doc-date <YYYY-MM-DD> --publisher "<who>"
```

Polls go in the polls folder, context documents in the context folder. The script keeps the original format, skips duplicates, never overwrites, and refuses banned domains.

### 4. Write the data, validate, render

Fill `_data/dataset.json` and `_data/candidates.json` following [DATA-FORMAT.md](DATA-FORMAT.md). Order candidates from left to right by the usual classification of their party family (and say in `meta.method` that this order is indicative). For each candidate, write the analysis in three parts (idea, feasibility, dynamics) with reference links, and the school of thought it relates to, marked as your reading unless the candidate claims it.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/validate_data.py --root "<folder>"   # must end with 0 error(s)
python ${CLAUDE_SKILL_DIR}/scripts/render_index.py --root "<folder>"
```

Fix every error before going on. Warnings are fine if you can explain them.

Seed the glossary with the 8 to 15 terms a reader needs to follow this election and that you used in the data: voting-system words (runoff, sponsorships, threshold, list vote…), the budget terms of the context section (structural deficit, debt-to-GDP…), and terms that recur in the platforms. One `glossary.py add` per term (see Phase 2), no `--question` since none was asked.

### 5. Write the state of play

Write `<folder>/00 - <state of play>.md` (exact name in `radar.config.json` → `folders.state`) with the template in [STATE-TEMPLATE.md](STATE-TEMPLATE.md), in the workspace language. It is short: links, ranges, what exists and what is missing. Every number in it comes from `_data`.

### 6. Publish the page (if the Artifact tool is available)

1. Call the Artifact tool with action `capabilities` and read how the `db` capability is declared and used.
2. Copy `index.html` to the outputs folder and publish it with `db` declared, a title from `meta.title`, one emoji favicon.
3. Write the three database documents with `write_db` (one `batch`): collection `site`, doc `dataset` (content of `dataset.json`), doc `candidates` (content of `candidates.json`) and doc `glossary` (content of `glossary.json`).
4. Store the page URL in `radar.config.json` → `page.url`.

The page reads the database first and falls back on embedded data, so the automations only need to write the database, never republish.

### 7. Create the two automations

Fill the two prompts in [AUTOMATIONS.md](AUTOMATIONS.md) with the workspace values, then create them with whatever scheduler the environment has. Local sync first, page update about 30 minutes later. Write the task names and times into `radar.config.json` → `automations`. If you cannot schedule, save the filled prompts to `<folder>/AUTOMATIONS.md` and give the user the exact steps.

### 8. Hand over

In the workspace language, short:

- the folder path, the page link, the two automations and their times
- what to put in the discussion project: the instructions file (`folders.instructions`, generated from [PROJECT-RULES.md](PROJECT-RULES.md)) as project instructions, the state-of-play file as a project file
- where the glossary lives, and that it will grow with their questions
- what is missing (platforms not published, pollsters not found, figures without a source) and when it is expected, if known

## Phase 2: Discuss

When the user talks about the election inside the workspace (or a project holding its state of play):

1. Read the state of play, then `_data/*.json` or the live page database, before answering. Your knowledge of the campaign is older than the workspace; the workspace wins.
2. Answer with [PROJECT-RULES.md](PROJECT-RULES.md): sourced, the whole picture (idea, feasibility given the budget context, dynamics: financing, coalitions, runoff transfers), a sparring partner who disagrees when the evidence says so, links to schools of thought.
3. If the question needs a fact the workspace lacks, search, archive the source with `fetch_source.py`, and update `_data` (validate, render, write the database, add a changelog line) so the next answer starts from it.
4. **Grow the glossary.** After each answer, add every term that the user asked about ("c'est quoi…", "what does … mean") or that your answer relied on and that a non-specialist would not know. Check `glossary.py list` first: an existing term gets the new question appended (and a better definition only with a source), never a duplicate.

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/glossary.py --root "<folder>" add --term "<term in workspace language>" \
     --def "<one or two plain sentences, no jargon inside the definition>" --src "<label>|<url>" \
     [--alias "<other name or acronym>"] [--related <candidate id>] [--see "<other term>"] --question "<the user's question, verbatim>"
   ```

   The definition is neutral and sourced (statistics office, official glossary, encyclopaedia entry with references); what a candidate does with the concept goes in the candidate's card, not in the definition. Then validate, re-render and write `site/glossary` to the page database. Mention new terms in one short line at the end of the answer ("Ajouté au glossaire : …"), nothing more.
5. Never change a figure without a new source; record every change in `changelog`.
