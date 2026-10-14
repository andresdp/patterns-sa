# Discovered scenario boxes — Text task — HDH ON

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all configurations with HDH ON
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

### Box 1 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 9.000]
- `Pattern Instances`: [1.500, 3.500]
- `Client Selector Stress Percentage`: [37.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (21/21)
  - HDH: ON (21/21)
  - Message Compressor: OFF (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (10/10)
  - HDH: ON (10/10)
  - Message Compressor: OFF (10/10)
- **Operating envelope**:
  - Pattern Instances [1.5, 3.5]
  - Client Selector Stress Percentage [37.5, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2381 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0149 |
| Train absolute lift | 0.2232 |
| Train observations | 336 |
| Train target observations | 5 |
| Train samples in box | 21 |
| Train targets in box | 5 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2381 |
| Coverage | 1 |
| Mean | 0.2381 |
| Mass | 0.0625 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 2 |
| Runs retained by box | 10 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.0139 |
| Precision inside box | 0.2000 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.1861 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `Client Selector Stress Percentage`: [47.500, 75.000]
- `HDH Stress Percentage`: [62.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (21/21)
  - HDH: ON (21/21)
  - Message Compressor: OFF (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - Client Selector Stress Percentage [47.5, 75] (%)
  - HDH Stress Percentage [62.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1905 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0238 |
| Train absolute lift | 0.1667 |
| Train observations | 336 |
| Train target observations | 8 |
| Train samples in box | 21 |
| Train targets in box | 4 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1905 |
| Coverage | 0.5000 |
| Mean | 0.1905 |
| Mass | 0.0625 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 2 |
| Runs retained by box | 9 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0139 |
| Precision inside box | 0.1111 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.0972 |

### Box 3 — L-S (L,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.500]
- `Client Selector Stress Percentage`: [22.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (21/21)
  - HDH: ON (21/21)
  - Message Compressor: ON (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: ON (9/9)
  - Message Compressor: ON (9/9)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)
  - Client Selector Stress Percentage [22.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3333 |
| Train target prevalence | 0.1875 |
| Train absolute lift | 0.8125 |
| Train observations | 336 |
| Train target observations | 63 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.3333 |
| Mean | 1 |
| Mass | 0.0625 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 26 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1806 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3462 |
| Absolute lift over held-out prevalence | 0.8194 |

### Box 4 — L-M (L,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 37.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (126/168), ON (42/168)
  - HDH: ON (168/168)
  - Message Compressor: OFF (84/168), ON (84/168)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (54/72), ON (18/72)
  - HDH: ON (72/72)
  - Message Compressor: OFF (36/72), ON (36/72)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [20, 37.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6774 |
| Train target prevalence | 0.7381 |
| Train absolute lift | 0.2619 |
| Train observations | 336 |
| Train target observations | 248 |
| Train samples in box | 168 |
| Train targets in box | 168 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.6774 |
| Mean | 1 |
| Mass | 0.5000 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 109 |
| Runs retained by box | 72 |
| Target runs inside box | 72 |
| Target prevalence before box | 0.7569 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6606 |
| Absolute lift over held-out prevalence | 0.2431 |

### Box 5 — L-L (L,L)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Client Selector Stress Percentage`: (not selected) or <= 47.500
- `HDH Stress Percentage`: [62.500, 75.000]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

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
  - Client Selector Stress Percentage [20, 47.5] (%)
  - HDH Stress Percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3929 |
| Train recall / coverage | 0.9167 |
| Train target prevalence | 0.0357 |
| Train absolute lift | 0.3571 |
| Train observations | 336 |
| Train target observations | 12 |
| Train samples in box | 28 |
| Train targets in box | 11 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.3929 |
| Coverage | 0.9167 |
| Mean | 0.3929 |
| Mass | 0.0833 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 5 |
| Runs retained by box | 12 |
| Target runs inside box | 5 |
| Target prevalence before box | 0.0347 |
| Precision inside box | 0.4167 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.3819 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `delay_percentage`: [12.490, 100.000]
- `Total Clients`: [5.999, 10.000]
- `Client Selector Stress Percentage`: (not selected) or <= 37.493
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (126/168), ON (42/168)
  - HDH: ON (168/168)
  - Message Compressor: OFF (84/168), ON (84/168)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (54/72), ON (18/72)
  - HDH: ON (72/72)
  - Message Compressor: OFF (36/72), ON (36/72)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [20, 37.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6774 |
| Train target prevalence | 0.7381 |
| Train absolute lift | 0.2619 |
| Train observations | 336 |
| Train target observations | 248 |
| Train samples in box | 168 |
| Train targets in box | 168 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 109 |
| Runs retained by box | 72 |
| Target runs inside box | 72 |
| Target prevalence before box | 0.7569 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6606 |
| Absolute lift over held-out prevalence | 0.2431 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.490]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/42), ON (21/42)
  - HDH: ON (42/42)
  - Message Compressor: ON (42/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/18), ON (9/18)
  - HDH: ON (18/18)
  - Message Compressor: ON (18/18)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6667 |
| Train target prevalence | 0.1875 |
| Train absolute lift | 0.8125 |
| Train observations | 336 |
| Train target observations | 63 |
| Train samples in box | 42 |
| Train targets in box | 42 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 26 |
| Runs retained by box | 18 |
| Target runs inside box | 18 |
| Target prevalence before box | 0.1806 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6923 |
| Absolute lift over held-out prevalence | 0.8194 |

### Box 3 — L-L (L,L)

**Learned box conditions**

- `Client Selector Stress Percentage`: (not selected) or <= 62.502
- `HDH Instances`: [2.499, 8.000]
- `delay_percentage`: [12.490, 50.010]
- `JSD Mean`: [0.000, 0.017]
- `Pattern Instances`: [1.000, 4.998]
- `Total Clients`: [4.000, 5.999]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (10/10)
  - HDH: ON (10/10)
  - Message Compressor: OFF (10/10)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (4/4)
  - HDH: ON (4/4)
  - Message Compressor: OFF (4/4)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 62.5] (%)
  - HDH Instances [2.5, 8]
  - delay percentage [12.5, 50] (%)
  - JSD Mean [0, 0.0175]
  - Pattern Instances [1, 5]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4000 |
| Train recall / coverage | 0.3333 |
| Train target prevalence | 0.0357 |
| Train absolute lift | 0.3643 |
| Train observations | 336 |
| Train target observations | 12 |
| Train samples in box | 10 |
| Train targets in box | 4 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 5 |
| Runs retained by box | 4 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0347 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0347 |

### Box 4 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [12.490, 100.000]
- `Pattern Instances`: [1.499, 2.498]
- `Total Clients`: [5.999, 9.000]
- `Client Selector Stress Percentage`: [62.502, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (2/2)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Pattern Instances [1.5, 2.5]
  - Client Selector Stress Percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 0.4000 |
| Train target prevalence | 0.0149 |
| Train absolute lift | 0.6518 |
| Train observations | 336 |
| Train target observations | 5 |
| Train samples in box | 3 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 2 |
| Runs retained by box | 2 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0139 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0139 |
