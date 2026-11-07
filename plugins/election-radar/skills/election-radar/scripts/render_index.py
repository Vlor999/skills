#!/usr/bin/env python3
"""Render the local index.html (with its glossary) and one fiche.html per candidate from _data/*.json.

Usage: python render_index.py --root <workspace> [--template <path>] [--out <file>]

index.html embeds the data, so it opens straight from the disk (file://) and can also be
published as is: on a published page, the live database takes over the embedded data.
Each fiche.html links to the documents archived for that candidate (from sources.json),
so the user can open the local copy even if the original page disappears.
"""

import argparse
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def embed(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def fiche(c, ds, local_docs, lang):
    e = lambda s: html.escape(str(s or ""))
    a = lambda s: (
        f'<a href="{e(s.get("u"))}">{e(s.get("t") or s.get("u"))}</a>'
        if s and s.get("u")
        else ""
    )
    rows = []
    for p in ds.get("polls", []):
        vals = [h["r"][c["id"]] for h in p.get("hyps", []) if c["id"] in h.get("r", {})]
        if vals:
            rows.append(
                f"<tr><td>{a({'t': p['inst'], 'u': p['src']})}</td><td>{e(p.get('field'))}</td>"
                f"<td>{min(vals):g}–{max(vals):g} %</td></tr>"
            )
    A = c.get("analysis") or {}
    ana = (
        f"<p>{e(A)}</p>"
        if isinstance(A, str)
        else "".join(f"<p><b>{e(k)}</b> {e(v)}</p>" for k, v in A.items() if v)
    )
    docs = "".join(
        f"<li>{a(d)} {e(d.get('date') or '')}</li>"
        for d in c.get("program", {}).get("docs", [])
    )
    local = "".join(
        f'<li><a href="{e(os.path.basename(f["path"]))}">{e(f.get("title") or os.path.basename(f["path"]))}</a>'
        f' · {e(f.get("doc_date") or "")} · <a href="{e(f["url"])}">↗</a></li>'
        for f in local_docs
    )
    ideas = "".join(
        f"<li>{e(p.get('t'))} <small>{a(p.get('src'))}</small></li>"
        for p in c.get("ideas", [])
    )
    cour = c.get("courant") or {}
    return f"""<!doctype html><html lang="{e(lang)}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(c["name"])}</title>
<style>:root{{color-scheme:light dark}}body{{font:15px/1.55 system-ui,sans-serif;max-width:860px;margin:32px auto;padding:0 16px}}
h1{{margin:0}}.tag{{display:inline-block;border:1px solid #8886;border-radius:99px;padding:1px 9px;font-size:13px;margin-right:6px}}
.box{{border-left:4px solid {e(c.get("color"))};padding:4px 14px;margin:18px 0}}table{{border-collapse:collapse}}td{{padding:4px 10px;border-bottom:1px solid #8884}}
small{{color:#888}}</style></head><body>
<h1>{e(c["name"])}</h1><p><span class="tag">{e(c.get("party"))}</span><span class="tag">{e(c.get("family"))}</span></p>
<div class="box"><h2>Documents (local)</h2><ul>{local or "<li>—</li>"}</ul><h3>Web</h3><ul>{docs or "<li>—</li>"}</ul></div>
<div class="box"><h2>Propositions / Proposals</h2><ul>{ideas or "<li>—</li>"}</ul></div>
<div class="box"><h2>Analyse / Analysis</h2>{ana or "<p>—</p>"}<p>{" ".join(a(r) for r in c.get("arefs", []))}</p></div>
<div class="box"><h2>{e(cour.get("label", ""))}</h2><p>{e(cour.get("def", ""))}</p></div>
<div class="box"><h2>Sondages / Polls</h2><table>{"".join(rows) or "<tr><td>—</td></tr>"}</table></div>
<p><small>{e(ds["meta"].get("updated"))}</small></p></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument(
        "--template", default=os.path.join(HERE, "..", "assets", "index-template.html")
    )
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    root = os.path.abspath(os.path.expanduser(a.root))
    cfg = json.load(open(os.path.join(root, "radar.config.json"), encoding="utf-8"))
    ddir = os.path.join(root, cfg["folders"]["data"])
    ds = json.load(open(os.path.join(ddir, "dataset.json"), encoding="utf-8"))
    cands = json.load(open(os.path.join(ddir, "candidates.json"), encoding="utf-8"))
    gp = os.path.join(ddir, "glossary.json")
    gloss = (
        json.load(open(gp, encoding="utf-8")) if os.path.exists(gp) else {"terms": []}
    )
    tpl = open(a.template, encoding="utf-8").read()

    page = (
        tpl.replace("/*__DATASET__*/null", embed(ds))
        .replace("/*__CANDIDATES__*/null", embed(cands))
        .replace("/*__GLOSSARY__*/null", embed(gloss))
        .replace("__LANG__", html.escape(ds["meta"].get("lang", "en")))
        .replace("__TITLE__", html.escape(ds["meta"].get("title", "")))
    )
    out = a.out or os.path.join(root, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)

    man = (
        json.load(open(os.path.join(root, "sources.json"), encoding="utf-8"))
        if os.path.exists(os.path.join(root, "sources.json"))
        else {"files": []}
    )
    made = []
    for c in cands.get("list", []):
        cdir_rel = os.path.join(cfg["folders"]["candidates"], c["id"])
        os.makedirs(os.path.join(root, cdir_rel), exist_ok=True)
        local = [f for f in man["files"] if os.path.dirname(f["path"]) == cdir_rel]
        p = os.path.join(root, cdir_rel, "fiche.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(fiche(c, ds, local, ds["meta"].get("lang", "en")))
        made.append(p)
    print(json.dumps({"index": out, "fiches": len(made)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
