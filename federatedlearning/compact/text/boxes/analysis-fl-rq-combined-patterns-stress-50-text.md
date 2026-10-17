# Discovered scenario boxes — Text task — all available client counts (4, 8, 10) — 50% stress

## Analysis scope

- **Task:** text classification
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
| 1 | 1 | L-M | CART Box 1 | Evaluated | 0.7297 | 0.7442 | -0.0145 | 1 | 0.5745 | 27 / 47 | 27 / 54 | 2 | — |
| 2 | 2 | L-M | PRIM Box 4 | Evaluated | 0.6377 | 0.6242 | 0.0135 | 1 | 0.4681 | 22 / 47 | 22 / 54 | 3 | — |
| 3 | 1 | L-S | CART Box 2 | Evaluated | 0.1774 | 0.3683 | -0.1908 | 0.2340 | 0.1429 | 1 / 7 | 3 / 54 | 5 | — |
| 4 | 2 | L-S | PRIM Box 3 | Evaluated | 0.1774 | 0.3683 | -0.1908 | 0.2340 | 0.1429 | 1 / 7 | 3 / 54 | 5 | — |
| — | — | M-M | PRIM Box 2 | Unvalidated: no held-out target examples | not available | 0.1118 | not available | not available | not available | 0 / 0 | 11 / 54 | 2 | — |
| — | — | L-L | PRIM Box 5 | Unvalidated: no held-out target examples | not available | 0.2394 | not available | not available | not available | 0 / 0 | 3 / 54 | 3 | — |
| — | — | M-S | PRIM Box 1 | Unvalidated: no held-out target examples | not available | 0.3467 | not available | not available | not available | 0 / 0 | 6 / 54 | 3 | — |

## PRIM

### Box 1 — M-S (M,S) — Unvalidated: no held-out target examples

**Learned box conditions**

- `Total Clients`: [4.000, 9.000]
- `Client Selector Criteria`: {CPU}
- `HDH Instances`: [0.500, 2.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: ON (6/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - HDH Instances [0.5, 2.5]
- **Other design conditions**:
  - Total Clients [4, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2222 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0159 |
| Train absolute lift | 0.2063 |
| Train observations | 126 |
| Train target observations | 2 |
| Train samples in box | 9 |
| Train targets in box | 2 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2222 |
| Coverage | 1 |
| Mean | 0.2222 |
| Mass | 0.0714 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 0 |
| Runs retained by box | 6 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 2 — M-M (M,M) — Unvalidated: no held-out target examples

**Learned box conditions**

- `JSD Mean`: [0.007, 0.070]
- `HDH Instances`: [0.500, 5.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (12/15), ON (3/15)
  - HDH: ON (15/15)
  - Message Compressor: OFF (9/15), ON (6/15)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (8/11), ON (3/11)
  - HDH: ON (11/11)
  - Message Compressor: OFF (7/11), ON (4/11)
- **Operating envelope**:
  - JSD Mean [0.007, 0.07]
  - HDH Instances [0.5, 5]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.0667 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0079 |
| Train absolute lift | 0.0587 |
| Train observations | 126 |
| Train target observations | 1 |
| Train samples in box | 15 |
| Train targets in box | 1 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.0667 |
| Coverage | 1 |
| Mean | 0.0667 |
| Mass | 0.1190 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 0 |
| Runs retained by box | 11 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 3 — L-S (L,S)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Client Selector Criteria`: {CPU}
- `Pattern Types Active`: [1.000, 1.500]
- `Pattern Instances`: [1.000, 4.000]
- `HDH Instances`: [0.000, 2.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (7/7)
  - HDH: OFF (7/7)
  - Message Compressor: OFF (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: OFF (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - Pattern Instances [1, 4]
  - HDH Instances [0, 2.5]
- **Other design conditions**:
  - Total Clients [4, 6]
  - Pattern Types Active [1, 1.5]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5714 |
| Train recall / coverage | 0.2857 |
| Train target prevalence | 0.1111 |
| Train absolute lift | 0.4603 |
| Train observations | 126 |
| Train target observations | 14 |
| Train samples in box | 7 |
| Train targets in box | 4 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.5714 |
| Coverage | 0.2857 |
| Mean | 0.5714 |
| Mass | 0.0556 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 7 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.1296 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.1429 |
| Absolute lift over held-out prevalence | 0.2037 |

### Box 4 — L-M (L,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `JSD Mean`: (not selected) or <= 0.032
- `Pattern Instances`: [4.500, 15.000]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (34/49), ON (15/49)
  - HDH: OFF (28/49), ON (21/49)
  - Message Compressor: OFF (8/49), ON (41/49)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (15/22), ON (7/22)
  - HDH: OFF (12/22), ON (10/22)
  - Message Compressor: OFF (4/22), ON (18/22)
- **Operating envelope**:
  - JSD Mean [-0.007, 0.0315]
  - Pattern Instances [4.5, 15]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4537 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train observations | 126 |
| Train target observations | 108 |
| Train samples in box | 49 |
| Train targets in box | 49 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.4537 |
| Mean | 1 |
| Mass | 0.3889 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 47 |
| Runs retained by box | 22 |
| Target runs inside box | 22 |
| Target prevalence before box | 0.8704 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4681 |
| Absolute lift over held-out prevalence | 0.1296 |

### Box 5 — L-L (L,L) — Unvalidated: no held-out target examples

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Pattern Instances`: [4.500, 15.000]
- `HDH Instances`: [0.500, 5.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/7)
  - HDH: ON (7/7)
  - Message Compressor: ON (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: ON (3/3)
  - Message Compressor: ON (3/3)
- **Operating envelope**:
  - Pattern Instances [4.5, 15]
  - HDH Instances [0.5, 5]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1429 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0079 |
| Train absolute lift | 0.1349 |
| Train observations | 126 |
| Train target observations | 1 |
| Train samples in box | 7 |
| Train targets in box | 1 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1429 |
| Coverage | 1 |
| Mean | 0.1429 |
| Mass | 0.0556 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 0 |
| Runs retained by box | 3 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `Pattern Instances`: [3.500, 15.000]
- `Total Clients`: [5.999, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (42/64), ON (22/64)
  - HDH: OFF (28/64), ON (36/64)
  - Message Compressor: OFF (22/64), ON (42/64)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/27), ON (9/27)
  - HDH: OFF (12/27), ON (15/27)
  - Message Compressor: OFF (9/27), ON (18/27)
- **Operating envelope**:
  - Pattern Instances [3.5, 15]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5926 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train observations | 126 |
| Train target observations | 108 |
| Train samples in box | 64 |
| Train targets in box | 64 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 47 |
| Runs retained by box | 27 |
| Target runs inside box | 27 |
| Target prevalence before box | 0.8704 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5745 |
| Absolute lift over held-out prevalence | 0.1296 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `Client Selector Criteria`: {CPU}
- `JSD Mean`: (not selected) or <= -0.003
- `Pattern Instances`: [1.000, 1.999]
- `HDH Instances`: [0.000, 1.500]
- `Total Clients`: [4.000, 5.999]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (7/7)
  - HDH: OFF (7/7)
  - Message Compressor: OFF (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: OFF (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - JSD Mean [-0.007, -0.0035]
  - Pattern Instances [1, 2]
  - HDH Instances [0, 1.5]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5714 |
| Train recall / coverage | 0.2857 |
| Train target prevalence | 0.1111 |
| Train absolute lift | 0.4603 |
| Train observations | 126 |
| Train target observations | 14 |
| Train samples in box | 7 |
| Train targets in box | 4 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 7 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.1296 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.1429 |
| Absolute lift over held-out prevalence | 0.2037 |
