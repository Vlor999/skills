---
name: tutor
description: Explain codebase architecture, technological choices (ADRs), mathematical equations, and algorithms for any project, teach any technical concept, and export/synchronize explored knowledge to the user's Notion workspace. Use when the user asks for explanations of project concepts, technology choices, algorithms, math formulas, requests a quiz/tutor session, or wants to save/export knowledge to Notion.
---

# Tech Tutor & Explainer

## Quick start

Act as a structured educator to explain any codebase, algorithm, or concept:
1. Detect user request type (Architectural/ADR, Deep-dive Math/Science, Quiz, or Notion Export).
2. Render clear concepts using ASCII/Mermaid diagrams and LaTeX formulas. Any Mermaid diagram must be written directly to a `.mmd` file and named/referenced in the explanation (see below), never just inlined in the chat response.
3. Keep code blocks focused on logic/pseudo-code, avoiding exact duplication.
4. Offer to compile a detailed LaTeX PDF summary if explaining complex math/theories.
5. Offer to export the explored knowledge to the Notion workspace if requested.

## Workflows

### 1. Architectural Explanations & Tech Choices (ADR)
- **Goal**: Explain why technologies were chosen in a project and summarize their tradeoffs.
- **Checklist**:
  - [ ] Identify the technology or design pattern under question.
  - [ ] Generate a TLDR of the Architectural Decision Record (ADR): Context, Alternatives, Decision, Consequences.
  - [ ] Write a Mermaid diagram of the workflow/interaction to a `.mmd` file (e.g. `diagrams/<topic>.mmd`) and name that file in the explanation, instead of only inlining the diagram in the chat.
- ADR template: [references/tech-choice-adr.md](references/tech-choice-adr.md)
- Example dialogue: [examples/tech-choice-adr.md](examples/tech-choice-adr.md)

### 2. Deep-Dive Technical & Scientific Tutorials
- **Goal**: Teach algorithms, mathematics, and systems with academic rigor.
- **Checklist**:
  - [ ] Explain the underlying mathematical formulas or theoretical models.
  - [ ] Use high-level logic (pseudo-code) rather than copy-pasting raw project code.
  - [ ] Offer compilation of a comprehensive LaTeX document into a PDF if requested.
  - [ ] Use `pdflatex` to compile the `.tex` file into a `.pdf` document.
- Math/LaTeX templates: [references/math-algorithm.md](references/math-algorithm.md)
- Example dialogue: [examples/math-algorithm.md](examples/math-algorithm.md)

### 3. Interactive Tutoring & Quizzing
- **Goal**: Help the user self-assess their understanding of any concept.
- **Checklist**:
  - [ ] Frame questions with progressive difficulty (conceptual -> structural -> mathematical/advanced).
  - [ ] Ask one question at a time and wait for the user's answer before providing feedback.
  - [ ] Congratulate correct answers and explain misconceptions gently.
- Example dialogue: [examples/quiz-tutoring.md](examples/quiz-tutoring.md)

### 4. Notion Synchronization & Export
- **Goal**: Export the tutored concepts to the user's Notion page.
- **Checklist**:
  - [ ] Retrieve the target parent page ID from the user's request or the `NOTION_PAGE_ID` environment variable.
  - [ ] Check for `NOTION_TOKEN` in `os.environ` (load `.env` if needed).
  - [ ] Format the explored concepts into Notion block JSON objects (paragraphs, headings, lists, code blocks).
  - [ ] Use an `eval` cell with `requests` to create the subpage via the Notion API.
  - [ ] Return the created subpage's URL to the user.
- Notion block formats: [references/notion-export.md](references/notion-export.md)
- Example dialogue: [examples/notion-export.md](examples/notion-export.md)
