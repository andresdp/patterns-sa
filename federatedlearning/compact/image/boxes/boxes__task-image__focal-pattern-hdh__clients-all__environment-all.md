# Discovered scenario boxes — Image task — HDH ON

## Analysis scope

- **Task:** image classification
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

### Box 1 — S-S (S,S)

**Learned box conditions**

- `JSD Mean`: [0.002, 0.120]
- `Client Selector Stress Percentage`: [37.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (36/36)
  - HDH: ON (36/36)
  - Message Compressor: OFF (36/36)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (18/18)
  - HDH: ON (18/18)
  - Message Compressor: OFF (18/18)
- **Operating envelope**:
  - JSD Mean [0.002, 0.12]
  - Client Selector Stress Percentage [37.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.8571 |
| Train target prevalence | 0.0625 |
| Train absolute lift | 0.4375 |
| Train observations | 336 |
| Train target observations | 21 |
| Train samples in box | 36 |
| Train targets in box | 18 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.5000 |
| Coverage | 0.8571 |
| Mean | 0.5000 |
| Mass | 0.1071 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 9 |
| Runs retained by box | 18 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.0625 |
| Precision inside box | 0.5000 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.4375 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Alpha Dirichlet Mean`: [0.600, 0.688]
- `JSD Mean`: [0.018, 0.120]
- `Client Selector Stress Percentage`: (not selected) or <= 35.000
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (56/56)
  - HDH: ON (56/56)
  - Message Compressor: OFF (42/56), ON (14/56)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (24/24)
  - HDH: ON (24/24)
  - Message Compressor: OFF (18/24), ON (6/24)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.688]
  - JSD Mean [0.0181, 0.12]
  - Client Selector Stress Percentage [20, 35] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5895 |
| Train target prevalence | 0.2827 |
| Train absolute lift | 0.7173 |
| Train observations | 336 |
| Train target observations | 95 |
| Train samples in box | 56 |
| Train targets in box | 56 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5895 |
| Mean | 1 |
| Mass | 0.1667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 41 |
| Runs retained by box | 24 |
| Target runs inside box | 24 |
| Target prevalence before box | 0.2847 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5854 |
| Absolute lift over held-out prevalence | 0.7153 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.500]
- `Client Selector Stress Percentage`: (not selected) or <= 22.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

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
  - delay percentage [0, 12.5] (%)
  - Client Selector Stress Percentage [20, 22.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3750 |
| Train target prevalence | 0.1667 |
| Train absolute lift | 0.8333 |
| Train observations | 336 |
| Train target observations | 56 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.3750 |
| Mean | 1 |
| Mass | 0.0625 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 23 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1597 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3913 |
| Absolute lift over held-out prevalence | 0.8403 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.613, 0.900]
- `JSD Mean`: [0.001, 0.014]
- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 22.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (52/52)
  - HDH: ON (52/52)
  - Message Compressor: OFF (19/52), ON (33/52)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (22/22)
  - HDH: ON (22/22)
  - Message Compressor: OFF (8/22), ON (14/22)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.613, 0.9]
  - JSD Mean [0.000625, 0.0142]
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [20, 22.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3171 |
| Train target prevalence | 0.4881 |
| Train absolute lift | 0.5119 |
| Train observations | 336 |
| Train target observations | 164 |
| Train samples in box | 52 |
| Train targets in box | 52 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.3171 |
| Mean | 1 |
| Mass | 0.1548 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 71 |
| Runs retained by box | 22 |
| Target runs inside box | 22 |
| Target prevalence before box | 0.4931 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3099 |
| Absolute lift over held-out prevalence | 0.5069 |

## CART

### Box 1 — S-M (S,M)

**Learned box conditions**

- `JSD Mean`: [0.023, 0.120]
- `Client Selector Stress Percentage`: (not selected) or <= 34.995
- `Total Clients`: [5.999, 10.000]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (74/74)
  - HDH: ON (74/74)
  - Message Compressor: OFF (51/74), ON (23/74)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (34/34)
  - HDH: ON (34/34)
  - Message Compressor: OFF (23/34), ON (11/34)
- **Operating envelope**:
  - JSD Mean [0.0227, 0.12]
  - Client Selector Stress Percentage [20, 35] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7789 |
| Train target prevalence | 0.2827 |
| Train absolute lift | 0.7173 |
| Train observations | 336 |
| Train target observations | 95 |
| Train samples in box | 74 |
| Train targets in box | 74 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 41 |
| Runs retained by box | 34 |
| Target runs inside box | 33 |
| Target prevalence before box | 0.2847 |
| Precision inside box | 0.9706 |
| Recall / target coverage | 0.8049 |
| Absolute lift over held-out prevalence | 0.6859 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `JSD Mean`: [0.001, 0.006]
- `Client Selector Stress Percentage`: (not selected) or <= 22.505
- `delay_percentage`: [12.490, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (36/36)
  - HDH: ON (36/36)
  - Message Compressor: OFF (13/36), ON (23/36)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (12/12)
  - HDH: ON (12/12)
  - Message Compressor: OFF (4/12), ON (8/12)
- **Operating envelope**:
  - JSD Mean [0.000635, 0.00584]
  - Client Selector Stress Percentage [20, 22.5] (%)
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2195 |
| Train target prevalence | 0.4881 |
| Train absolute lift | 0.5119 |
| Train observations | 336 |
| Train target observations | 164 |
| Train samples in box | 36 |
| Train targets in box | 36 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 71 |
| Runs retained by box | 12 |
| Target runs inside box | 12 |
| Target prevalence before box | 0.4931 |
| Precision inside box | 1 |
| Recall / target coverage | 0.1690 |
| Absolute lift over held-out prevalence | 0.5069 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `JSD Mean`: [0.000, 0.006]
- `delay_percentage`: [0.000, 12.490]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (17/33), ON (16/33)
  - HDH: ON (33/33)
  - Message Compressor: ON (33/33)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (7/14), ON (7/14)
  - HDH: ON (14/14)
  - Message Compressor: ON (14/14)
- **Operating envelope**:
  - JSD Mean [0, 0.00584]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5893 |
| Train target prevalence | 0.1667 |
| Train absolute lift | 0.8333 |
| Train observations | 336 |
| Train target observations | 56 |
| Train samples in box | 33 |
| Train targets in box | 33 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 23 |
| Runs retained by box | 14 |
| Target runs inside box | 14 |
| Target prevalence before box | 0.1597 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6087 |
| Absolute lift over held-out prevalence | 0.8403 |

### Box 4 — S-S (S,S)

**Learned box conditions**

- `JSD Mean`: [0.018, 0.108]
- `Client Selector Stress Percentage`: [62.502, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (13/13)
  - HDH: ON (13/13)
  - Message Compressor: OFF (13/13)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - JSD Mean [0.0181, 0.108]
  - Client Selector Stress Percentage [62.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6190 |
| Train target prevalence | 0.0625 |
| Train absolute lift | 0.9375 |
| Train observations | 336 |
| Train target observations | 21 |
| Train samples in box | 13 |
| Train targets in box | 13 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 144 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 8 |
| Target prevalence before box | 0.0625 |
| Precision inside box | 0.8889 |
| Recall / target coverage | 0.8889 |
| Absolute lift over held-out prevalence | 0.8264 |
