#!/usr/bin/env python3
"""Download one official document into the workspace, in its original format, and log it.

Usage:
  python fetch_source.py --root <workspace> --url <url> --dest "Candidats/lepen" \
      --name "programme-2027" --title "Programme 2027" [--doc-date 2026-10-12] [--publisher "RN"]

- Refuses banned domains (radar.config.json -> sources.banned_domains).
- Keeps the original format (extension from Content-Type, else from the URL).
- Skips the download when the same bytes are already archived (sha256).
- When a document at the same URL changed, keeps the old file and saves the new one
  with the date appended, so nothing the user archived is ever overwritten.
- Appends an entry to sources.json: url, path, sha256, fetched, doc_date, title, publisher.
Prints one JSON line: {"status": "new|unchanged|updated|refused|error", ...}.
"""

import argparse
import hashlib
import json
import mimetypes
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

EXT = {
    "application/pdf": ".pdf",
    "text/html": ".html",
    "application/json": ".json",
    "text/csv": ".csv",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/msword": ".doc",
    "application/vnd.ms-excel": ".xls",
    "text/plain": ".txt",
    "image/png": ".png",
    "image/jpeg": ".jpg",
}


def out(**kw):
    print(json.dumps(kw, ensure_ascii=False))
    sys.exit(0 if kw.get("status") not in ("error",) else 1)


def banned(host, cfg):
    host = host.lower()
    return any(
        host == d or host.endswith("." + d)
        for d in cfg.get("sources", {}).get("banned_domains", [])
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--dest", required=True, help="Folder relative to root")
    ap.add_argument("--name", required=True, help="File stem, no extension")
    ap.add_argument("--title", default="")
    ap.add_argument("--doc-date", default=None)
    ap.add_argument("--publisher", default="")
    a = ap.parse_args()

    root = os.path.abspath(os.path.expanduser(a.root))
    with open(os.path.join(root, "radar.config.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    host = urllib.parse.urlparse(a.url).hostname or ""
    if banned(host, cfg):
        out(status="refused", reason=f"banned domain: {host}", url=a.url)

    req = urllib.request.Request(
        a.url, headers={"User-Agent": "Mozilla/5.0 (election-radar archiver)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    except Exception as e:
        out(status="error", reason=str(e), url=a.url)

    ext = (
        EXT.get(ctype)
        or os.path.splitext(urllib.parse.urlparse(a.url).path)[1]
        or mimetypes.guess_extension(ctype)
        or ".bin"
    )
    sha = hashlib.sha256(body).hexdigest()
    man_path = os.path.join(root, "sources.json")
    man = (
        json.load(open(man_path, encoding="utf-8"))
        if os.path.exists(man_path)
        else {"files": []}
    )

    same = [e for e in man["files"] if e["sha256"] == sha]
    if same:
        out(status="unchanged", path=same[0]["path"], url=a.url)

    stem = re.sub(r"[^\w\-. ]+", "-", a.name).strip("-") or "document"
    dest_dir = os.path.join(root, a.dest)
    os.makedirs(dest_dir, exist_ok=True)
    rel = os.path.join(a.dest, stem + ext)
    status = "new"
    if os.path.exists(os.path.join(root, rel)) or any(
        e["url"] == a.url for e in man["files"]
    ):
        status = "updated"
        rel = os.path.join(a.dest, f"{stem}_{datetime.now().date().isoformat()}{ext}")
    with open(os.path.join(root, rel), "wb") as f:
        f.write(body)

    entry = {
        "url": a.url,
        "path": rel,
        "sha256": sha,
        "content_type": ctype,
        "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "doc_date": a.doc_date,
        "title": a.title,
        "publisher": a.publisher,
    }
    man["files"].append(entry)
    with open(man_path, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=2)
    out(status=status, **entry)


if __name__ == "__main__":
    main()
