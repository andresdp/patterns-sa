# Discovered scenario boxes — Image task — message_compressor

## Analysis scope

- **Task:** image classification
- **Configuration slice:** message_compressor
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

## PRIM

### Box 1 — S-M (S,M)

**Learned box conditions**

- `Message Compressor Instances`: [6.000, 10.000]
- `non_iid_percentage`: [50.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (14/14)
  - HDH: OFF (14/14)
  - Message Compressor: ON (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (6/6)
  - HDH: OFF (6/6)
  - Message Compressor: ON (6/6)
- **Operating envelope**:
  - Message Compressor Instances [6, 10]
  - non-IID percentage [50, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9333 |
| Train target prevalence | 0.1020 |
| Train absolute lift | 0.8980 |
| Train observations | 147 |
| Train target observations | 15 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.9333 |
| Mean | 1 |
| Mass | 0.0952 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 7 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8571 |
| Absolute lift over held-out prevalence | 0.8889 |

### Box 2 — M-S (M,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: ON (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (9/9)
  - Message Compressor: ON (9/9)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.8571 |
| Train observations | 147 |
| Train target observations | 21 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 1 |
| Mean | 1 |
| Mass | 0.1429 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1429 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8571 |

### Box 3 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (105/105)
  - HDH: OFF (105/105)
  - Message Compressor: ON (105/105)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (45/45)
  - HDH: OFF (45/45)
  - Message Compressor: ON (45/45)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9459 |
| Train target prevalence | 0.7551 |
| Train absolute lift | 0.2449 |
| Train observations | 147 |
| Train target observations | 111 |
| Train samples in box | 105 |
| Train targets in box | 105 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.9459 |
| Mean | 1 |
| Mass | 0.7143 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 47 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.7460 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9574 |
| Absolute lift over held-out prevalence | 0.2540 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `delay_percentage`: [12.485, 100.000]
- `Alpha Dirichlet Mean`: [0.750, 0.900]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (105/105)
  - HDH: OFF (105/105)
  - Message Compressor: ON (105/105)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (45/45)
  - HDH: OFF (45/45)
  - Message Compressor: ON (45/45)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Alpha Dirichlet Mean [0.75, 0.9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9459 |
| Train target prevalence | 0.7551 |
| Train absolute lift | 0.2449 |
| Train observations | 147 |
| Train target observations | 111 |
| Train samples in box | 105 |
| Train targets in box | 105 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 47 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.7460 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9574 |
| Absolute lift over held-out prevalence | 0.2540 |

### Box 2 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.485]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: ON (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (9/9)
  - Message Compressor: ON (9/9)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.8571 |
| Train observations | 147 |
| Train target observations | 21 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1429 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8571 |

### Box 3 — S-M (S,M)

**Learned box conditions**

- `delay_percentage`: [12.485, 100.000]
- `Alpha Dirichlet Mean`: [0.600, 0.750]
- `Message Compressor Instances`: [5.999, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (14/14)
  - HDH: OFF (14/14)
  - Message Compressor: ON (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (6/6)
  - HDH: OFF (6/6)
  - Message Compressor: ON (6/6)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Alpha Dirichlet Mean [0.6, 0.75]
  - Message Compressor Instances [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9333 |
| Train target prevalence | 0.1020 |
| Train absolute lift | 0.8980 |
| Train observations | 147 |
| Train target observations | 15 |
| Train samples in box | 14 |
| Train targets in box | 14 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 7 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8571 |
| Absolute lift over held-out prevalence | 0.8889 |
