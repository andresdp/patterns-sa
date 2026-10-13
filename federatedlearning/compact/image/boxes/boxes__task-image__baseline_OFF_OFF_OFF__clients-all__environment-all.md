# Discovered scenario boxes — Image task — baseline

## Analysis scope

- **Task:** image classification
- **Configuration slice:** baseline
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

The architectural interpretation traces conditions through declared system-spec relationships. Box metrics describe observed discovery/evaluation performance; they are not causal effects.

Held-out absolute lift is box precision minus the held-out target prevalence, reported as a proportion.

## PRIM

### Box 1 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Alpha Dirichlet Mean`: [0.600, 0.750]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.75]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9231 |
| Train target prevalence | 0.2460 |
| Train absolute lift | 0.7540 |
| Train samples in box | 12 |
| Train targets in box | 12 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 13 |
| Runs retained by box | 12 |
| Target runs inside box | 12 |
| Target prevalence before box | 0.2407 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9231 |
| Absolute lift over held-out prevalence | 0.7593 |

### Box 2 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1667 |
| Train absolute lift | 0.8333 |
| Train samples in box | 9 |
| Train targets in box | 9 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1667 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8333 |

### Box 3 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [12.5, 100] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8438 |
| Train target prevalence | 0.5873 |
| Train absolute lift | 0.4127 |
| Train samples in box | 27 |
| Train targets in box | 27 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 32 |
| Runs retained by box | 27 |
| Target runs inside box | 27 |
| Target prevalence before box | 0.5926 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8438 |
| Absolute lift over held-out prevalence | 0.4074 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [12.488, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [12.5, 100] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8438 |
| Train target prevalence | 0.5873 |
| Train absolute lift | 0.4127 |
| Train samples in box | 27 |
| Train targets in box | 27 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 32 |
| Runs retained by box | 27 |
| Target runs inside box | 27 |
| Target prevalence before box | 0.5926 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8438 |
| Absolute lift over held-out prevalence | 0.4074 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.750]
- `Total Clients`: [5.999, 10.000]
- `delay_percentage`: [12.488, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.75]
  - delay percentage [12.5, 100] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9231 |
| Train target prevalence | 0.2460 |
| Train absolute lift | 0.7540 |
| Train samples in box | 12 |
| Train targets in box | 12 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 13 |
| Runs retained by box | 12 |
| Target runs inside box | 12 |
| Target prevalence before box | 0.2407 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9231 |
| Absolute lift over held-out prevalence | 0.7593 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.488]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1667 |
| Train absolute lift | 0.8333 |
| Train samples in box | 9 |
| Train targets in box | 9 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1667 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8333 |
