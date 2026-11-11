# Workspace procedures

These procedures replace scripts: you carry them out with your own tools. Write JSON as UTF-8, indented by 2 spaces, without escaping non-ASCII characters. Dates are ISO `YYYY-MM-DD`.

## Create the workspace

1. If `<root>/radar.config.json` already exists, stop: the workspace is initialised; edit it instead.
2. Pick the folder names from the workspace language (first two letters of `lang`; any other language uses `en`):

   | key | fr | en | es | de |
   |---|---|---|---|---|
   | candidates | `Candidats` | `Candidates` | `Candidatos` | `Kandidaten` |
   | polls | `Sondages` | `Polls` | `Encuestas` | `Umfragen` |
   | context | `Contexte` | `Context` | `Contexto` | `Kontext` |
   | data | `_data` | `_data` | `_data` | `_data` |
   | state | `00 - État des lieux.md` | `00 - State of play.md` | `00 - Estado de la cuestión.md` | `00 - Lagebild.md` |
   | instructions | `instructions-projet.md` | `project-instructions.md` | `instrucciones-proyecto.md` | `projekt-anweisungen.md` |
   | glossary | `Glossaire.md` | `Glossary.md` | `Glosario.md` | `Glossar.md` |

3. Create the folders `candidates`, `polls`, `context` and `data` under `<root>`.
4. Write `<root>/radar.config.json`:

   ```json
   {
     "title": "Radar <election> <year>",
     "country": "<country>", "election": "<election>", "year": 2027,
     "lang": "<lang>", "timezone": "<tz>",
     "system": "two-round | single-round | proportional | other",
     "folders": { "candidates": "…", "polls": "…", "context": "…", "data": "_data",
                  "state": "…", "instructions": "…", "glossary": "…" },
     "sources": { "banned_domains": ["<lowercase domains, sorted>"], "with_care": ["wikipedia.org"] },
     "page": { "url": null, "db_docs": ["site/dataset", "site/candidates", "site/glossary"] },
     "automations": { "local_sync": null, "page_update": null },
     "created": "<today>"
   }
   ```

5. Write the empty data files, only if they don't exist:
   - `_data/dataset.json`: `meta` with title, country, election, year, lang, system, `updated` and `checkedAt` set to today, empty `lede`, empty `scenarios` and `method`; empty `polls`, `second` and `context`; `changelog` with one entry `{"date": "<today>", "note": "init"}`.
   - `_data/candidates.json`: `{"list": []}`
   - `_data/glossary.json`: `{"terms": []}`
   - `<root>/sources.json`: `{"files": []}`

## Archive a document

Goal: a local copy of each official document, in its original format, that is never overwritten, with a manifest entry saying where it came from.

1. **Refuse banned sources.** If the URL's host equals a domain in `sources.banned_domains` or ends with `.` + that domain, do not download it, and say so.
2. **Download** the URL into memory or a temporary file, following redirects. With a shell, a plain HTTP download tool works (for example `curl -fsSL -A "election-radar archiver" -o <tmp> "<url>"`). Never execute or open as code anything you download.
3. **Choose the extension** from the response's content type (`.pdf`, `.html`, `.json`, `.csv`, `.txt`, `.docx`, `.xlsx`, `.doc`, `.xls`, `.png`, `.jpg`), else from the URL path, else `.bin`.
4. **Skip duplicates.** Compute the file's SHA-256 (`shasum -a 256` or `sha256sum`). If an entry in `sources.json` has the same `sha256`, stop: the document is already archived (status *unchanged*).
5. **Never overwrite.** The target is `<dest>/<short-name><ext>`, where `<dest>` is the candidate's folder (`<candidates>/<candidate id>`), the polls folder or the context folder, and `<short-name>` uses letters, digits, `-`, `_`, `.` and spaces only. If that file exists, or the same URL is already in the manifest, save as `<short-name>_<today><ext>` instead (status *updated*). Never delete or replace an archived file.
6. **Log it.** Append to `sources.json` → `files`:

   ```json
   {"url": "…", "path": "<dest>/<file>", "sha256": "…", "content_type": "application/pdf",
    "fetched": "<UTC timestamp, ISO 8601>", "doc_date": "<YYYY-MM-DD or null>",
    "title": "…", "publisher": "…"}
   ```

   `path` is relative to the workspace root. `doc_date` is the date of the document itself, not of the download.

