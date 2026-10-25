---
tags: [oss-compliance-audit]
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

I'm about to publish v1.0 of my Python library `tinyparse` on PyPI. It's a free hobby project, no website, just the GitHub repo and the PyPI package. Can you do a full legal/compliance check of the repo first? Put the report in COMPLIANCE.md and don't change anything else yet.

Input files: README.md, LICENSE, pyproject.toml, tinyparse/__init__.py, tinyparse/core.py, tinyparse/vendor/fastscan.py, .env, .github/workflows/release.yml
