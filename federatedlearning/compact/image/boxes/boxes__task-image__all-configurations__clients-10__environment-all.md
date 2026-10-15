# Discovered scenario boxes — Image task — all

## Analysis scope

- **Task:** image classification
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

## Cross-algorithm box ranking and duplicate marks

The table includes a **global rank** across all scoreable boxes and a **within-target rank** that compares PRIM/CART boxes for the same tradeoff. The held-out score is the harmonic mean of normalized enrichment and target coverage: normalized enrichment = max(0, (precision − baseline prevalence) / (1 − baseline prevalence)); score = 2 × enrichment × coverage / (enrichment + coverage). The score ranges from 0 to 1. Compare ranks alongside target support counts because tradeoffs can have different numbers of held-out examples; training-to-test stability and rule complexity are also shown.

**Unvalidated** means the held-out evaluation is unavailable or contains no target examples, so the rule has no held-out target evidence. A supported rule that selects no held-out rows is evaluated with score 0. Duplicate checks compare boxes for the same target only. Exact duplicates have identical readable conditions, including categories and NaN/not-selected inclusion. Near duplicates require the same constrained parameters and at least 90% condition similarity; when held-out membership can be compared, it must also reach 95% Jaccard similarity. Duplicate boxes are retained and individually marked.

| Global rank | Within-target rank | Target | Box | Status | Test score | Train score | Score Δ (test−train) | Enrichment | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| 1 | 1 | M-S | CART Box 3 | Evaluated | 0.9677 | 0.9589 | 0.0088 | 1 | 0.9375 | 15 / 16 | 15 / 117 | 2 | Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | 2 | M-S | PRIM Box 3 | Evaluated | 0.9677 | 0.9589 | 0.0088 | 1 | 0.9375 | 15 / 16 | 15 / 117 | 2 | Representative for CART Box 3 |
| 3 | 1 | M-M | CART Box 1 | Evaluated | 0.9027 | 0.8981 | 0.0045 | 1 | 0.8226 | 51 / 62 | 51 / 117 | 3 | — |
| 4 | 2 | M-M | PRIM Box 4 | Evaluated | 0.9027 | 0.8981 | 0.0045 | 1 | 0.8226 | 51 / 62 | 51 / 117 | 4 | — |
| 5 | 1 | S-M | CART Box 2 | Evaluated | 0.9000 | 0.9065 | -0.0065 | 1 | 0.8182 | 27 / 33 | 27 / 117 | 2 | Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%) |
| 6 | 2 | S-M | PRIM Box 2 | Evaluated | 0.9000 | 0.9065 | -0.0065 | 1 | 0.8182 | 27 / 33 | 27 / 117 | 2 | Representative for CART Box 2 |
| 7 | 1 | S-S | PRIM Box 1 | Evaluated | 0.4861 | 0.7330 | -0.2469 | 0.4730 | 0.5000 | 3 / 6 | 6 / 117 | 2 | — |
| 8 | 2 | S-S | CART Box 4 | Evaluated | 0.2136 | 0.3735 | -0.1599 | 0.2973 | 0.1667 | 1 / 6 | 3 / 117 | 3 | — |

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.675]
- `Client Selector Stress Percentage`: [22.500, 75.000]
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
  - Alpha Dirichlet Mean [0.6, 0.675]
  - Client Selector Stress Percentage [22.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.7143 |
| Train recall / coverage | 0.7692 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.6667 |
| Train observations | 273 |
| Train target observations | 13 |
| Train samples in box | 14 |
| Train targets in box | 10 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.7143 |
| Coverage | 0.7692 |
| Mean | 0.7143 |
| Mass | 0.0513 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 6 |
| Runs retained by box | 6 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.0513 |
| Precision inside box | 0.5000 |
| Recall / target coverage | 0.5000 |
| Absolute lift over held-out prevalence | 0.4487 |

### Box 2 — S-M (S,M) — Representative for CART Box 2

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.825]
- `Client Selector Stress Percentage`: (not selected) or <= 35.000
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (63/63)
  - HDH: OFF (21/63), ON (42/63)
  - Message Compressor: OFF (42/63), ON (21/63)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (27/27)
  - HDH: OFF (9/27), ON (18/27)
  - Message Compressor: OFF (18/27), ON (9/27)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.825]
  - Client Selector Stress Percentage [20, 35] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8289 |
| Train target prevalence | 0.2784 |
| Train absolute lift | 0.7216 |
| Train observations | 273 |
| Train target observations | 76 |
| Train samples in box | 63 |
| Train targets in box | 63 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.8289 |
| Mean | 1 |
| Mass | 0.2308 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 33 |
| Runs retained by box | 27 |
| Target runs inside box | 27 |
| Target prevalence before box | 0.2821 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8182 |
| Absolute lift over held-out prevalence | 0.7179 |

