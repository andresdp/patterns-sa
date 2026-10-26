# Review 4 — RQ2 on the full-design notebooks (bundle)

Preliminary review of the RQ2 results of `image/analysis-fl-rq-full-design-image.ipynb` and `text/analysis-fl-rq-full-design-text.ipynb` (AP4FED compact campaign, 870 runs per task, 0 % and 100 % delay excluded).

Contents:
- `review4_rq2_full_design.md`: the report, with figures and tables linked by relative path; open it from this folder.
- `review4_rq2_full_design.pdf`: the same report as a PDF (14 pages; the rule tables in §6.3–6.4 are on landscape pages).
- `figures/`: the seven figures, PNG at 300 dpi.
  - `rq2fd_feature_credit.png`: Figure 1, feature credit by variable family.
  - `rq2fd_box_decomposition.png`: Figure 2, lift decomposition per ADEPT box.
  - `rq2fd_design_map_image.png`, `rq2fd_design_map_text.png`: Figures 3a and 3b, design maps.
  - `rq2fd_pattern_effects.png`: Figure 4, paired pattern effects.
  - `rq2fd_rule_cards.png`: Figure 5, rule cards.
  - `rq2fd_how_computed.png`: Figure 6, how Figures 4 and 5 are computed.
- `data/`: the tables behind the figures, as CSV.
  - `rq2fd_box_translation.csv`, `rq2fd_box_cells.csv`: the ADEPT boxes translated into designed variables.
  - `rq2fd_design_map.csv`: goal shares per environment point × configuration × client count.
  - `rq2fd_pattern_effects.csv`: paired ON − OFF effects with seed CIs.
  - `rq2fd_architect_rules.csv`: the rules I1–I4 and T1–T5 with CIs.
  - `rq2fd_how_computed_cells.csv`: the twin cells behind Figure 6a.
