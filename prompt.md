# Image-to-Markdown Conversion Instructions

Convert the provided image containing text, mathematical content, and/or diagrams into clean markdown format following these guidelines:

## Text Formatting
- Convert all readable text to markdown
- Preserve document structure using appropriate headers (# ## ###)
- Maintain paragraph breaks and formatting
- Use **bold** and *italic* formatting where visually indicated
- Convert lists to proper markdown format (- for bullets, 1. for numbered)

## Mathematical Content
- Convert ALL mathematical expressions to LaTeX format using $...$ delimiters for inline math
- Use $$...$$ for display/block equations
- Include proper LaTeX syntax for:
  - Fractions: `\frac{numerator}{denominator}`
  - Superscripts: `x^{2}`
  - Subscripts: `x_{1}`
  - Greek letters: `\alpha`, `\beta`, etc.
  - Mathematical operators: `\sum`, `\int`, `\partial`, etc.
  - Matrices: `\begin{matrix}...\end{matrix}`
- Preserve equation numbering if present

## Diagram Descriptions
When you encounter diagrams, charts, figures, or visual elements:

1. **Insert a detailed description** in the following format:
   ```
   **[DIAGRAM DESCRIPTION]**
   [Provide comprehensive description here]
   ```

2. **Include in your description:**
   - Type of diagram (flowchart, graph, geometric figure, circuit, etc.)
   - All visible elements, labels, and text within the diagram
   - Spatial relationships and connections between elements
   - Colors, shapes, and visual styling if relevant
   - Any arrows, lines, or directional indicators
   - Numerical values, coordinates, or measurements shown
   - Legend or key information if present

3. **For specific diagram types:**
   - **Graphs/Charts**: Describe axes, data series, trends, scale, units
   - **Geometric figures**: Describe shapes, angles, measurements, labels
   - **Flowcharts**: Describe process flow, decision points, connections
   - **Technical diagrams**: Describe components, connections, specifications

## Special Cases to Handle
- **Blank lines/spaces for writing**: Convert dotted lines, underscores, or blank spaces intended for handwritten responses to a simple placeholder like `[BLANK LINE]` or `_____` (maximum 5 underscores)
- **Fill-in-the-blank sections**: Use `_____` for short blanks or `[ANSWER SPACE]` for larger areas
- **Dotted or dashed lines**: Do NOT reproduce long sequences of dots or dashes - use brief placeholders instead
- **Repetitive visual elements**: Summarize rather than reproduce (e.g., "decorative border" instead of copying pattern)

## Output Format
- Provide clean, properly formatted markdown
- Ensure mathematical expressions render correctly
- Place diagram descriptions in logical positions within the text flow
- Maintain the original document's organization and hierarchy
- NEVER generate long sequences of repeated characters (dots, dashes, underscores)
- Keep placeholder representations concise

## Output Format Requirements
- Output the converted content directly as markdown text
- Do NOT wrap your response in code blocks or markdown tags
- Do NOT use ```markdown or ``` tags around your output
- NEVER generate long repetitive sequences of dots, dashes, or any character
- Use concise placeholders for blank spaces instead of reproducing visual elements
- Begin immediately with the converted content