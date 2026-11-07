# State-of-play template

Translate the headings into the workspace language. Every number comes from `_data` and keeps its source. Target: one screen to one and a half; this file is read first by people and by every automation run.

```markdown
# {{title}}: point de départ ({{date}})

Page interactive : {{page_url or "local: index.html"}}
Automatisations : « {{local_sync_name}} » ({{time}}), « {{page_update_name}} » ({{time}}), {{timezone}}.
Dossier local : {{root}}
Glossaire : {{glossary file}} ({{n}} termes), aussi consultable sur la page

## Règles de travail
- (the rules from the project instructions, one line each)

## Cadre de l'élection
Date(s) du scrutin, mode de scrutin, règles de candidature, échéances proches — each with its source.

## Candidats
One line per candidate: name, party, declared or not (source), programme status (full / partial / none, with link and document date).

## Sondages retenus (dernière vague par institut)
Pollster/client and fieldwork dates, one line. Source primaire : {{primary poll source}}.
Ordres de grandeur : range per main candidate across pollsters.
Seconds tours / sièges : range per tested duel.

## Contexte
The binding budget and economic figures with date and source; planned independent costings and when.

## Ce qui manque
Programmes not yet published, pollsters not found, figures without a source. Expected dates if known.

## Ce qui a changé
- {{date}} : (appended by the local sync, newest first; keep the last ~15 lines)
```
