# Discovered scenario boxes — Image task — all

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all
- **Client-count scope:** 10 clients
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
- `CPU Mean`: [8.000, 8.750]
- `Alpha Dirichlet Mean`: [0.600, 0.825]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: ON (14/14)
  - HDH: OFF (7/14), ON (7/14)
  - Message Compressor: OFF (14/14)
- **Operating envelope**:
  - CPU Mean [8, 8.75]
  - Alpha Dirichlet Mean [0.6, 0.825]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.4524 |
| Train samples in box | 6 |
| Train targets in box | 3 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 6 |
| Runs retained by box | 6 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.0513 |
| Precision inside box | 0.5000 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.4487 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Alpha Dirichlet Mean`: [0.600, 0.825]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (63/63)
  - HDH: OFF (21/63), ON (42/63)
  - Message Compressor: OFF (42/63), ON (21/63)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.825]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8182 |
| Train target prevalence | 0.2784 |
| Train absolute lift | 0.7216 |
| Train samples in box | 27 |
| Train targets in box | 27 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 33 |
| Runs retained by box | 27 |
| Target runs inside box | 27 |
| Target prevalence before box | 0.2821 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8182 |
| Absolute lift over held-out prevalence | 0.7179 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.825, 0.900]
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (21/35), ON (14/35)
  - HDH: OFF (21/35), ON (14/35)
  - Message Compressor: OFF (7/35), ON (28/35)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.825, 0.9]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9375 |
| Train target prevalence | 0.1392 |
| Train absolute lift | 0.8608 |
| Train samples in box | 15 |
| Train targets in box | 15 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 16 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.1368 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9375 |
| Absolute lift over held-out prevalence | 0.8632 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `CPU Mean`: [10.250, 11.000]
- `Alpha Dirichlet Mean`: [0.675, 0.900]
- `JSD Mean`: (not selected) or <= 0.013
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (63/105), ON (42/105)
  - HDH: OFF (63/105), ON (42/105)
  - Message Compressor: OFF (35/105), ON (70/105)
- **Operating envelope**:
  - CPU Mean [10.2, 11]
  - Alpha Dirichlet Mean [0.675, 0.9]
  - JSD Mean [-0.01, 0.0131]
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7258 |
| Train target prevalence | 0.5348 |
| Train absolute lift | 0.4652 |
| Train samples in box | 45 |
| Train targets in box | 45 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 62 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.5299 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7258 |
| Absolute lift over held-out prevalence | 0.4701 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.825, 0.900]
- `delay_percentage`: [12.500, 100.000]
- `CPU Mean`: [10.250, 11.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (63/105), ON (42/105)
  - HDH: OFF (63/105), ON (42/105)
  - Message Compressor: OFF (35/105), ON (70/105)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.825, 0.9]
  - delay percentage [12.5, 100] (%)
  - CPU Mean [10.3, 11]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7258 |
| Train target prevalence | 0.5348 |
| Train absolute lift | 0.4652 |
| Train samples in box | 45 |
| Train targets in box | 45 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 62 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.5299 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7258 |
| Absolute lift over held-out prevalence | 0.4701 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.825]
- `Client Selector Criteria`: {(not selected)}
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (63/63)
  - HDH: OFF (21/63), ON (42/63)
  - Message Compressor: OFF (42/63), ON (21/63)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.825]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8182 |
| Train target prevalence | 0.2784 |
| Train absolute lift | 0.7216 |
| Train samples in box | 27 |
| Train targets in box | 27 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 33 |
| Runs retained by box | 27 |
| Target runs inside box | 27 |
| Target prevalence before box | 0.2821 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8182 |
| Absolute lift over held-out prevalence | 0.7179 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.825, 0.900]
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (21/35), ON (14/35)
  - HDH: OFF (21/35), ON (14/35)
  - Message Compressor: OFF (7/35), ON (28/35)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.825, 0.9]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9375 |
| Train target prevalence | 0.1392 |
| Train absolute lift | 0.8608 |
| Train samples in box | 15 |
| Train targets in box | 15 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 16 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.1368 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9375 |
| Absolute lift over held-out prevalence | 0.8632 |

### Box 4 — S-S (S,S)

**Learned box conditions**

- `JSD Mean`: (not selected) or <= 0.010
- `Alpha Dirichlet Mean`: [0.600, 0.825]
- `Client Selector Criteria`: {CPU}
- `CPU Mean`: [8.000, 8.750]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: ON (8/8)
  - HDH: OFF (7/8), ON (1/8)
  - Message Compressor: OFF (8/8)
- **Operating envelope**:
  - JSD Mean [-0.01, 0.01]
  - Alpha Dirichlet Mean [0.6, 0.825]
  - CPU Mean [8, 8.75]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3333 |
| Train recall / coverage | 0.1667 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.2857 |
| Train samples in box | 3 |
| Train targets in box | 1 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 6 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0513 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.1667 |
| Absolute lift over held-out prevalence | 0.2821 |
