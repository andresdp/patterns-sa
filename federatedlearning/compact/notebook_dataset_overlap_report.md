# Compact Notebook Dataset Overlap Check

Row-overlap counts use source CSV path and physical line number. Exact duplicate datasets are determined separately with DataComPy by comparing the actual selected row values, aligned on `run_id`, with original column labels ignored. Counts refer to source rows before ADEPT feature derivation; the maintained notebook filters do not filter on those derived features.

An identical input population does not by itself mean the notebooks perform identical analyses: predictor exclusions, plots, summaries, or downstream procedures may differ.

## Text (13 notebooks)

| Notebook | Selected rows |
|:---|---:|
| `analysis-fl-rq-baseline-text.ipynb` | 180 |
| `analysis-fl-rq-c10-text.ipynb` | 390 |
| `analysis-fl-rq-c4-text.ipynb` | 390 |
| `analysis-fl-rq-c8-text.ipynb` | 390 |
| `analysis-fl-rq-client_selector-text.ipynb` | 150 |
| `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | 210 |
| `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | 180 |
| `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | 360 |
| `analysis-fl-rq-hdh-text.ipynb` | 150 |
| `analysis-fl-rq-message_compressor-text.ipynb` | 210 |
| `analysis-fl-rq-stress-only-client_selector-text.ipynb` | 150 |
| `analysis-fl-rq-stress-only-hdh-text.ipynb` | 150 |
| `analysis-fl-rq-stress-only-message_compressor-text.ipynb` | 210 |

### Exact duplicate datasets by data values

`datacompy.PandasCompare` compared all 78 notebook pairs. Each frame uses positional field names and joins rows on unique `run_id`; all remaining cell values are compared at zero tolerance. `run_id` aligns the same observations, and source row order does not affect the result.

**Review status: unresolved.** These pairs are flagged for review; no notebook is removed or reformulated by this check. Keep both until a decision is made about whether their distinct analysis purpose justifies the shared input population.

- **Review pending — 2 notebooks, 150 identical rows:** `analysis-fl-rq-client_selector-text.ipynb`, `analysis-fl-rq-stress-only-client_selector-text.ipynb`
  - datacompy `analysis-fl-rq-client_selector-text.ipynb` ↔ `analysis-fl-rq-stress-only-client_selector-text.ipynb`: **PASS**; 150 matching row IDs; all row values match=True.
- **Review pending — 2 notebooks, 150 identical rows:** `analysis-fl-rq-hdh-text.ipynb`, `analysis-fl-rq-stress-only-hdh-text.ipynb`
  - datacompy `analysis-fl-rq-hdh-text.ipynb` ↔ `analysis-fl-rq-stress-only-hdh-text.ipynb`: **PASS**; 150 matching row IDs; all row values match=True.
- **Review pending — 2 notebooks, 210 identical rows:** `analysis-fl-rq-message_compressor-text.ipynb`, `analysis-fl-rq-stress-only-message_compressor-text.ipynb`
  - datacompy `analysis-fl-rq-message_compressor-text.ipynb` ↔ `analysis-fl-rq-stress-only-message_compressor-text.ipynb`: **PASS**; 210 matching row IDs; all row values match=True.

### Strict subset relationships

None.

### Other non-empty overlaps

| Notebook A | Notebook B | Shared rows | A rows | B rows |
|:---|:---|---:|---:|---:|
| `analysis-fl-rq-baseline-text.ipynb` | `analysis-fl-rq-c10-text.ipynb` | 60 | 180 | 390 |
| `analysis-fl-rq-baseline-text.ipynb` | `analysis-fl-rq-c4-text.ipynb` | 60 | 180 | 390 |
| `analysis-fl-rq-baseline-text.ipynb` | `analysis-fl-rq-c8-text.ipynb` | 60 | 180 | 390 |
| `analysis-fl-rq-c10-text.ipynb` | `analysis-fl-rq-client_selector-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c10-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c10-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | 60 | 390 | 180 |
| `analysis-fl-rq-c10-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | 120 | 390 | 360 |
| `analysis-fl-rq-c10-text.ipynb` | `analysis-fl-rq-hdh-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c10-text.ipynb` | `analysis-fl-rq-message_compressor-text.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c10-text.ipynb` | `analysis-fl-rq-stress-only-client_selector-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c10-text.ipynb` | `analysis-fl-rq-stress-only-hdh-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c10-text.ipynb` | `analysis-fl-rq-stress-only-message_compressor-text.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c4-text.ipynb` | `analysis-fl-rq-client_selector-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c4-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c4-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | 60 | 390 | 180 |
| `analysis-fl-rq-c4-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | 120 | 390 | 360 |
| `analysis-fl-rq-c4-text.ipynb` | `analysis-fl-rq-hdh-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c4-text.ipynb` | `analysis-fl-rq-message_compressor-text.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c4-text.ipynb` | `analysis-fl-rq-stress-only-client_selector-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c4-text.ipynb` | `analysis-fl-rq-stress-only-hdh-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c4-text.ipynb` | `analysis-fl-rq-stress-only-message_compressor-text.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c8-text.ipynb` | `analysis-fl-rq-client_selector-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c8-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c8-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | 60 | 390 | 180 |
| `analysis-fl-rq-c8-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | 120 | 390 | 360 |
| `analysis-fl-rq-c8-text.ipynb` | `analysis-fl-rq-hdh-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c8-text.ipynb` | `analysis-fl-rq-message_compressor-text.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c8-text.ipynb` | `analysis-fl-rq-stress-only-client_selector-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c8-text.ipynb` | `analysis-fl-rq-stress-only-hdh-text.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c8-text.ipynb` | `analysis-fl-rq-stress-only-message_compressor-text.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-client_selector-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | 30 | 150 | 210 |
| `analysis-fl-rq-client_selector-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | 30 | 150 | 180 |
| `analysis-fl-rq-client_selector-text.ipynb` | `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | 90 | 150 | 360 |
| `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | `analysis-fl-rq-hdh-text.ipynb` | 30 | 210 | 150 |
| `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | `analysis-fl-rq-message_compressor-text.ipynb` | 30 | 210 | 210 |
| `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | `analysis-fl-rq-stress-only-client_selector-text.ipynb` | 30 | 210 | 150 |
| `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | `analysis-fl-rq-stress-only-hdh-text.ipynb` | 30 | 210 | 150 |
| `analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | `analysis-fl-rq-stress-only-message_compressor-text.ipynb` | 30 | 210 | 210 |
| `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | `analysis-fl-rq-hdh-text.ipynb` | 30 | 180 | 150 |
| `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | `analysis-fl-rq-message_compressor-text.ipynb` | 30 | 180 | 210 |
| `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | `analysis-fl-rq-stress-only-client_selector-text.ipynb` | 30 | 180 | 150 |
| `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | `analysis-fl-rq-stress-only-hdh-text.ipynb` | 30 | 180 | 150 |
| `analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | `analysis-fl-rq-stress-only-message_compressor-text.ipynb` | 30 | 180 | 210 |
| `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | `analysis-fl-rq-hdh-text.ipynb` | 90 | 360 | 150 |
| `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | `analysis-fl-rq-message_compressor-text.ipynb` | 90 | 360 | 210 |
| `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | `analysis-fl-rq-stress-only-client_selector-text.ipynb` | 90 | 360 | 150 |
| `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | `analysis-fl-rq-stress-only-hdh-text.ipynb` | 90 | 360 | 150 |
| `analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | `analysis-fl-rq-stress-only-message_compressor-text.ipynb` | 90 | 360 | 210 |

## Image (13 notebooks)

| Notebook | Selected rows |
|:---|---:|
| `analysis-fl-rq-baseline-image.ipynb` | 180 |
| `analysis-fl-rq-c10-image.ipynb` | 390 |
| `analysis-fl-rq-c4-image.ipynb` | 390 |
| `analysis-fl-rq-c8-image.ipynb` | 390 |
| `analysis-fl-rq-client_selector-image.ipynb` | 150 |
| `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | 210 |
| `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | 180 |
| `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | 360 |
| `analysis-fl-rq-hdh-image.ipynb` | 150 |
| `analysis-fl-rq-message_compressor-image.ipynb` | 210 |
| `analysis-fl-rq-stress-only-client_selector-image.ipynb` | 150 |
| `analysis-fl-rq-stress-only-hdh-image.ipynb` | 150 |
| `analysis-fl-rq-stress-only-message_compressor-image.ipynb` | 210 |

