# Discovered scenario boxes — Image task — all

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all
- **Client-count scope:** 4 clients
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
| 1 | 1 | S-S | PRIM Box 1 | Evaluated | 0.7914 | 0.5313 | 0.2602 | 0.6549 | 1 | 4 / 4 | 6 / 117 | 2 | — |
| 2 | 1 | M-S | CART Box 2 | Evaluated | 0.6667 | 0.6796 | -0.0129 | 1 | 0.5000 | 15 / 30 | 15 / 117 | 1 | — |
| 3 | 2 | M-S | PRIM Box 3 | Evaluated | 0.6667 | 0.6796 | -0.0129 | 1 | 0.5000 | 15 / 30 | 15 / 117 | 2 | — |
| 4 | 1 | M-M | CART Box 1 | Evaluated | 0.4660 | 0.4609 | 0.0051 | 1 | 0.3038 | 24 / 79 | 24 / 117 | 4 | — |
| 5 | 2 | M-M | PRIM Box 4 | Evaluated | 0.4356 | 0.4545 | -0.0189 | 1 | 0.2785 | 22 / 79 | 22 / 117 | 4 | — |
| 6 | 1 | S-M | PRIM Box 2 | Evaluated | 0.2767 | 0.2721 | 0.0045 | 0.3097 | 0.2500 | 1 / 4 | 3 / 117 | 4 | — |
| 7 | 2 | S-M | CART Box 3 | Evaluated: no held-out rows selected | 0 | 0.3333 | -0.3333 | 0 | 0 | 0 / 4 | 0 / 117 | 4 | — |
| 8 | 2 | S-S | CART Box 4 | Evaluated: no held-out rows selected | 0 | 0.4000 | -0.4000 | 0 | 0 | 0 / 4 | 0 / 117 | 4 | — |

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `Client Selector Stress Percentage`: [35.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (7/14), ON (7/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (3/6), ON (3/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
  - Client Selector Stress Percentage [35, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.7500 |
| Train target prevalence | 0.0293 |
| Train absolute lift | 0.3993 |
| Train observations | 273 |
| Train target observations | 8 |
| Train samples in box | 14 |
| Train targets in box | 6 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.4286 |
| Coverage | 0.7500 |
| Mean | 0.4286 |
| Mass | 0.0513 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 4 |
| Runs retained by box | 6 |
| Target runs inside box | 4 |
| Target prevalence before box | 0.0342 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.6325 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `JSD Mean`: (not selected) or <= 0.027
- `delay_percentage`: [0.000, 50.000]
- `Client Selector Stress Percentage`: (not selected) or <= 47.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (17/17)
  - HDH: OFF (7/17), ON (10/17)
  - Message Compressor: OFF (17/17)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: OFF (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
  - JSD Mean [-0.006, 0.0275]
  - delay percentage [0, 50] (%)
  - Client Selector Stress Percentage [20, 47.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2353 |
| Train recall / coverage | 0.4000 |
| Train target prevalence | 0.0366 |
| Train absolute lift | 0.1987 |
| Train observations | 273 |
| Train target observations | 10 |
| Train samples in box | 17 |
| Train targets in box | 4 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2353 |
| Coverage | 0.4000 |
| Mean | 0.2353 |
| Mass | 0.0623 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 4 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0342 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.2500 |
| Absolute lift over held-out prevalence | 0.2991 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `JSD Mean`: (not selected) or <= 0.019
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/35), ON (14/35)
  - HDH: OFF (21/35), ON (14/35)
  - Message Compressor: OFF (7/35), ON (28/35)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/15), ON (6/15)
  - HDH: OFF (9/15), ON (6/15)
  - Message Compressor: OFF (3/15), ON (12/15)
- **Operating envelope**:
  - JSD Mean [-0.006, 0.0188]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5147 |
| Train target prevalence | 0.2491 |
| Train absolute lift | 0.7509 |
| Train observations | 273 |
| Train target observations | 68 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5147 |
| Mean | 1 |
| Mass | 0.1282 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 30 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.2564 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.7436 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.688, 0.875]
- `JSD Mean`: (not selected) or <= 0.019
- `delay_percentage`: [37.500, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 22.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (55/55)
  - HDH: OFF (42/55), ON (13/55)
  - Message Compressor: OFF (14/55), ON (41/55)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (22/22)
  - HDH: OFF (18/22), ON (4/22)
  - Message Compressor: OFF (6/22), ON (16/22)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.688, 0.875]
  - JSD Mean [-0.006, 0.0188]
  - delay percentage [37.5, 100] (%)
  - Client Selector Stress Percentage [20, 22.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2941 |
| Train target prevalence | 0.6850 |
| Train absolute lift | 0.3150 |
| Train observations | 273 |
| Train target observations | 187 |
| Train samples in box | 55 |
| Train targets in box | 55 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.2941 |
| Mean | 1 |
| Mass | 0.2015 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 22 |
| Target runs inside box | 22 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2785 |
| Absolute lift over held-out prevalence | 0.3248 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Client Selector Stress Percentage`: (not selected) or <= 22.497
- `Alpha Dirichlet Mean`: [0.688, 0.875]
- `JSD Mean`: (not selected) or <= -0.003
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (56/56)
  - HDH: OFF (56/56)
  - Message Compressor: OFF (21/56), ON (35/56)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (24/24)
  - HDH: OFF (24/24)
  - Message Compressor: OFF (9/24), ON (15/24)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 22.5] (%)
  - Alpha Dirichlet Mean [0.688, 0.875]
  - JSD Mean [-0.006, -0.00299]
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2995 |
| Train target prevalence | 0.6850 |
| Train absolute lift | 0.3150 |
| Train observations | 273 |
| Train target observations | 187 |
| Train samples in box | 56 |
| Train targets in box | 56 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 24 |
| Target runs inside box | 24 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3038 |
| Absolute lift over held-out prevalence | 0.3248 |

### Box 2 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/35), ON (14/35)
  - HDH: OFF (21/35), ON (14/35)
  - Message Compressor: OFF (7/35), ON (28/35)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/15), ON (6/15)
  - HDH: OFF (9/15), ON (6/15)
  - Message Compressor: OFF (3/15), ON (12/15)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5147 |
| Train target prevalence | 0.2491 |
| Train absolute lift | 0.7509 |
| Train observations | 273 |
| Train target observations | 68 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 30 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.2564 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.7436 |

### Box 3 — S-M (S,M)

**Learned box conditions**

- `Client Selector Stress Percentage`: (not selected) or <= 22.497
- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `JSD Mean`: [0.019, 0.027]
- `delay_percentage`: [12.500, 50.010]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (2/2)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: no matching rows
  - HDH: no matching rows
  - Message Compressor: no matching rows
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 22.5] (%)
  - Alpha Dirichlet Mean [0.625, 0.688]
  - JSD Mean [0.0188, 0.0275]
  - delay percentage [12.5, 50] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2000 |
| Train target prevalence | 0.0366 |
| Train absolute lift | 0.9634 |
| Train observations | 273 |
| Train target observations | 10 |
| Train samples in box | 2 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 4 |
| Runs retained by box | 0 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0342 |
| Precision inside box | not available |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | not available |

### Box 4 — S-S (S,S)

**Learned box conditions**

- `Client Selector Stress Percentage`: [37.500, 75.000]
- `JSD Mean`: [0.010, 0.035]
- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (2/2)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: no matching rows
  - HDH: no matching rows
  - Message Compressor: no matching rows
- **Operating envelope**:
  - Client Selector Stress Percentage [37.5, 75] (%)
  - JSD Mean [0.01, 0.035]
  - Alpha Dirichlet Mean [0.625, 0.688]
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.0293 |
| Train absolute lift | 0.9707 |
| Train observations | 273 |
| Train target observations | 8 |
| Train samples in box | 2 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 4 |
| Runs retained by box | 0 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0342 |
| Precision inside box | not available |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | not available |
