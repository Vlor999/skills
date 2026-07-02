# Formatting Mathematical & Scientific Concepts

To explain complex scientific or math-heavy concepts, use precise LaTeX notation:
- Use inline math (`$formula$`) for terms and inline variables (e.g., $x \in \mathbb{R}$).
- Use block math (`$$formula$$`) for load-bearing equations.

## Examples of Core Concepts
- **Similarity Metrics**:
  - Cosine Similarity: $\cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$
  - Euclidean Distance: $d(p, q) = \sqrt{\sum_{i=1}^n (p_i - q_i)^2}$
- **Complexity Analysis**:
  - Time/Space Complexity: Express using Big O notation (e.g., $\mathcal{O}(N \log N)$).

## LaTeX to PDF Compilation Workflow

If the user wants a publication-grade reference document of the tutored concepts:
1. Write a clean `.tex` file using standard packages (`amsmath`, `geometry`, `hyperref`, etc.).
2. Compile the document locally using the `pdflatex` utility:
   ```bash
   pdflatex -interaction=nonstopmode output.tex
   ```
3. Provide the compiled PDF path to the user.
