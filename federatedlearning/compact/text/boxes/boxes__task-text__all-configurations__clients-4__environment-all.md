# Discovered scenario boxes — Text task — all

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all
- **Client-count scope:** 4 clients
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

The architectural interpretation traces conditions through declared system-spec relationships. Box metrics describe observed discovery/evaluation performance; they are not causal effects.

Held-out absolute lift is box precision minus the held-out target prevalence, reported as a proportion.

## PRIM

### Box 1 — M-S (M,S)

**Learned box conditions**

- `CPU Mean`: [8.250, 10.125]
- `HDH Instances`: [0.500, 3.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - CPU Mean [8.25, 10.1]
  - HDH Instances [0.5, 3]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1250 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0110 |
| Train absolute lift | 0.1140 |
| Train samples in box | 8 |
| Train targets in box | 1 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 2 |
| Runs retained by box | 8 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0171 |
| Precision inside box | 0.1250 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.1079 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `Client Selector Criteria`: {CPU}
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.1935 |
| Train target prevalence | 0.2527 |
| Train absolute lift | 0.7473 |
| Train samples in box | 6 |
| Train targets in box | 6 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 31 |
| Runs retained by box | 6 |
| Target runs inside box | 6 |
| Target prevalence before box | 0.2650 |
| Precision inside box | 1 |
| Recall / target coverage | 0.1935 |
| Absolute lift over held-out prevalence | 0.7350 |

### Box 3 — L-M (L,M)

**Learned box conditions**

- `Client Selector Criteria`: {(not selected)}
- `Pattern Instances`: [0.000, 5.500]
- `HDH Instances`: [0.000, 2.500]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Operating envelope**:
  - Pattern Instances [0, 5.5]
  - HDH Instances [0, 2.5]
  - delay percentage [12.5, 100] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5696 |
| Train target prevalence | 0.6740 |
| Train absolute lift | 0.3260 |
| Train samples in box | 45 |
| Train targets in box | 45 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5696 |
| Absolute lift over held-out prevalence | 0.3248 |

### Box 4 — L-L (L,L)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `Pattern Instances`: [2.500, 7.000]
- `HDH Instances`: [0.500, 3.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
  - Pattern Instances [2.5, 7]
  - HDH Instances [0.5, 3]

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4167 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0440 |
| Train absolute lift | 0.3727 |
| Train samples in box | 12 |
| Train targets in box | 5 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 5 |
| Runs retained by box | 12 |
| Target runs inside box | 5 |
| Target prevalence before box | 0.0427 |
| Precision inside box | 0.4167 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.3739 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `Pattern Instances`: [0.000, 5.499]
- `HDH Instances`: [0.000, 2.500]
- `Client Selector Criteria`: {(not selected)}
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Operating envelope**:
  - Pattern Instances [0, 5.5]
  - HDH Instances [0, 2.5]
  - delay percentage [12.5, 100] (%)
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5696 |
| Train target prevalence | 0.6740 |
| Train absolute lift | 0.3260 |
| Train samples in box | 45 |
| Train targets in box | 45 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 79 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.6752 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5696 |
| Absolute lift over held-out prevalence | 0.3248 |

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
| Train recall / coverage | 0.4839 |
| Train target prevalence | 0.2527 |
| Train absolute lift | 0.7473 |
| Train samples in box | 15 |
| Train targets in box | 15 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 31 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.2650 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4839 |
| Absolute lift over held-out prevalence | 0.7350 |

### Box 3 — L-L (L,L)

**Learned box conditions**

- `HDH Instances`: [2.500, 3.000]
- `Client Selector Criteria`: {(not selected)}
- `Pattern Types Active`: [1.500, 3.000]
- `delay_percentage`: [50.010, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Operating envelope**:
  - HDH Instances [2.5, 3]
  - delay percentage [50, 100] (%)
- **Other design conditions**:
  - Pattern Types Active [1.5, 3]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6000 |
| Train target prevalence | 0.0440 |
| Train absolute lift | 0.9560 |
| Train samples in box | 3 |
| Train targets in box | 3 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 5 |
| Runs retained by box | 3 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.0427 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6000 |
| Absolute lift over held-out prevalence | 0.9573 |
