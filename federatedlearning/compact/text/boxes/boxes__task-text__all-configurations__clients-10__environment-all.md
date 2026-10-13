# Discovered scenario boxes — Text task — all

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all
- **Client-count scope:** 10 clients
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

- `Client Selector Criteria`: {CPU}
- `CPU Mean`: [8.000, 8.750]
- `Alpha Dirichlet Mean`: [0.600, 0.825]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (7/14), ON (7/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (3/6), ON (3/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - CPU Mean [8, 8.75]
  - Alpha Dirichlet Mean [0.6, 0.825]

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
| Target runs before box | 0 |
| Runs retained by box | 6 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `CPU Mean`: [8.000, 10.250]
- `HDH Instances`: [0.500, 8.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/20), ON (13/20)
  - HDH: ON (20/20)
  - Message Compressor: OFF (20/20)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/9), ON (6/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - CPU Mean [8, 10.2]
  - HDH Instances [0.5, 8]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1000 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0073 |
| Train absolute lift | 0.0927 |
| Train observations | 273 |
| Train target observations | 2 |
| Train samples in box | 20 |
| Train targets in box | 2 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1000 |
| Coverage | 1 |
| Mean | 0.1000 |
| Mass | 0.0733 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 1 |
| Runs retained by box | 9 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0085 |
| Precision inside box | 0.1111 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.1026 |

### Box 3 — L-S (L,S)

**Learned box conditions**

- `HDH Instances`: [0.000, 4.500]
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
  - HDH Instances [0, 4.5]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6140 |
| Train target prevalence | 0.2088 |
| Train absolute lift | 0.7912 |
| Train observations | 273 |
| Train target observations | 57 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.6140 |
| Mean | 1 |
| Mass | 0.1282 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 24 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.2051 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6250 |
| Absolute lift over held-out prevalence | 0.7949 |

### Box 4 — L-M (L,M)

**Learned box conditions**

- `CPU Mean`: [10.250, 11.000]
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
  - CPU Mean [10.2, 11]
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7230 |
| Train target prevalence | 0.7802 |
| Train absolute lift | 0.2198 |
| Train observations | 273 |
| Train target observations | 213 |
| Train samples in box | 154 |
| Train targets in box | 154 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.7230 |
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

- `CPU Mean`: [10.250, 11.000]
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
  - CPU Mean [10.3, 11]
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7230 |
| Train target prevalence | 0.7802 |
| Train absolute lift | 0.2198 |
| Train observations | 273 |
| Train target observations | 213 |
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
| Train recall / coverage | 0.6140 |
| Train target prevalence | 0.2088 |
| Train absolute lift | 0.7912 |
| Train observations | 273 |
| Train target observations | 57 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 24 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.2051 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6250 |
| Absolute lift over held-out prevalence | 0.7949 |
