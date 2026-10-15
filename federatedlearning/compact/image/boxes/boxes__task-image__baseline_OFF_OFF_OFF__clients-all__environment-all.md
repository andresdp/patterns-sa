# Discovered scenario boxes — Image task — baseline

## Analysis scope

- **Task:** image classification
- **Configuration slice:** baseline
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
| 1 | 1 | M-S | CART Box 3 | Evaluated | 1 | 1 | 0 | 1 | 1 | 9 / 9 | 9 / 54 | 1 | Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | 2 | M-S | PRIM Box 2 | Evaluated | 1 | 1 | 0 | 1 | 1 | 9 / 9 | 9 / 54 | 1 | Representative for CART Box 3 |
| 3 | 1 | S-M | PRIM Box 1 | Evaluated | 0.9600 | 0.9492 | 0.0108 | 1 | 0.9231 | 12 / 13 | 12 / 54 | 2 | — |
| 4 | 2 | S-M | CART Box 2 | Evaluated | 0.9600 | 0.9492 | 0.0108 | 1 | 0.9231 | 12 / 13 | 12 / 54 | 3 | — |
| 5 | 1 | M-M | CART Box 1 | Evaluated | 0.9153 | 0.9197 | -0.0045 | 1 | 0.8438 | 27 / 32 | 27 / 54 | 2 | Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%) |
| 6 | 2 | M-M | PRIM Box 3 | Evaluated | 0.9153 | 0.9197 | -0.0045 | 1 | 0.8438 | 27 / 32 | 27 / 54 | 2 | Representative for CART Box 1 |

## PRIM

### Box 1 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Alpha Dirichlet Mean`: [0.600, 0.750]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (28/28)
  - HDH: OFF (28/28)
  - Message Compressor: OFF (28/28)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (12/12)
  - HDH: OFF (12/12)
  - Message Compressor: OFF (12/12)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.75]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9032 |
| Train target prevalence | 0.2460 |
| Train absolute lift | 0.7540 |
| Train observations | 126 |
| Train target observations | 31 |
| Train samples in box | 28 |
| Train targets in box | 28 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.9032 |
| Mean | 1 |
| Mass | 0.2222 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 13 |
| Runs retained by box | 12 |
| Target runs inside box | 12 |
| Target prevalence before box | 0.2407 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9231 |
| Absolute lift over held-out prevalence | 0.7593 |

### Box 2 — M-S (M,S) — Representative for CART Box 3

**Learned box conditions**

- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: OFF (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1667 |
| Train absolute lift | 0.8333 |
| Train observations | 126 |
| Train target observations | 21 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 1 |
| Mean | 1 |
| Mass | 0.1667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1667 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8333 |

### Box 3 — M-M (M,M) — Representative for CART Box 1

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (63/63)
  - HDH: OFF (63/63)
  - Message Compressor: OFF (63/63)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (27/27)
  - HDH: OFF (27/27)
  - Message Compressor: OFF (27/27)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8514 |
| Train target prevalence | 0.5873 |
| Train absolute lift | 0.4127 |
| Train observations | 126 |
| Train target observations | 74 |
| Train samples in box | 63 |
| Train targets in box | 63 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.8514 |
| Mean | 1 |
| Mass | 0.5000 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 32 |
| Runs retained by box | 27 |
| Target runs inside box | 27 |
| Target prevalence before box | 0.5926 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8438 |
| Absolute lift over held-out prevalence | 0.4074 |

## CART

### Box 1 — M-M (M,M) — Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `delay_percentage`: [12.488, 100.000]
- `Alpha Dirichlet Mean`: [0.750, 0.900]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (63/63)
  - HDH: OFF (63/63)
  - Message Compressor: OFF (63/63)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (27/27)
  - HDH: OFF (27/27)
  - Message Compressor: OFF (27/27)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Alpha Dirichlet Mean [0.75, 0.9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8514 |
| Train target prevalence | 0.5873 |
| Train absolute lift | 0.4127 |
| Train observations | 126 |
| Train target observations | 74 |
| Train samples in box | 63 |
| Train targets in box | 63 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 32 |
| Runs retained by box | 27 |
| Target runs inside box | 27 |
| Target prevalence before box | 0.5926 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8438 |
| Absolute lift over held-out prevalence | 0.4074 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- `delay_percentage`: [12.488, 100.000]
- `Alpha Dirichlet Mean`: [0.600, 0.750]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (28/28)
  - HDH: OFF (28/28)
  - Message Compressor: OFF (28/28)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (12/12)
  - HDH: OFF (12/12)
  - Message Compressor: OFF (12/12)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Alpha Dirichlet Mean [0.6, 0.75]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9032 |
| Train target prevalence | 0.2460 |
| Train absolute lift | 0.7540 |
| Train observations | 126 |
| Train target observations | 31 |
| Train samples in box | 28 |
| Train targets in box | 28 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 13 |
| Runs retained by box | 12 |
| Target runs inside box | 12 |
| Target prevalence before box | 0.2407 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9231 |
| Absolute lift over held-out prevalence | 0.7593 |

### Box 3 — M-S (M,S) — Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.488]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: OFF (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1667 |
| Train absolute lift | 0.8333 |
| Train observations | 126 |
| Train target observations | 21 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1667 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8333 |
