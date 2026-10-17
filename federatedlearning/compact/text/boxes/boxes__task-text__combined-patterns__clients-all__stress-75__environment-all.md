# Discovered scenario boxes — Text task — all available client counts (4, 8, 10) — 75% stress

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all supported non-empty combinations with every active pattern at target stress
- **Target stress:** 75%
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

## Cross-algorithm box ranking and duplicate marks

The table includes a **global rank** across all scoreable boxes and a **within-target rank** that compares PRIM/CART boxes for the same tradeoff. The held-out score is the harmonic mean of normalized enrichment and target coverage: normalized enrichment = max(0, (precision − baseline prevalence) / (1 − baseline prevalence)); score = 2 × enrichment × coverage / (enrichment + coverage). The score ranges from 0 to 1. Compare ranks alongside target support counts because tradeoffs can have different numbers of held-out examples; training-to-test stability and rule complexity are also shown.

**Unvalidated** means the held-out evaluation is unavailable or contains no target examples, so the rule has no held-out target evidence. A supported rule that selects no held-out rows is evaluated with score 0. Duplicate checks compare boxes for the same target only. Exact duplicates have identical readable conditions, including categories and NaN/not-selected inclusion. Near duplicates require the same constrained parameters and at least 90% condition similarity; when held-out membership can be compared, it must also reach 95% Jaccard similarity. Duplicate boxes are retained and individually marked.

| Global rank | Within-target rank | Target | Box | Status | Test score | Train score | Score Δ (test−train) | Enrichment | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| 1 | 1 | L-M | CART Box 1 | Evaluated | 0.7119 | 0.7153 | -0.0035 | 1 | 0.5526 | 42 / 76 | 42 / 108 | 2 | Near duplicate of PRIM Box 4 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | 2 | L-M | PRIM Box 4 | Evaluated | 0.7119 | 0.7153 | -0.0035 | 1 | 0.5526 | 42 / 76 | 42 / 108 | 2 | Representative for CART Box 1 |
| 3 | 1 | L-S | PRIM Box 3 | Evaluated | 0.6034 | 0.7524 | -0.1491 | 0.6471 | 0.5652 | 13 / 23 | 18 / 108 | 3 | — |
| 4 | 1 | L-L | PRIM Box 5 | Evaluated | 0.5307 | 0.7097 | -0.1790 | 0.4757 | 0.6000 | 3 / 5 | 6 / 108 | 2 | — |
| 5 | 1 | M-S | PRIM Box 1 | Evaluated | 0.3077 | 0.2511 | 0.0566 | 0.2000 | 0.6667 | 2 / 3 | 9 / 108 | 2 | — |
| 6 | 2 | L-L | CART Box 3 | Evaluated | 0.2403 | 0.2633 | -0.0230 | 0.3010 | 0.2000 | 1 / 5 | 3 / 108 | 4 | — |
| 7 | 1 | M-M | PRIM Box 2 | Evaluated | 0.1864 | 0.3107 | -0.1243 | 0.1028 | 1 | 1 / 1 | 9 / 108 | 2 | — |
| 8 | 2 | L-S | CART Box 2 | Evaluated | 0.1511 | 0.2058 | -0.0547 | 0.5765 | 0.0870 | 2 / 23 | 3 / 108 | 5 | — |

## PRIM

### Box 1 — M-S (M,S)

**Learned box conditions**

