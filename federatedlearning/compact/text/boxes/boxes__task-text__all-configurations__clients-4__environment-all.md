# Discovered scenario boxes — Text task — all

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all
- **Client-count scope:** 4 clients
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

### Box 1 — M-S (M,S)

**Learned box conditions**

- `CPU Mean`: [8.250, 10.125]
- `HDH Instances`: [0.500, 3.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/17), ON (10/17)
  - HDH: ON (17/17)
  - Message Compressor: OFF (17/17)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/8), ON (5/8)
  - HDH: ON (8/8)
  - Message Compressor: OFF (8/8)
- **Operating envelope**:
  - CPU Mean [8.25, 10.1]
  - HDH Instances [0.5, 3]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1250 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0110 |
| Train absolute lift | 0.1140 |
| Train samples in box | 8 |
| Train targets in box | 1 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 2 |
| Runs retained by box | 8 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0171 |
| Precision inside box | 0.1250 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.1079 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `Client Selector Criteria`: {CPU}
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
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

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.1935 |
| Train target prevalence | 0.2527 |
| Train absolute lift | 0.7473 |
| Train samples in box | 6 |
| Train targets in box | 6 |

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

### Box 3 — L-M (L,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Pattern Instances`: [0.000, 5.500]
- `HDH Instances`: [0.000, 2.500]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
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
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5696 |
| Train target prevalence | 0.6740 |
| Train absolute lift | 0.3260 |
| Train samples in box | 45 |
| Train targets in box | 45 |

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

### Box 4 — L-L (L,L)

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
| Train precision / density | 0.4167 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0440 |
| Train absolute lift | 0.3727 |
| Train samples in box | 12 |
| Train targets in box | 5 |

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

- `Client Selector Criteria`: {(not selected)}
- `delay_percentage`: [12.500, 100.000]
- `HDH Instances`: [0.000, 2.500]
- `Pattern Instances`: [0.000, 5.499]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (105/105)
  - HDH: OFF (77/105), ON (28/105)
  - Message Compressor: OFF (49/105), ON (56/105)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (45/45)
  - HDH: OFF (33/45), ON (12/45)
  - Message Compressor: OFF (21/45), ON (24/45)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - HDH Instances [0, 2.5]
  - Pattern Instances [0, 5.5]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5696 |
| Train target prevalence | 0.6740 |
| Train absolute lift | 0.3260 |
| Train samples in box | 45 |
| Train targets in box | 45 |

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
| Train recall / coverage | 0.4839 |
| Train target prevalence | 0.2527 |
| Train absolute lift | 0.7473 |
| Train samples in box | 15 |
| Train targets in box | 15 |

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

- `Client Selector Criteria`: {(not selected)}
- `delay_percentage`: [50.010, 100.000]
- `HDH Instances`: [2.500, 3.000]
- `Pattern Types Active`: [1.500, 3.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/7)
  - HDH: ON (7/7)
  - Message Compressor: ON (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: ON (3/3)
  - Message Compressor: ON (3/3)
- **Operating envelope**:
  - delay percentage [50, 100] (%)
  - HDH Instances [2.5, 3]
- **Other design conditions**:
  - Pattern Types Active [1.5, 3]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6000 |
| Train target prevalence | 0.0440 |
| Train absolute lift | 0.9560 |
| Train samples in box | 3 |
| Train targets in box | 3 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 5 |
| Runs retained by box | 3 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.0427 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6000 |
| Absolute lift over held-out prevalence | 0.9573 |
