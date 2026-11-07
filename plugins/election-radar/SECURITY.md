# Security policy: Election Radar

## Reporting a vulnerability

Report security issues privately through GitHub's private vulnerability
reporting: <https://github.com/Vlor999/skills/security/advisories/new>.

Please include the affected file, the steps to reproduce and the impact. Do not
open a public issue for a security problem.

Reports from Anthropic and from third parties are both welcome. Each report is
acknowledged and investigated; a fix, when needed, is released as a new plugin
version and noted in the advisory.

## Scope

- The skill instructions (`skills/election-radar/*.md`).
- The Python scripts in `skills/election-radar/scripts/`.
- The page template `skills/election-radar/assets/index-template.html`.

## Security properties

- Scripts use the Python standard library only; nothing is installed.
- `fetch_source.py` is the only script that uses the network. It sends one
  HTTP GET to the URL it is given, refuses domains banned in the workspace
  config, and never executes what it downloads.
- Scripts write to the workspace folder passed as `--root` (and the sub-folder
  given by `--dest`, relative to it); archived files are never overwritten or
  deleted.
- The rendered page HTML-escapes every data value before inserting it, and
  `validate_data.py` rejects any source URL that is not `http://` or `https://`.
- No hooks, MCP servers, executables, credentials or telemetry.
