# Technical & Academic Tutoring Reference

This guide provides structures, templates, and methodologies for explaining architectures, documenting technical decisions (ADRs), teaching scientific or mathematical concepts, and exporting them to Notion.

---

## 1. Architectural Decision Record (ADR) Template

When explaining project technology choices, structure the explanation using this simplified ADR format:

*   **Context**: What is the problem we are trying to solve? What are the requirements and constraints?
*   **Alternatives**: What other options were considered, and why were they not chosen?
*   **Decision**: What technology, library, or design pattern was selected?
*   **Consequences**:
    *   *Pros*: What benefits does this decision bring to the project?
    *   *Cons*: What are the drawbacks, limitations, or risks?

---

## 2. Formatting Mathematical & Scientific Concepts

To explain complex scientific or math-heavy concepts, use precise LaTeX notation:
- Use inline math (`$formula$`) for terms and inline variables (e.g., $x \in \mathbb{R}$).
- Use block math (`$$formula$$`) for load-bearing equations.

### Examples of Core Concepts:
- **Similarity Metrics**:
  - Cosine Similarity: $\cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$
  - Euclidean Distance: $d(p, q) = \sqrt{\sum_{i=1}^n (p_i - q_i)^2}$
- **Complexity Analysis**:
  - Time/Space Complexity: Express using Big O notation (e.g., $\mathcal{O}(N \log N)$).

---

## 3. LaTeX to PDF Compilation Workflow

If the user wants a publication-grade reference document of the tutored concepts:
1. Write a clean `.tex` file using standard packages (`amsmath`, `geometry`, `hyperref`, etc.).
2. Compile the document locally using the `pdflatex` utility:
   ```bash
   pdflatex -interaction=nonstopmode output.tex
   ```
3. Provide the compiled PDF path to the user.

---

## 4. Notion API Block Formats

When exporting to the Notion API (`POST https://api.notion.com/v1/pages`), format blocks using the children list:

### Heading 1
```json
{
  "object": "block",
  "type": "heading_1",
  "heading_1": {
    "rich_text": [{"type": "text", "text": {"content": "Heading Text"}}]
  }
}
```

### Paragraph
```json
{
  "object": "block",
  "type": "paragraph",
  "paragraph": {
    "rich_text": [{"type": "text", "text": {"content": "Paragraph text content."}}]
  }
}
```

### Bulleted List Item
```json
{
  "object": "block",
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [{"type": "text", "text": {"content": "List item text"}}]
  }
}
```

### Code Block
```json
{
  "object": "block",
  "type": "code",
  "code": {
    "rich_text": [{"type": "text", "text": {"content": "print('hello world')"}}],
    "language": "python"
  }
}
```