### Exact duplicate datasets by data values

`datacompy.PandasCompare` compared all 78 notebook pairs. Each frame uses positional field names and joins rows on unique `run_id`; all remaining cell values are compared at zero tolerance. `run_id` aligns the same observations, and source row order does not affect the result.

**Review status: unresolved.** These pairs are flagged for review; no notebook is removed or reformulated by this check. Keep both until a decision is made about whether their distinct analysis purpose justifies the shared input population.

- **Review pending — 2 notebooks, 150 identical rows:** `analysis-fl-rq-client_selector-image.ipynb`, `analysis-fl-rq-stress-only-client_selector-image.ipynb`
  - datacompy `analysis-fl-rq-client_selector-image.ipynb` ↔ `analysis-fl-rq-stress-only-client_selector-image.ipynb`: **PASS**; 150 matching row IDs; all row values match=True.
- **Review pending — 2 notebooks, 150 identical rows:** `analysis-fl-rq-hdh-image.ipynb`, `analysis-fl-rq-stress-only-hdh-image.ipynb`
  - datacompy `analysis-fl-rq-hdh-image.ipynb` ↔ `analysis-fl-rq-stress-only-hdh-image.ipynb`: **PASS**; 150 matching row IDs; all row values match=True.
- **Review pending — 2 notebooks, 210 identical rows:** `analysis-fl-rq-message_compressor-image.ipynb`, `analysis-fl-rq-stress-only-message_compressor-image.ipynb`
  - datacompy `analysis-fl-rq-message_compressor-image.ipynb` ↔ `analysis-fl-rq-stress-only-message_compressor-image.ipynb`: **PASS**; 210 matching row IDs; all row values match=True.

