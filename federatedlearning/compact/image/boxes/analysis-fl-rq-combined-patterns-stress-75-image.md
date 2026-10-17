# Discovered scenario boxes — Image task — all available client counts (4, 8, 10) — 75% stress

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all supported non-empty combinations with every active pattern at target stress
- **Target stress:** 75%
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
| 1 | 1 | S-M | CART Box 1 | Evaluated | 0.8571 | 0.8485 | 0.0087 | 1 | 0.7500 | 30 / 40 | 30 / 108 | 3 | — |
| 2 | 2 | S-M | PRIM Box 2 | Evaluated | 0.7500 | 0.7417 | 0.0083 | 1 | 0.6000 | 24 / 40 | 24 / 108 | 3 | — |
| 3 | 1 | M-M | CART Box 2 | Evaluated | 0.5714 | 0.5676 | 0.0039 | 1 | 0.4000 | 18 / 45 | 18 / 108 | 3 | — |
| 4 | 2 | M-M | PRIM Box 4 | Evaluated | 0.5714 | 0.5676 | 0.0039 | 1 | 0.4000 | 18 / 45 | 18 / 108 | 4 | — |
| 5 | 1 | S-S | CART Box 3 | Evaluated | 0.4444 | 0.5714 | -0.1270 | 1 | 0.2857 | 4 / 14 | 4 / 108 | 4 | — |
| 6 | 2 | S-S | PRIM Box 1 | Evaluated | 0.4444 | 0.6047 | -0.1602 | 1 | 0.2857 | 4 / 14 | 4 / 108 | 4 | — |
| 7 | 1 | M-S | PRIM Box 3 | Evaluated | 0.3674 | 0.5926 | -0.2252 | 0.2536 | 0.6667 | 6 / 9 | 19 / 108 | 4 | — |
| 8 | 2 | M-S | CART Box 4 | Evaluated | 0.1579 | 0.2071 | -0.0492 | 0.2727 | 0.1111 | 1 / 9 | 3 / 108 | 4 | — |

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Client Selector Criteria`: {CPU}
- `JSD Mean`: [0.010, 0.110]
- `delay_percentage`: [25.000, 50.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (13/13)
  - HDH: ON (13/13)
  - Message Compressor: OFF (13/13)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (4/4)
  - HDH: ON (4/4)
  - Message Compressor: OFF (4/4)
- **Operating envelope**:
  - JSD Mean [0.01, 0.11]
  - delay percentage [25, 50] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4333 |
| Train target prevalence | 0.1190 |
| Train absolute lift | 0.8810 |
| Train observations | 252 |
| Train target observations | 30 |
| Train samples in box | 13 |
| Train targets in box | 13 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.4333 |
| Mean | 1 |
| Mass | 0.0516 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 14 |
| Runs retained by box | 4 |
| Target runs inside box | 4 |
| Target prevalence before box | 0.1296 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2857 |
| Absolute lift over held-out prevalence | 0.8704 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Client Selector Criteria`: {(not selected)}
- `JSD Mean`: [0.004, 0.120]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (56/56)
  - HDH: ON (56/56)
  - Message Compressor: OFF (42/56), ON (14/56)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (24/24)
  - HDH: ON (24/24)
  - Message Compressor: OFF (18/24), ON (6/24)
- **Operating envelope**:
  - JSD Mean [0.004, 0.12]
- **Other design conditions**:
  - Total Clients [6, 10]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5895 |
