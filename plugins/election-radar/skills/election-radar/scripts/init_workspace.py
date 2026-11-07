#!/usr/bin/env python3
"""Create the local election workspace: folders, config, empty data files.

Usage:
  python init_workspace.py --root "~/Desktop/Présidentielle 2027" --country FR \
      --election "Présidentielle" --year 2027 --lang fr [--title "..."] [--tz Europe/Paris] \
      [--ban cnews.fr --ban foxnews.com] [--system two-round]

Never overwrites existing data: if the config already exists, it stops and says so.
"""

import argparse
import json
import os
import sys
from datetime import date

# Folder names follow the workspace language so the folder reads naturally to the user.
FOLDERS = {
    "fr": {
        "candidates": "Candidats",
        "polls": "Sondages",
        "context": "Contexte",
        "data": "_data",
        "state": "00 - État des lieux.md",
        "instructions": "instructions-projet.md",
        "glossary": "Glossaire.md",
    },
    "en": {
        "candidates": "Candidates",
        "polls": "Polls",
        "context": "Context",
        "data": "_data",
        "state": "00 - State of play.md",
        "instructions": "project-instructions.md",
        "glossary": "Glossary.md",
    },
    "es": {
        "candidates": "Candidatos",
        "polls": "Encuestas",
        "context": "Contexto",
        "data": "_data",
        "state": "00 - Estado de la cuestión.md",
        "instructions": "instrucciones-proyecto.md",
        "glossary": "Glosario.md",
    },
    "de": {
        "candidates": "Kandidaten",
        "polls": "Umfragen",
        "context": "Kontext",
        "data": "_data",
        "state": "00 - Lagebild.md",
        "instructions": "projekt-anweisungen.md",
        "glossary": "Glossar.md",
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument(
        "--country", required=True, help="Country name or ISO code, as the user says it"
    )
    ap.add_argument(
        "--election", required=True, help="Election type, in the workspace language"
    )
    ap.add_argument("--year", required=True, type=int)
    ap.add_argument(
        "--lang",
        required=True,
        help="BCP-47 language of every output (fr, en, es-MX...)",
    )
    ap.add_argument("--title", default=None)
    ap.add_argument("--tz", default="UTC")
    ap.add_argument(
        "--system",
        default="two-round",
        choices=["two-round", "single-round", "proportional", "other"],
    )
    ap.add_argument(
        "--ban",
        action="append",
        default=[],
        help="Domain never used as a source (repeatable)",
    )
    a = ap.parse_args()

    root = os.path.abspath(os.path.expanduser(a.root))
    cfg_path = os.path.join(root, "radar.config.json")
    if os.path.exists(cfg_path):
        sys.exit(
            f"Workspace already initialised: {cfg_path}. Edit it instead of re-running init."
        )

    folders = FOLDERS.get(a.lang.split("-")[0].lower(), FOLDERS["en"])
    title = a.title or f"Radar {a.election} {a.year}"
    for key in ("candidates", "polls", "context", "data"):
        os.makedirs(os.path.join(root, folders[key]), exist_ok=True)

    today = date.today().isoformat()
    cfg = {
        "title": title,
        "country": a.country,
        "election": a.election,
        "year": a.year,
        "lang": a.lang,
        "timezone": a.tz,
        "system": a.system,
        "folders": folders,
        "sources": {
            "banned_domains": sorted(set(d.lower() for d in a.ban)),
            "with_care": ["wikipedia.org"],
        },
        "page": {
            "url": None,
            "db_docs": ["site/dataset", "site/candidates", "site/glossary"],
        },
        "automations": {"local_sync": None, "page_update": None},
        "created": today,
    }
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    data_dir = os.path.join(root, folders["data"])
    dataset = {
        "meta": {
            "title": title,
            "country": a.country,
            "election": a.election,
            "year": a.year,
            "lang": a.lang,
            "system": a.system,
            "updated": today,
            "checkedAt": today,
            "lede": "",
            "scenarios": [],
            "method": [],
        },
        "polls": [],
        "second": [],
        "context": [],
        "changelog": [{"date": today, "note": "init"}],
    }
    for name, obj in (
        ("dataset.json", dataset),
        ("candidates.json", {"list": []}),
        ("glossary.json", {"terms": []}),
    ):
        p = os.path.join(data_dir, name)
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)
    man = os.path.join(root, "sources.json")
    if not os.path.exists(man):
        with open(man, "w", encoding="utf-8") as f:
            json.dump({"files": []}, f, indent=2)

    print(
        json.dumps(
            {"root": root, "config": cfg_path, "folders": folders},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
