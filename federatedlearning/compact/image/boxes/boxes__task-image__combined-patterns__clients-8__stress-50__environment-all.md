# Discovered scenario boxes — Image task — 8 clients — 50% stress

## Analysis scope

- **Task:** image classification
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
| 1 | 1 | M-M | CART Box 1 | Evaluated | 0.7059 | 0.7568 | -0.0509 | 1 | 0.5455 | 6 / 11 | 6 / 18 | 2 | — |
| 2 | 2 | M-M | PRIM Box 4 | Evaluated | 0.7059 | 0.7568 | -0.0509 | 1 | 0.5455 | 6 / 11 | 6 / 18 | 2 | — |
| 3 | 1 | S-M | PRIM Box 2 | Evaluated | 0.4590 | 0.5546 | -0.0956 | 0.5385 | 0.4000 | 2 / 5 | 3 / 18 | 3 | — |
| 4 | 1 | M-S | PRIM Box 3 | Evaluated | 0.4545 | 0.3429 | 0.1117 | 0.2941 | 1 | 1 / 1 | 3 / 18 | 2 | — |
| 5 | 2 | S-M | CART Box 2 | Evaluated | 0.3333 | 0.5263 | -0.1930 | 1 | 0.2000 | 1 / 5 | 1 / 18 | 3 | — |
| 6 | 2 | M-S | CART Box 4 | Evaluated | 0 | 0.3871 | -0.3871 | 0 | 0 | 0 / 1 | 1 / 18 | 2 | — |
| 7 | 1 | S-S | CART Box 3 | Evaluated | 0 | 0.7879 | -0.7879 | 0 | 0 | 0 / 1 | 1 / 18 | 2 | — |
| 8 | 2 | S-S | PRIM Box 1 | Evaluated | 0 | 0.7879 | -0.7879 | 0 | 0 | 0 / 1 | 1 / 18 | 3 | — |

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `CPU Mean`: [9.500, 10.125]
- `Alpha Dirichlet Mean`: [0.750, 0.812]
- `JSD Mean`: [0.022, 0.049]
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
  - CPU Mean [9.5, 10.1]
  - Alpha Dirichlet Mean [0.75, 0.812]
  - JSD Mean [0.0225, 0.0487]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.6190 |
| Train observations | 42 |
| Train target observations | 2 |
| Train samples in box | 3 |
| Train targets in box | 2 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.6667 |
| Coverage | 1 |
| Mean | 0.6667 |
| Mass | 0.0714 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 1 |
| Runs retained by box | 1 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0556 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0556 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `CPU Mean`: [10.125, 10.750]
- `Alpha Dirichlet Mean`: [0.750, 0.812]
- `Pattern Types Active`: [1.000, 1.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/7)
  - HDH: ON (7/7)
  - Message Compressor: OFF (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - CPU Mean [10.1, 10.8]
  - Alpha Dirichlet Mean [0.75, 0.812]
- **Other design conditions**:
  - Pattern Types Active [1, 1.5]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.8571 |
| Train recall / coverage | 0.4286 |
| Train target prevalence | 0.3333 |
| Train absolute lift | 0.5238 |
| Train observations | 42 |
| Train target observations | 14 |
| Train samples in box | 7 |
| Train targets in box | 6 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.8571 |
| Coverage | 0.4286 |
| Mean | 0.8571 |
| Mass | 0.1667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 5 |
| Runs retained by box | 3 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.2778 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.4000 |
| Absolute lift over held-out prevalence | 0.3889 |

### Box 3 — M-S (M,S)

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
| Train precision / density | 0.2857 |
| Train recall / coverage | 0.6667 |
| Train target prevalence | 0.0714 |
| Train absolute lift | 0.2143 |
| Train observations | 42 |
| Train target observations | 3 |
| Train samples in box | 7 |
| Train targets in box | 2 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2857 |
| Coverage | 0.6667 |
| Mean | 0.2857 |
| Mass | 0.1667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 1 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0556 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.2778 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.812, 0.875]
- `Pattern Instances`: [3.000, 9.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/14), ON (7/14)
  - HDH: OFF (14/14)
  - Message Compressor: ON (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/6), ON (3/6)
  - HDH: OFF (6/6)
  - Message Compressor: ON (6/6)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.812, 0.875]
  - Pattern Instances [3, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6087 |
| Train target prevalence | 0.5476 |
| Train absolute lift | 0.4524 |
| Train observations | 42 |
| Train target observations | 23 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.6087 |
| Mean | 1 |
| Mass | 0.3333 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 11 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.6111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5455 |
| Absolute lift over held-out prevalence | 0.3889 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `JSD Mean`: (not selected) or <= 0.010
- `Pattern Instances`: [3.001, 9.000]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/14), ON (7/14)
  - HDH: OFF (14/14)
  - Message Compressor: ON (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/6), ON (3/6)
  - HDH: OFF (6/6)
  - Message Compressor: ON (6/6)
- **Operating envelope**:
  - JSD Mean [0.00825, 0.0104]
  - Pattern Instances [3, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6087 |
| Train target prevalence | 0.5476 |
| Train absolute lift | 0.4524 |
| Train observations | 42 |
| Train target observations | 23 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 11 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.6111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5455 |
| Absolute lift over held-out prevalence | 0.3889 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `CPU Mean`: [10.125, 10.750]
- `JSD Mean`: [0.026, 0.055]
- `Pattern Instances`: [-0.000, 3.999]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (5/5)
  - HDH: ON (5/5)
  - Message Compressor: OFF (5/5)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (1/1)
  - HDH: ON (1/1)
  - Message Compressor: OFF (1/1)
- **Operating envelope**:
  - CPU Mean [10.1, 10.8]
  - JSD Mean [0.0262, 0.055]
  - Pattern Instances [-4.44e-16, 4]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3571 |
| Train target prevalence | 0.3333 |
| Train absolute lift | 0.6667 |
| Train observations | 42 |
| Train target observations | 14 |
| Train samples in box | 5 |
| Train targets in box | 5 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 5 |
| Runs retained by box | 1 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.2778 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2000 |
| Absolute lift over held-out prevalence | 0.7222 |

### Box 3 — S-S (S,S)

**Learned box conditions**

- `CPU Mean`: [9.500, 10.125]
- `JSD Mean`: [0.023, 0.049]
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
  - CPU Mean [9.5, 10.1]
  - JSD Mean [0.0225, 0.0487]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.6190 |
| Train observations | 42 |
| Train target observations | 2 |
| Train samples in box | 3 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 1 |
| Runs retained by box | 1 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0556 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0556 |

### Box 4 — M-S (M,S)

**Learned box conditions**

- `CPU Mean`: [9.500, 10.125]
- `JSD Mean`: [0.010, 0.023]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (2/2)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (1/1)
  - HDH: ON (1/1)
  - Message Compressor: OFF (1/1)
- **Operating envelope**:
  - CPU Mean [9.5, 10.1]
  - JSD Mean [0.0104, 0.0225]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.3333 |
| Train target prevalence | 0.0714 |
| Train absolute lift | 0.4286 |
| Train observations | 42 |
| Train target observations | 3 |
| Train samples in box | 2 |
| Train targets in box | 1 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 18 |
| Target runs before box | 1 |
| Runs retained by box | 1 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0556 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0556 |
