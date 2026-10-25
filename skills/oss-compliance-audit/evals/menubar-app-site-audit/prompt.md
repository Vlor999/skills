---
tags: [oss-compliance-audit]
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Salut, j'ai un petit projet open source : une app de barre des menus macOS (Volta) avec son site vitrine dans `site/`, publiée sur GitHub Pages et via un DMG. Je suis un particulier en France, c'est gratuit. Avant de la partager plus largement, tu peux vérifier que le projet respecte bien les réglementations ? Fais juste l'audit pour l'instant, je te dirai quoi corriger. Écris le rapport dans `AUDIT.md`.

Input files: README.md, LICENSE, site/index.html, site/app.js, site/style.css, App/Telemetry.swift, App/Info.plist, Package.resolved
