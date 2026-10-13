# Discovered scenario boxes — Text task — client_selector

## Analysis scope

- **Task:** text classification
- **Configuration slice:** client_selector
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

The architectural interpretation traces conditions through declared system-spec relationships. Box metrics describe observed discovery/evaluation performance; they are not causal effects.

Held-out absolute lift is box precision minus the held-out target prevalence, reported as a proportion.

## PRIM

### Box 1 — L-S (L,S)

**Learned box conditions**

- `CPU Mean`: [8.000, 8.875]
- `non_iid_percentage`: [25.000, 50.000]
- `delay_percentage`: [25.000, 50.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - CPU Mean [8, 8.88]
  - non-IID percentage [25, 50] (%)
  - delay percentage [25, 50] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.7778 |
| Train recall / coverage | 0.3500 |
| Train target prevalence | 0.4571 |
| Train absolute lift | 0.3206 |
| Train samples in box | 9 |
| Train targets in box | 7 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 20 |
| Runs retained by box | 9 |
| Target runs inside box | 7 |
| Target prevalence before box | 0.4444 |
| Precision inside box | 0.7778 |
| Recall / target coverage | 0.3500 |
| Absolute lift over held-out prevalence | 0.3333 |

### Box 2 — L-M (L,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `low_spec_percentage`: [25.000, 37.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - low-spec percentage [25, 37.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.5143 |
| Train absolute lift | 0.4857 |
| Train samples in box | 6 |
| Train targets in box | 6 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 24 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.5333 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2500 |
| Absolute lift over held-out prevalence | 0.4667 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- `low_spec_percentage`: [25.000, 37.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - low-spec percentage [25, 37.5] (%)
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.2500 |
| Train target prevalence | 0.5143 |
| Train absolute lift | 0.4857 |
| Train samples in box | 6 |
| Train targets in box | 6 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 24 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.5333 |
| Precision inside box | 1 |
| Recall / target coverage | 0.2500 |
| Absolute lift over held-out prevalence | 0.4667 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- `delay_percentage`: [25.000, 50.000]
- `non_iid_percentage`: [50.000, 75.000]
- `low_spec_percentage`: [62.500, 75.000]
- `Alpha Dirichlet Mean`: [0.612, 0.900]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [25, 50] (%)
  - non-IID percentage [50, 75] (%)
  - low-spec percentage [62.5, 75] (%)
  - Alpha Dirichlet Mean [0.612, 0.9]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.1500 |
| Train target prevalence | 0.4571 |
| Train absolute lift | 0.5429 |
| Train samples in box | 3 |
| Train targets in box | 3 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 20 |
| Runs retained by box | 3 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.4444 |
| Precision inside box | 1 |
| Recall / target coverage | 0.1500 |
| Absolute lift over held-out prevalence | 0.5556 |
