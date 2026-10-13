# Discovered scenario boxes — Image task — all

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all
- **Client-count scope:** 4 clients
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

- `Client Selector Criteria`: {CPU}
- `Alpha Dirichlet Mean`: [0.625, 0.688]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (7/14), ON (7/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (3/6), ON (3/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.7500 |
| Train target prevalence | 0.0293 |
| Train absolute lift | 0.3993 |
| Train observations | 273 |
| Train target observations | 8 |
| Train samples in box | 14 |
| Train targets in box | 6 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.4286 |
| Coverage | 0.7500 |
| Mean | 0.4286 |
| Mass | 0.0513 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 4 |
| Runs retained by box | 6 |
| Target runs inside box | 4 |
| Target prevalence before box | 0.0342 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.6325 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `CPU Mean`: [8.250, 9.500]
- `Alpha Dirichlet Mean`: [0.625, 0.688]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (14/14)
  - HDH: OFF (7/14), ON (7/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (6/6)
  - HDH: OFF (3/6), ON (3/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - CPU Mean [8.25, 9.5]
  - Alpha Dirichlet Mean [0.625, 0.688]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2143 |
| Train recall / coverage | 0.3000 |
| Train target prevalence | 0.0366 |
| Train absolute lift | 0.1777 |
| Train observations | 273 |
| Train target observations | 10 |
| Train samples in box | 14 |
| Train targets in box | 3 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2143 |
| Coverage | 0.3000 |
| Mean | 0.2143 |
| Mass | 0.0513 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 4 |
| Runs retained by box | 6 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0342 |
| Precision inside box | 0.1667 |
| Recall / target coverage | 0.2500 |
| Absolute lift over held-out prevalence | 0.1325 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `JSD Mean`: (not selected) or <= 0.019
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** `JSD Mean`

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
  - JSD Mean [-0.006, 0.0188]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5147 |
| Train target prevalence | 0.2491 |
| Train absolute lift | 0.7509 |
| Train observations | 273 |
| Train target observations | 68 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5147 |
| Mean | 1 |
| Mass | 0.1282 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 30 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.2564 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.7436 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Alpha Dirichlet Mean`: [0.688, 0.875]
- `JSD Mean`: (not selected) or <= 0.025
- `delay_percentage`: [37.500, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (56/56)
  - HDH: OFF (42/56), ON (14/56)
  - Message Compressor: OFF (14/56), ON (42/56)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (24/24)
  - HDH: OFF (18/24), ON (6/24)
  - Message Compressor: OFF (6/24), ON (18/24)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.688, 0.875]
  - JSD Mean [-0.006, 0.025]
  - delay percentage [37.5, 100] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2995 |
| Train target prevalence | 0.6850 |
| Train absolute lift | 0.3150 |
| Train observations | 273 |
| Train target observations | 187 |
| Train samples in box | 56 |
| Train targets in box | 56 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.2995 |
| Mean | 1 |
| Mass | 0.2051 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 24 |
| Target runs inside box | 24 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3038 |
| Absolute lift over held-out prevalence | 0.3248 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `JSD Mean`: (not selected) or <= 0.047
- `delay_percentage`: [37.485, 100.000]
- `Alpha Dirichlet Mean`: [0.688, 0.875]
- **Includes NaN / not-selected values:** `Client Selector Criteria`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (56/56)
  - HDH: OFF (42/56), ON (14/56)
  - Message Compressor: OFF (14/56), ON (42/56)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (24/24)
  - HDH: OFF (18/24), ON (6/24)
  - Message Compressor: OFF (6/24), ON (18/24)
- **Operating envelope**:
  - JSD Mean [-0.006, 0.0475]
  - delay percentage [37.5, 100] (%)
  - Alpha Dirichlet Mean [0.688, 0.875]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2995 |
| Train target prevalence | 0.6850 |
| Train absolute lift | 0.3150 |
| Train observations | 273 |
| Train target observations | 187 |
| Train samples in box | 56 |
| Train targets in box | 56 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 24 |
| Target runs inside box | 24 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3038 |
| Absolute lift over held-out prevalence | 0.3248 |

### Box 2 — M-S (M,S)

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
| Train recall / coverage | 0.5147 |
| Train target prevalence | 0.2491 |
| Train absolute lift | 0.7509 |
| Train observations | 273 |
| Train target observations | 68 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 30 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.2564 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.7436 |

### Box 3 — S-S (S,S)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `JSD Mean`: [0.047, 0.060]
- `delay_percentage`: [12.500, 50.010]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (2/2)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (2/2)
- **Operating envelope**:
  - JSD Mean [0.0475, 0.06]
  - delay percentage [12.5, 50] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.0293 |
| Train absolute lift | 0.9707 |
| Train observations | 273 |
| Train target observations | 8 |
| Train samples in box | 2 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 4 |
| Runs retained by box | 2 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0342 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0342 |

### Box 4 — S-M (S,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `JSD Mean`: [0.047, 0.060]
- `delay_percentage`: [50.010, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (1/2), ON (1/2)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (2/2)
  - HDH: ON (2/2)
  - Message Compressor: OFF (1/2), ON (1/2)
- **Operating envelope**:
  - JSD Mean [0.0475, 0.06]
  - delay percentage [50, 100] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2000 |
| Train target prevalence | 0.0366 |
| Train absolute lift | 0.9634 |
| Train observations | 273 |
| Train target observations | 10 |
| Train samples in box | 2 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 4 |
| Runs retained by box | 2 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0342 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0342 |
