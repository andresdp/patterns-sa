# Discovered scenario boxes — Image task — all

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all
- **Client-count scope:** 4 clients
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

The architectural interpretation traces conditions through declared system-spec relationships. Box metrics describe observed discovery/evaluation performance; they are not causal effects.

Held-out absolute lift is box precision minus the held-out target prevalence, reported as a proportion.

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `Client Selector Criteria`: {CPU}
- `Alpha Dirichlet Mean`: [0.625, 0.688]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0293 |
| Train absolute lift | 0.6374 |
| Train samples in box | 6 |
| Train targets in box | 4 |

**Held-out metrics**

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
- **Operating envelope**:
  - CPU Mean [8.25, 9.5]
  - Alpha Dirichlet Mean [0.625, 0.688]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1667 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.0366 |
| Train absolute lift | 0.1300 |
| Train samples in box | 6 |
| Train targets in box | 1 |

**Held-out metrics**

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
- **Operating envelope**:
  - JSD Mean [-0.006, 0.0188]
  - delay percentage [0, 12.5] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.2491 |
| Train absolute lift | 0.7509 |
| Train samples in box | 15 |
| Train targets in box | 15 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 30 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.2564 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2000 |
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
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.688, 0.875]
  - JSD Mean [-0.006, 0.025]
  - delay percentage [37.5, 100] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3038 |
| Train target prevalence | 0.6850 |
| Train absolute lift | 0.3150 |
| Train samples in box | 24 |
| Train targets in box | 24 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.0759 |
| Absolute lift over held-out prevalence | 0.3248 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `delay_percentage`: [37.485, 100.000]
- `JSD Mean`: (not selected) or <= 0.047
- `Alpha Dirichlet Mean`: [0.688, 0.875]
- **Includes NaN / not-selected values:** `Client Selector Criteria`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Operating envelope**:
  - delay percentage [37.5, 100] (%)
  - JSD Mean [-0.006, 0.0475]
  - Alpha Dirichlet Mean [0.688, 0.875]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3038 |
| Train target prevalence | 0.6850 |
| Train absolute lift | 0.3150 |
| Train samples in box | 24 |
| Train targets in box | 24 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.0759 |
| Absolute lift over held-out prevalence | 0.3248 |

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
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.2491 |
| Train absolute lift | 0.7509 |
| Train samples in box | 15 |
| Train targets in box | 15 |

**Held-out metrics**

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
