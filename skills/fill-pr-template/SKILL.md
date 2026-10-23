---
name: fill-pr-template
description: Rédige le corps d'une pull request à partir des changements de la branche, des tests réellement lancés et du ticket, en remplissant `.github/pull_request_template.md` s'il existe. Écrit le résultat dans un fichier temporaire hors arborescence projet. Use when asked to write a PR description, fill the PR template, or prepare PR content from a git diff.
user-invocable: true
---

Rédige le corps d'une PR et l'écrit dans un fichier, prêt pour `gh pr create --body-file`.

**Signature :** `/fill-pr-template [lien ou identifiant du ticket]`

Ce skill ne crée pas la PR et ne lance aucun test. Il rédige, rien de plus.

---

## Étape 1 — Localiser le fichier de sortie

```bash
echo "$(git rev-parse --absolute-git-dir)/PR_BODY.md"
```

`git rev-parse` et pas `.git/` en dur : dans un worktree, `.git` est un **fichier**, pas un
répertoire, et l'écriture échouerait. `--absolute-git-dir` plutôt que `--git-dir`, qui renvoie un
chemin relatif quand on est à la racine du repo et casserait après un `cd`. Le chemin résolu est
propre à chaque worktree, donc deux worktrees en parallèle ne se marchent pas dessus. Il pointe
enfin vers un répertoire que git ne suit pas : le brouillon n'apparaît ni dans `git status` ni dans
le diff de la PR qu'il décrit.

---

## Étape 2 — Rassembler les faits

Branche de base — jamais en dur, elle diffère d'un repo à l'autre (`main`, `develop`, …) :

```bash
BASE=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || echo origin/main)
git diff --stat "$BASE"...HEAD
git diff "$BASE"...HEAD
git log --oneline "$BASE"..HEAD
```

Rassemble aussi :

- **Ticket** : le lien ou l'identifiant passé en argument. Ne le devine pas, ne le cherche pas.
- **Tests lancés** : uniquement ceux dont tu as la trace dans la session en cours, avec leur résultat.
- **Commandes du projet** : lis le `CLAUDE.md`, puis le `Makefile` / `package.json` / `pyproject.toml`
  pour connaître les commandes de lint et de test, même si tu ne les as pas lancées.

---

## Étape 3 — Choisir le format

```bash
ls .github/pull_request_template.md
```

**Fichier présent** → c'est le format. Reprends ses titres et ses cases à cocher tels quels, sans en
ajouter ni en retirer. Voir « Remplir le template » ci-dessous.

**Fichier absent** → format court :

```markdown
## Intention

<1-2 phrases : ce que fait ce changement et pourquoi.>

## Points d'attention

- <risque ou décision non évidente>
```

Omettre « Points d'attention » s'il n'y a rien de notable. Pas de liste exhaustive de fichiers.

---

## Étape 4 — Remplir le template

**Description** — ce qui change et pourquoi, du point de vue de l'utilisateur du code. Décris des
comportements, pas des noms de fonctions.

**Lien du ticket** — la ligne `Fixes :` du template :

| Argument reçu | Rendu |
|---|---|
| une URL | `Fixes : [ticket](<url>)` |
| un identifiant (`ATL-42`) | `Fixes : ATL-42` |
| rien | `Fixes : N/A` — et **préviens explicitement** l'utilisateur que la PR partira sans ticket |

**Type de changement** — coche selon le diff. « Breaking change » seulement si un contrat existant
(API, schéma, format de config, signature publique) change de façon incompatible.

**Tests** — la règle est stricte :

- Coché uniquement si la commande a réellement tourné dans cette session, avec son résultat
  (`- [x] make test — 42 passés`).
- Non lancée → case laissée vide, commande quand même listée sous « How to run » pour le relecteur.
- Aucun test lancé et aucune commande trouvée dans le projet → `N/A`.
- Ne coche jamais une case « au cas où ». Une case cochée est une affirmation vérifiable.

**Fichiers modifiés** — les fichiers et répertoires structurants, pas le `git diff --name-only` brut.
Ignore lockfiles, fichiers générés et renommages en masse.

---

## Étape 5 — Écrire et rendre la main

Écris le markdown dans le fichier de l'étape 1, puis affiche :

- le chemin du fichier,
- le corps généré,
- la commande prête à l'emploi : `gh pr create --body-file <chemin>`,
- tout avertissement (ticket manquant, tests non lancés).

---

## Règles

- N'invente jamais un test, un fichier, un lien ou une dépendance. Information manquante → `N/A`.
- Ne lance ni lint ni tests : c'est le travail de l'appelant, et un skill de rédaction qui déclenche
  une suite de tests de trois minutes est une mauvaise surprise.
- Ne modifie aucun fichier du projet, y compris `.github/pull_request_template.md`.
- Décris les résultats, pas les détails d'implémentation.