### Box 3 — M-S (M,S) — Representative for CART Box 3

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.825, 0.900]
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
  - Alpha Dirichlet Mean [0.825, 0.9]
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9211 |
| Train target prevalence | 0.1392 |
| Train absolute lift | 0.8608 |
| Train observations | 273 |
| Train target observations | 38 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.9211 |
| Mean | 1 |
| Mass | 0.1282 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 16 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.1368 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9375 |
| Absolute lift over held-out prevalence | 0.8632 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.675, 0.900]
- `JSD Mean`: (not selected) or <= 0.013
- `delay_percentage`: [12.500, 100.000]
- `Client Selector Stress Percentage`: (not selected) or <= 37.500
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (77/119), ON (42/119)
  - HDH: OFF (77/119), ON (42/119)
  - Message Compressor: OFF (42/119), ON (77/119)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (33/51), ON (18/51)
  - HDH: OFF (33/51), ON (18/51)
  - Message Compressor: OFF (18/51), ON (33/51)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.675, 0.9]
  - JSD Mean [-0.01, 0.0131]
  - delay percentage [12.5, 100] (%)
  - Client Selector Stress Percentage [20, 37.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8151 |
| Train target prevalence | 0.5348 |
| Train absolute lift | 0.4652 |
| Train observations | 273 |
| Train target observations | 146 |
| Train samples in box | 119 |
| Train targets in box | 119 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.8151 |
| Mean | 1 |
| Mass | 0.4359 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 62 |
| Runs retained by box | 51 |
| Target runs inside box | 51 |
| Target prevalence before box | 0.5299 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8226 |
| Absolute lift over held-out prevalence | 0.4701 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Client Selector Stress Percentage`: (not selected) or <= 37.500
- `delay_percentage`: [12.500, 100.000]
- `Alpha Dirichlet Mean`: [0.825, 0.900]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (77/119), ON (42/119)
  - HDH: OFF (77/119), ON (42/119)
  - Message Compressor: OFF (42/119), ON (77/119)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (33/51), ON (18/51)
  - HDH: OFF (33/51), ON (18/51)
  - Message Compressor: OFF (18/51), ON (33/51)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 37.5] (%)
  - delay percentage [12.5, 100] (%)
  - Alpha Dirichlet Mean [0.825, 0.9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8151 |
| Train target prevalence | 0.5348 |
| Train absolute lift | 0.4652 |
| Train observations | 273 |
| Train target observations | 146 |
| Train samples in box | 119 |
| Train targets in box | 119 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 62 |
| Runs retained by box | 51 |
| Target runs inside box | 51 |
| Target prevalence before box | 0.5299 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8226 |
| Absolute lift over held-out prevalence | 0.4701 |

### Box 2 — S-M (S,M) — Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `Client Selector Stress Percentage`: (not selected) or <= 34.996
- `Alpha Dirichlet Mean`: [0.600, 0.825]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (63/63)
  - HDH: OFF (21/63), ON (42/63)
  - Message Compressor: OFF (42/63), ON (21/63)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (27/27)
  - HDH: OFF (9/27), ON (18/27)
  - Message Compressor: OFF (18/27), ON (9/27)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 35] (%)
  - Alpha Dirichlet Mean [0.6, 0.825]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8289 |
| Train target prevalence | 0.2784 |
| Train absolute lift | 0.7216 |
| Train observations | 273 |
| Train target observations | 76 |
| Train samples in box | 63 |
| Train targets in box | 63 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 33 |
| Runs retained by box | 27 |
| Target runs inside box | 27 |
| Target prevalence before box | 0.2821 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8182 |
| Absolute lift over held-out prevalence | 0.7179 |

### Box 3 — M-S (M,S) — Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `delay_percentage`: [0.000, 12.500]
- `Alpha Dirichlet Mean`: [0.825, 0.900]
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
  - Alpha Dirichlet Mean [0.825, 0.9]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.9211 |
| Train target prevalence | 0.1392 |
| Train absolute lift | 0.8608 |
| Train observations | 273 |
| Train target observations | 38 |
| Train samples in box | 35 |
| Train targets in box | 35 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 16 |
| Runs retained by box | 15 |
| Target runs inside box | 15 |
| Target prevalence before box | 0.1368 |
| Precision inside box | 1 |
| Recall / target coverage | 0.9375 |
| Absolute lift over held-out prevalence | 0.8632 |

### Box 4 — S-S (S,S)

**Learned box conditions**

- `Client Selector Stress Percentage`: [62.498, 75.000]
- `Alpha Dirichlet Mean`: [0.600, 0.825]
- `JSD Mean`: (not selected) or <= 0.010
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (8/8)
  - HDH: OFF (7/8), ON (1/8)
  - Message Compressor: OFF (8/8)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (3/3)
  - HDH: OFF (3/3)
  - Message Compressor: OFF (3/3)
- **Operating envelope**:
  - Client Selector Stress Percentage [62.5, 75] (%)
  - Alpha Dirichlet Mean [0.6, 0.825]
  - JSD Mean [-0.01, 0.01]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.3077 |
| Train target prevalence | 0.0476 |
| Train absolute lift | 0.4524 |
| Train observations | 273 |
| Train target observations | 13 |
| Train samples in box | 8 |
| Train targets in box | 4 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 117 |
| Target runs before box | 6 |
| Runs retained by box | 3 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0513 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.1667 |
| Absolute lift over held-out prevalence | 0.2821 |
