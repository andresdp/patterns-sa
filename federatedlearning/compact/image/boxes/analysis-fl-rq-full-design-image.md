# Discovered scenario boxes — Image task — all

## Analysis scope

- **Task:** image classification
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
| 1 | 1 | S-M | PRIM Box 2 | Evaluated | 0.7636 | 0.7656 | -0.0020 | 1 | 0.6176 | 42 / 68 | 42 / 261 | 3 | — |
| 2 | 2 | S-M | CART Box 2 | Evaluated | 0.7636 | 0.7656 | -0.0020 | 1 | 0.6176 | 42 / 68 | 42 / 261 | 4 | — |
| 3 | 1 | S-S | PRIM Box 1 | Evaluated | 0.6523 | 0.6430 | 0.0093 | 0.5874 | 0.7333 | 11 / 15 | 18 / 261 | 3 | — |
| 4 | 1 | M-M | CART Box 1 | Evaluated | 0.5023 | 0.5070 | -0.0047 | 1 | 0.3354 | 54 / 161 | 54 / 261 | 3 | — |
| 5 | 2 | M-M | PRIM Box 4 | Evaluated | 0.5023 | 0.5070 | -0.0047 | 1 | 0.3354 | 54 / 161 | 54 / 261 | 5 | — |
| 6 | 2 | S-S | CART Box 3 | Evaluated | 0.4211 | 0.4545 | -0.0335 | 1 | 0.2667 | 4 / 15 | 4 / 261 | 5 | — |
| 7 | 1 | M-S | PRIM Box 3 | Evaluated | 0.3835 | 0.5717 | -0.1883 | 0.3006 | 0.5294 | 9 / 17 | 26 / 261 | 4 | — |
| 8 | 2 | M-S | CART Box 4 | Evaluated | 0.0976 | 0.1114 | -0.0138 | 0.2869 | 0.0588 | 1 / 17 | 3 / 261 | 5 | — |

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `Client Selector Strategy`: {Resource-Based}
- `low_spec_percentage`: [62.500, 75.000]
- `non_iid_percentage`: [37.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (42/42)
  - HDH: OFF (21/42), ON (21/42)
  - Message Compressor: OFF (42/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (18/18)
  - HDH: OFF (9/18), ON (9/18)
  - Message Compressor: OFF (18/18)
- **Operating envelope**:
  - low-spec percentage [62.5, 75] (%)
  - non-IID percentage [37.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5952 |
| Train recall / coverage | 0.7353 |
| Train target prevalence | 0.0558 |
| Train absolute lift | 0.5394 |
| Train observations | 609 |
| Train target observations | 34 |
| Train samples in box | 42 |
| Train targets in box | 25 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.5952 |
| Coverage | 0.7353 |
| Mean | 0.5952 |
| Mass | 0.0690 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 15 |
| Runs retained by box | 18 |
| Target runs inside box | 11 |
| Target prevalence before box | 0.0575 |
| Precision inside box | 0.6111 |
| Recall / target coverage | 0.7333 |
| Absolute lift over held-out prevalence | 0.5536 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `non_iid_percentage`: [62.500, 75.000]
- `Client Selector Stress Percentage`: (not selected) or <= 35.000
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (98/98)
  - HDH: OFF (42/98), ON (56/98)
  - Message Compressor: OFF (70/98), ON (28/98)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (42/42)
  - HDH: OFF (18/42), ON (24/42)
  - Message Compressor: OFF (30/42), ON (12/42)
- **Operating envelope**:
  - non-IID percentage [62.5, 75] (%)
  - Client Selector Stress Percentage [20, 35] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6203 |
| Train target prevalence | 0.2594 |
| Train absolute lift | 0.7406 |
| Train observations | 609 |
| Train target observations | 158 |
| Train samples in box | 98 |
| Train targets in box | 98 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.6203 |
| Mean | 1 |
| Mass | 0.1609 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 68 |
| Runs retained by box | 42 |
| Target runs inside box | 42 |
| Target prevalence before box | 0.2605 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6176 |
| Absolute lift over held-out prevalence | 0.7395 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Client Selector Strategy`: {Resource-Based}
- `JSD Mean`: (not selected) or <= 0.020
- `delay_percentage`: [25.000, 37.500]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (58/58)
  - HDH: OFF (35/58), ON (23/58)
  - Message Compressor: OFF (44/58), ON (14/58)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (26/26)
  - HDH: OFF (15/26), ON (11/26)
  - Message Compressor: OFF (20/26), ON (6/26)
- **Operating envelope**:
  - JSD Mean [-0.0115, 0.02]
  - delay percentage [25, 37.5] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5345 |
| Train recall / coverage | 0.6739 |
| Train target prevalence | 0.0755 |
| Train absolute lift | 0.4589 |
| Train observations | 609 |
| Train target observations | 46 |
| Train samples in box | 58 |
| Train targets in box | 31 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.5345 |
| Coverage | 0.6739 |
| Mean | 0.5345 |
| Mass | 0.0952 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 17 |
| Runs retained by box | 26 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.0651 |
| Precision inside box | 0.3462 |
| Recall / target coverage | 0.5294 |
| Absolute lift over held-out prevalence | 0.2810 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Client Selector Strategy`: {(not selected)}
- `HDH Batch Size`: (not selected) or <= 30.400
- `Alpha Dirichlet Mean`: [0.688, 0.900]
- `JSD Mean`: (not selected) or <= 0.010
- `Client Selector Stress Percentage`: (not selected) or <= 62.500
- **Includes NaN / not-selected values:** `Client Selector Strategy`, `Client Selector Stress Percentage`, `HDH Batch Size`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
  - HDH = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (126/126)
  - HDH: OFF (126/126)
  - Message Compressor: OFF (42/126), ON (84/126)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (54/54)
  - HDH: OFF (54/54)
  - Message Compressor: OFF (18/54), ON (36/54)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.688, 0.9]
  - JSD Mean [-0.0115, 0.0095]
  - Client Selector Stress Percentage [20, 62.5] (%)
- **Other parameter conditions**:
  - Strategy {(not selected)}
  - HDH Batch Size [28.8, 30.4]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3396 |
| Train target prevalence | 0.6092 |
| Train absolute lift | 0.3908 |
| Train observations | 609 |
| Train target observations | 371 |
| Train samples in box | 126 |
| Train targets in box | 126 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.3396 |
| Mean | 1 |
| Mass | 0.2069 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 161 |
| Runs retained by box | 54 |
| Target runs inside box | 54 |
| Target prevalence before box | 0.6169 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3354 |
| Absolute lift over held-out prevalence | 0.3831 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Client Selector Strategy`: {(not selected)}
- `Alpha Dirichlet Mean`: [0.812, 0.900]
- `HDH Latent Dim`: (not selected) or <= 95.000
- **Includes NaN / not-selected values:** `Client Selector Strategy`, `HDH Latent Dim`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
  - HDH = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (126/126)
  - HDH: OFF (126/126)
  - Message Compressor: OFF (42/126), ON (84/126)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (54/54)
  - HDH: OFF (54/54)
  - Message Compressor: OFF (18/54), ON (36/54)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.812, 0.9]
- **Other parameter conditions**:
  - Strategy {(not selected)}
  - HDH Latent Dim [90, 95]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3396 |
| Train target prevalence | 0.6092 |
| Train absolute lift | 0.3908 |
| Train observations | 609 |
| Train target observations | 371 |
| Train samples in box | 126 |
| Train targets in box | 126 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 161 |
| Runs retained by box | 54 |
| Target runs inside box | 54 |
| Target prevalence before box | 0.6169 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3354 |
| Absolute lift over held-out prevalence | 0.3831 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Alpha Dirichlet Mean`: [0.600, 0.812]
- `non_iid_percentage`: [62.510, 75.000]
- `Total Clients`: [5.999, 10.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (98/98)
  - HDH: OFF (42/98), ON (56/98)
  - Message Compressor: OFF (70/98), ON (28/98)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (42/42)
  - HDH: OFF (18/42), ON (24/42)
  - Message Compressor: OFF (30/42), ON (12/42)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.812]
  - non-IID percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 10]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6203 |
| Train target prevalence | 0.2594 |
| Train absolute lift | 0.7406 |
| Train observations | 609 |
| Train target observations | 158 |
| Train samples in box | 98 |
| Train targets in box | 98 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 68 |
| Runs retained by box | 42 |
| Target runs inside box | 42 |
| Target prevalence before box | 0.2605 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6176 |
| Absolute lift over held-out prevalence | 0.7395 |

### Box 3 — S-S (S,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.812]
- `JSD Mean`: [0.018, 0.093]
- `Client Selector Criteria`: {CPU}
- `Total Clients`: [5.999, 10.000]
- `HDH Stress Percentage`: [62.494, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (10/10)
  - HDH: ON (10/10)
  - Message Compressor: OFF (10/10)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (4/4)
  - HDH: ON (4/4)
  - Message Compressor: OFF (4/4)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.812]
  - JSD Mean [0.0175, 0.0925]
  - HDH Stress Percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2941 |
| Train target prevalence | 0.0558 |
| Train absolute lift | 0.9442 |
| Train observations | 609 |
| Train target observations | 34 |
| Train samples in box | 10 |
| Train targets in box | 10 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 15 |
| Runs retained by box | 4 |
| Target runs inside box | 4 |
| Target prevalence before box | 0.0575 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2667 |
| Absolute lift over held-out prevalence | 0.9425 |

### Box 4 — M-S (M,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.812]
- `JSD Mean`: (not selected) or <= 0.015
- `Client Selector Stress Percentage`: [62.494, 75.000]
- `Total Clients`: [4.000, 5.999]
- `HDH Beta 1`: (not selected) or <= 0.475
- **Includes NaN / not-selected values:** `HDH Beta 1`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - HDH = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (7/7)
  - HDH: OFF (7/7)
  - Message Compressor: OFF (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: OFF (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.812]
  - JSD Mean [-0.0115, 0.015]
  - Client Selector Stress Percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 6]
- **Other parameter conditions**:
  - HDH Beta 1 [0.45, 0.475]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.0652 |
| Train target prevalence | 0.0755 |
| Train absolute lift | 0.3530 |
| Train observations | 609 |
| Train target observations | 46 |
| Train samples in box | 7 |
| Train targets in box | 3 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 261 |
| Target runs before box | 17 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0651 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.0588 |
| Absolute lift over held-out prevalence | 0.2682 |
