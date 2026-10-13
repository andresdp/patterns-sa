# Discovered scenario boxes — Text task — hdh

## Analysis scope

- **Task:** text classification
- **Configuration slice:** hdh
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

The architectural interpretation traces conditions through declared system-spec relationships. Box metrics describe observed discovery/evaluation performance; they are not causal effects.

Held-out absolute lift is box precision minus the held-out target prevalence, reported as a proportion.

## PRIM

### Box 1 — L-M (L,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - No uncertainty conditions in this box
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7143 |
| Train target prevalence | 0.9143 |
| Train absolute lift | 0.0857 |
| Train samples in box | 30 |
| Train targets in box | 30 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 42 |
| Runs retained by box | 30 |
| Target runs inside box | 30 |
| Target prevalence before box | 0.9333 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7143 |
| Absolute lift over held-out prevalence | 0.0667 |

### Box 2 — L-L (L,L)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `delay_percentage`: [50.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [50, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3333 |
| Train recall / coverage | 0.3333 |
| Train target prevalence | 0.0571 |
| Train absolute lift | 0.2762 |
| Train samples in box | 3 |
| Train targets in box | 1 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 3 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0667 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.3333 |
| Absolute lift over held-out prevalence | 0.2667 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - No uncertainty conditions in this box
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7143 |
| Train target prevalence | 0.9143 |
| Train absolute lift | 0.0857 |
| Train samples in box | 30 |
| Train targets in box | 30 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 42 |
| Runs retained by box | 30 |
| Target runs inside box | 30 |
| Target prevalence before box | 0.9333 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7143 |
| Absolute lift over held-out prevalence | 0.0667 |

### Box 2 — L-L (L,L)

**Learned box conditions**

- `delay_percentage`: [50.000, 75.000]
- `Total Clients`: [4.000, 5.999]
- `JSD Mean`: [0.000, 0.018]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [50, 75] (%)
  - JSD Mean [0, 0.0175]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3333 |
| Train recall / coverage | 0.3333 |
| Train target prevalence | 0.0571 |
| Train absolute lift | 0.2762 |
| Train samples in box | 3 |
| Train targets in box | 1 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 3 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0667 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.3333 |
| Absolute lift over held-out prevalence | 0.2667 |
