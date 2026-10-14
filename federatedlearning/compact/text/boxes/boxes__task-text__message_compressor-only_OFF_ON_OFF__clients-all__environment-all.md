# Discovered scenario boxes — Text task — message_compressor

## Analysis scope

- **Task:** text classification
- **Configuration slice:** message_compressor
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
| 1 | 1 | L-M | CART Box 1 | Evaluated | 1 | 1 | 0 | 1 | 1 | 54 / 54 | 54 / 63 | 1 | Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | 2 | L-M | PRIM Box 2 | Evaluated | 1 | 1 | 0 | 1 | 1 | 54 / 54 | 54 / 63 | 1 | Representative for CART Box 1 |
| 3 | 1 | L-S | CART Box 2 | Evaluated | 1 | 1 | 0 | 1 | 1 | 9 / 9 | 9 / 63 | 1 | — |
| 4 | 2 | L-S | PRIM Box 1 | Evaluated | 1 | 1 | 0 | 1 | 1 | 9 / 9 | 9 / 63 | 2 | — |

## PRIM

### Box 1 — L-S (L,S)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.750, 0.900]
- `delay_percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: ON (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (9/9)
  - Message Compressor: ON (9/9)
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
| Train observations | 147 |
| Train target observations | 21 |
| Train samples in box | 21 |
| Train targets in box | 21 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 1 |
| Mean | 1 |
| Mass | 0.1429 |

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

### Box 2 — L-M (L,M) — Representative for CART Box 1

**Learned box conditions**

- `delay_percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (126/126)
  - HDH: OFF (126/126)
  - Message Compressor: ON (126/126)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (54/54)
  - HDH: OFF (54/54)
  - Message Compressor: ON (54/54)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train observations | 147 |
| Train target observations | 126 |
| Train samples in box | 126 |
| Train targets in box | 126 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 1 |
| Mean | 1 |
| Mass | 0.8571 |

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

### Box 1 — L-M (L,M) — Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `delay_percentage`: [12.485, 100.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (126/126)
  - HDH: OFF (126/126)
  - Message Compressor: ON (126/126)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (54/54)
  - HDH: OFF (54/54)
  - Message Compressor: ON (54/54)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.8571 |
| Train absolute lift | 0.1429 |
| Train observations | 147 |
| Train target observations | 126 |
| Train samples in box | 126 |
| Train targets in box | 126 |

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
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/21)
  - HDH: OFF (21/21)
  - Message Compressor: ON (21/21)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: OFF (9/9)
  - Message Compressor: ON (9/9)
- **Operating envelope**:
  - delay percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.1429 |
| Train absolute lift | 0.8571 |
| Train observations | 147 |
| Train target observations | 21 |
| Train samples in box | 21 |
| Train targets in box | 21 |

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
