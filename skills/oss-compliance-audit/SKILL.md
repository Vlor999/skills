---
name: oss-compliance-audit
description: Audits an open source project (repository, website or landing page, distributed binaries, update and package channels) for legal and regulatory compliance, then fixes what the user approves. Covers GDPR and ePrivacy (third-party requests, cookies, privacy notice accuracy), French LCEN legal notice, trademarks (third-party logos, attribution), open source licenses and third-party notices in shipped binaries, disclaimers, security policy, the EU Cyber Resilience Act and platform rules. Use when the user asks whether their project, app, site or repo is "compliant", "legal", "conforme", respects "regulations" or "réglementation", needs legal notices, a privacy policy, license notices or a disclaimer, or before a public launch, rename or release.
argument-hint: "[path or repo] [extra jurisdictions]"
---

# Open source compliance audit

Audit first, fix second. The user decides what gets fixed, because several fixes publish personal or legal information in their name.

You are not a lawyer, and the report says so once. Your job is to find concrete, verifiable gaps with evidence (file:line, a network request, a missing file) and propose the smallest fix for each.

Default scope: France + EU, plus basic US points (trademarks, DMCA). Widen it if the project targets other markets (languages of the site, app store regions, the author's country), and say which jurisdictions you used.

## 1. Inventory the surfaces

Before judging anything, list what the project actually exposes. Each surface brings its own rules:

- **Repository**: license, README, docs, contribution and security files, workflows, vendored code.
- **Website / landing page**: hosting, every third-party request, cookies and storage, forms, analytics.
- **Distributed artifacts**: app bundle, installer, package (npm, PyPI, crates, Homebrew, stores), what is bundled inside it.
- **Runtime behavior**: what the software sends over the network (update checks, telemetry, crash reports), what it stores, what privileges it has.
- **Identity**: project name, logos and icons, other companies' marks it uses, author identity (individual or company, professional or not, country).

Read the code, don't trust the README: privacy claims are checked against real network calls (`grep` for URLs, HTTP clients, analytics SDKs, update frameworks).

## 2. Check each area

Work through [CHECKLIST.md](CHECKLIST.md). It gives, for each area, what to look for, the legal basis, and the usual fix. Skip areas that don't apply, and say why in one line.

For the website, measure instead of guessing: run `node ${CLAUDE_SKILL_DIR}/scripts/site-requests.js <url-or-dir>` (needs Playwright). It lists every host contacted, cookies set and storage keys, so a "no tracking" claim is backed by evidence.

## 3. Report

Use the format in [REPORT.md](REPORT.md): findings ranked 🔴 (fix before the next public release), 🟠 (fix soon), 🟡 (keep in mind), each with evidence, legal basis and the proposed fix. End with the decisions only the user can take (what contact to publish, whether to rename, which jurisdictions). Write the report in the user's language.

Stop after the report and ask which findings to fix. Don't fix silently.

## 4. Fix

- Follow the repository's own rules (CLAUDE.md, AGENTS.md, contributing guide, branch and commit conventions, required checks). They win over this skill.
- Never invent the publisher's identity, address or email. Ask. An individual in France publishing non-professionally may stay anonymous towards the public by naming the host; a company or professional must give its identity.
- Visible changes (site, app UI) get a local render or build shown to the user before commit.
- One commit per area (fonts, logo, legal notice, notices, docs), so each can be reviewed or reverted alone.
- Prefer removing a risk over documenting it: self-host a font rather than add a consent banner for it.
- Re-run the checks that found the issue (site requests, grep) to prove the fix.

## 5. Hand over

List what was fixed, what is left for the user (settings only they can change, such as enabling private vulnerability reporting, trademark searches, account-level choices), and what to re-check before each release.
