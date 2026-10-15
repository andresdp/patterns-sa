# Discovered scenario boxes — Text task — 8 clients — 50% stress

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all non-empty combinations with every active pattern at target stress
- **Target stress:** 50%
- **Client-count scope:** 8 clients
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
| 1 | 1 | L-M | CART Box 1 | Evaluated | 0.8966 | 0.9254 | -0.0288 | 1 | 0.8125 | 13 / 16 | 13 / 18 | 1 | — |
| 2 | 2 | L-M | PRIM Box 4 | Evaluated | 0.8966 | 0.8923 | 0.0042 | 1 | 0.8125 | 13 / 16 | 13 / 18 | 2 | — |
| 3 | 1 | L-S | PRIM Box 3 | Evaluated | 0.3333 | 0.4941 | -0.1608 | 0.2500 | 0.5000 | 1 / 2 | 3 / 18 | 2 | — |
| 4 | 2 | L-S | CART Box 2 | Evaluated: no held-out rows selected | 0 | 0.3208 | -0.3208 | 0 | 0 | 0 / 2 | 0 / 18 | 2 | — |
| — | — | M-M | PRIM Box 2 | Unvalidated: no held-out target examples | not available | 0.2174 | not available | not available | not available | 0 / 0 | 3 / 18 | 2 | — |
| — | — | M-S | PRIM Box 1 | Unvalidated: no held-out target examples | not available | 0.3762 | not available | not available | not available | 0 / 0 | 2 / 18 | 3 | — |

## PRIM

### Box 1 — M-S (M,S) — Unvalidated: no held-out target examples

**Learned box conditions**

- `CPU Mean`: [9.500, 10.125]
- `JSD Mean`: [-0.002, 0.039]
- `Pattern Instances`: [1.000, 3.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (4/4)
  - HDH: ON (4/4)
  - Message Compressor: OFF (4/4)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (2/2)
- **Operating envelope**:
  - CPU Mean [9.5, 10.1]
  - JSD Mean [-0.00194, 0.0387]
  - Pattern Instances [1, 3.5]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2500 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0238 |
| Train absolute lift | 0.2262 |
| Train observations | 42 |
| Train target observations | 1 |
| Train samples in box | 4 |
| Train targets in box | 1 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2500 |
| Coverage | 1 |
| Mean | 0.2500 |
| Mass | 0.0952 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 0 |
| Runs retained by box | 2 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 2 — M-M (M,M) — Unvalidated: no held-out target examples

**Learned box conditions**

- `CPU Mean`: [9.500, 10.125]
- `JSD Mean`: [-0.002, 0.039]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (7/7)
  - HDH: ON (7/7)
  - Message Compressor: OFF (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - CPU Mean [9.5, 10.1]
  - JSD Mean [-0.00194, 0.0387]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1429 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0238 |
| Train absolute lift | 0.1190 |
| Train observations | 42 |
| Train target observations | 1 |
| Train samples in box | 7 |
| Train targets in box | 1 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1429 |
| Coverage | 1 |
| Mean | 0.1429 |
| Mass | 0.1667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 0 |
| Runs retained by box | 3 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 3 — L-S (L,S)

**Learned box conditions**

- `CPU Mean`: [9.500, 10.125]
- `Pattern Types Active`: [1.000, 1.500]
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
  - CPU Mean [9.5, 10.1]
- **Other design conditions**:
  - Pattern Types Active [1, 1.5]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.7500 |
| Train target prevalence | 0.0952 |
| Train absolute lift | 0.3333 |
| Train observations | 42 |
| Train target observations | 4 |
| Train samples in box | 7 |
| Train targets in box | 3 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.4286 |
| Coverage | 0.7500 |
| Mean | 0.4286 |
| Mass | 0.1667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 2 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.2222 |

### Box 4 — L-M (L,M)

**Learned box conditions**

- `JSD Mean`: (not selected) or <= 0.026
- `Pattern Instances`: [3.500, 12.000]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (19/29), ON (10/29)
  - HDH: OFF (14/29), ON (15/29)
  - Message Compressor: OFF (9/29), ON (20/29)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/13), ON (4/13)
  - HDH: OFF (6/13), ON (7/13)
  - Message Compressor: OFF (4/13), ON (9/13)
- **Operating envelope**:
  - JSD Mean [-0.00387, 0.0263]
  - Pattern Instances [3.5, 12]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8056 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train observations | 42 |
| Train target observations | 36 |
| Train samples in box | 29 |
| Train targets in box | 29 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.8056 |
| Mean | 1 |
| Mass | 0.6905 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 16 |
| Runs retained by box | 13 |
| Target runs inside box | 13 |
| Target prevalence before box | 0.8889 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8125 |
| Absolute lift over held-out prevalence | 0.1111 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `Pattern Instances`: [3.500, 12.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/31), ON (10/31)
  - HDH: OFF (14/31), ON (17/31)
  - Message Compressor: OFF (10/31), ON (21/31)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/13), ON (4/13)
  - HDH: OFF (6/13), ON (7/13)
  - Message Compressor: OFF (4/13), ON (9/13)
- **Operating envelope**:
  - Pattern Instances [3.5, 12]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8611 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train observations | 42 |
| Train target observations | 36 |
| Train samples in box | 31 |
| Train targets in box | 31 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 16 |
| Runs retained by box | 13 |
| Target runs inside box | 13 |
| Target prevalence before box | 0.8889 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8125 |
| Absolute lift over held-out prevalence | 0.1111 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `JSD Mean`: [0.018, 0.039]
- `Pattern Instances`: [1.000, 3.500]
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
  - JSD Mean [0.0175, 0.0387]
  - Pattern Instances [1, 3.5]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.0952 |
| Train absolute lift | 0.4048 |
| Train observations | 42 |
| Train target observations | 4 |
| Train samples in box | 2 |
| Train targets in box | 1 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 2 |
| Runs retained by box | 0 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.1111 |
| Precision inside box | not available |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | not available |
