# Discovered scenario boxes — Text task — all

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all
- **Client-count scope:** 8 clients
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

### Box 1 — M-S (M,S)

**Learned box conditions**

- `CPU Mean`: [8.250, 10.125]
- `HDH Instances`: [0.500, 4.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: ON (14/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: ON (6/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - CPU Mean [8.25, 10.1]
  - HDH Instances [0.5, 4.5]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2143 |
| Train recall / coverage | 0.7500 |
| Train target prevalence | 0.0147 |
| Train absolute lift | 0.1996 |
| Train observations | 273 |
| Train target observations | 4 |
| Train samples in box | 14 |
| Train targets in box | 3 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2143 |
| Coverage | 0.7500 |
| Mean | 0.2143 |
| Mass | 0.0513 |

**Held-out metrics (test partition)**

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

### Box 2 — M-M (M,M)

**Learned box conditions**

- `CPU Mean`: [8.250, 8.875]
- `HDH Instances`: [0.500, 6.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/14), ON (7/14)
  - HDH: ON (14/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/6), ON (3/6)
  - HDH: ON (6/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - CPU Mean [8.25, 8.88]
  - HDH Instances [0.5, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.0714 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0037 |
| Train absolute lift | 0.0678 |
| Train observations | 273 |
| Train target observations | 1 |
| Train samples in box | 14 |
| Train targets in box | 1 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.0714 |
| Coverage | 1 |
| Mean | 0.0714 |
| Mass | 0.0513 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 1 |
| Runs retained by box | 6 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0085 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0085 |

### Box 3 — L-S (L,S)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/35), ON (14/35)
  - HDH: OFF (21/35), ON (14/35)
  - Message Compressor: OFF (7/35), ON (28/35)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/15), ON (6/15)
  - HDH: OFF (9/15), ON (6/15)
  - Message Compressor: OFF (3/15), ON (12/15)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6604 |
| Train target prevalence | 0.1941 |
| Train absolute lift | 0.8059 |
| Train observations | 273 |
| Train target observations | 53 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.6604 |
| Mean | 1 |
| Mass | 0.1282 |

**Held-out metrics (test partition)**

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

### Box 4 — L-M (L,M)

**Learned box conditions**

- `CPU Mean`: [10.125, 10.750]
- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (112/154), ON (42/154)
  - HDH: OFF (77/154), ON (77/154)
  - Message Compressor: OFF (63/154), ON (91/154)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (48/66), ON (18/66)
  - HDH: OFF (33/66), ON (33/66)
  - Message Compressor: OFF (27/66), ON (39/66)
- **Operating envelope**:
  - CPU Mean [10.1, 10.8]
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7163 |
| Train target prevalence | 0.7875 |
| Train absolute lift | 0.2125 |
| Train observations | 273 |
| Train target observations | 215 |
| Train samples in box | 154 |
| Train targets in box | 154 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.7163 |
| Mean | 1 |
| Mass | 0.5641 |

**Held-out metrics (test partition)**

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (112/154), ON (42/154)
  - HDH: OFF (77/154), ON (77/154)
  - Message Compressor: OFF (63/154), ON (91/154)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (48/66), ON (18/66)
  - HDH: OFF (33/66), ON (33/66)
  - Message Compressor: OFF (27/66), ON (39/66)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - CPU Mean [10.1, 10.8]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7163 |
| Train target prevalence | 0.7875 |
| Train absolute lift | 0.2125 |
| Train observations | 273 |
| Train target observations | 215 |
| Train samples in box | 154 |
| Train targets in box | 154 |

**Held-out metrics (test partition)**

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/35), ON (14/35)
  - HDH: OFF (21/35), ON (14/35)
  - Message Compressor: OFF (7/35), ON (28/35)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/15), ON (6/15)
  - HDH: OFF (9/15), ON (6/15)
  - Message Compressor: OFF (3/15), ON (12/15)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6604 |
| Train target prevalence | 0.1941 |
| Train absolute lift | 0.8059 |
| Train observations | 273 |
| Train target observations | 53 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Held-out metrics (test partition)**

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

### Box 3 — M-S (M,S)

**Learned box conditions**

- `delay_percentage`: [12.500, 37.485]
- `HDH Instances`: [0.000, 1.501]
- `Pattern Types Active`: [1.500, 3.000]
- `Client Selector Criteria`: {CPU}
- `CPU Mean`: [8.250, 8.875]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (4/4)
  - HDH: ON (4/4)
  - Message Compressor: OFF (4/4)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (1/1)
  - HDH: ON (1/1)
  - Message Compressor: OFF (1/1)
- **Operating envelope**:
  - delay percentage [12.5, 37.5] (%)
  - HDH Instances [0, 1.5]
  - CPU Mean [8.25, 8.88]
- **Other design conditions**:
  - Pattern Types Active [1.5, 3]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0147 |
| Train absolute lift | 0.4853 |
| Train observations | 273 |
| Train target observations | 4 |
| Train samples in box | 4 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 1 |
| Runs retained by box | 1 |
| Target runs inside box | 0 |
| Target prevalence before box | 0.0085 |
| Precision inside box | 0 |
| Recall / target coverage | 0 |
| Absolute lift over held-out prevalence | -0.0085 |
