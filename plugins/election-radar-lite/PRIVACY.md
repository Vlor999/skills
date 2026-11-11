# Privacy policy: Election Radar Lite

Last updated: 2026-11-07

Election Radar Lite is a Claude plugin made of one skill: instructions only,
carried out by Claude on the user's own machine or Claude session. The author operates no server and collects no data.

## Data the plugin handles

- **Public information about candidates**: names, parties, public statements,
  platforms, poll results and official figures, taken from public sources.
- **The user's questions**: when a question leads to a new glossary entry, the
  question is stored verbatim with that entry (`_data/glossary.json`).
- **Workspace settings**: country, election, language, folder, timezone and
  banned source domains (`radar.config.json`).

## Where it is stored

- In the workspace folder the user chooses on their own machine
  (default `~/Desktop/<Election> <Year>`).
- If the user publishes the index page as a Claude artifact: in that
  artifact's own database, on Anthropic's platform, under the user's account
  and sharing settings.

Nothing is sent to the plugin author. Data stays until the user deletes the
folder or the artifact.

## Third parties contacted

- **Websites of official sources** (electoral authorities, pollsters,
  candidates, statistics offices): Claude sends a plain HTTP GET request to
  the URL being archived, with the User-Agent `election-radar archiver`. The site sees the request and the
  user's IP address.
- **Google Fonts**: the `index.html` Claude writes may load web fonts from
  `fonts.googleapis.com`, which sees the viewer's IP address.
  See [Google's privacy policy](https://policies.google.com/privacy).
- **Anthropic**: Claude itself (web search, artifacts, scheduled tasks) is
  governed by [Anthropic's privacy policy](https://www.anthropic.com/legal/privacy).

## Contact

Questions or requests: open an issue at
<https://github.com/Vlor999/skills/issues>.
