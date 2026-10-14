# Discovered scenario boxes — Text task — Client Selector ON

## Analysis scope

- **Task:** text classification
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

### Box 1 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 9.000]
- `Pattern Instances`: [1.000, 2.500]
- `non_iid_percentage`: [37.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (33/33)
  - HDH: OFF (14/33), ON (19/33)
  - Message Compressor: OFF (33/33)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (12/12)
  - HDH: OFF (6/12), ON (6/12)
  - Message Compressor: OFF (12/12)
- **Operating envelope**:
  - Pattern Instances [1, 2.5]
  - non-IID percentage [37.5, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2121 |
| Train recall / coverage | 0.8750 |
| Train target prevalence | 0.0238 |
| Train absolute lift | 0.1883 |
| Train observations | 336 |
| Train target observations | 8 |
| Train samples in box | 33 |
| Train targets in box | 7 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2121 |
| Coverage | 0.8750 |
| Mean | 0.2121 |
| Mass | 0.0982 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 3 |
| Runs retained by box | 12 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.0208 |
| Precision inside box | 0.1667 |
| Recall / target coverage | 0.6667 |
| Absolute lift over held-out prevalence | 0.1458 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `Pattern Instances`: [1.500, 11.000]
- `non_iid_percentage`: [62.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (17/17)
  - HDH: ON (17/17)
  - Message Compressor: OFF (17/17)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (8/8)
  - HDH: ON (8/8)
  - Message Compressor: OFF (8/8)
- **Operating envelope**:
  - Pattern Instances [1.5, 11]
  - non-IID percentage [62.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2353 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0119 |
| Train absolute lift | 0.2234 |
| Train observations | 336 |
| Train target observations | 4 |
| Train samples in box | 17 |
| Train targets in box | 4 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2353 |
| Coverage | 1 |
| Mean | 0.2353 |
| Mass | 0.0506 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 2 |
| Runs retained by box | 8 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0139 |
| Precision inside box | 0.1250 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.1111 |

### Box 3 — L-S (L,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 87.500]
- `Message Compressor Stress Percentage`: [-5.000, 12.500]
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
  - delay percentage [0, 87.5] (%)
  - Message Compressor Stress Percentage [-5, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3590 |
| Train target prevalence | 0.3482 |
| Train absolute lift | 0.6518 |
| Train observations | 336 |
| Train target observations | 117 |
| Train samples in box | 42 |
| Train targets in box | 42 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.3590 |
| Mean | 1 |
| Mass | 0.1250 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 50 |
| Runs retained by box | 18 |
| Target runs inside box | 18 |
| Target prevalence before box | 0.3472 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3600 |
| Absolute lift over held-out prevalence | 0.6528 |

### Box 4 — L-M (L,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Alpha Dirichlet Mean`: [0.812, 0.900]
- `Pattern Types Active`: [1.500, 3.000]
- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: [25.000, 62.500]
- `HDH Stress Percentage`: (not selected) or <= 62.500
- **Includes NaN / not-selected values:** `HDH Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (84/84)
  - HDH: OFF (42/84), ON (42/84)
  - Message Compressor: OFF (14/84), ON (70/84)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (36/36)
  - HDH: OFF (18/36), ON (18/36)
  - Message Compressor: OFF (6/36), ON (30/36)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.812, 0.9]
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [25, 62.5] (%)
  - HDH Stress Percentage [20, 62.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]
  - Pattern Types Active [1.5, 3]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4058 |
| Train target prevalence | 0.6161 |
| Train absolute lift | 0.3839 |
| Train observations | 336 |
| Train target observations | 207 |
| Train samples in box | 84 |
| Train targets in box | 84 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.4058 |
| Mean | 1 |
| Mass | 0.2500 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 89 |
| Runs retained by box | 36 |
| Target runs inside box | 36 |
| Target prevalence before box | 0.6181 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4045 |
| Absolute lift over held-out prevalence | 0.3819 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `delay_percentage`: [12.490, 100.000]
- `Total Clients`: [5.999, 10.000]
- `Pattern Instances`: [3.499, 11.000]
- `Client Selector Stress Percentage`: [25.000, 62.505]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (78/78)
  - HDH: OFF (42/78), ON (36/78)
  - Message Compressor: OFF (8/78), ON (70/78)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (33/33)
  - HDH: OFF (18/33), ON (15/33)
  - Message Compressor: OFF (3/33), ON (30/33)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Pattern Instances [3.5, 11]
  - Client Selector Stress Percentage [25, 62.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3768 |
| Train target prevalence | 0.6161 |
| Train absolute lift | 0.3839 |
| Train observations | 336 |
| Train target observations | 207 |
| Train samples in box | 78 |
| Train targets in box | 78 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 89 |
| Runs retained by box | 33 |
| Target runs inside box | 33 |
| Target prevalence before box | 0.6181 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3708 |
| Absolute lift over held-out prevalence | 0.3819 |

### Box 2 — L-S (L,S)

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
| Train recall / coverage | 0.3590 |
| Train target prevalence | 0.3482 |
| Train absolute lift | 0.6518 |
| Train observations | 336 |
| Train target observations | 117 |
| Train samples in box | 42 |
| Train targets in box | 42 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 50 |
| Runs retained by box | 18 |
| Target runs inside box | 18 |
| Target prevalence before box | 0.3472 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3600 |
| Absolute lift over held-out prevalence | 0.6528 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Pattern Instances`: [1.499, 2.501]
- `Client Selector Stress Percentage`: [62.505, 75.000]
- `Total Clients`: [5.999, 10.000]
- `delay_percentage`: [12.490, 50.010]
- `Alpha Dirichlet Mean`: [0.613, 0.900]
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
  - Pattern Instances [1.5, 2.5]
  - Client Selector Stress Percentage [62.5, 75] (%)
  - delay percentage [12.5, 50] (%)
  - Alpha Dirichlet Mean [0.613, 0.9]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.0238 |
| Train absolute lift | 0.6429 |
| Train observations | 336 |
| Train target observations | 8 |
| Train samples in box | 3 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 3 |
| Runs retained by box | 2 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0208 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0208 |
