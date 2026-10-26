# Discovered scenario boxes — Text task — all

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

## How to read the metrics

- **Discovery metrics = training partition.** ADEPT uses these training runs to rank parameters and fit the PRIM/CART boxes. The table evaluates each learned rule on those same training runs.
- **Held-out metrics = test partition.** Each fixed rule is applied to separate runs set aside by `partition_seed`; those runs were not used to discover the box. Every reported held-out metric, including prevalence and lift, is calculated from that test partition.
- Compare the two sets: a drop in test precision or lift can indicate that the training association is less stable out of sample. Test recall/coverage shows how many target runs the rule still captures.
- Precision is the share of runs inside the box that reach the target; recall/coverage is the share of target runs captured by the box. Absolute lift is precision minus the target prevalence in the same partition, reported as a proportion.
- These are observational performance measures, not causal effects or guarantees for future deployments.

The architectural interpretation traces conditions through declared system-spec relationships.

## Cross-algorithm box ranking and duplicate marks

The table includes a **global rank** across all scoreable boxes and a **within-target rank** that compares PRIM/CART boxes for the same tradeoff. The held-out score is the harmonic mean of normalized enrichment and target coverage: normalized enrichment = max(0, (precision − baseline prevalence) / (1 − baseline prevalence)); score = 2 × enrichment × coverage / (enrichment + coverage). The score ranges from 0 to 1. Compare ranks alongside target support counts because tradeoffs can have different numbers of held-out examples; training-to-test stability and rule complexity are also shown.

**Unvalidated** means the held-out evaluation is unavailable or contains no target examples, so the rule has no held-out target evidence. A supported rule that selects no held-out rows is evaluated with score 0. Duplicate checks compare boxes for the same target only. Exact duplicates have identical readable conditions, including categories and NaN/not-selected inclusion. Near duplicates require the same constrained parameters and at least 90% condition similarity; when held-out membership can be compared, it must also reach 95% Jaccard similarity. Duplicate boxes are retained and individually marked.

| Global rank | Within-target rank | Target | Box | Status | Test score | Train score | Score Δ (test−train) | Enrichment | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| 1 | 1 | L-M | CART Box 1 | Evaluated | 0.7304 | 0.7350 | -0.0046 | 1 | 0.5753 | 126 / 219 | 126 / 261 | 2 | Near duplicate of PRIM Box 4 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | 2 | L-M | PRIM Box 4 | Evaluated | 0.7304 | 0.7350 | -0.0046 | 1 | 0.5753 | 126 / 219 | 126 / 261 | 2 | Representative for CART Box 1 |
| 3 | 1 | L-S | PRIM Box 3 | Evaluated | 0.5799 | 0.5860 | -0.0061 | 0.7601 | 0.4688 | 15 / 32 | 19 / 261 | 5 | — |
| 4 | 1 | L-L | CART Box 3 | Evaluated | 0.5714 | 0.3515 | 0.2199 | 1 | 0.4000 | 2 / 5 | 2 / 261 | 5 | — |
| 5 | 2 | L-L | PRIM Box 5 | Evaluated | 0.4173 | 0.2762 | 0.1411 | 0.2637 | 1 | 5 / 5 | 18 / 261 | 3 | — |
| 6 | 1 | M-S | PRIM Box 1 | Evaluated | 0.2541 | 0.3277 | -0.0736 | 0.1570 | 0.6667 | 2 / 3 | 12 / 261 | 4 | — |
| 7 | 2 | L-S | CART Box 2 | Evaluated | 0.1714 | 0.1460 | 0.0254 | 1 | 0.0938 | 3 / 32 | 3 / 261 | 6 | — |
| 8 | 1 | M-M | PRIM Box 2 | Evaluated | 0.0935 | 0.2014 | -0.1079 | 0.0516 | 0.5000 | 1 / 2 | 17 / 261 | 2 | — |
| 9 | 2 | M-S | CART Box 4 | Evaluated | 0 | 0.3630 | -0.3630 | 0 | 0 | 0 / 3 | 2 / 261 | 4 | — |

## PRIM

