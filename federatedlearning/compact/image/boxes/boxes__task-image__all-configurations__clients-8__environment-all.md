# Discovered scenario boxes — Image task — all

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all
- **Client-count scope:** 8 clients
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
- `CPU Mean`: [8.250, 8.875]
- `Alpha Dirichlet Mean`: [0.625, 0.812]
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
  - CPU Mean [8.25, 8.88]
  - Alpha Dirichlet Mean [0.625, 0.812]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6429 |
| Train recall / coverage | 0.6923 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.5952 |
| Train observations | 273 |
| Train target observations | 13 |
| Train samples in box | 14 |
| Train targets in box | 9 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.6429 |
| Coverage | 0.6923 |
| Mean | 0.6429 |
| Mass | 0.0513 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 6 |
| Runs retained by box | 6 |
| Target runs inside box | 4 |
| Target prevalence before box | 0.0513 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.6667 |
| Absolute lift over held-out prevalence | 0.6154 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Alpha Dirichlet Mean`: [0.625, 0.688]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (49/49)
  - HDH: OFF (21/49), ON (28/49)
  - Message Compressor: OFF (35/49), ON (14/49)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (9/21), ON (12/21)
  - Message Compressor: OFF (15/21), ON (6/21)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6712 |
| Train target prevalence | 0.2674 |
| Train absolute lift | 0.7326 |
| Train observations | 273 |
| Train target observations | 73 |
| Train samples in box | 49 |
| Train targets in box | 49 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.6712 |
| Mean | 1 |
| Mass | 0.1795 |

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (14/21), ON (7/21)
  - Message Compressor: OFF (7/21), ON (14/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (6/9), ON (3/9)
  - Message Compressor: OFF (3/9), ON (6/9)
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
| Train observations | 273 |
| Train target observations | 42 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5000 |
| Mean | 1 |
| Mass | 0.0769 |

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (77/77)
  - HDH: OFF (56/77), ON (21/77)
  - Message Compressor: OFF (28/77), ON (49/77)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (33/33)
  - HDH: OFF (24/33), ON (9/33)
  - Message Compressor: OFF (12/33), ON (21/33)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.812, 0.875]
  - delay percentage [12.5, 100] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5310 |
| Train target prevalence | 0.5311 |
| Train absolute lift | 0.4689 |
| Train observations | 273 |
| Train target observations | 145 |
| Train samples in box | 77 |
| Train targets in box | 77 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5310 |
| Mean | 1 |
| Mass | 0.2821 |

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (77/77)
  - HDH: OFF (56/77), ON (21/77)
  - Message Compressor: OFF (28/77), ON (49/77)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (33/33)
  - HDH: OFF (24/33), ON (9/33)
  - Message Compressor: OFF (12/33), ON (21/33)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.813, 0.875]
  - delay percentage [12.5, 100] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5310 |
| Train target prevalence | 0.5311 |
| Train absolute lift | 0.4689 |
| Train observations | 273 |
| Train target observations | 145 |
| Train samples in box | 77 |
| Train targets in box | 77 |

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (49/49)
  - HDH: OFF (21/49), ON (28/49)
  - Message Compressor: OFF (35/49), ON (14/49)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (9/21), ON (12/21)
  - Message Compressor: OFF (15/21), ON (6/21)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6712 |
| Train target prevalence | 0.2674 |
| Train absolute lift | 0.7326 |
| Train observations | 273 |
| Train target observations | 73 |
| Train samples in box | 49 |
| Train targets in box | 49 |

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
- `Client Selector Criteria`: {(not selected)}
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (14/21), ON (7/21)
  - Message Compressor: OFF (7/21), ON (14/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (6/9), ON (3/9)
  - Message Compressor: OFF (3/9), ON (6/9)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.813, 0.875]
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
| Train observations | 273 |
| Train target observations | 42 |
| Train samples in box | 21 |
| Train targets in box | 21 |

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

### Box 4 — S-S (S,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.813]
- `Client Selector Criteria`: {CPU}
- `CPU Mean`: [8.250, 8.875]
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
  - Alpha Dirichlet Mean [0.625, 0.813]
  - CPU Mean [8.25, 8.88]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6429 |
| Train recall / coverage | 0.6923 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.5952 |
| Train observations | 273 |
| Train target observations | 13 |
| Train samples in box | 14 |
| Train targets in box | 9 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 6 |
| Runs retained by box | 6 |
| Target runs inside box | 4 |
| Target prevalence before box | 0.0513 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.6667 |
| Absolute lift over held-out prevalence | 0.6154 |
