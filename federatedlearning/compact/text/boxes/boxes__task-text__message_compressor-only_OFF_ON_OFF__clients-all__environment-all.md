# Discovered scenario boxes — Text task — message_compressor

## Analysis scope

- **Task:** text classification
- **Configuration slice:** message_compressor
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

The architectural interpretation traces conditions through declared system-spec relationships. Box metrics describe observed discovery/evaluation performance; they are not causal effects.

Held-out absolute lift is box precision minus the held-out target prevalence, reported as a proportion.

## PRIM

### Box 1 — L-S (L,S)

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

### Box 2 — L-M (L,M)

**Learned box conditions**

- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train samples in box | 54 |
| Train targets in box | 54 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 54 |
| Runs retained by box | 54 |
| Target runs inside box | 54 |
| Target prevalence before box | 0.8571 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.1429 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `delay_percentage`: [12.485, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)

**Discovery metrics**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train samples in box | 54 |
| Train targets in box | 54 |

**Held-out metrics**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 54 |
| Runs retained by box | 54 |
| Target runs inside box | 54 |
| Target prevalence before box | 0.8571 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.1429 |

### Box 2 — L-S (L,S)

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