Without a shell, archive text documents (HTML, plain text) with web fetch and log them the same way; for binary files you cannot save, record the link and its date in `_data` and list the file under "What is missing" in the state of play.

## Glossary procedure

`_data/glossary.json` changes only this way.

1. **Find the term.** Normalise a name by removing accents, lowercasing, and replacing every run of characters other than `a-z` and `0-9` with `-`, trimming `-` at both ends. A term matches when the normalised name or any alias equals its `id`, the normalised `term`, or one of its normalised aliases.
2. **New term**: it needs a definition and at least one source `{"t": label, "u": "https://…"}`; without both, do not add it. Create `{"id": <normalised term>, "term", "aliases": [], "def", "src": [], "related": [], "see": [], "questions": [], "added": <today>}`.
3. **Existing term**: replace `def` only with a new source for the new wording. Otherwise keep it.
4. **Merge** without duplicates: aliases (compare normalised, never the term itself), sources (compare by URL), `related` candidate ids, `see` term ids (resolve a name to its term's id).
5. **Question**: when the user asked, append `{"q": "<the user's question, verbatim>", "date": <today>}` to `questions`. Never rewrite earlier questions.
6. Set `updated` to today and save.
7. **Rewrite the Markdown glossary** (`folders.glossary`) from scratch, terms sorted by normalised name:

   ```markdown
   # <Glossary heading in the workspace language> : <title>

   ## <term>
   *<aliases, comma-separated>*

   <definition>

   - Sources : [label](url) ; [label](url)
   - <Candidates heading> : <candidate names>
   - <See also heading> : <term names>
   - <Questions heading> : « question » (date) / « question » (date)
   - <added> <date>
   ```

   Omit a line whose list is empty. Headings in French: Glossaire, Voir aussi, Candidats concernés, Sources, Questions à l'origine, ajouté le; translate them for other languages.

## Validation checklist

Run it before every page build and database write. An **error** blocks; a **warning** must be explainable. Report the result as `<n> error(s), <n> warning(s)` with one line per issue.

A **valid source URL** starts with `http://` or `https://` and its host is not a banned domain (same rule as in "Archive a document"). A **source** is an object `{t, u}` with a valid URL.

**Candidates** (`candidates.json` → `list`)
- Error: duplicate `id`; missing `id`, `name`, `party`, `family` or `color`.
- Error: `program.status` other than `full`, `partial` or `none`.
- Error: an invalid source in `statusSrc`, any `ideas[].src` or any `arefs[]`; an invalid URL in any `program.docs[].u`.
- Warning: a programme document without `date`; an `analysis` without `arefs`.

**Meta** (`dataset.json` → `meta`)
- Error: missing `title`, `country`, `election`, `year`, `lang`, `system` or `updated`; `updated` or `checkedAt` not ISO.
- Error: a scenario naming an unknown candidate in `with` or `without`.

**Polls** (`polls`)
- Error: invalid `src`; missing `inst`, `field`, `pub` or `n`; `pub` not ISO; no `hyps`.
- Error: in a hypothesis, an unknown candidate id, a value that is not a number between 0 and 100, or a total above 101.5.

**Runoffs** (`second`)
- Error: invalid `src`; an unknown candidate in a duel.
- Warning: `ra + rb` more than 1.5 away from 100 (check expressed votes).

**Context** (`context`)
- Error: invalid source. Warning: no `date`.

**Glossary** (`glossary.json` → `terms`)
- Error: duplicate ids; missing `term` or `def`; no source; an invalid source; a `related` id that is not a candidate.
- Warning: a `see` id that is not a term.
