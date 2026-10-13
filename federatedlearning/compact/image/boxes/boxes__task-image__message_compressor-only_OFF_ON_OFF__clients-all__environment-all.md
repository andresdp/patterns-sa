# Discovered scenario boxes — Image task — message_compressor

## Analysis scope

- **Task:** image classification
- **Configuration slice:** message_compressor
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

The architectural interpretation traces conditions through declared system-spec relationships. Box metrics describe observed discovery/evaluation performance; they are not causal effects.

Held-out absolute lift is box precision minus the held-out target prevalence, reported as a proportion.

## PRIM

### Box 1 — S-M (S,M)

**Learned box conditions**

- `Message Compressor Instances`: [6.000, 10.000]
- `non_iid_percentage`: [50.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Message Compressor Instances [6, 10]
  - non-IID percentage [50, 75] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8571 |
| Train target prevalence | 0.1020 |
| Train absolute lift | 0.8980 |
| Train samples in box | 6 |
| Train targets in box | 6 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 7 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8571 |
| Absolute lift over held-out prevalence | 0.8889 |

### Box 2 — M-S (M,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [0, 12.5] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.8571 |
| Train samples in box | 9 |
| Train targets in box | 9 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1429 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8571 |

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
| Train recall / coverage | 0.9574 |
| Train target prevalence | 0.7551 |
| Train absolute lift | 0.2449 |
| Train samples in box | 45 |
| Train targets in box | 45 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 47 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.7460 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9574 |
| Absolute lift over held-out prevalence | 0.2540 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `delay_percentage`: [12.485, 100.000]
- `Alpha Dirichlet Mean`: [0.750, 0.900]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Alpha Dirichlet Mean [0.75, 0.9]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9574 |
| Train target prevalence | 0.7551 |
| Train absolute lift | 0.2449 |
| Train samples in box | 45 |
| Train targets in box | 45 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 47 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.7460 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9574 |
| Absolute lift over held-out prevalence | 0.2540 |

### Box 2 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.485]
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
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.8571 |
| Train samples in box | 9 |
| Train targets in box | 9 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1429 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8571 |

### Box 3 — S-M (S,M)

**Learned box conditions**

- `delay_percentage`: [12.485, 100.000]
- `Alpha Dirichlet Mean`: [0.600, 0.750]
- `Message Compressor Instances`: [5.999, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Alpha Dirichlet Mean [0.6, 0.75]
  - Message Compressor Instances [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8571 |
| Train target prevalence | 0.1020 |
| Train absolute lift | 0.8980 |
| Train samples in box | 6 |
| Train targets in box | 6 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 7 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8571 |
| Absolute lift over held-out prevalence | 0.8889 |
