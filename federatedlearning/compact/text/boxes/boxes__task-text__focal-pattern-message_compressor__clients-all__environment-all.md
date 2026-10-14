# Discovered scenario boxes — Text task — Message Compressor ON

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all configurations with Message Compressor ON
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

### Box 1 — M-M (M,M)

**Learned box conditions**

- `HDH Instances`: [1.500, 8.000]
- `non_iid_percentage`: [62.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: ON (21/21)
  - Message Compressor: ON (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: ON (9/9)
  - Message Compressor: ON (9/9)
- **Operating envelope**:
  - HDH Instances [1.5, 8]
  - non-IID percentage [62.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.0476 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0024 |
| Train absolute lift | 0.0452 |
| Train observations | 420 |
| Train target observations | 1 |
| Train samples in box | 21 |
| Train targets in box | 1 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.0476 |
| Coverage | 1 |
| Mean | 0.0476 |
| Mass | 0.0500 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 0 |
| Runs retained by box | 9 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `Message Compressor Stress Percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (42/84), ON (42/84)
  - HDH: OFF (42/84), ON (42/84)
  - Message Compressor: ON (84/84)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/36), ON (18/36)
  - HDH: OFF (18/36), ON (18/36)
  - Message Compressor: ON (36/36)
- **Operating envelope**:
  - Message Compressor Stress Percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9032 |
| Train target prevalence | 0.2214 |
| Train absolute lift | 0.7786 |
| Train observations | 420 |
| Train target observations | 93 |
| Train samples in box | 84 |
| Train targets in box | 84 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.9032 |
| Mean | 1 |
| Mass | 0.2000 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 40 |
| Runs retained by box | 36 |
| Target runs inside box | 36 |
| Target prevalence before box | 0.2222 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9000 |
| Absolute lift over held-out prevalence | 0.7778 |

### Box 3 — L-M (L,M)

**Learned box conditions**

- `Message Compressor Instances`: [3.500, 10.000]
- `Client Selector Stress Percentage`: (not selected) or <= 62.500
- `Message Compressor Stress Percentage`: [12.500, 100.000]
- `HDH Stress Percentage`: (not selected) or <= 37.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `HDH Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (168/238), ON (70/238)
  - HDH: OFF (168/238), ON (70/238)
  - Message Compressor: ON (238/238)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (72/102), ON (30/102)
  - HDH: OFF (72/102), ON (30/102)
  - Message Compressor: ON (102/102)
- **Operating envelope**:
  - Message Compressor Instances [3.5, 10]
  - Client Selector Stress Percentage [20, 62.5] (%)
  - Message Compressor Stress Percentage [12.5, 100] (%)
  - HDH Stress Percentage [20, 37.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7414 |
| Train target prevalence | 0.7643 |
| Train absolute lift | 0.2357 |
| Train observations | 420 |
| Train target observations | 321 |
| Train samples in box | 238 |
| Train targets in box | 238 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.7414 |
| Mean | 1 |
| Mass | 0.5667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 137 |
| Runs retained by box | 102 |
| Target runs inside box | 102 |
| Target prevalence before box | 0.7611 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7445 |
| Absolute lift over held-out prevalence | 0.2389 |

### Box 4 — L-L (L,L)

**Learned box conditions**

- `Message Compressor Instances`: [1.000, 6.000]
- `non_iid_percentage`: [37.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (7/21), ON (14/21)
  - Message Compressor: ON (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (3/9), ON (6/9)
  - Message Compressor: ON (9/9)
- **Operating envelope**:
  - Message Compressor Instances [1, 6]
  - non-IID percentage [37.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2381 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0119 |
| Train absolute lift | 0.2262 |
| Train observations | 420 |
| Train target observations | 5 |
| Train samples in box | 21 |
| Train targets in box | 5 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2381 |
| Coverage | 1 |
| Mean | 0.2381 |
| Mass | 0.0500 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 3 |
| Runs retained by box | 9 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.0167 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.3167 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `Message Compressor Stress Percentage`: [12.508, 100.000]
- `HDH Stress Percentage`: (not selected) or <= 37.495
- `Message Compressor Instances`: [3.499, 10.000]
- **Includes NaN / not-selected values:** `HDH Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (168/238), ON (70/238)
  - HDH: OFF (168/238), ON (70/238)
  - Message Compressor: ON (238/238)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (72/102), ON (30/102)
  - HDH: OFF (72/102), ON (30/102)
  - Message Compressor: ON (102/102)
- **Operating envelope**:
  - Message Compressor Stress Percentage [12.5, 100] (%)
  - HDH Stress Percentage [20, 37.5] (%)
  - Message Compressor Instances [3.5, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7414 |
| Train target prevalence | 0.7643 |
| Train absolute lift | 0.2357 |
| Train observations | 420 |
| Train target observations | 321 |
| Train samples in box | 238 |
| Train targets in box | 238 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 137 |
| Runs retained by box | 102 |
| Target runs inside box | 102 |
| Target prevalence before box | 0.7611 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7445 |
| Absolute lift over held-out prevalence | 0.2389 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `Message Compressor Stress Percentage`: [0.000, 12.508]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (42/84), ON (42/84)
  - HDH: OFF (42/84), ON (42/84)
  - Message Compressor: ON (84/84)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/36), ON (18/36)
  - HDH: OFF (18/36), ON (18/36)
  - Message Compressor: ON (36/36)
- **Operating envelope**:
  - Message Compressor Stress Percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9032 |
| Train target prevalence | 0.2214 |
| Train absolute lift | 0.7786 |
| Train observations | 420 |
| Train target observations | 93 |
| Train samples in box | 84 |
| Train targets in box | 84 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 40 |
| Runs retained by box | 36 |
| Target runs inside box | 36 |
| Target prevalence before box | 0.2222 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9000 |
| Absolute lift over held-out prevalence | 0.7778 |

### Box 3 — L-L (L,L)

**Learned box conditions**

- `Message Compressor Stress Percentage`: [12.508, 100.000]
- `HDH Stress Percentage`: [62.501, 75.000]
- `Pattern Instances`: [2.000, 10.498]
- `Message Compressor Instances`: [3.499, 10.000]
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
  - Message Compressor Stress Percentage [12.5, 100] (%)
  - HDH Stress Percentage [62.5, 75] (%)
  - Pattern Instances [2, 10.5]
  - Message Compressor Instances [3.5, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5714 |
| Train recall / coverage | 0.8000 |
| Train target prevalence | 0.0119 |
| Train absolute lift | 0.5595 |
| Train observations | 420 |
| Train target observations | 5 |
| Train samples in box | 7 |
| Train targets in box | 4 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 3 |
| Runs retained by box | 3 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.0167 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.9833 |
