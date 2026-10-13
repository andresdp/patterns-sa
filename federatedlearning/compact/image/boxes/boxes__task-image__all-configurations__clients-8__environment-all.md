# Discovered scenario boxes — Image task — all

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all
- **Client-count scope:** 8 clients
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

## How to read the metrics

- **Discovery metrics = training partition.** ADEPT uses these training runs to rank parameters and fit the PRIM/CART boxes. The table describes how well each learned rule matches the data it was discovered from.
- **Held-out metrics = test partition.** Each fixed rule is applied to separate runs set aside by `partition_seed`; those runs were not used to discover the box. These metrics show whether the observed association carries over to unseen data partitions.
- Compare the two sets: a drop in test precision or lift can indicate that the training association is less stable out of sample. Test recall/coverage shows how many target runs the rule still captures.
- Precision is the share of runs inside the box that reach the target; recall/coverage is the share of target runs captured by the box. Absolute lift is precision minus the target prevalence in the same partition, reported as a proportion.
- These are observational performance measures, not causal effects or guarantees for future deployments.

The architectural interpretation traces conditions through declared system-spec relationships.

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `Client Selector Criteria`: {CPU}
- `CPU Mean`: [8.250, 10.125]
- `JSD Mean`: [0.003, 0.090]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Operating envelope**:
  - CPU Mean [8.25, 10.1]
  - JSD Mean [0.00267, 0.09]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.3333 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.4524 |
| Train samples in box | 4 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 6 |
| Runs retained by box | 4 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.0513 |
| Precision inside box | 0.5000 |
| Recall / target coverage | 0.3333 |
| Absolute lift over held-out prevalence | 0.4487 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Alpha Dirichlet Mean`: [0.625, 0.688]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6774 |
| Train target prevalence | 0.2674 |
| Train absolute lift | 0.7326 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 31 |
| Runs retained by box | 21 |
| Target runs inside box | 21 |
| Target prevalence before box | 0.2650 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6774 |
| Absolute lift over held-out prevalence | 0.7350 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Alpha Dirichlet Mean`: [0.688, 0.875]
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.688, 0.875]
  - delay percentage [0, 12.5] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.1538 |
| Train absolute lift | 0.8462 |
| Train samples in box | 9 |
| Train targets in box | 9 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 18 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1538 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.8462 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Alpha Dirichlet Mean`: [0.812, 0.875]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.812, 0.875]
  - delay percentage [12.5, 100] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5323 |
| Train target prevalence | 0.5311 |
| Train absolute lift | 0.4689 |
| Train samples in box | 33 |
| Train targets in box | 33 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 62 |
| Runs retained by box | 33 |
| Target runs inside box | 33 |
| Target prevalence before box | 0.5299 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5323 |
| Absolute lift over held-out prevalence | 0.4701 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.813, 0.875]
- `Client Selector Criteria`: {(not selected)}
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.813, 0.875]
  - delay percentage [12.5, 100] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5323 |
| Train target prevalence | 0.5311 |
| Train absolute lift | 0.4689 |
| Train samples in box | 33 |
| Train targets in box | 33 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 62 |
| Runs retained by box | 33 |
| Target runs inside box | 33 |
| Target prevalence before box | 0.5299 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5323 |
| Absolute lift over held-out prevalence | 0.4701 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `Client Selector Criteria`: {(not selected)}
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6774 |
| Train target prevalence | 0.2674 |
| Train absolute lift | 0.7326 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 31 |
| Runs retained by box | 21 |
| Target runs inside box | 21 |
| Target prevalence before box | 0.2650 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6774 |
| Absolute lift over held-out prevalence | 0.7350 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.813, 0.875]
- `JSD Mean`: (not selected) or <= 0.006
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.813, 0.875]
  - JSD Mean [-0.00717, 0.00584]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7222 |
| Train target prevalence | 0.1538 |
| Train absolute lift | 0.8462 |
| Train samples in box | 13 |
| Train targets in box | 13 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 18 |
| Runs retained by box | 13 |
| Target runs inside box | 13 |
| Target prevalence before box | 0.1538 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7222 |
| Absolute lift over held-out prevalence | 0.8462 |

### Box 4 — S-S (S,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `Client Selector Criteria`: {CPU}
- `JSD Mean`: [0.014, 0.090]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
  - JSD Mean [0.0137, 0.09]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.1667 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.9524 |
| Train samples in box | 1 |
| Train targets in box | 1 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 6 |
| Runs retained by box | 1 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0513 |
| Precision inside box | 1 |
| Recall / target coverage | 0.1667 |
| Absolute lift over held-out prevalence | 0.9487 |
