# Discovered scenario boxes — Text task — message_compressor

## Analysis scope

- **Task:** text classification
- **Configuration slice:** message_compressor
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

## How to read the metrics

- **Discovery metrics = training partition.** ADEPT uses these training runs to rank parameters and fit the PRIM/CART boxes. The table describes how well each learned rule matches the data it was discovered from.
- **Held-out metrics = test partition.** Each fixed rule is applied to separate runs set aside by `partition_seed`; those runs were not used to discover the box. These metrics show whether the observed association carries over to unseen data partitions.
- Compare the two sets: a drop in test precision or lift can indicate that the training association is less stable out of sample. Test recall/coverage shows how many target runs the rule still captures.
- Precision is the share of runs inside the box that reach the target; recall/coverage is the share of target runs captured by the box. Absolute lift is precision minus the target prevalence in the same partition, reported as a proportion.
- These are observational performance measures, not causal effects or guarantees for future deployments.

The architectural interpretation traces conditions through declared system-spec relationships.

## PRIM

### Box 1 — L-S (L,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: ON (21/21)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.75, 0.9]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.8571 |
| Train samples in box | 9 |
| Train targets in box | 9 |

**Held-out metrics (test partition)**

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
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (126/126)
  - HDH: OFF (126/126)
  - Message Compressor: ON (126/126)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train samples in box | 54 |
| Train targets in box | 54 |

**Held-out metrics (test partition)**

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
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (126/126)
  - HDH: OFF (126/126)
  - Message Compressor: ON (126/126)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train samples in box | 54 |
| Train targets in box | 54 |

**Held-out metrics (test partition)**

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
- **Pattern activation among training discovery rows matching this box**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: ON (21/21)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.8571 |
| Train samples in box | 9 |
| Train targets in box | 9 |

**Held-out metrics (test partition)**

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
