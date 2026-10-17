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

## Cross-algorithm box ranking and duplicate marks

The table includes a **global rank** across all scoreable boxes and a **within-target rank** that compares PRIM/CART boxes for the same tradeoff. The held-out score is the harmonic mean of normalized enrichment and target coverage: normalized enrichment = max(0, (precision − baseline prevalence) / (1 − baseline prevalence)); score = 2 × enrichment × coverage / (enrichment + coverage). The score ranges from 0 to 1. Compare ranks alongside target support counts because tradeoffs can have different numbers of held-out examples; training-to-test stability and rule complexity are also shown.

**Unvalidated** means the held-out evaluation is unavailable or contains no target examples, so the rule has no held-out target evidence. A supported rule that selects no held-out rows is evaluated with score 0. Duplicate checks compare boxes for the same target only. Exact duplicates have identical readable conditions, including categories and NaN/not-selected inclusion. Near duplicates require the same constrained parameters and at least 90% condition similarity; when held-out membership can be compared, it must also reach 95% Jaccard similarity. Duplicate boxes are retained and individually marked.

| Global rank | Within-target rank | Target | Box | Status | Test score | Train score | Score Δ (test−train) | Enrichment | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| 1 | 1 | L-M | CART Box 1 | Evaluated | 0.9176 | 0.9169 | 0.0008 | 1 | 0.8478 | 78 / 92 | 78 / 117 | 2 | Near duplicate of PRIM Box 4 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | 2 | L-M | PRIM Box 4 | Evaluated | 0.9176 | 0.9169 | 0.0008 | 1 | 0.8478 | 78 / 92 | 78 / 117 | 2 | Representative for CART Box 1 |
| 3 | 1 | L-S | CART Box 2 | Evaluated | 0.7895 | 0.7955 | -0.0060 | 1 | 0.6522 | 15 / 23 | 15 / 117 | 1 | Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%) |
| 4 | 2 | L-S | PRIM Box 3 | Evaluated | 0.7895 | 0.7955 | -0.0060 | 1 | 0.6522 | 15 / 23 | 15 / 117 | 1 | Representative for CART Box 2 |
| 5 | 1 | M-S | PRIM Box 1 | Evaluated | 0.2386 | 0.3316 | -0.0930 | 0.1355 | 1 | 1 / 1 | 7 / 117 | 3 | — |
| 6 | 1 | M-M | PRIM Box 2 | Evaluated | 0 | 0.1274 | -0.1274 | 0 | 0 | 0 / 1 | 6 / 117 | 2 | — |
| 7 | 2 | M-S | CART Box 3 | Evaluated | 0 | 0.4963 | -0.4963 | 0 | 0 | 0 / 1 | 1 / 117 | 4 | — |

## PRIM

### Box 1 — M-S (M,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.812]
- `Pattern Instances`: [0.000, 3.500]
- `Client Selector Stress Percentage`: [35.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (19/19)
  - HDH: OFF (7/19), ON (12/19)
  - Message Compressor: OFF (19/19)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (7/7)
  - HDH: OFF (3/7), ON (4/7)
  - Message Compressor: OFF (7/7)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.812]
  - Pattern Instances [0, 3.5]
  - Client Selector Stress Percentage [35, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2105 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0147 |
| Train absolute lift | 0.1959 |
| Train observations | 273 |
| Train target observations | 4 |
| Train samples in box | 19 |
| Train targets in box | 4 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2105 |
| Coverage | 1 |
| Mean | 0.2105 |
| Mass | 0.0696 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 1 |
| Runs retained by box | 7 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0085 |
| Precision inside box | 0.1429 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.1343 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.625, 0.688]
- `Client Selector Stress Percentage`: [35.000, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (7/14), ON (7/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (3/6), ON (3/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
  - Client Selector Stress Percentage [35, 75] (%)

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

### Box 3 — L-S (L,S) — Representative for CART Box 2

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

### Box 4 — L-M (L,M) — Representative for CART Box 1

**Learned box conditions**

- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 37.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (140/182), ON (42/182)
  - HDH: OFF (98/182), ON (84/182)
  - Message Compressor: OFF (84/182), ON (98/182)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (60/78), ON (18/78)
  - HDH: OFF (42/78), ON (36/78)
  - Message Compressor: OFF (36/78), ON (42/78)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [20, 37.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8465 |
| Train target prevalence | 0.7875 |
| Train absolute lift | 0.2125 |
| Train observations | 273 |
| Train target observations | 215 |
| Train samples in box | 182 |
| Train targets in box | 182 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.8465 |
| Mean | 1 |
| Mass | 0.6667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 92 |
| Runs retained by box | 78 |
| Target runs inside box | 78 |
| Target prevalence before box | 0.7863 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8478 |
| Absolute lift over held-out prevalence | 0.2137 |

## CART

### Box 1 — L-M (L,M) — Near duplicate of PRIM Box 4 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 37.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (140/182), ON (42/182)
  - HDH: OFF (98/182), ON (84/182)
  - Message Compressor: OFF (84/182), ON (98/182)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (60/78), ON (18/78)
  - HDH: OFF (42/78), ON (36/78)
  - Message Compressor: OFF (36/78), ON (42/78)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [20, 37.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8465 |
| Train target prevalence | 0.7875 |
| Train absolute lift | 0.2125 |
| Train observations | 273 |
| Train target observations | 215 |
| Train samples in box | 182 |
| Train targets in box | 182 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 92 |
| Runs retained by box | 78 |
| Target runs inside box | 78 |
| Target prevalence before box | 0.7863 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8478 |
| Absolute lift over held-out prevalence | 0.2137 |

### Box 2 — L-S (L,S) — Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%)

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
- `Pattern Instances`: [0.000, 2.499]
- `HDH Instances`: [0.500, 6.000]
- `Client Selector Stress Percentage`: [62.498, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
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
  - Pattern Instances [0, 2.5]
  - HDH Instances [0.5, 6]
  - Client Selector Stress Percentage [62.5, 75] (%)

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
