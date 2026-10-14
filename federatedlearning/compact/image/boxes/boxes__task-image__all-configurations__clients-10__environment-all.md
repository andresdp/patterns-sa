# Discovered scenario boxes — Image task — all

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all
- **Client-count scope:** 10 clients
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

- `Alpha Dirichlet Mean`: [0.600, 0.675]
- `Client Selector Stress Percentage`: [22.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (7/14), ON (7/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (3/6), ON (3/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.675]
  - Client Selector Stress Percentage [22.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.7143 |
| Train recall / coverage | 0.7692 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.6667 |
| Train observations | 273 |
| Train target observations | 13 |
| Train samples in box | 14 |
| Train targets in box | 10 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.7143 |
| Coverage | 0.7692 |
| Mean | 0.7143 |
| Mass | 0.0513 |

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

- `Alpha Dirichlet Mean`: [0.600, 0.825]
- `Client Selector Stress Percentage`: (not selected) or <= 35.000
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (63/63)
  - HDH: OFF (21/63), ON (42/63)
  - Message Compressor: OFF (42/63), ON (21/63)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (27/27)
  - HDH: OFF (9/27), ON (18/27)
  - Message Compressor: OFF (18/27), ON (9/27)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.825]
  - Client Selector Stress Percentage [20, 35] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8289 |
| Train target prevalence | 0.2784 |
| Train absolute lift | 0.7216 |
| Train observations | 273 |
| Train target observations | 76 |
| Train samples in box | 63 |
| Train targets in box | 63 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.8289 |
| Mean | 1 |
| Mass | 0.2308 |

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/35), ON (14/35)
  - HDH: OFF (21/35), ON (14/35)
  - Message Compressor: OFF (7/35), ON (28/35)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/15), ON (6/15)
  - HDH: OFF (9/15), ON (6/15)
  - Message Compressor: OFF (3/15), ON (12/15)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.825, 0.9]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9211 |
| Train target prevalence | 0.1392 |
| Train absolute lift | 0.8608 |
| Train observations | 273 |
| Train target observations | 38 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.9211 |
| Mean | 1 |
| Mass | 0.1282 |

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

- `Alpha Dirichlet Mean`: [0.675, 0.900]
- `JSD Mean`: (not selected) or <= 0.013
- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 37.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (77/119), ON (42/119)
  - HDH: OFF (77/119), ON (42/119)
  - Message Compressor: OFF (42/119), ON (77/119)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (33/51), ON (18/51)
  - HDH: OFF (33/51), ON (18/51)
  - Message Compressor: OFF (18/51), ON (33/51)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.675, 0.9]
  - JSD Mean [-0.01, 0.0131]
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [20, 37.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8151 |
| Train target prevalence | 0.5348 |
| Train absolute lift | 0.4652 |
| Train observations | 273 |
| Train target observations | 146 |
| Train samples in box | 119 |
| Train targets in box | 119 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.8151 |
| Mean | 1 |
| Mass | 0.4359 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 62 |
| Runs retained by box | 51 |
| Target runs inside box | 51 |
| Target prevalence before box | 0.5299 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8226 |
| Absolute lift over held-out prevalence | 0.4701 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Client Selector Stress Percentage`: (not selected) or <= 37.500
- `Alpha Dirichlet Mean`: [0.825, 0.900]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (77/119), ON (42/119)
  - HDH: OFF (77/119), ON (42/119)
  - Message Compressor: OFF (42/119), ON (77/119)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (33/51), ON (18/51)
  - HDH: OFF (33/51), ON (18/51)
  - Message Compressor: OFF (18/51), ON (33/51)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 37.5] (%)
  - Alpha Dirichlet Mean [0.825, 0.9]
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8151 |
| Train target prevalence | 0.5348 |
| Train absolute lift | 0.4652 |
| Train observations | 273 |
| Train target observations | 146 |
| Train samples in box | 119 |
| Train targets in box | 119 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 62 |
| Runs retained by box | 51 |
| Target runs inside box | 51 |
| Target prevalence before box | 0.5299 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8226 |
| Absolute lift over held-out prevalence | 0.4701 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Client Selector Stress Percentage`: (not selected) or <= 34.996
- `Alpha Dirichlet Mean`: [0.600, 0.825]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (63/63)
  - HDH: OFF (21/63), ON (42/63)
  - Message Compressor: OFF (42/63), ON (21/63)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (27/27)
  - HDH: OFF (9/27), ON (18/27)
  - Message Compressor: OFF (18/27), ON (9/27)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 35] (%)
  - Alpha Dirichlet Mean [0.6, 0.825]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8289 |
| Train target prevalence | 0.2784 |
| Train absolute lift | 0.7216 |
| Train observations | 273 |
| Train target observations | 76 |
| Train samples in box | 63 |
| Train targets in box | 63 |

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/35), ON (14/35)
  - HDH: OFF (21/35), ON (14/35)
  - Message Compressor: OFF (7/35), ON (28/35)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/15), ON (6/15)
  - HDH: OFF (9/15), ON (6/15)
  - Message Compressor: OFF (3/15), ON (12/15)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.825, 0.9]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9211 |
| Train target prevalence | 0.1392 |
| Train absolute lift | 0.8608 |
| Train observations | 273 |
| Train target observations | 38 |
| Train samples in box | 35 |
| Train targets in box | 35 |

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

- `Client Selector Stress Percentage`: [62.498, 75.000]
- `JSD Mean`: (not selected) or <= 0.010
- `Alpha Dirichlet Mean`: [0.600, 0.825]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (8/8)
  - HDH: OFF (7/8), ON (1/8)
  - Message Compressor: OFF (8/8)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: OFF (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - Client Selector Stress Percentage [62.5, 75] (%)
  - JSD Mean [-0.01, 0.01]
  - Alpha Dirichlet Mean [0.6, 0.825]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.3077 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.4524 |
| Train observations | 273 |
| Train target observations | 13 |
| Train samples in box | 8 |
| Train targets in box | 4 |

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
