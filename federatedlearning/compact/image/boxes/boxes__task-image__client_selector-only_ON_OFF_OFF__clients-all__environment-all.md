# Discovered scenario boxes — Image task — client_selector

## Analysis scope

- **Task:** image classification
- **Configuration slice:** client_selector
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

The architectural interpretation traces conditions through declared system-spec relationships. Box metrics describe observed discovery/evaluation performance; they are not causal effects.

Held-out absolute lift is box precision minus the held-out target prevalence, reported as a proportion.

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `CPU Mean`: [8.000, 8.125]
- `non_iid_percentage`: [50.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - CPU Mean [8, 8.12]
  - non-IID percentage [50, 75] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3333 |
| Train recall / coverage | 0.2000 |
| Train target prevalence | 0.1238 |
| Train absolute lift | 0.2095 |
| Train samples in box | 3 |
| Train targets in box | 1 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 5 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.2000 |
| Absolute lift over held-out prevalence | 0.2222 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `non_iid_percentage`: [50.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - non-IID percentage [50, 75] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.3571 |
| Train samples in box | 6 |
| Train targets in box | 3 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 6 |
| Runs retained by box | 6 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.1333 |
| Precision inside box | 0.5000 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.3667 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `CPU Mean`: [8.125, 8.875]
- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [25.000, 50.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - CPU Mean [8.12, 8.88]
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [25, 50] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 0.1818 |
| Train target prevalence | 0.2381 |
| Train absolute lift | 0.4286 |
| Train samples in box | 3 |
| Train targets in box | 2 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 11 |
| Runs retained by box | 3 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.2444 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.1818 |
| Absolute lift over held-out prevalence | 0.4222 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `CPU Mean`: [10.125, 11.000]
- `non_iid_percentage`: [25.000, 50.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - CPU Mean [10.1, 11]
  - non-IID percentage [25, 50] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2609 |
| Train target prevalence | 0.4952 |
| Train absolute lift | 0.5048 |
| Train samples in box | 6 |
| Train targets in box | 6 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 23 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.5111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2609 |
| Absolute lift over held-out prevalence | 0.4889 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- `CPU Mean`: [10.125, 11.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - CPU Mean [10.1, 11]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2609 |
| Train target prevalence | 0.4952 |
| Train absolute lift | 0.5048 |
| Train samples in box | 6 |
| Train targets in box | 6 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 23 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.5111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2609 |
| Absolute lift over held-out prevalence | 0.4889 |

### Box 2 — S-S (S,S)

**Learned box conditions**

- `delay_percentage`: [25.000, 50.000]
- `Alpha Dirichlet Mean`: [0.600, 0.612]
- `Total Clients`: [5.999, 10.000]
- `CPU Mean`: [8.000, 8.874]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [25, 50] (%)
  - Alpha Dirichlet Mean [0.6, 0.612]
  - CPU Mean [8, 8.87]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3333 |
| Train recall / coverage | 0.2000 |
| Train target prevalence | 0.1238 |
| Train absolute lift | 0.2095 |
| Train samples in box | 3 |
| Train targets in box | 1 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 5 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.2000 |
| Absolute lift over held-out prevalence | 0.2222 |
