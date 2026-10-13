# Discovered scenario boxes — Text task — hdh

## Analysis scope

- **Task:** text classification
- **Configuration slice:** hdh
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

### Box 1 — L-M (L,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (70/70)
  - HDH: ON (70/70)
  - Message Compressor: OFF (70/70)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (30/30)
  - HDH: ON (30/30)
  - Message Compressor: OFF (30/30)
- **Operating envelope**:
  - No uncertainty conditions in this box
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7143 |
| Train target prevalence | 0.9143 |
| Train absolute lift | 0.0857 |
| Train samples in box | 30 |
| Train targets in box | 30 |

**Held-out metrics (test partition)**

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/7)
  - HDH: ON (7/7)
  - Message Compressor: OFF (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - delay percentage [50, 75] (%)
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3333 |
| Train recall / coverage | 0.3333 |
| Train target prevalence | 0.0571 |
| Train absolute lift | 0.2762 |
| Train samples in box | 3 |
| Train targets in box | 1 |

**Held-out metrics (test partition)**

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (70/70)
  - HDH: ON (70/70)
  - Message Compressor: OFF (70/70)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (30/30)
  - HDH: ON (30/30)
  - Message Compressor: OFF (30/30)
- **Operating envelope**:
  - No uncertainty conditions in this box
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7143 |
| Train target prevalence | 0.9143 |
| Train absolute lift | 0.0857 |
| Train samples in box | 30 |
| Train targets in box | 30 |

**Held-out metrics (test partition)**

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (4/4)
  - HDH: ON (4/4)
  - Message Compressor: OFF (4/4)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - delay percentage [50, 75] (%)
  - JSD Mean [0, 0.0175]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3333 |
| Train recall / coverage | 0.3333 |
| Train target prevalence | 0.0571 |
| Train absolute lift | 0.2762 |
| Train samples in box | 3 |
| Train targets in box | 1 |

**Held-out metrics (test partition)**

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
