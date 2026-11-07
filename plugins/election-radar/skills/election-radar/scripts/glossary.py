#!/usr/bin/env python3
"""Add or update a glossary term, then rewrite the Markdown glossary.

Usage:
  python glossary.py --root <workspace> add --term "Déficit structurel" \
      --def "Déficit public hors effets de la conjoncture ..." \
      --src "Insee|https://www.insee.fr/..." [--src "label|url" ...] \
      [--alias "solde structurel"] [--related philippe --related attal] \
      [--see dette-publique] [--question "Est-ce que le plan d'économies de Retailleau tient ?"]
  python glossary.py --root <workspace> list
  python glossary.py --root <workspace> render

A term is matched by its id, its name or any alias (case and accents ignored), so asking
about "solde structurel" updates "Déficit structurel" instead of creating a duplicate.
On update: the definition is replaced only if --def is given, sources/aliases/related/see are
merged, and the triggering question is appended to the term's history.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import date


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def load(root):
    cfg = json.load(open(os.path.join(root, "radar.config.json"), encoding="utf-8"))
    path = os.path.join(root, cfg["folders"]["data"], "glossary.json")
    g = (
        json.load(open(path, encoding="utf-8"))
        if os.path.exists(path)
        else {"terms": []}
    )
    return cfg, path, g


def find(g, *names):
    keys = {norm(n) for n in names if n}
    for t in g["terms"]:
        if keys & (
            {t["id"], norm(t["term"])} | {norm(a) for a in t.get("aliases", [])}
        ):
            return t
    return None


def merge(lst, items, key=lambda x: x):
    seen = {key(x) for x in lst}
    for x in items:
        if key(x) not in seen:
            lst.append(x)
            seen.add(key(x))
    return lst


def render_md(root, cfg, g):
    lang = cfg.get("lang", "en")[:2]
    H = {
        "fr": (
            "Glossaire",
            "Voir aussi",
            "Candidats concernés",
            "Sources",
            "Questions à l'origine",
            "ajouté le",
        ),
        "es": (
            "Glosario",
            "Ver también",
            "Candidatos",
            "Fuentes",
            "Preguntas de origen",
            "añadido el",
        ),
        "de": (
            "Glossar",
            "Siehe auch",
            "Kandidaten",
            "Quellen",
            "Ausgangsfragen",
            "hinzugefügt am",
        ),
    }.get(lang, ("Glossary", "See also", "Candidates", "Sources", "Asked in", "added"))
    names = {t["id"]: t["term"] for t in g["terms"]}
    cp = os.path.join(root, cfg["folders"]["data"], "candidates.json")
    cnames = (
        {
            c["id"]: c["name"]
            for c in json.load(open(cp, encoding="utf-8")).get("list", [])
        }
        if os.path.exists(cp)
        else {}
    )
    out = [f"# {H[0]} : {cfg['title']}", ""]
    for t in sorted(g["terms"], key=lambda t: norm(t["term"])):
        out.append(f"## {t['term']}")
        if t.get("aliases"):
            out.append(f"*{', '.join(t['aliases'])}*")
        out += ["", t["def"], ""]
        out.append(
            f"- {H[3]} : "
            + " ; ".join(f"[{s['t']}]({s['u']})" for s in t.get("src", []))
        )
        if t.get("related"):
            out.append(
                f"- {H[2]} : {', '.join(cnames.get(i, i) for i in t['related'])}"
            )
        if t.get("see"):
            out.append(f"- {H[1]} : {', '.join(names.get(i, i) for i in t['see'])}")
        if t.get("questions"):
            out.append(
                f"- {H[4]} : "
                + " / ".join(f"« {q['q']} » ({q['date']})" for q in t["questions"])
            )
        out.append(f"- {H[5]} {t.get('added')}")
        out.append("")
    p = os.path.join(root, cfg["folders"].get("glossary", "Glossary.md"))
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_ = sub.add_parser("add")
    a_.add_argument("--term", required=True)
    a_.add_argument("--def", dest="defn")
    a_.add_argument("--src", action="append", default=[], help="label|url")
    a_.add_argument("--alias", action="append", default=[])
    a_.add_argument("--related", action="append", default=[], help="candidate id")
    a_.add_argument("--see", action="append", default=[], help="other term id or name")
    a_.add_argument("--question", default=None)
    sub.add_parser("list")
    sub.add_parser("render")
    a = ap.parse_args()

    root = os.path.abspath(os.path.expanduser(a.root))
    cfg, path, g = load(root)
    today = date.today().isoformat()

    if a.cmd == "list":
        for t in sorted(g["terms"], key=lambda t: norm(t["term"])):
            print(f"{t['id']:30} {t['term']}  ({len(t.get('questions', []))} q)")
        return
    if a.cmd == "add":
        srcs = []
        for s in a.src:
            label, _, url = s.rpartition("|")
            if not url.startswith(("http://", "https://")):
                sys.exit(f"Bad --src (expected 'label|https://...'): {s}")
            srcs.append({"t": label or url, "u": url})
        t = find(g, a.term, *a.alias)
        status = "updated"
        if t is None:
            if not a.defn or not srcs:
                sys.exit(
                    "New term: --def and at least one --src are required (no definition without a source)."
                )
            t = {
                "id": norm(a.term),
                "term": a.term,
                "aliases": [],
                "def": a.defn,
                "src": [],
                "related": [],
                "see": [],
                "questions": [],
                "added": today,
            }
            g["terms"].append(t)
            status = "new"
        elif a.defn:
            if not srcs:
                sys.exit("Changing a definition needs a --src for the new wording.")
            t["def"] = a.defn
        merge(t["aliases"], [x for x in a.alias if norm(x) != norm(t["term"])], norm)
        merge(t["src"], srcs, lambda s: s["u"])
        merge(t["related"], a.related)
        merge(t["see"], [(find(g, s) or {"id": norm(s)})["id"] for s in a.see])
        if a.question:
            t.setdefault("questions", []).append({"q": a.question, "date": today})
        t["updated"] = today
        with open(path, "w", encoding="utf-8") as f:
            json.dump(g, f, ensure_ascii=False, indent=2)
        print(
            json.dumps(
                {"status": status, "id": t["id"], "md": render_md(root, cfg, g)},
                ensure_ascii=False,
            )
        )
        return
    print(json.dumps({"md": render_md(root, cfg, g)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
