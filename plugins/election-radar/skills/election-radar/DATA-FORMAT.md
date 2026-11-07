# Data format

Three files in `<workspace>/_data/`. The same JSON objects go into the page database (collection `site`, documents `dataset`, `candidates` and `glossary`). `scripts/validate_data.py` checks them.

All text fields are in the workspace language. A source is always `{"t": "label", "u": "https://..."}`. Dates are ISO `YYYY-MM-DD`.

## dataset.json

```json
{
  "meta": {
    "title": "Radar Présidentielle 2027",
    "eyebrow": "Élection présidentielle française de 2027",
    "country": "France", "election": "Présidentielle", "year": 2027,
    "lang": "fr",
    "system": "two-round",
    "updated": "2026-11-06",
    "checkedAt": "2026-11-07",
    "lede": "One or two sentences: what the page shows and where the numbers come from.",
    "defaultSelected": "candidate-id",
    "scenarios": [
      {"id": "P", "label": "Avec Philippe, sans Attal", "with": ["philippe"], "without": ["attal"]}
    ],
    "secondNote": "Optional sentence under the runoff bars (abstention, blank votes), sourced in method.",
    "method": [
      {"h": "What the bubble measures", "p": "…", "links": [{"t": "…", "u": "…"}]},
      {"h": "The left-right axis", "p": "Indicative order of party families, not a measured distance."},
      {"h": "Sources excluded", "p": "…"}
    ],
    "labels": {"axis": "Optional override of any interface label"}
  },
  "polls": [
    {
      "inst": "Ifop", "client": "LCI", "field": "27–29 oct. 2026", "pub": "2026-11-03",
      "n": "1 103", "src": "https://primary-source/notice.pdf", "note": "optional",
      "hyps": [
        {"label": "H1", "r": {"lepen": 34, "melenchon": 15, "philippe": 16}}
      ]
    }
  ],
  "second": [
    {"inst": "Elabe", "client": "BFMTV", "field": "14–16 oct. 2026", "src": "https://…",
     "duels": [{"a": "melenchon", "b": "lepen", "ra": 30, "rb": 70}]}
  ],
  "context": [
    {"label": "Public debt 2026", "value": "119.3 % of GDP", "note": "optional",
     "date": "2026-09-19", "src": {"t": "INSEE / AFP", "u": "https://…"}}
  ],
  "changelog": [{"date": "2026-11-07", "note": "What changed and from which source."}]
}
```

Rules:

- `labels`: interface texts are built in for fr, en, es, de. For another language, override every key (see `LABELS.en` in `assets/index-template.html`), including `slugs`, the sub-page addresses: plain ASCII letters, digits and hyphens, never `settings`, `sidebar`, `customize`, `upgrade`, `downloads` or anything starting with `comment-` or `g-` (reserved by the host page and the glossary).
- `system`: `two-round` shows runoff duels; anything else shows the `second` list under the "seat projections" heading (put seat projections there with the same `duels` shape only if they really are two-way; otherwise leave `second` empty and describe seats in `context`).
- **One entry per pollster: its latest wave.** Replace the old wave when a new one comes out and say so in the changelog.
- `hyps[].r` holds only candidates tested in that scenario. A candidate absent from a scenario is absent from `r`, never `0`.
- `scenarios` filter hypotheses by who is in or out. Create one only when pollsters really test alternatives (two rival candidates from the same camp, for example).
- Keep `changelog` to the last ~30 entries; roll older ones into one summary line.
- `updated` changes when a figure changes; `checkedAt` changes on every run.

## candidates.json

```json
{
  "list": [
    {
      "id": "lepen", "name": "Marine Le Pen", "short": "Le Pen",
      "party": "RN", "family": "Extrême droite", "color": "#1d2a6b",
      "declared": false,
      "status": "Candidate tested by every pollster; declaration not yet made",
      "statusSrc": {"t": "…", "u": "…"},
      "program": {
        "status": "partial",
        "docs": [{"t": "Counter-budget 2026", "u": "https://…", "date": "2025-10-15",
                  "note": "Budget 2026, not the presidential platform"}]
      },
      "ideas": [{"t": "Proposal in one sentence", "src": {"t": "…", "u": "…"}}],
      "analysis": {
        "idea": "What the proposal aims at, in neutral terms.",
        "feasibility": "Cost and financing against the budget context, with figures from sources.",
        "dynamics": "Coalitions, runoff transfers, institutional obstacles (parliament, EU rules, courts)."
      },
      "arefs": [{"t": "Reference used in the analysis", "u": "https://…"}],
      "mecanisme": {
        "mesure": "The flagship measure, sourced.",
        "effet": "The effect the candidate announces.",
        "condition": "What must hold for it to work (your analysis).",
        "risque": "What could go wrong, with a historical or empirical precedent when one exists."
      },
      "courant": {
        "label": "School of thought", "def": "Two-sentence definition.",
        "figures": "Reference authors", "lien": "How it shows in this candidate's proposals",
        "claimed": false,
        "links": [{"t": "…", "u": "…"}]
      }
    }
  ]
}
```

Rules:

- Order of `list` = left-to-right order on the axis. Neighbouring candidates of the same `family` share a band.
- `program.status`: `full` (complete platform), `partial` (detailed proposals), `none`.
- `mecanisme` (optional, shown as a four-step strip): one flagship measure per candidate. Give it to every candidate who has a sourced flagship measure, not just some.
- `courant.claimed`: `true` only when the candidate claims the tradition, with the source in `links`.
- `analysis` and `courant` are your reading: keep them proportionate and apply the same grid to every candidate. When a candidate claims a school of thought, say so with the source.
- Colours: the party's usual colour when it has one, otherwise a distinct neutral colour.

## glossary.json

Written by `scripts/glossary.py`, never by hand (it merges aliases and questions and refuses a definition without a source).

```json
{
  "terms": [
    {
      "id": "droits-de-succession",
      "term": "Droits de succession",
      "aliases": ["héritage", "héritages"],
      "def": "Impôt payé par les héritiers sur ce qu'ils reçoivent…",
      "src": [{"t": "Service-public.fr", "u": "https://www.service-public.fr/…"}],
      "related": ["glucksmann"],
      "see": ["csg"],
      "questions": [{"q": "Est-ce que la proposition de Glucksmann sur l'héritage tient la route ?", "date": "2026-11-07"}],
      "added": "2026-11-07", "updated": "2026-11-07"
    }
  ]
}
```

Rules:

- `aliases` drive the underlining in candidate cards: add the plural and the common short forms the platforms actually use. Keep aliases of 3 characters or more; shorter ones are not underlined.
- `related` lists the candidates whose proposals use the term; the page shows them as buttons that open the card.
- `questions` keeps the user's wording: it is the history of what the user wanted to understand, so never rewrite it.