- `Client Selector Criteria`: {CPU}
- `HDH Instances`: [0.500, 8.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (16/16)
  - HDH: ON (16/16)
  - Message Compressor: OFF (16/16)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - HDH Instances [0.5, 8]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.1875 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0238 |
| Train absolute lift | 0.1637 |
| Train observations | 252 |
| Train target observations | 6 |
| Train samples in box | 16 |
| Train targets in box | 3 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.1875 |
| Coverage | 0.5000 |
| Mean | 0.1875 |
| Mass | 0.0635 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 3 |
| Runs retained by box | 9 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.0278 |
| Precision inside box | 0.2222 |
| Recall / target coverage | 0.6667 |
| Absolute lift over held-out prevalence | 0.1944 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `Client Selector Criteria`: {CPU}
- `HDH Instances`: [0.500, 8.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (16/16)
  - HDH: ON (16/16)
  - Message Compressor: OFF (16/16)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - HDH Instances [0.5, 8]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2500 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0317 |
| Train absolute lift | 0.2183 |
| Train observations | 252 |
| Train target observations | 8 |
| Train samples in box | 16 |
| Train targets in box | 4 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2500 |
| Coverage | 0.5000 |
| Mean | 0.2500 |
| Mass | 0.0635 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 1 |
| Runs retained by box | 9 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0093 |
| Precision inside box | 0.1111 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.1019 |

### Box 3 — L-S (L,S)

**Learned box conditions**

- `Client Selector Criteria`: {CPU}
- `Pattern Instances`: [1.000, 1.500]
- `delay_percentage`: [25.000, 50.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (47/47)
  - HDH: OFF (42/47), ON (5/47)
  - Message Compressor: OFF (47/47)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (18/18)
  - HDH: OFF (18/18)
  - Message Compressor: OFF (18/18)
- **Operating envelope**:
  - Pattern Instances [1, 1.5]
  - delay percentage [25, 50] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.8085 |
| Train recall / coverage | 0.7451 |
| Train target prevalence | 0.2024 |
| Train absolute lift | 0.6061 |
| Train observations | 252 |
| Train target observations | 51 |
| Train samples in box | 47 |
| Train targets in box | 38 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.8085 |
| Coverage | 0.7451 |
| Mean | 0.8085 |
| Mass | 0.1865 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 23 |
| Runs retained by box | 18 |
| Target runs inside box | 13 |
| Target prevalence before box | 0.2130 |
| Precision inside box | 0.7222 |
| Recall / target coverage | 0.5652 |
| Absolute lift over held-out prevalence | 0.5093 |

### Box 4 — L-M (L,M) — Representative for CART Box 1

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Pattern Instances`: [3.500, 18.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (98/98)
  - HDH: OFF (42/98), ON (56/98)
  - Message Compressor: OFF (42/98), ON (56/98)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (42/42)
  - HDH: OFF (18/42), ON (24/42)
  - Message Compressor: OFF (18/42), ON (24/42)
- **Operating envelope**:
  - Pattern Instances [3.5, 18]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5568 |
| Train target prevalence | 0.6984 |
| Train absolute lift | 0.3016 |
| Train observations | 252 |
| Train target observations | 176 |
| Train samples in box | 98 |
| Train targets in box | 98 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.5568 |
| Mean | 1 |
| Mass | 0.3889 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 76 |
| Runs retained by box | 42 |
| Target runs inside box | 42 |
| Target prevalence before box | 0.7037 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5526 |
| Absolute lift over held-out prevalence | 0.2963 |

### Box 5 — L-L (L,L)

**Learned box conditions**

- `HDH Instances`: [0.500, 4.500]
- `delay_percentage`: [50.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (14/14)
  - HDH: ON (14/14)
  - Message Compressor: OFF (7/14), ON (7/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (6/6)
  - HDH: ON (6/6)
  - Message Compressor: OFF (3/6), ON (3/6)
- **Operating envelope**:
  - HDH Instances [0.5, 4.5]
  - delay percentage [50, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6429 |
| Train recall / coverage | 0.8182 |
| Train target prevalence | 0.0437 |
| Train absolute lift | 0.5992 |
| Train observations | 252 |
| Train target observations | 11 |
| Train samples in box | 14 |
| Train targets in box | 9 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.6429 |
| Coverage | 0.8182 |
| Mean | 0.6429 |
| Mass | 0.0556 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 5 |
| Runs retained by box | 6 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.0463 |
| Precision inside box | 0.5000 |
| Recall / target coverage | 0.6000 |
| Absolute lift over held-out prevalence | 0.4537 |

## CART

### Box 1 — L-M (L,M) — Near duplicate of PRIM Box 4 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `Pattern Instances`: [3.500, 18.000]
- `Total Clients`: [5.999, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (98/98)
  - HDH: OFF (42/98), ON (56/98)
  - Message Compressor: OFF (42/98), ON (56/98)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (42/42)
  - HDH: OFF (18/42), ON (24/42)
  - Message Compressor: OFF (18/42), ON (24/42)
- **Operating envelope**:
  - Pattern Instances [3.5, 18]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5568 |
| Train target prevalence | 0.6984 |
| Train absolute lift | 0.3016 |
| Train observations | 252 |
| Train target observations | 176 |
| Train samples in box | 98 |
| Train targets in box | 98 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 76 |
| Runs retained by box | 42 |
| Target runs inside box | 42 |
| Target prevalence before box | 0.7037 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5526 |
| Absolute lift over held-out prevalence | 0.2963 |

### Box 2 — L-S (L,S)

**Learned box conditions**

- `non_iid_percentage`: [25.000, 50.001]
- `delay_percentage`: [25.000, 50.001]
- `JSD Mean`: (not selected) or <= -0.008
- `Pattern Instances`: [1.000, 1.502]
- `Total Clients`: [5.999, 9.000]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (7/7)
  - HDH: OFF (7/7)
  - Message Compressor: OFF (7/7)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: OFF (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - non-IID percentage [25, 50] (%)
  - delay percentage [25, 50] (%)
  - JSD Mean [-0.0155, -0.00776]
  - Pattern Instances [1, 1.5]
- **Other design conditions**:
  - Total Clients [6, 9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.8571 |
| Train recall / coverage | 0.1176 |
| Train target prevalence | 0.2024 |
| Train absolute lift | 0.6548 |
| Train observations | 252 |
| Train target observations | 51 |
| Train samples in box | 7 |
| Train targets in box | 6 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 23 |
| Runs retained by box | 3 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.2130 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.0870 |
| Absolute lift over held-out prevalence | 0.4537 |

### Box 3 — L-L (L,L)

**Learned box conditions**

- `Pattern Instances`: [2.501, 3.500]
- `delay_percentage`: [50.001, 75.000]
- `Client Selector Criteria`: {(not selected)}
- `JSD Mean`: [-0.008, 0.017]
- **Includes NaN / not-selected values:** `Client Selector Criteria`

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (4/4)
  - HDH: ON (4/4)
  - Message Compressor: OFF (4/4)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/3)
  - HDH: ON (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - Pattern Instances [2.5, 3.5]
  - delay percentage [50, 75] (%)
  - JSD Mean [-0.00776, 0.0175]
- **Other parameter conditions**:
  - Criteria {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.1818 |
| Train target prevalence | 0.0437 |
| Train absolute lift | 0.4563 |
| Train observations | 252 |
| Train target observations | 11 |
| Train samples in box | 4 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 108 |
| Target runs before box | 5 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0463 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.2000 |
| Absolute lift over held-out prevalence | 0.2870 |
