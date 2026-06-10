---
name: fill-pr-template
description: Fill a Pull Request (PR) template in a repository based on git diff and commits compared to main. Use when the user requests to fill a PR template, draft a PR description, or write a pull request file (pr.md).
---

# Fill PR Template (RTK Optimized)

This skill automates the creation of a Pull Request (PR) description file named `pr.md` at the workspace root by analyzing the current git branch's commits, diffs, and structure compared to `main`. It automatically locates and parses any repository-specific PR template (e.g., in `.github/pull_request_template.md`).

## ⚡ RTK (Rust Token Killer) Optimization
To maximize token savings (60-90%) and get extremely compact, optimized command and file outputs:
- **Use Terminal Shell Commands**: Always run git and file operations directly in the terminal via shell/bash commands (e.g., `git`, `cat`, `grep`/`rg`, `find`). The shell hooks automatically intercept and optimize these commands (e.g., `git status` -> `rtk git status`).
- **Avoid Built-in Agent Tools**: Do not use the agent's built-in file view, list directory, or search tools (which do not pass through the bash hook). Instead, use `cat` / `find` / `grep` in the terminal, or prefix them explicitly:
  ```bash
  rtk read .github/pull_request_template.md
  rtk find "pull_request"
  ```

## Quick Start

To generate `pr.md` for the current branch:

1. Identify the current branch and its merge base with `main`:
   ```bash
   rtk git branch --show-current
   rtk git merge-base main HEAD
   ```
2. Gather commits on this branch (automatically token-optimized by RTK):
   ```bash
   rtk git log $(git merge-base main HEAD)..HEAD --pretty=format:"- %s (%h) by %an"
   ```
3. Gather diff stat and changed files:
   ```bash
   rtk git diff --name-status $(git merge-base main HEAD)..HEAD
   rtk git diff --stat $(git merge-base main HEAD)..HEAD
   ```
4. Locate the PR template file:
   ```bash
   find . -type f -name "*pull_request*_template.md" -not -path "*/.*" -not -path "*venv*"
   ```
   *(Or read it directly with RTK)*:
   ```bash
   rtk read .github/pull_request_template.md
   ```
5. Synthesize the collected information to fill out the PR template beautifully and write the completed PR description to [pr.md](file:///Users/adnet/dev/onboarding_de_sncf/pr.md) in the workspace root.

## Workflows

### 1. Gather Git Branch & Commit Context
Run terminal commands to check the current branch and locate its common ancestor with the base branch (`main`):
```bash
rtk git branch --show-current
rtk git merge-base main HEAD
```
Extract all the commits made on the current branch since the merge-base:
```bash
rtk git log $(git merge-base main HEAD)..HEAD --pretty=format:"- %s (%h) by %an"
```

### 2. Extract Diffs and File Changes
Get the list of modified/added/deleted files and their status:
```bash
rtk git diff --name-status $(git merge-base main HEAD)..HEAD
```
Get a high-level overview of line additions/deletions per file:
```bash
rtk git diff --stat $(git merge-base main HEAD)..HEAD
```
Inspect the actual code diff to understand functional modifications:
```bash
rtk git diff $(git merge-base main HEAD)..HEAD
```

### 3. Locate and Read PR Template
Locate the Pull Request template inside the workspace. The file is usually named `pull_request_template.md` or `pull_requests_template.md` inside a `.github` directory or the root.
To find it using RTK-optimized shell searching:
```bash
find . -type f -name "*pull_request*_template.md" -not -path "*/.*" -not -path "*venv*"
```
If a template is found, read its content using `cat` or `rtk read` to keep the context size minimal:
```bash
rtk read .github/pull_request_template.md
```
If not found in the current workspace, check other branches where a template might have been added recently:
```bash
rtk git show feat/add-template-pr:.github/pull_request_template.md
# Or check main branch
rtk git show main:.github/pull_request_template.md
```
*If absolutely no template is found across these locations, fallback to this default template:*
```markdown
## 📝 Description

<!-- Provide a clear summary of what this PR does and why. -->

## 🔗 Related Issues

<!-- List any related issues or tickets. -->

## 🧩 Type of Change

- [ ] New feature
- [ ] Bug fix
- [ ] Refactoring (no functional changes)
- [ ] Documentation update
- [ ] Infrastructure / CI/CD

## ✅ How to Test

<!-- Describe how to test this change. -->
```

### 4. Synthesize and Write `pr.md`
Synthesize the collected branch name, commits, file diffs, and template requirements:
- **📝 Description**: Write a cohesive, high-level summary of what was accomplished and why. Focus on the logical changes and the business/functional impact.
- **🧩 Type of Change**: Check the checkbox that best matches the nature of changes.
- **✅ How to Test**: Document exact verification steps, terminal commands (e.g., `pytest`, `make test`), and any new test files created or modified.
- **🔗 Related Issues**: Link any issues mentioned in the commits or branch.

Save the completed template to a file named `pr.md` in the root of the workspace. Review it for professional formatting and completeness, then present the file path to the user.
