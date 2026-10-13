# Discovered scenario boxes — Text task — all

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all
- **Client-count scope:** 8 clients
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

The architectural interpretation traces conditions through declared system-spec relationships. Box metrics describe observed discovery/evaluation performance; they are not causal effects.

Held-out absolute lift is box precision minus the held-out target prevalence, reported as a proportion.

## PRIM

### Box 1 — M-S (M,S)

**Learned box conditions**

- `CPU Mean`: [8.250, 10.125]
- `HDH Instances`: [0.500, 4.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - CPU Mean [8.25, 10.1]
  - HDH Instances [0.5, 4.5]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1667 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0147 |
| Train absolute lift | 0.1520 |
| Train samples in box | 6 |
| Train targets in box | 1 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 1 |
| Runs retained by box | 6 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0085 |
| Precision inside box | 0.1667 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.1581 |

### Box 2 — L-S (L,S)

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
| Train recall / coverage | 0.6522 |
| Train target prevalence | 0.1941 |
| Train absolute lift | 0.8059 |
| Train samples in box | 15 |
| Train targets in box | 15 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 23 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.1966 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6522 |
| Absolute lift over held-out prevalence | 0.8034 |

### Box 3 — L-M (L,M)

**Learned box conditions**

- `CPU Mean`: [10.125, 10.750]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - CPU Mean [10.1, 10.8]
  - delay percentage [12.5, 100] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7174 |
| Train target prevalence | 0.7875 |
| Train absolute lift | 0.2125 |
| Train samples in box | 66 |
| Train targets in box | 66 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 92 |
| Runs retained by box | 66 |
| Target runs inside box | 66 |
| Target prevalence before box | 0.7863 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7174 |
| Absolute lift over held-out prevalence | 0.2137 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `delay_percentage`: [12.500, 100.000]
- `CPU Mean`: [10.125, 10.750]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - CPU Mean [10.1, 10.8]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7174 |
| Train target prevalence | 0.7875 |
| Train absolute lift | 0.2125 |
| Train samples in box | 66 |
| Train targets in box | 66 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 92 |
| Runs retained by box | 66 |
| Target runs inside box | 66 |
| Target prevalence before box | 0.7863 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7174 |
| Absolute lift over held-out prevalence | 0.2137 |

### Box 2 — L-S (L,S)

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
| Train recall / coverage | 0.6522 |
| Train target prevalence | 0.1941 |
| Train absolute lift | 0.8059 |
| Train samples in box | 15 |
| Train targets in box | 15 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 23 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.1966 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6522 |
| Absolute lift over held-out prevalence | 0.8034 |