### Strict subset relationships

None.

### Other non-empty overlaps

| Notebook A | Notebook B | Shared rows | A rows | B rows |
|:---|:---|---:|---:|---:|
| `analysis-fl-rq-baseline-image.ipynb` | `analysis-fl-rq-c10-image.ipynb` | 60 | 180 | 390 |
| `analysis-fl-rq-baseline-image.ipynb` | `analysis-fl-rq-c4-image.ipynb` | 60 | 180 | 390 |
| `analysis-fl-rq-baseline-image.ipynb` | `analysis-fl-rq-c8-image.ipynb` | 60 | 180 | 390 |
| `analysis-fl-rq-c10-image.ipynb` | `analysis-fl-rq-client_selector-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c10-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c10-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | 60 | 390 | 180 |
| `analysis-fl-rq-c10-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | 120 | 390 | 360 |
| `analysis-fl-rq-c10-image.ipynb` | `analysis-fl-rq-hdh-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c10-image.ipynb` | `analysis-fl-rq-message_compressor-image.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c10-image.ipynb` | `analysis-fl-rq-stress-only-client_selector-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c10-image.ipynb` | `analysis-fl-rq-stress-only-hdh-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c10-image.ipynb` | `analysis-fl-rq-stress-only-message_compressor-image.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c4-image.ipynb` | `analysis-fl-rq-client_selector-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c4-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c4-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | 60 | 390 | 180 |
| `analysis-fl-rq-c4-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | 120 | 390 | 360 |
| `analysis-fl-rq-c4-image.ipynb` | `analysis-fl-rq-hdh-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c4-image.ipynb` | `analysis-fl-rq-message_compressor-image.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c4-image.ipynb` | `analysis-fl-rq-stress-only-client_selector-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c4-image.ipynb` | `analysis-fl-rq-stress-only-hdh-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c4-image.ipynb` | `analysis-fl-rq-stress-only-message_compressor-image.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c8-image.ipynb` | `analysis-fl-rq-client_selector-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c8-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c8-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | 60 | 390 | 180 |
| `analysis-fl-rq-c8-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | 120 | 390 | 360 |
| `analysis-fl-rq-c8-image.ipynb` | `analysis-fl-rq-hdh-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c8-image.ipynb` | `analysis-fl-rq-message_compressor-image.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-c8-image.ipynb` | `analysis-fl-rq-stress-only-client_selector-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c8-image.ipynb` | `analysis-fl-rq-stress-only-hdh-image.ipynb` | 50 | 390 | 150 |
| `analysis-fl-rq-c8-image.ipynb` | `analysis-fl-rq-stress-only-message_compressor-image.ipynb` | 70 | 390 | 210 |
| `analysis-fl-rq-client_selector-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | 30 | 150 | 210 |
| `analysis-fl-rq-client_selector-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | 30 | 150 | 180 |
| `analysis-fl-rq-client_selector-image.ipynb` | `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | 90 | 150 | 360 |
| `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | `analysis-fl-rq-hdh-image.ipynb` | 30 | 210 | 150 |
| `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | `analysis-fl-rq-message_compressor-image.ipynb` | 30 | 210 | 210 |
| `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | `analysis-fl-rq-stress-only-client_selector-image.ipynb` | 30 | 210 | 150 |
| `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | `analysis-fl-rq-stress-only-hdh-image.ipynb` | 30 | 210 | 150 |
| `analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | `analysis-fl-rq-stress-only-message_compressor-image.ipynb` | 30 | 210 | 210 |
| `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | `analysis-fl-rq-hdh-image.ipynb` | 30 | 180 | 150 |
| `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | `analysis-fl-rq-message_compressor-image.ipynb` | 30 | 180 | 210 |
| `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | `analysis-fl-rq-stress-only-client_selector-image.ipynb` | 30 | 180 | 150 |
| `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | `analysis-fl-rq-stress-only-hdh-image.ipynb` | 30 | 180 | 150 |
| `analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | `analysis-fl-rq-stress-only-message_compressor-image.ipynb` | 30 | 180 | 210 |
| `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | `analysis-fl-rq-hdh-image.ipynb` | 90 | 360 | 150 |
| `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | `analysis-fl-rq-message_compressor-image.ipynb` | 90 | 360 | 210 |
| `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | `analysis-fl-rq-stress-only-client_selector-image.ipynb` | 90 | 360 | 150 |
| `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | `analysis-fl-rq-stress-only-hdh-image.ipynb` | 90 | 360 | 150 |
| `analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | `analysis-fl-rq-stress-only-message_compressor-image.ipynb` | 90 | 360 | 210 |
