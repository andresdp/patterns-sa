# Discovered scenario boxes — Text task — baseline

## Analysis scope

- **Task:** text classification
- **Configuration slice:** baseline
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

## How to read the metrics

- **Discovery metrics = training partition.** ADEPT uses these training runs to rank parameters and fit the PRIM/CART boxes. The table evaluates each learned rule on those same training runs.
- **Held-out metrics = test partition.** Each fixed rule is applied to separate runs set aside by `partition_seed`; those runs were not used to discover the box. Every reported held-out metric, including prevalence and lift, is calculated from that test partition.
- Compare the two sets: a drop in test precision or lift can indicate that the training association is less stable out of sample. Test recall/coverage shows how many target runs the rule still captures.
- Precision is the share of runs inside the box that reach the target; recall/coverage is the share of target runs captured by the box. Absolute lift is precision minus the target prevalence in the same partition, reported as a proportion.
- These are observational performance measures, not causal effects or guarantees for future deployments.

The architectural interpretation traces conditions through declared system-spec relationships.

## PRIM

### Box 1 — L-S (L,S)

**Learned box conditions**

- `non_iid_percentage`: [25.000, 50.000]
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: OFF (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - non-IID percentage [25, 50] (%)
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1667 |
| Train absolute lift | 0.8333 |
| Train observations | 126 |
| Train target observations | 21 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 1 |
| Mean | 1 |
| Mass | 0.1667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1667 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8333 |

### Box 2 — L-M (L,M)

**Learned box conditions**

- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (105/105)
  - HDH: OFF (105/105)
  - Message Compressor: OFF (105/105)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (45/45)
  - HDH: OFF (45/45)
  - Message Compressor: OFF (45/45)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.8333 |
| Train absolute lift | 0.1667 |
| Train observations | 126 |
| Train target observations | 105 |
| Train samples in box | 105 |
| Train targets in box | 105 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 1 |
| Mean | 1 |
| Mass | 0.8333 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 45 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.8333 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.1667 |

## CART

### Box 1 — L-M (L,M)

**Learned box conditions**

- `delay_percentage`: [12.488, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (105/105)
  - HDH: OFF (105/105)
  - Message Compressor: OFF (105/105)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (45/45)
  - HDH: OFF (45/45)
  - Message Compressor: OFF (45/45)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.8333 |
| Train absolute lift | 0.1667 |
| Train observations | 126 |
| Train target observations | 105 |
| Train samples in box | 105 |
| Train targets in box | 105 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 45 |
| Runs retained by box | 45 |
| Target runs inside box | 45 |
| Target prevalence before box | 0.8333 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.1667 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.488]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: OFF (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1667 |
| Train absolute lift | 0.8333 |
| Train observations | 126 |
| Train target observations | 21 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 54 |
| Target runs before box | 9 |
| Runs retained by box | 9 |
| Target runs inside box | 9 |
| Target prevalence before box | 0.1667 |
| Precision inside box | 1 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.8333 |
