# Security policy: Election Radar Lite

## Reporting a vulnerability

Report security issues privately through GitHub's private vulnerability
reporting: <https://github.com/Vlor999/skills/security/advisories/new>.

Please include the affected file, the steps to reproduce and the impact. Do not
open a public issue for a security problem.

Reports from Anthropic and from third parties are both welcome. Each report is
acknowledged and investigated; a fix, when needed, is released as a new plugin
version and noted in the advisory.

## Scope

The skill instructions in `skills/election-radar-lite/*.md` and the plugin
manifest.

## Security properties

- The plugin contains only Markdown, JSON, a license and a PNG icon: no
  scripts, hooks, MCP servers, executables, credentials or telemetry.
- The instructions tell Claude to download only official documents it found,
  to refuse domains banned in the workspace config, and never to execute or
  open as code anything it downloads.
- Writes go to the workspace folder the user chooses; archived files are never
  overwritten or deleted.
- The page specification requires every data value to be HTML-escaped and only
  `http://` or `https://` source URLs, checked by the validation checklist.
