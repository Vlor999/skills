# Election Radar

Election Radar sets up a sourced election-watch workspace for any country,
election and year, in the language you choose, and then serves as the working
method for discussing the campaign inside it.

## What it builds

- **Local archive**: a folder holding official documents (platforms, poll
  notices, budget and economic figures) in their original format, sorted by
  candidate, with a `sources.json` manifest recording each file's URL, SHA-256,
  fetch date and document date.
- **State of play**: a short Markdown page (`00 - …md`) that a person or a
  future session reads first.
- **Index page**: `index.html`, rebuilt from `_data/*.json`: candidates on an
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

- **Python scripts** (standard library only), run by Claude from the skill
  folder: `init_workspace.py`, `fetch_source.py`, `validate_data.py`,
  `render_index.py`, `glossary.py`. No hooks, no MCP server, no package install.
- **Network**: `fetch_source.py` downloads only the URL Claude passes to it
  (an official document found by web search), with the User-Agent
  `Mozilla/5.0 (election-radar archiver)`, and refuses domains banned in the
  workspace config. No other script uses the network.
- **Web fonts**: the generated `index.html` loads fonts from Google Fonts.
- **Files**: writes only inside the workspace folder the user chooses
  (default `~/Desktop/<Election> <Year>`). Archived files are never overwritten
  or deleted; a changed document is saved next to the old one with a date.
- **Artifact database** (optional): when a page is published, the automations
  write three documents (`dataset`, `candidates`, `glossary`) to that
  artifact's own database. No data is sent anywhere else.

## Install

In Claude Code:

```text
/plugin install election-radar --marketplace Vlor999/skills
```

Or from a shell:

```bash
claude plugin marketplace add Vlor999/skills
claude plugin install election-radar@vlor999-skills
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
