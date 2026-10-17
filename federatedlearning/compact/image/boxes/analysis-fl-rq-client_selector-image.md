# Discovered scenario boxes — Image task — client_selector

## Analysis scope

- **Task:** image classification
- **Configuration slice:** client_selector
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
| 1 | 1 | S-M | PRIM Box 2 | Evaluated | 0.4583 | 0.3636 | 0.0947 | 0.4231 | 0.5000 | 3 / 6 | 6 / 45 | 2 | — |
| 2 | 1 | M-M | CART Box 1 | Evaluated | 0.4138 | 0.4242 | -0.0104 | 1 | 0.2609 | 6 / 23 | 6 / 45 | 2 | — |
| 3 | 2 | M-M | PRIM Box 4 | Evaluated | 0.4138 | 0.4242 | -0.0104 | 1 | 0.2609 | 6 / 23 | 6 / 45 | 3 | — |
| 4 | 1 | M-S | PRIM Box 3 | Evaluated | 0.2744 | 0.4375 | -0.1631 | 0.5588 | 0.1818 | 2 / 11 | 3 / 45 | 4 | — |
| 5 | 1 | S-S | PRIM Box 1 | Evaluated | 0.2222 | 0.3841 | -0.1618 | 0.2500 | 0.2000 | 1 / 5 | 3 / 45 | 2 | — |
| 6 | 2 | S-S | CART Box 4 | Evaluated | 0.2222 | 0.3841 | -0.1618 | 0.2500 | 0.2000 | 1 / 5 | 3 / 45 | 4 | — |
| 7 | 2 | S-M | CART Box 2 | Evaluated | 0 | 0.3478 | -0.3478 | 0 | 0 | 0 / 6 | 3 / 45 | 3 | — |
| 8 | 2 | M-S | CART Box 3 | Evaluated | 0 | 0.1622 | -0.1622 | 0 | 0 | 0 / 11 | 3 / 45 | 4 | — |

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `CPU Mean`: [8.000, 8.125]
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
  - CPU Mean [8, 8.12]
  - non-IID percentage [50, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5714 |
| Train recall / coverage | 0.3077 |
| Train target prevalence | 0.1238 |
| Train absolute lift | 0.4476 |
| Train observations | 105 |
| Train target observations | 13 |
| Train samples in box | 7 |
| Train targets in box | 4 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.5714 |
| Coverage | 0.3077 |
| Mean | 0.5714 |
| Mass | 0.0667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 5 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.2000 |
| Absolute lift over held-out prevalence | 0.2222 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `non_iid_percentage`: [50.000, 75.000]
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
  - non-IID percentage [50, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.4000 |
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.2857 |
| Train observations | 105 |
| Train target observations | 15 |
| Train samples in box | 14 |
| Train targets in box | 6 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.4286 |
| Coverage | 0.4000 |
| Mean | 0.4286 |
| Mass | 0.1333 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 6 |
| Runs retained by box | 6 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.1333 |
| Precision inside box | 0.5000 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.3667 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `CPU Mean`: [8.125, 8.875]
- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [25.000, 50.000]
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
  - CPU Mean [8.12, 8.88]
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [25, 50] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2800 |
| Train target prevalence | 0.2381 |
| Train absolute lift | 0.7619 |
| Train observations | 105 |
| Train target observations | 25 |
| Train samples in box | 7 |
| Train targets in box | 7 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.2800 |
| Mean | 1 |
| Mass | 0.0667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 11 |
| Runs retained by box | 3 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.2444 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.1818 |
| Absolute lift over held-out prevalence | 0.4222 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `CPU Mean`: [10.125, 11.000]
- `non_iid_percentage`: [25.000, 50.000]
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
  - CPU Mean [10.1, 11]
  - non-IID percentage [25, 50] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2692 |
| Train target prevalence | 0.4952 |
| Train absolute lift | 0.5048 |
| Train observations | 105 |
| Train target observations | 52 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.2692 |
| Mean | 1 |
| Mass | 0.1333 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 23 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.5111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2609 |
| Absolute lift over held-out prevalence | 0.4889 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- `CPU Mean`: [10.125, 11.000]
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
  - CPU Mean [10.1, 11]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2692 |
| Train target prevalence | 0.4952 |
| Train absolute lift | 0.5048 |
| Train observations | 105 |
| Train target observations | 52 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 23 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.5111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2609 |
| Absolute lift over held-out prevalence | 0.4889 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `delay_percentage`: [50.000, 75.000]
- `CPU Mean`: [8.000, 8.874]
- `Total Clients`: [9.000, 10.000]
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
  - delay percentage [50, 75] (%)
  - CPU Mean [8, 8.87]
- **Other design conditions**:
  - Total Clients [9, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5714 |
| Train recall / coverage | 0.2667 |
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.4286 |
| Train observations | 105 |
| Train target observations | 15 |
| Train samples in box | 7 |
| Train targets in box | 4 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 6 |
| Runs retained by box | 3 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.1333 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.1333 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [25.000, 50.000]
- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `CPU Mean`: [8.000, 8.874]
- `Total Clients`: [9.000, 10.000]
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
  - delay percentage [25, 50] (%)
  - Alpha Dirichlet Mean [0.75, 0.9]
  - CPU Mean [8, 8.87]
- **Other design conditions**:
  - Total Clients [9, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.1200 |
| Train target prevalence | 0.2381 |
| Train absolute lift | 0.1905 |
| Train observations | 105 |
| Train target observations | 25 |
| Train samples in box | 7 |
| Train targets in box | 3 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 11 |
| Runs retained by box | 3 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.2444 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.2444 |

### Box 4 — S-S (S,S)

**Learned box conditions**

- `delay_percentage`: [25.000, 50.000]
- `Alpha Dirichlet Mean`: [0.600, 0.612]
- `CPU Mean`: [8.000, 8.874]
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
  - delay percentage [25, 50] (%)
  - Alpha Dirichlet Mean [0.6, 0.612]
  - CPU Mean [8, 8.87]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5714 |
| Train recall / coverage | 0.3077 |
| Train target prevalence | 0.1238 |
| Train absolute lift | 0.4476 |
| Train observations | 105 |
| Train target observations | 13 |
| Train samples in box | 7 |
| Train targets in box | 4 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 5 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.2000 |
| Absolute lift over held-out prevalence | 0.2222 |
