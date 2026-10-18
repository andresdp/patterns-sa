# Discovered scenario boxes — Image task — all available client counts (4, 8, 10) — 50% stress

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all supported non-empty combinations with every active pattern at target stress
- **Target stress:** 50%
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
| 1 | 1 | M-S | PRIM Box 3 | Evaluated | 0.7066 | 0.4242 | 0.2823 | 0.6327 | 0.8000 | 4 / 5 | 6 / 54 | 4 | — |
| 2 | 1 | M-M | CART Box 1 | Evaluated | 0.6923 | 0.6667 | 0.0256 | 1 | 0.5294 | 18 / 34 | 18 / 54 | 2 | — |
| 3 | 1 | S-M | PRIM Box 2 | Evaluated | 0.6000 | 0.6087 | -0.0087 | 1 | 0.4286 | 6 / 14 | 6 / 54 | 3 | — |
| 4 | 2 | M-M | PRIM Box 4 | Evaluated | 0.4186 | 0.4242 | -0.0056 | 1 | 0.2647 | 9 / 34 | 9 / 54 | 3 | — |
| 5 | 2 | S-M | CART Box 2 | Evaluated | 0.2500 | 0.5455 | -0.2955 | 1 | 0.1429 | 2 / 14 | 2 / 54 | 2 | — |
| 6 | 2 | M-S | CART Box 3 | Evaluated | 0 | 0.2637 | -0.2637 | 0 | 0 | 0 / 5 | 1 / 54 | 2 | — |
| 7 | 1 | S-S | CART Box 4 | Evaluated: no held-out rows selected | 0 | 0.6667 | -0.6667 | 0 | 0 | 0 / 1 | 0 / 54 | 2 | — |
| 8 | 2 | S-S | PRIM Box 1 | Evaluated | 0 | 0.5977 | -0.5977 | 0 | 0 | 0 / 1 | 4 / 54 | 3 | — |

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `CPU Mean`: [9.500, 10.125]
- `JSD Mean`: [0.024, 0.062]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (4/4)
  - HDH: ON (4/4)
  - Message Compressor: OFF (4/4)
- **Operating envelope**:
  - CPU Mean [9.5, 10.1]
  - JSD Mean [0.0238, 0.062]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4444 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0317 |
