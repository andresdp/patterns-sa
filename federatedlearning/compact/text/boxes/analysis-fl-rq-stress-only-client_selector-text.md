# Discovered scenario boxes — Text task — Client Selector only

## Analysis scope

- **Task:** text classification
- **Configuration slice:** exactly Client Selector ON; other patterns OFF
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
| 1 | 1 | L-S | PRIM Box 2 | Evaluated | 0.4421 | 0.4970 | -0.0549 | 0.6000 | 0.3500 | 7 / 20 | 9 / 45 | 3 | — |
| 2 | 1 | L-M | CART Box 1 | Evaluated | 0.4000 | 0.4118 | -0.0118 | 1 | 0.2500 | 6 / 24 | 6 / 45 | 2 | Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%) |
| 3 | 2 | L-M | PRIM Box 3 | Evaluated | 0.4000 | 0.4118 | -0.0118 | 1 | 0.2500 | 6 / 24 | 6 / 45 | 2 | Representative for CART Box 1 |
| 4 | 2 | L-S | CART Box 2 | Evaluated | 0.2609 | 0.1194 | 0.1415 | 1 | 0.1500 | 3 / 20 | 3 / 45 | 5 | — |
| 5 | 1 | M-S | PRIM Box 1 | Evaluated | 0 | 0.3789 | -0.3789 | 0 | 0 | 0 / 1 | 3 / 45 | 2 | — |

## PRIM

### Box 1 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `non_iid_percentage`: [50.000, 75.000]
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
  - non-IID percentage [50, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2857 |
| Train recall / coverage | 0.6667 |
| Train target prevalence | 0.0286 |
| Train absolute lift | 0.2571 |
| Train observations | 105 |
| Train target observations | 3 |
| Train samples in box | 7 |
| Train targets in box | 2 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2857 |
| Coverage | 0.6667 |
| Mean | 0.2857 |
| Mass | 0.0667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 1 |
| Runs retained by box | 3 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0222 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0222 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `CPU Mean`: [8.000, 8.875]
- `non_iid_percentage`: [25.000, 50.000]
- `delay_percentage`: [25.000, 50.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: OFF (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: OFF (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - CPU Mean [8, 8.88]
  - non-IID percentage [25, 50] (%)
  - delay percentage [25, 50] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.8571 |
| Train recall / coverage | 0.3750 |
| Train target prevalence | 0.4571 |
| Train absolute lift | 0.4000 |
| Train observations | 105 |
| Train target observations | 48 |
| Train samples in box | 21 |
| Train targets in box | 18 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.8571 |
| Coverage | 0.3750 |
| Mean | 0.8571 |
| Mass | 0.2000 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 20 |
| Runs retained by box | 9 |
| Target runs inside box | 7 |
| Target prevalence before box | 0.4444 |
| Precision inside box | 0.7778 |
| Recall / target coverage | 0.3500 |
| Absolute lift over held-out prevalence | 0.3333 |

### Box 3 — L-M (L,M) — Representative for CART Box 1

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Client Selector Stress Percentage`: [25.000, 37.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (14/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (6/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - Client Selector Stress Percentage [25, 37.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2593 |
| Train target prevalence | 0.5143 |
| Train absolute lift | 0.4857 |
| Train observations | 105 |
| Train target observations | 54 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.2593 |
| Mean | 1 |
| Mass | 0.1333 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 24 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.5333 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2500 |
| Absolute lift over held-out prevalence | 0.4667 |

## CART

### Box 1 — L-M (L,M) — Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- `Client Selector Stress Percentage`: [25.000, 37.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (14/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (6/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - Client Selector Stress Percentage [25, 37.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2593 |
| Train target prevalence | 0.5143 |
| Train absolute lift | 0.4857 |
| Train observations | 105 |
| Train target observations | 54 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 24 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.5333 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2500 |
| Absolute lift over held-out prevalence | 0.4667 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `non_iid_percentage`: [50.000, 75.000]
- `delay_percentage`: [25.000, 50.000]
- `Alpha Dirichlet Mean`: [0.612, 0.900]
- `Client Selector Stress Percentage`: [62.500, 75.000]
- `Total Clients`: [5.999, 10.000]
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
  - non-IID percentage [50, 75] (%)
  - delay percentage [25, 50] (%)
  - Alpha Dirichlet Mean [0.612, 0.9]
  - Client Selector Stress Percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5714 |
| Train recall / coverage | 0.0833 |
| Train target prevalence | 0.4571 |
| Train absolute lift | 0.1143 |
| Train observations | 105 |
| Train target observations | 48 |
| Train samples in box | 7 |
| Train targets in box | 4 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 20 |
| Runs retained by box | 3 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.4444 |
| Precision inside box | 1 |
| Recall / target coverage | 0.1500 |
| Absolute lift over held-out prevalence | 0.5556 |
