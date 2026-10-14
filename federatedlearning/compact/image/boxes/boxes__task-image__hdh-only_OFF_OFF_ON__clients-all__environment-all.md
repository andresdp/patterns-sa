# Discovered scenario boxes — Image task — hdh

## Analysis scope

- **Task:** image classification
- **Configuration slice:** hdh
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

- `Total Clients`: [4.000, 6.000]
- `Alpha Dirichlet Mean`: [0.600, 0.688]
- `JSD Mean`: [0.026, 0.066]
- `delay_percentage`: [25.000, 50.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (6/6)
  - HDH: ON (6/6)
  - Message Compressor: OFF (6/6)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (2/2)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.688]
  - JSD Mean [0.0263, 0.0663]
  - delay percentage [25, 50] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3333 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0190 |
| Train absolute lift | 0.3143 |
| Train observations | 105 |
| Train target observations | 2 |
| Train samples in box | 6 |
| Train targets in box | 2 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.3333 |
| Coverage | 1 |
| Mean | 0.3333 |
| Mass | 0.0571 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 0 |
| Runs retained by box | 2 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Alpha Dirichlet Mean`: [0.600, 0.812]
- `JSD Mean`: [0.019, 0.081]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (53/53)
  - HDH: ON (53/53)
  - Message Compressor: OFF (53/53)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (20/20)
  - HDH: ON (20/20)
  - Message Compressor: OFF (20/20)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.812]
  - JSD Mean [0.0194, 0.081]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9298 |
| Train target prevalence | 0.5429 |
| Train absolute lift | 0.4571 |
| Train observations | 105 |
| Train target observations | 57 |
| Train samples in box | 53 |
| Train targets in box | 53 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.9298 |
| Mean | 1 |
| Mass | 0.5048 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 25 |
| Runs retained by box | 20 |
| Target runs inside box | 19 |
| Target prevalence before box | 0.5556 |
| Precision inside box | 0.9500 |
| Recall / target coverage | 0.7600 |
| Absolute lift over held-out prevalence | 0.3944 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Alpha Dirichlet Mean`: [0.812, 0.900]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/7)
  - HDH: ON (7/7)
  - Message Compressor: OFF (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.812, 0.9]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1429 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0095 |
| Train absolute lift | 0.1333 |
| Train observations | 105 |
| Train target observations | 1 |
| Train samples in box | 7 |
| Train targets in box | 1 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1429 |
| Coverage | 1 |
| Mean | 0.1429 |
| Mass | 0.0667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 0 |
| Runs retained by box | 3 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Alpha Dirichlet Mean`: [0.613, 0.900]
- `JSD Mean`: [0.000, 0.057]
- `HDH Instances`: [0.500, 2.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.613, 0.9]
  - JSD Mean [0, 0.0575]
  - HDH Instances [0.5, 2]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2000 |
| Train target prevalence | 0.4286 |
| Train absolute lift | 0.5714 |
| Train observations | 105 |
| Train target observations | 45 |
| Train samples in box | 9 |
| Train targets in box | 9 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.2000 |
| Mean | 1 |
| Mass | 0.0857 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 20 |
| Runs retained by box | 3 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.4444 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.1000 |
| Absolute lift over held-out prevalence | 0.2222 |

## CART

### Box 1 — S-M (S,M)

**Learned box conditions**

- `JSD Mean`: [0.018, 0.081]
- `Total Clients`: [5.999, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (54/54)
  - HDH: ON (54/54)
  - Message Compressor: OFF (54/54)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (20/20)
  - HDH: ON (20/20)
  - Message Compressor: OFF (20/20)
- **Operating envelope**:
  - JSD Mean [0.0181, 0.081]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9474 |
| Train target prevalence | 0.5429 |
| Train absolute lift | 0.4571 |
| Train observations | 105 |
| Train target observations | 57 |
| Train samples in box | 54 |
| Train targets in box | 54 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 25 |
| Runs retained by box | 20 |
| Target runs inside box | 19 |
| Target prevalence before box | 0.5556 |
| Precision inside box | 0.9500 |
| Recall / target coverage | 0.7600 |
| Absolute lift over held-out prevalence | 0.3944 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `JSD Mean`: [0.001, 0.014]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (19/19)
  - HDH: ON (19/19)
  - Message Compressor: OFF (19/19)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (8/8)
  - HDH: ON (8/8)
  - Message Compressor: OFF (8/8)
- **Operating envelope**:
  - JSD Mean [0.000991, 0.0144]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4222 |
| Train target prevalence | 0.4286 |
| Train absolute lift | 0.5714 |
| Train observations | 105 |
| Train target observations | 45 |
| Train samples in box | 19 |
| Train targets in box | 19 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 20 |
| Runs retained by box | 8 |
| Target runs inside box | 8 |
| Target prevalence before box | 0.4444 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4000 |
| Absolute lift over held-out prevalence | 0.5556 |

### Box 3 — S-S (S,S)

**Learned box conditions**

- `JSD Mean`: [0.051, 0.066]
- `Total Clients`: [4.000, 5.999]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: no matching rows
  - HDH: no matching rows
  - Message Compressor: no matching rows
- **Operating envelope**:
  - JSD Mean [0.0513, 0.0663]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0190 |
| Train absolute lift | 0.6476 |
| Train observations | 105 |
| Train target observations | 2 |
| Train samples in box | 3 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 0 |
| Runs retained by box | 0 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | not available |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | not available |