| Train absolute lift | 0.4127 |
| Train observations | 126 |
| Train target observations | 4 |
| Train samples in box | 9 |
| Train targets in box | 4 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.4444 |
| Coverage | 1 |
| Mean | 0.4444 |
| Mass | 0.0714 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 1 |
| Runs retained by box | 4 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0185 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0185 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [9.000, 10.000]
- `CPU Mean`: [10.125, 11.000]
- `JSD Mean`: [0.014, 0.062]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (14/14)
  - HDH: ON (14/14)
  - Message Compressor: OFF (7/14), ON (7/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (6/6)
  - HDH: ON (6/6)
  - Message Compressor: OFF (3/6), ON (3/6)
- **Operating envelope**:
  - CPU Mean [10.1, 11]
  - JSD Mean [0.0138, 0.062]
- **Other design conditions**:
  - Total Clients [9, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4375 |
| Train target prevalence | 0.2540 |
| Train absolute lift | 0.7460 |
| Train observations | 126 |
| Train target observations | 32 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.4375 |
| Mean | 1 |
| Mass | 0.1111 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 14 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.2593 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4286 |
| Absolute lift over held-out prevalence | 0.7407 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `CPU Mean`: [9.500, 10.125]
- `JSD Mean`: (not selected) or <= 0.032
- `Pattern Instances`: [0.000, 2.000]
- **Includes NaN / not-selected values:** `JSD Mean`

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
  - CPU Mean [9.5, 10.1]
  - JSD Mean [-0.0018, 0.0325]
  - Pattern Instances [0, 2]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0952 |
| Train absolute lift | 0.3333 |
| Train observations | 126 |
| Train target observations | 12 |
| Train samples in box | 14 |
| Train targets in box | 6 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.4286 |
| Coverage | 0.5000 |
| Mean | 0.4286 |
| Mass | 0.1111 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 5 |
| Runs retained by box | 6 |
| Target runs inside box | 4 |
| Target prevalence before box | 0.0926 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.8000 |
| Absolute lift over held-out prevalence | 0.5741 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `CPU Mean`: [10.125, 10.875]
- `JSD Mean`: (not selected) or <= 0.029
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (7/21), ON (14/21)
  - Message Compressor: OFF (7/21), ON (14/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (3/9), ON (6/9)
  - Message Compressor: OFF (3/9), ON (6/9)
- **Operating envelope**:
  - CPU Mean [10.1, 10.9]
  - JSD Mean [-0.0018, 0.0287]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2692 |
| Train target prevalence | 0.6190 |
| Train absolute lift | 0.3810 |
| Train observations | 126 |
| Train target observations | 78 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.2692 |
| Mean | 1 |
| Mass | 0.1667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 34 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.6296 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2647 |
| Absolute lift over held-out prevalence | 0.3704 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `JSD Mean`: (not selected) or <= 0.011
- `Pattern Instances`: [3.502, 10.000]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (25/39), ON (14/39)
  - HDH: OFF (35/39), ON (4/39)
  - Message Compressor: ON (39/39)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (12/18), ON (6/18)
  - HDH: OFF (15/18), ON (3/18)
  - Message Compressor: ON (18/18)
- **Operating envelope**:
  - JSD Mean [-0.0018, 0.0113]
  - Pattern Instances [3.5, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.6190 |
| Train absolute lift | 0.3810 |
| Train observations | 126 |
| Train target observations | 78 |
| Train samples in box | 39 |
| Train targets in box | 39 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 34 |
| Runs retained by box | 18 |
| Target runs inside box | 18 |
| Target prevalence before box | 0.6296 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5294 |
| Absolute lift over held-out prevalence | 0.3704 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `JSD Mean`: [0.025, 0.062]
- `CPU Mean`: [10.875, 11.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (12/12)
  - HDH: ON (12/12)
  - Message Compressor: OFF (6/12), ON (6/12)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (1/2), ON (1/2)
- **Operating envelope**:
  - JSD Mean [0.025, 0.062]
  - CPU Mean [10.9, 11]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3750 |
| Train target prevalence | 0.2540 |
| Train absolute lift | 0.7460 |
| Train observations | 126 |
| Train target observations | 32 |
| Train samples in box | 12 |
| Train targets in box | 12 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 14 |
| Runs retained by box | 2 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.2593 |
| Precision inside box | 1 |
| Recall / target coverage | 0.1429 |
| Absolute lift over held-out prevalence | 0.7407 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `JSD Mean`: [0.011, 0.019]
- `CPU Mean`: [9.500, 10.125]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (1/1)
  - HDH: ON (1/1)
  - Message Compressor: OFF (1/1)
- **Operating envelope**:
  - JSD Mean [0.0113, 0.0187]
  - CPU Mean [9.5, 10.1]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 0.1667 |
| Train target prevalence | 0.0952 |
| Train absolute lift | 0.5714 |
| Train observations | 126 |
| Train target observations | 12 |
| Train samples in box | 3 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 5 |
| Runs retained by box | 1 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0926 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0926 |

### Box 4 — S-S (S,S)

**Learned box conditions**

- `JSD Mean`: [0.043, 0.049]
- `CPU Mean`: [9.500, 10.125]
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
  - JSD Mean [0.043, 0.0487]
  - CPU Mean [9.5, 10.1]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0317 |
| Train absolute lift | 0.9683 |
| Train observations | 126 |
| Train target observations | 4 |
| Train samples in box | 2 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 1 |
| Runs retained by box | 0 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0185 |
| Precision inside box | not available |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | not available |
