#!/usr/bin/env python3
"""Check _data/dataset.json, _data/candidates.json and _data/glossary.json before anything is rendered or published.

Usage: python validate_data.py --root <workspace>
Exit 0 when clean (warnings allowed), 1 when there are errors. Prints one line per issue.

What it enforces is the workspace's core rule: no figure without a source.
- every poll has a source URL, fieldwork, publication date, and percentages in 0..100
- every candidate id used in polls, runoffs and scenarios exists
- every context figure, proposal, program document and glossary definition has a source URL
- no source URL comes from a banned domain
- dates are ISO (YYYY-MM-DD)
"""

import argparse
import json
import os
import re
import sys
import urllib.parse

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = os.path.abspath(os.path.expanduser(a.root))
    cfg = json.load(open(os.path.join(root, "radar.config.json"), encoding="utf-8"))
    ddir = os.path.join(root, cfg["folders"]["data"])
    ds = json.load(open(os.path.join(ddir, "dataset.json"), encoding="utf-8"))
    cands = json.load(
        open(os.path.join(ddir, "candidates.json"), encoding="utf-8")
    ).get("list", [])
    banned = cfg.get("sources", {}).get("banned_domains", [])
    errs, warns = [], []

    def url_ok(u, where):
        if not u or not str(u).startswith(("http://", "https://")):
            errs.append(f"{where}: missing or invalid source URL")
            return
        h = (urllib.parse.urlparse(u).hostname or "").lower()
        if any(h == d or h.endswith("." + d) for d in banned):
            errs.append(f"{where}: banned source domain {h}")

    def src_ok(s, where):
        if not isinstance(s, dict):
            errs.append(f"{where}: source must be {{t, u}}")
            return
        url_ok(s.get("u"), where)

    ids = [c.get("id") for c in cands]
    if len(ids) != len(set(ids)):
        errs.append("candidates: duplicate ids")
    idset = set(ids)
    for c in cands:
        w = f"candidate {c.get('id')}"
        for k in ("id", "name", "party", "family", "color"):
            if not c.get(k):
                errs.append(f"{w}: missing {k}")
        if c.get("statusSrc"):
            src_ok(c["statusSrc"], w + " statusSrc")
        for i, p in enumerate(c.get("ideas", [])):
            src_ok(p.get("src"), f"{w} idea {i + 1}")
        for i, d in enumerate(c.get("program", {}).get("docs", [])):
            url_ok(d.get("u"), f"{w} program doc {i + 1}")
            if not d.get("date"):
                warns.append(
                    f"{w} program doc {i + 1}: no document date (say when it was written)"
                )
        for i, r in enumerate(c.get("arefs", [])):
            src_ok(r, f"{w} analysis ref {i + 1}")
        if c.get("analysis") and not c.get("arefs"):
            warns.append(f"{w}: analysis has no reference links")
        if c.get("program", {}).get("status") not in ("full", "partial", "none"):
            errs.append(f"{w}: program.status must be full|partial|none")

    meta = ds.get("meta", {})
    for k in ("title", "country", "election", "year", "lang", "system", "updated"):
        if meta.get(k) in (None, ""):
            errs.append(f"meta: missing {k}")
    for k in ("updated", "checkedAt"):
        if meta.get(k) and not ISO.match(str(meta[k])):
            errs.append(f"meta.{k}: not ISO date")
    for s in meta.get("scenarios", []):
        for cid in s.get("with", []) + s.get("without", []):
            if cid not in idset:
                errs.append(f"scenario {s.get('id')}: unknown candidate {cid}")

    for i, p in enumerate(ds.get("polls", [])):
        w = f"poll {i + 1} ({p.get('inst')})"
        url_ok(p.get("src"), w)
        for k in ("inst", "field", "pub", "n"):
            if not p.get(k):
                errs.append(f"{w}: missing {k}")
        if p.get("pub") and not ISO.match(str(p["pub"])):
            errs.append(f"{w}: pub not ISO date")
        if not p.get("hyps"):
            errs.append(f"{w}: no scenarios (hyps)")
        for j, h in enumerate(p.get("hyps", [])):
            tot = 0
            for cid, v in h.get("r", {}).items():
                if cid not in idset:
                    errs.append(f"{w} hyp {j + 1}: unknown candidate {cid}")
                if not isinstance(v, (int, float)) or not 0 <= v <= 100:
                    errs.append(f"{w} hyp {j + 1}: bad value {cid}={v}")
                else:
                    tot += v
            if tot > 101.5:
                errs.append(f"{w} hyp {j + 1}: total {tot:.1f} % > 100")

    for i, s in enumerate(ds.get("second", [])):
        w = f"runoff poll {i + 1} ({s.get('inst')})"
        url_ok(s.get("src"), w)
        for d in s.get("duels", []):
            for cid in (d.get("a"), d.get("b")):
                if cid not in idset:
                    errs.append(f"{w}: unknown candidate {cid}")
            if abs((d.get("ra", 0) + d.get("rb", 0)) - 100) > 1.5:
                warns.append(
                    f"{w}: {d.get('a')}/{d.get('b')} do not sum to 100 (check expressed votes)"
                )

    for i, k in enumerate(ds.get("context", [])):
        w = f"context {i + 1} ({k.get('label')})"
        src_ok(k.get("src"), w)
        if not k.get("date"):
            warns.append(f"{w}: no date for the figure")

    gpath = os.path.join(ddir, "glossary.json")
    terms = (
        json.load(open(gpath, encoding="utf-8")).get("terms", [])
        if os.path.exists(gpath)
        else []
    )
    tids = {t.get("id") for t in terms}
    if len(tids) != len(terms):
        errs.append("glossary: duplicate ids")
    for t in terms:
        w = f"glossary {t.get('id')}"
        if not t.get("term") or not t.get("def"):
            errs.append(f"{w}: missing term or definition")
        if not t.get("src"):
            errs.append(f"{w}: definition has no source")
        for i, s in enumerate(t.get("src", [])):
            src_ok(s, f"{w} source {i + 1}")
        for cid in t.get("related", []):
            if cid not in idset:
                errs.append(f"{w}: unknown candidate {cid}")
        for sid in t.get("see", []):
            if sid not in tids:
                warns.append(f"{w}: 'see' points to missing term {sid}")

    for m in errs:
        print("ERROR  " + m)
    for m in warns:
        print("WARN   " + m)
    print(f"{len(errs)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
