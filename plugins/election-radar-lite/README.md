# Election Radar Lite

Election Radar Lite sets up a sourced election-watch workspace for any country,
election and year, in the language you choose, and then serves as the working
method for discussing the campaign inside it.

This is the instructions-only edition of
[Election Radar](../election-radar/README.md): it ships Markdown and JSON only,
no scripts and no page template. Claude carries out the archiving, validation,
glossary and page-building procedures itself, with its own tools. The full
edition does the same work with deterministic scripts; install one or the
other, not both.

## What it builds

- **Local archive**: a folder holding official documents (platforms, poll
  notices, budget and economic figures) in their original format, sorted by
  candidate, with a `sources.json` manifest recording each file's URL, SHA-256,
  fetch date and document date.
- **State of play**: a short Markdown page (`00 - …md`) that a person or a
  future session reads first.
- **Index page**: `index.html`, written by Claude from `_data/*.json` following
  a page specification: candidates on an
  indicative left-right axis, poll averages, runoffs or seat projections,
  candidate cards, budget context. A ☰ menu splits it into sub-pages, each with
  its own address in the workspace language (`#glossaire`, `#glossary`…).
  Optionally published as a Claude artifact that reads its data from the
  artifact's database.
- **Glossary**: every technical term met in the discussion, with a sourced
  neutral definition and the question it came from.
- **Two automations**: *local sync* (archive new documents) then *page update*
  (refresh figures and the live page), created with the scheduler available
  (Cowork scheduled tasks, Claude Code routines, or cron with `claude -p`).

## Editorial rules

- No figure without a source URL and document date; missing data is reported
  as missing, never estimated.
- Primary sources first (official poll notices, candidates' own platforms,
  statistics offices).
- Same sections, depth and feasibility criteria for every candidate. Partisan
  media are refused as sources, whatever their side; the list is set per
  workspace.
- No voting recommendation. The skill analyses ideas, feasibility and dynamics;
  the user decides.

## What it runs, fetches and writes

Disclosed for review and for users:

- **No bundled code**: the plugin contains only Markdown, JSON, a license and
  its icon. No scripts, hooks, MCP servers or package installs.
- **Network**: to archive an official document, Claude downloads the URL with
  its own tools (web fetch, or an HTTP download such as `curl` in a shell),
  with the User-Agent `election-radar archiver`, and refuses domains banned in
  the workspace config. Downloaded files are stored, never executed.
- **Web fonts**: the `index.html` Claude writes may load fonts from Google
  Fonts.
- **Files**: writes only inside the workspace folder the user chooses
  (default `~/Desktop/<Election> <Year>`). Archived files are never overwritten
  or deleted; a changed document is saved next to the old one with a date.
- **Artifact database** (optional): when a page is published, the automations
  write three documents (`dataset`, `candidates`, `glossary`) to that
  artifact's own database. No data is sent anywhere else.

## Install

In Claude Code:

```text
/plugin install election-radar-lite --marketplace Vlor999/skills
```

Or from a shell:

```bash
claude plugin marketplace add Vlor999/skills
claude plugin install election-radar-lite@vlor999-skills
```

## Best setup

Claude Desktop in **Cowork** mode provides everything the skill uses: local
files and shell, web search, the Artifact tool and scheduled tasks. Scheduled
tasks run only while the computer is awake and Claude Desktop is open.

Start with a request such as: *"Set up a radar for the 2027 French presidential
election, in French."*

## Example requests

- *"Set up a radar for the 2027 French presidential election, in French."*
- *"Track the 2026 US midterms in English, local folder ~/Documents/Midterms."*
- Inside the workspace: *"What does structural deficit mean, and does
  candidate X's savings plan hold up against it?"*

## Limitations

- Analyses and glossary definitions are written by Claude and can be wrong;
  every figure links to its source so it can be checked.
- The left-right order of candidates is indicative and stated as such.
- The skill never recommends a vote.
- Automations need a scheduler (Cowork scheduled tasks, Claude Code routines
  or cron); without one, the prompts are saved to the workspace to run by hand.
- The live page needs the Artifact tool; otherwise only the local
  `index.html` is produced.
- Without scripts, archiving, validation and page building depend on Claude
  following the procedures; results can vary more than with the full edition.

## Support

Questions and bug reports: <https://github.com/Vlor999/skills/issues>.

## Security

Report vulnerabilities privately, as described in [SECURITY.md](SECURITY.md).

## Privacy

See the [Privacy policy](PRIVACY.md): what the plugin stores, where, and which
third parties it contacts.

## Terms

See the [Terms of use](TERMS.md).

## License

MIT, see [LICENSE](LICENSE).
