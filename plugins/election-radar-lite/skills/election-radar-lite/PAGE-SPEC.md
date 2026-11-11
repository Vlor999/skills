# Index page specification

You write `index.html` yourself from `_data/*.json`, the first time at init and again whenever the data changes locally. Keep the same structure from one build to the next so the user finds the page they know. The page is one self-contained HTML file: inline CSS and JavaScript, no external scripts; web fonts from Google Fonts are allowed.

## Data

- Embed the three data files in the page (`dataset`, `candidates`, `glossary`) as JSON inside a `<script type="application/json">` block, escaping `</` as `<\/`, so the page works when opened straight from disk.
- On a published page with the `db` capability, read collection `site`, documents `dataset`, `candidates` and `glossary`, and re-render when they change. Use the database copy of `dataset` only if its `meta.updated` is not older than the embedded one; use `candidates` only if its `list` is not empty. If the database does not answer within 10 seconds, show the *offline* label and keep the embedded data. Load the Artifact `db` capability guidance before writing this code.
- Insert every data value as text, or HTML-escaped (`& < > " '`). Links come only from source objects `{t, u}` whose URL passed validation, opened in a new tab with `rel="noopener"`.

## Layout

A sticky top bar with a ☰ button (left) that opens a menu of sub-pages, and the page title with the current sub-page name. Each sub-page is a view selected by the URL hash, using the slugs below; an unknown hash shows the first view. Close the menu with Escape or a click outside; arrow keys move within it. The runoff entry appears only when `second` has data.

| View | Hash slug (fr / en / es / de) | Content |
|---|---|---|
| The field and candidate cards | `radar` | header (eyebrow, title, lede, "data as of" and "checked on" dates), scenario buttons, the axis, the selected candidate's card |
| Runoff, or Seats when `system` is not `two-round` | `second-tour` / `runoff` / `segunda-vuelta` / `stichwahl` | one bar per tested duel, pollster and fieldwork, `secondNote` under the bars |
| Budget context | `contexte` / `context` / `contexto` / `kontext` | one panel per `context` item: label, value, note, source link and date |
| Polls used | `sondages` / `polls` / `encuestas` / `umfragen` | table: pollster, client, fieldwork, published, sample, number of scenarios, source link |
| Glossary | `glossaire` / `glossary` / `glosario` / `glossar` | search box (matches term, aliases and definition, accents ignored), terms sorted alphabetically |
| Method and log | `methode` / `method` / `metodo` / `methode` | `meta.method` blocks with their links, then `changelog`, newest first |

A hash `#g-<term id>` opens the glossary on that term.

## The axis

- Candidates in the order of `candidates.json` → `list`, evenly spaced from left to right, with "◀ left" and "right ▶" labels. Neighbouring candidates of the same `family` share a labelled band.
- Scenario buttons: "All scenarios" plus one per `meta.scenarios`. A hypothesis belongs to a scenario when every candidate in `with` appears in its results and none in `without` does.
- For each candidate: for each poll, average the candidate's values over the poll's hypotheses that belong to the selected scenario; the bubble shows the average of those per-poll averages, with its size proportional to it and the percentage written on it. Also keep the minimum and maximum across all hypotheses. A candidate absent from every matching hypothesis shows as "not tested in this scenario", never as 0.
- Clicking a bubble selects the candidate and shows the card; `meta.defaultSelected` is selected first.

## The candidate card

In this order: name, party and family, declared or not with `statusSrc`, programme status and documents (with document dates and notes), key proposals with their sources, the first-round figure (average, number of pollsters, range across scenarios, one line per poll), the four-step `mecanisme` strip (measure, intended effect, what must hold, risk, with the note that the measure is sourced and the rest is analysis to challenge), the analysis (idea, feasibility, dynamics) with `arefs`, and the school of thought (`courant`, marked "claimed" only when `claimed` is true).

Underline the first occurrence of each glossary term or alias (3 characters or more, whole words, case and accents ignored) in the card's text, linking to `#g-<id>` with the definition as tooltip.

## Glossary entries

Term, aliases, definition, sources, "see also" links, the first question it came from (with date, and "+n" when there are more), and buttons for `related` candidates that open their card.

## Interface texts

Use the workspace language. Built in for fr, en, es and de; `meta.labels` overrides any text. The texts are: view names and the menu labels; the axis title and hint; left/right; all scenarios; card; runoff and seat-projection titles; context, polls, method and log titles; data-as-of, checked-on, daily-update and offline labels; the polls table headers; card headings (platform and documents, key proposals, analysis, idea, feasibility, dynamics, school of thought, first round, average of, pollsters, range, not tested, no platform, programme statuses, declared, not declared, source, document dated); the mechanism strip headings and note; the glossary title, search placeholder, empty message, "asked in", "see also", "candidates", "terms"; and the footer: "Page maintained by an agent. Every figure links to its source; report errors."

## Style

Light and dark themes from `prefers-color-scheme`, readable at phone width (16 px side margins, no horizontal scroll), candidate colours from `color`, visible keyboard focus, and `prefers-reduced-motion` respected.

## Candidate pages (optional)

You may also write `<candidates>/<id>/fiche.html` for each candidate: the same card, plus links to the local copies of the documents archived for that candidate (from `sources.json`), so they open even if the original page disappears.