| Train target prevalence | 0.3770 |
| Train absolute lift | 0.6230 |
| Train observations | 252 |
| Train target observations | 95 |
| Train samples in box | 56 |
| Train targets in box | 56 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5895 |
| Mean | 1 |
| Mass | 0.2222 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 40 |
| Runs retained by box | 24 |
| Target runs inside box | 24 |
| Target prevalence before box | 0.3704 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6000 |
| Absolute lift over held-out prevalence | 0.6296 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Client Selector Criteria`: {CPU}
- `Alpha Dirichlet Mean`: [0.613, 0.900]
- `JSD Mean`: (not selected) or <= 0.033
- `delay_percentage`: [25.000, 50.000]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (39/39)
  - HDH: OFF (35/39), ON (4/39)
  - Message Compressor: OFF (39/39)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (19/19)
  - HDH: OFF (15/19), ON (4/19)
  - Message Compressor: OFF (19/19)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.613, 0.9]
  - JSD Mean [-0.012, 0.0325]
  - delay percentage [25, 50] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4872 |
| Train recall / coverage | 0.9048 |
| Train target prevalence | 0.0833 |
| Train absolute lift | 0.4038 |
| Train observations | 252 |
| Train target observations | 21 |
| Train samples in box | 39 |
| Train targets in box | 19 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.4872 |
| Coverage | 0.9048 |
| Mean | 0.4872 |
| Mass | 0.1548 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 9 |
| Runs retained by box | 19 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.0833 |
| Precision inside box | 0.3158 |
| Recall / target coverage | 0.6667 |
| Absolute lift over held-out prevalence | 0.2325 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `JSD Mean`: (not selected) or <= 0.051
- `delay_percentage`: [50.000, 75.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (42/42)
  - HDH: OFF (42/42)
  - Message Compressor: ON (42/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/18)
  - HDH: OFF (18/18)
  - Message Compressor: ON (18/18)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.75, 0.9]
  - JSD Mean [-0.012, 0.0506]
  - delay percentage [50, 75] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3962 |
| Train target prevalence | 0.4206 |
| Train absolute lift | 0.5794 |
| Train observations | 252 |
| Train target observations | 106 |
| Train samples in box | 42 |
| Train targets in box | 42 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.3962 |
| Mean | 1 |
| Mass | 0.1667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 45 |
| Runs retained by box | 18 |
| Target runs inside box | 18 |
| Target prevalence before box | 0.4167 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4000 |
| Absolute lift over held-out prevalence | 0.5833 |

## CART

### Box 1 — S-M (S,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.750]
- `Client Selector Criteria`: {(not selected)}
- `Total Clients`: [5.999, 10.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (70/70)
  - HDH: OFF (14/70), ON (56/70)
  - Message Compressor: OFF (42/70), ON (28/70)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (30/30)
  - HDH: OFF (6/30), ON (24/30)
  - Message Compressor: OFF (18/30), ON (12/30)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.75]
- **Other design conditions**:
  - Total Clients [6, 10]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7368 |
| Train target prevalence | 0.3770 |
| Train absolute lift | 0.6230 |
| Train observations | 252 |
| Train target observations | 95 |
| Train samples in box | 70 |
| Train targets in box | 70 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 40 |
| Runs retained by box | 30 |
| Target runs inside box | 30 |
| Target prevalence before box | 0.3704 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7500 |
| Absolute lift over held-out prevalence | 0.6296 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [50.001, 75.000]
- `Client Selector Criteria`: {(not selected)}
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (42/42)
  - HDH: OFF (42/42)
  - Message Compressor: ON (42/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/18)
  - HDH: OFF (18/18)
  - Message Compressor: ON (18/18)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [50, 75] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3962 |
| Train target prevalence | 0.4206 |
| Train absolute lift | 0.5794 |
| Train observations | 252 |
| Train target observations | 106 |
| Train samples in box | 42 |
| Train targets in box | 42 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 45 |
| Runs retained by box | 18 |
| Target runs inside box | 18 |
| Target prevalence before box | 0.4167 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4000 |
| Absolute lift over held-out prevalence | 0.5833 |

### Box 3 — S-S (S,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.750]
- `Client Selector Criteria`: {CPU}
- `Total Clients`: [5.999, 10.000]
- `JSD Mean`: [0.004, 0.097]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (12/12)
  - HDH: ON (12/12)
  - Message Compressor: OFF (12/12)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (4/4)
  - HDH: ON (4/4)
  - Message Compressor: OFF (4/4)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.75]
  - JSD Mean [0.004, 0.0975]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4000 |
| Train target prevalence | 0.1190 |
| Train absolute lift | 0.8810 |
| Train observations | 252 |
| Train target observations | 30 |
| Train samples in box | 12 |
| Train targets in box | 12 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 14 |
| Runs retained by box | 4 |
| Target runs inside box | 4 |
| Target prevalence before box | 0.1296 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2857 |
| Absolute lift over held-out prevalence | 0.8704 |

### Box 4 — M-S (M,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.750]
- `Client Selector Criteria`: {CPU}
- `Total Clients`: [4.000, 5.999]
- `JSD Mean`: (not selected) or <= -0.006
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
  - Alpha Dirichlet Mean [0.6, 0.75]
  - JSD Mean [-0.012, -0.00601]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.1429 |
| Train target prevalence | 0.0833 |
| Train absolute lift | 0.3452 |
| Train observations | 252 |
| Train target observations | 21 |
| Train samples in box | 7 |
| Train targets in box | 3 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 9 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0833 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.1111 |
| Absolute lift over held-out prevalence | 0.2500 |
