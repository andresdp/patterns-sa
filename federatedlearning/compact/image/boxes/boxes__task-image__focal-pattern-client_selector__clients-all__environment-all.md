# Discovered scenario boxes — Image task — Client Selector ON

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all configurations with Client Selector ON
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

### Box 1 — S-S (S,S)

**Learned box conditions**

- `JSD Mean`: [-0.006, 0.105]
- `non_iid_percentage`: [62.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (19/19)
  - HDH: ON (19/19)
  - Message Compressor: OFF (19/19)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - JSD Mean [-0.006, 0.105]
  - non-IID percentage [62.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.8421 |
| Train recall / coverage | 0.4706 |
| Train target prevalence | 0.1012 |
| Train absolute lift | 0.7409 |
| Train observations | 336 |
| Train target observations | 34 |
| Train samples in box | 19 |
| Train targets in box | 16 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.8421 |
| Coverage | 0.4706 |
| Mean | 0.8421 |
| Mass | 0.0565 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 14 |
| Runs retained by box | 9 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.0972 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.4286 |
| Absolute lift over held-out prevalence | 0.5694 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `non_iid_percentage`: [37.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (42/42)
  - HDH: OFF (14/42), ON (28/42)
  - Message Compressor: OFF (42/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (18/18)
  - HDH: OFF (6/18), ON (12/18)
  - Message Compressor: OFF (18/18)
- **Operating envelope**:
  - non-IID percentage [37.5, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3810 |
| Train recall / coverage | 0.5714 |
| Train target prevalence | 0.0833 |
| Train absolute lift | 0.2976 |
| Train observations | 336 |
| Train target observations | 28 |
| Train samples in box | 42 |
| Train targets in box | 16 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.3810 |
| Coverage | 0.5714 |
| Mean | 0.3810 |
| Mass | 0.1250 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 12 |
| Runs retained by box | 18 |
| Target runs inside box | 5 |
| Target prevalence before box | 0.0833 |
| Precision inside box | 0.2778 |
| Recall / target coverage | 0.4167 |
| Absolute lift over held-out prevalence | 0.1944 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `CPU Mean`: [8.125, 11.000]
- `Alpha Dirichlet Mean`: [0.688, 0.900]
- `JSD Mean`: (not selected) or <= 0.038
- `delay_percentage`: [0.000, 87.500]
- `Message Compressor Stress Percentage`: [-5.000, 12.500]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (42/42)
  - HDH: OFF (21/42), ON (21/42)
  - Message Compressor: ON (42/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (18/18)
  - HDH: OFF (9/18), ON (9/18)
  - Message Compressor: ON (18/18)
- **Operating envelope**:
  - CPU Mean [8.12, 11]
  - Alpha Dirichlet Mean [0.688, 0.9]
  - JSD Mean [-0.012, 0.038]
  - delay percentage [0, 87.5] (%)
  - Message Compressor Stress Percentage [-5, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.2500 |
| Train absolute lift | 0.7500 |
| Train observations | 336 |
| Train target observations | 84 |
| Train samples in box | 42 |
| Train targets in box | 42 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5000 |
| Mean | 1 |
| Mass | 0.1250 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 37 |
| Runs retained by box | 18 |
| Target runs inside box | 17 |
| Target prevalence before box | 0.2569 |
| Precision inside box | 0.9444 |
| Recall / target coverage | 0.4595 |
| Absolute lift over held-out prevalence | 0.6875 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Alpha Dirichlet Mean`: [0.688, 0.900]
- `JSD Mean`: (not selected) or <= 0.015
- `non_iid_percentage`: [25.000, 25.000]
- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: [25.000, 37.500]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (84/84)
  - HDH: OFF (42/84), ON (42/84)
  - Message Compressor: OFF (28/84), ON (56/84)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (36/36)
  - HDH: OFF (18/36), ON (18/36)
  - Message Compressor: OFF (12/36), ON (24/36)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.688, 0.9]
  - JSD Mean [-0.012, 0.015]
  - non-IID percentage [25, 25] (%)
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [25, 37.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4421 |
| Train target prevalence | 0.5655 |
| Train absolute lift | 0.4345 |
| Train observations | 336 |
| Train target observations | 190 |
| Train samples in box | 84 |
| Train targets in box | 84 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.4263 |
| Mean | 1 |
| Mass | 0.2411 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 81 |
| Runs retained by box | 36 |
| Target runs inside box | 33 |
| Target prevalence before box | 0.5625 |
| Precision inside box | 0.9167 |
| Recall / target coverage | 0.4074 |
| Absolute lift over held-out prevalence | 0.3542 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `delay_percentage`: [12.490, 100.000]
- `Client Selector Stress Percentage`: [25.000, 37.510]
- `Total Clients`: [5.999, 10.000]
- `CPU Mean`: [8.875, 11.000]
- `Alpha Dirichlet Mean`: [0.813, 0.900]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (84/84)
  - HDH: OFF (42/84), ON (42/84)
  - Message Compressor: OFF (28/84), ON (56/84)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (36/36)
  - HDH: OFF (18/36), ON (18/36)
  - Message Compressor: OFF (12/36), ON (24/36)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [25, 37.5] (%)
  - CPU Mean [8.88, 11]
  - Alpha Dirichlet Mean [0.813, 0.9]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4421 |
| Train target prevalence | 0.5655 |
| Train absolute lift | 0.4345 |
| Train observations | 336 |
| Train target observations | 190 |
| Train samples in box | 84 |
| Train targets in box | 84 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 81 |
| Runs retained by box | 36 |
| Target runs inside box | 33 |
| Target prevalence before box | 0.5625 |
| Precision inside box | 0.9167 |
| Recall / target coverage | 0.4074 |
| Absolute lift over held-out prevalence | 0.3542 |

### Box 2 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.490]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (42/42)
  - HDH: OFF (21/42), ON (21/42)
  - Message Compressor: ON (42/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (18/18)
  - HDH: OFF (9/18), ON (9/18)
  - Message Compressor: ON (18/18)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.2500 |
| Train absolute lift | 0.7500 |
| Train observations | 336 |
| Train target observations | 84 |
| Train samples in box | 42 |
| Train targets in box | 42 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 37 |
| Runs retained by box | 18 |
| Target runs inside box | 17 |
| Target prevalence before box | 0.2569 |
| Precision inside box | 0.9444 |
| Recall / target coverage | 0.4595 |
| Absolute lift over held-out prevalence | 0.6875 |

### Box 3 — S-S (S,S)

**Learned box conditions**

- `delay_percentage`: [12.490, 100.000]
- `JSD Mean`: [0.010, 0.105]
- `Total Clients`: [5.999, 10.000]
- `Alpha Dirichlet Mean`: [0.600, 0.813]
- `non_iid_percentage`: [62.505, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (11/11)
  - HDH: ON (11/11)
  - Message Compressor: OFF (11/11)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: ON (6/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - JSD Mean [0.01, 0.105]
  - Alpha Dirichlet Mean [0.6, 0.813]
  - non-IID percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3235 |
| Train target prevalence | 0.1012 |
| Train absolute lift | 0.8988 |
| Train observations | 336 |
| Train target observations | 34 |
| Train samples in box | 11 |
| Train targets in box | 11 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 14 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.0972 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4286 |
| Absolute lift over held-out prevalence | 0.9028 |

### Box 4 — S-M (S,M)

**Learned box conditions**

- `delay_percentage`: [12.490, 100.000]
- `JSD Mean`: (not selected) or <= -0.006
- `Total Clients`: [5.999, 10.000]
- `CPU Mean`: [8.000, 8.125]
- `Alpha Dirichlet Mean`: [0.600, 0.813]
- `non_iid_percentage`: [62.505, 75.000]
- **Includes NaN / not-selected values:** `JSD Mean`

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
  - delay percentage [12.5, 100] (%)
  - JSD Mean [-0.012, -0.00599]
  - CPU Mean [8, 8.12]
  - Alpha Dirichlet Mean [0.6, 0.813]
  - non-IID percentage [62.5, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.1071 |
| Train target prevalence | 0.0833 |
| Train absolute lift | 0.3452 |
| Train observations | 336 |
| Train target observations | 28 |
| Train samples in box | 7 |
| Train targets in box | 3 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 12 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0833 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.0833 |
| Absolute lift over held-out prevalence | 0.2500 |
