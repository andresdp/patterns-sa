# Discovered scenario boxes — Text task — all

## Analysis scope

- **Task:** text classification
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
| 1 | 1 | L-M | CART Box 1 | Evaluated | 0.7258 | 0.7266 | -0.0008 | 1 | 0.5696 | 45 / 79 | 45 / 117 | 4 | — |
| 2 | 2 | L-M | PRIM Box 4 | Evaluated | 0.7258 | 0.7266 | -0.0008 | 1 | 0.5696 | 45 / 79 | 45 / 117 | 4 | — |
| 3 | 1 | L-S | CART Box 2 | Evaluated | 0.6522 | 0.6731 | -0.0209 | 1 | 0.4839 | 15 / 31 | 15 / 117 | 1 | — |
| 4 | 1 | L-L | PRIM Box 5 | Evaluated | 0.5618 | 0.5220 | 0.0397 | 0.3906 | 1 | 5 / 5 | 12 / 117 | 3 | — |
| 5 | 2 | L-L | CART Box 3 | Evaluated | 0.4958 | 0.3084 | 0.1874 | 0.6518 | 0.4000 | 2 / 5 | 3 / 117 | 4 | — |
| 6 | 1 | M-S | PRIM Box 1 | Evaluated | 0.3453 | 0.2353 | 0.1100 | 0.2087 | 1 | 2 / 2 | 9 / 117 | 2 | — |
| 7 | 2 | L-S | PRIM Box 3 | Evaluated | 0.3243 | 0.3373 | -0.0130 | 1 | 0.1935 | 6 / 31 | 6 / 117 | 2 | — |
| — | — | M-M | PRIM Box 2 | Unvalidated: no held-out target examples | not available | 0.2464 | not available | not available | not available | 0 / 0 | 14 / 117 | 2 | — |

## PRIM