### Box 1 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 9.000]
- `Client Selector Strategy`: {Resource-Based}
- `HDH Instances`: [0.000, 1.500]
- `non_iid_percentage`: [37.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (33/33)
  - HDH: OFF (14/33), ON (19/33)
  - Message Compressor: OFF (33/33)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (12/12)
  - HDH: OFF (6/12), ON (6/12)
  - Message Compressor: OFF (12/12)
- **Operating envelope**:
  - HDH Instances [0, 1.5]
  - non-IID percentage [37.5, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2121 |
| Train recall / coverage | 0.8750 |
| Train target prevalence | 0.0131 |
| Train absolute lift | 0.1990 |
| Train observations | 609 |
| Train target observations | 8 |
| Train samples in box | 33 |
| Train targets in box | 7 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2121 |
| Coverage | 0.8750 |
| Mean | 0.2121 |
| Mass | 0.0542 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 3 |
| Runs retained by box | 12 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.0115 |
| Precision inside box | 0.1667 |
| Recall / target coverage | 0.6667 |
| Absolute lift over held-out prevalence | 0.1552 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `HDH Instances`: [0.500, 8.000]
- `low_spec_percentage`: [62.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/38), ON (17/38)
  - HDH: ON (38/38)
  - Message Compressor: OFF (38/38)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/17), ON (8/17)
  - HDH: ON (17/17)
  - Message Compressor: OFF (17/17)
- **Operating envelope**:
  - HDH Instances [0.5, 8]
  - low-spec percentage [62.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1316 |
| Train recall / coverage | 0.6250 |
| Train target prevalence | 0.0131 |
| Train absolute lift | 0.1184 |
| Train observations | 609 |
| Train target observations | 8 |
| Train samples in box | 38 |
| Train targets in box | 5 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1316 |
| Coverage | 0.6250 |
| Mean | 0.1316 |
| Mass | 0.0624 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 2 |
| Runs retained by box | 17 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0077 |
| Precision inside box | 0.0588 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.0512 |

### Box 3 — L-S (L,S)

**Learned box conditions**

- `Client Selector Strategy`: {Resource-Based}
- `CPU Mean`: [8.000, 8.875]
- `Message Compressor Instances`: [0.000, 1.500]
- `HDH Instances`: [0.000, 0.500]
- `delay_percentage`: [25.000, 50.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (46/46)
  - HDH: OFF (42/46), ON (4/46)
  - Message Compressor: OFF (46/46)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (19/19)
  - HDH: OFF (18/19), ON (1/19)
  - Message Compressor: OFF (19/19)
- **Operating envelope**:
  - CPU Mean [8, 8.88]
  - Message Compressor Instances [0, 1.5]
  - HDH Instances [0, 0.5]
  - delay percentage [25, 50] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.7826 |
| Train recall / coverage | 0.4800 |
| Train target prevalence | 0.1232 |
| Train absolute lift | 0.6595 |
| Train observations | 609 |
| Train target observations | 75 |
| Train samples in box | 46 |
| Train targets in box | 36 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.7826 |
| Coverage | 0.4800 |
| Mean | 0.7826 |
| Mass | 0.0755 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 32 |
| Runs retained by box | 19 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.1226 |
| Precision inside box | 0.7895 |
| Recall / target coverage | 0.4688 |
| Absolute lift over held-out prevalence | 0.6669 |

### Box 4 — L-M (L,M) — Representative for CART Box 1

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Client Selector Stress Percentage`: (not selected) or <= 37.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (238/294), ON (56/294)
  - HDH: OFF (154/294), ON (140/294)
  - Message Compressor: OFF (154/294), ON (140/294)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (102/126), ON (24/126)
  - HDH: OFF (66/126), ON (60/126)
  - Message Compressor: OFF (66/126), ON (60/126)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 37.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5810 |
| Train target prevalence | 0.8309 |
| Train absolute lift | 0.1691 |
| Train observations | 609 |
| Train target observations | 506 |
| Train samples in box | 294 |
| Train targets in box | 294 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5810 |
| Mean | 1 |
| Mass | 0.4828 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 219 |
| Runs retained by box | 126 |
| Target runs inside box | 126 |
| Target prevalence before box | 0.8391 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5753 |
| Absolute lift over held-out prevalence | 0.1609 |

### Box 5 — L-L (L,L)

**Learned box conditions**

- `Total Clients`: [4.000, 9.000]
- `HDH Instances`: [0.500, 8.000]
- `delay_percentage`: [37.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (42/42)
  - HDH: ON (42/42)
  - Message Compressor: OFF (14/42), ON (28/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/18)
  - HDH: ON (18/18)
  - Message Compressor: OFF (6/18), ON (12/18)
- **Operating envelope**:
  - HDH Instances [0.5, 8]
  - delay percentage [37.5, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1905 |
| Train recall / coverage | 0.6667 |
| Train target prevalence | 0.0197 |
| Train absolute lift | 0.1708 |
| Train observations | 609 |
| Train target observations | 12 |
| Train samples in box | 42 |
| Train targets in box | 8 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1905 |
| Coverage | 0.6667 |
| Mean | 0.1905 |
| Mass | 0.0690 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 5 |
| Runs retained by box | 18 |
| Target runs inside box | 5 |
| Target prevalence before box | 0.0192 |
| Precision inside box | 0.2778 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.2586 |

## CART

### Box 1 — L-M (L,M) — Near duplicate of PRIM Box 4 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- `Client Selector Stress Percentage`: (not selected) or <= 37.501
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (238/294), ON (56/294)
  - HDH: OFF (154/294), ON (140/294)
  - Message Compressor: OFF (154/294), ON (140/294)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (102/126), ON (24/126)
  - HDH: OFF (66/126), ON (60/126)
  - Message Compressor: OFF (66/126), ON (60/126)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 37.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5810 |
| Train target prevalence | 0.8309 |
| Train absolute lift | 0.1691 |
| Train observations | 609 |
| Train target observations | 506 |
| Train samples in box | 294 |
| Train targets in box | 294 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 219 |
| Runs retained by box | 126 |
| Target runs inside box | 126 |
| Target prevalence before box | 0.8391 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5753 |
| Absolute lift over held-out prevalence | 0.1609 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `HDH Instances`: [0.000, 0.501]
- `CPU Mean`: [8.125, 11.000]
- `non_iid_percentage`: [25.000, 50.010]
- `Total Clients`: [4.000, 5.999]
- `Client Selector Stress Percentage`: [62.494, 75.000]
- `delay_percentage`: [25.000, 50.010]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (7/7)
  - HDH: OFF (7/7)
  - Message Compressor: OFF (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: OFF (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - HDH Instances [0, 0.501]
  - CPU Mean [8.12, 11]
  - non-IID percentage [25, 50] (%)
  - Client Selector Stress Percentage [62.5, 75] (%)
  - delay percentage [25, 50] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.8571 |
| Train recall / coverage | 0.0800 |
| Train target prevalence | 0.1232 |
| Train absolute lift | 0.7340 |
| Train observations | 609 |
| Train target observations | 75 |
| Train samples in box | 7 |
| Train targets in box | 6 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 32 |
| Runs retained by box | 3 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.1226 |
| Precision inside box | 1 |
| Recall / target coverage | 0.0938 |
| Absolute lift over held-out prevalence | 0.8774 |

### Box 3 — L-L (L,L)

**Learned box conditions**

- `Total Clients`: [4.000, 5.999]
- `JSD Mean`: (not selected) or <= 0.018
- `Client Selector Stress Percentage`: (not selected) or <= 37.501
- `Message Compressor Instances`: [2.001, 10.000]
- `HDH Stress Percentage`: [62.494, 75.000]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (5/5)
  - HDH: ON (5/5)
  - Message Compressor: ON (5/5)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (2/2)
  - HDH: ON (2/2)
  - Message Compressor: ON (2/2)
- **Operating envelope**:
  - JSD Mean [-0.0155, 0.0175]
  - Client Selector Stress Percentage [20, 37.5] (%)
  - Message Compressor Instances [2, 10]
  - HDH Stress Percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6000 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.0197 |
| Train absolute lift | 0.5803 |
| Train observations | 609 |
| Train target observations | 12 |
| Train samples in box | 5 |
| Train targets in box | 3 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 5 |
| Runs retained by box | 2 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.0192 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4000 |
| Absolute lift over held-out prevalence | 0.9808 |

### Box 4 — M-S (M,S)

**Learned box conditions**

- `HDH Instances`: [0.501, 1.500]
- `delay_percentage`: [25.000, 50.010]
- `Total Clients`: [5.999, 9.000]
- `Client Selector Stress Percentage`: [62.494, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (2/2)
- **Operating envelope**:
  - HDH Instances [0.501, 1.5]
  - delay percentage [25, 50] (%)
  - Client Selector Stress Percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.0131 |
| Train absolute lift | 0.6535 |
| Train observations | 609 |
| Train target observations | 8 |
| Train samples in box | 3 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 3 |
| Runs retained by box | 2 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0115 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0115 |
