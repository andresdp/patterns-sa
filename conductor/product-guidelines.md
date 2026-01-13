# Product Guidelines: patterns-sa

## Communication Style
- **Pragmatic and Technical Tone:** Information should be presented clearly and directly. Focus on how to apply the analysis techniques and how to interpret the results for architectural decision-making. Avoid unnecessary jargon, but maintain technical accuracy.
- **Clarify over Brevity:** While being concise is valued, ensure that complex analytical concepts are explained thoroughly enough to be actionable.

## Documentation & Code Style
- **Explanatory Documentation:** Documentation (both external and internal) must focus on the "why." Explain the rationale behind specific analysis algorithms or architectural choices in the codebase.
- **Self-Documenting Code:** Strive for clean, readable code with meaningful variable names, but supplement it with comments for non-obvious logic or research-specific implementations.

## Visual Identity & Reporting
- **Scientific and Clean Visuals:** All charts and visualizations should be publication-quality. Utilize tools like Seaborn and Matplotlib with clean, consistent themes suitable for inclusion in research papers and academic reports.
- **High Contrast and Clarity:** Ensure that data series are easily distinguishable and that all axes and legends are clearly labeled.

## Error Handling & Reliability
- **Fail-Fast and Verbose:** In a research context, visibility is key. Analysis logic should fail explicitly when encountering unexpected data or states.
- **Detailed Error Reporting:** Provide informative error messages and tracebacks to assist users and researchers in debugging their simulation datasets or analysis scripts.