### Box 1 — M-S (M,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.812]
- `Client Selector Stress Percentage`: [35.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (21/21)
  - HDH: OFF (7/21), ON (14/21)
  - Message Compressor: OFF (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: OFF (3/9), ON (6/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.812]
  - Client Selector Stress Percentage [35, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1429 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0110 |
| Train absolute lift | 0.1319 |
| Train observations | 273 |
| Train target observations | 3 |
| Train samples in box | 21 |
| Train targets in box | 3 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1429 |
| Coverage | 1 |
| Mean | 0.1429 |
| Mass | 0.0769 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 2 |
| Runs retained by box | 9 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.0171 |
| Precision inside box | 0.2222 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.2051 |

### Box 2 — M-M (M,M) — Unvalidated: no held-out target examples

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `HDH Instances`: [0.500, 3.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (28/32), ON (4/32)
  - HDH: ON (32/32)
  - Message Compressor: OFF (25/32), ON (7/32)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (12/14), ON (2/14)
  - HDH: ON (14/14)
  - Message Compressor: OFF (11/14), ON (3/14)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
  - HDH Instances [0.5, 3]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1562 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0183 |
| Train absolute lift | 0.1379 |
| Train observations | 273 |
| Train target observations | 5 |
| Train samples in box | 32 |
| Train targets in box | 5 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1562 |
| Coverage | 1 |
| Mean | 0.1562 |
| Mass | 0.1172 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 0 |
| Runs retained by box | 14 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 3 — L-S (L,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.500]
- `Client Selector Stress Percentage`: [22.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (7/14), ON (7/14)
  - Message Compressor: ON (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (3/6), ON (3/6)
  - Message Compressor: ON (6/6)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)
  - Client Selector Stress Percentage [22.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2029 |
| Train target prevalence | 0.2527 |
| Train absolute lift | 0.7473 |
| Train observations | 273 |
| Train target observations | 69 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.2029 |
| Mean | 1 |
| Mass | 0.0513 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 31 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.2650 |
| Precision inside box | 1 |
| Recall / target coverage | 0.1935 |
| Absolute lift over held-out prevalence | 0.7350 |

### Box 4 — L-M (L,M)

**Learned box conditions**

- `Pattern Instances`: [0.000, 5.500]
- `HDH Instances`: [0.000, 2.500]
- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 22.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (105/105)
  - HDH: OFF (77/105), ON (28/105)
  - Message Compressor: OFF (49/105), ON (56/105)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (45/45)
  - HDH: OFF (33/45), ON (12/45)
  - Message Compressor: OFF (21/45), ON (24/45)
- **Operating envelope**:
  - Pattern Instances [0, 5.5]
  - HDH Instances [0, 2.5]
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [20, 22.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5707 |
| Train target prevalence | 0.6740 |
| Train absolute lift | 0.3260 |
| Train observations | 273 |
| Train target observations | 184 |
| Train samples in box | 105 |
| Train targets in box | 105 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5707 |
| Mean | 1 |
| Mass | 0.3846 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5696 |
| Absolute lift over held-out prevalence | 0.3248 |

### Box 5 — L-L (L,L)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `Pattern Instances`: [2.500, 7.000]
- `HDH Instances`: [0.500, 3.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (28/28)
  - HDH: ON (28/28)
  - Message Compressor: OFF (21/28), ON (7/28)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (12/12)
  - HDH: ON (12/12)
  - Message Compressor: OFF (9/12), ON (3/12)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
  - Pattern Instances [2.5, 7]
  - HDH Instances [0.5, 3]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3929 |
| Train recall / coverage | 0.9167 |
| Train target prevalence | 0.0440 |
| Train absolute lift | 0.3489 |
| Train observations | 273 |
| Train target observations | 12 |
| Train samples in box | 28 |
| Train targets in box | 11 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.3929 |
| Coverage | 0.9167 |
| Mean | 0.3929 |
| Mass | 0.1026 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 5 |
| Runs retained by box | 12 |
| Target runs inside box | 5 |
| Target prevalence before box | 0.0427 |
| Precision inside box | 0.4167 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.3739 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `HDH Stress Percentage`: (not selected) or <= 62.498
- `Pattern Instances`: [0.000, 5.499]
- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 22.497
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `HDH Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (105/105)
  - HDH: OFF (77/105), ON (28/105)
  - Message Compressor: OFF (49/105), ON (56/105)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (45/45)
  - HDH: OFF (33/45), ON (12/45)
  - Message Compressor: OFF (21/45), ON (24/45)
- **Operating envelope**:
  - HDH Stress Percentage [20, 62.5] (%)
  - Pattern Instances [0, 5.5]
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [20, 22.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5707 |
| Train target prevalence | 0.6740 |
| Train absolute lift | 0.3260 |
| Train observations | 273 |
| Train target observations | 184 |
| Train samples in box | 105 |
| Train targets in box | 105 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5696 |
| Absolute lift over held-out prevalence | 0.3248 |

### Box 2 — L-S (L,S)

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
| Train recall / coverage | 0.5072 |
| Train target prevalence | 0.2527 |
| Train absolute lift | 0.7473 |
| Train observations | 273 |
| Train target observations | 69 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 31 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.2650 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4839 |
| Absolute lift over held-out prevalence | 0.7350 |

### Box 3 — L-L (L,L)

**Learned box conditions**

- `HDH Stress Percentage`: [62.498, 75.000]
- `Pattern Instances`: [0.000, 5.000]
- `delay_percentage`: [50.010, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 62.498
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

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
  - HDH Stress Percentage [62.5, 75] (%)
  - Pattern Instances [0, 5]
  - delay percentage [50, 100] (%)
  - Client Selector Stress Percentage [20, 62.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.0440 |
| Train absolute lift | 0.3846 |
| Train observations | 273 |
| Train target observations | 12 |
| Train samples in box | 7 |
| Train targets in box | 3 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 5 |
| Runs retained by box | 3 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.0427 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.4000 |
| Absolute lift over held-out prevalence | 0.6239 |
