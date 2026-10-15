# Discovered scenario boxes — Text task — HDH only

## Analysis scope

- **Task:** text classification
- **Configuration slice:** exactly HDH ON; other patterns OFF
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
| 1 | 1 | L-M | CART Box 1 | Evaluated | 0.8333 | 0.8434 | -0.0100 | 1 | 0.7143 | 30 / 42 | 30 / 45 | 1 | Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | 2 | L-M | PRIM Box 2 | Evaluated | 0.8333 | 0.8434 | -0.0100 | 1 | 0.7143 | 30 / 42 | 30 / 45 | 1 | Representative for CART Box 1 |
| 3 | 1 | L-L | PRIM Box 3 | Evaluated | 0.3077 | 0.6000 | -0.2923 | 0.2857 | 0.3333 | 1 / 3 | 3 / 45 | 2 | — |
| 4 | 2 | L-L | CART Box 2 | Evaluated | 0.3077 | 0.3899 | -0.0822 | 0.2857 | 0.3333 | 1 / 3 | 3 / 45 | 3 | — |
| — | — | M-M | PRIM Box 1 | Unvalidated: no held-out target examples | not available | 0.3713 | not available | not available | not available | 0 / 0 | 9 / 45 | 3 | — |

## PRIM

### Box 1 — M-M (M,M) — Unvalidated: no held-out target examples

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Alpha Dirichlet Mean`: [0.600, 0.688]
- `JSD Mean`: [0.000, 0.018]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (12/12)
  - HDH: ON (12/12)
  - Message Compressor: OFF (12/12)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/9)
  - HDH: ON (9/9)
  - Message Compressor: OFF (9/9)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.688]
  - JSD Mean [0, 0.0175]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.2500 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0286 |
| Train absolute lift | 0.2214 |
| Train observations | 105 |
| Train target observations | 3 |
| Train samples in box | 12 |
| Train targets in box | 3 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.2500 |
| Coverage | 1 |
| Mean | 0.2500 |
| Mass | 0.1143 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 0 |
| Runs retained by box | 9 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 2 — L-M (L,M) — Representative for CART Box 1

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
| Train recall / coverage | 0.7292 |
| Train target prevalence | 0.9143 |
| Train absolute lift | 0.0857 |
| Train observations | 105 |
| Train target observations | 96 |
| Train samples in box | 70 |
| Train targets in box | 70 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.7292 |
| Mean | 1 |
| Mass | 0.6667 |

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

### Box 3 — L-L (L,L)

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
| Train precision / density | 0.5714 |
| Train recall / coverage | 0.6667 |
| Train target prevalence | 0.0571 |
| Train absolute lift | 0.5143 |
| Train observations | 105 |
| Train target observations | 6 |
| Train samples in box | 7 |
| Train targets in box | 4 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.5714 |
| Coverage | 0.6667 |
| Mean | 0.5714 |
| Mass | 0.0667 |

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

### Box 1 — L-M (L,M) — Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%)

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
| Train recall / coverage | 0.7292 |
| Train target prevalence | 0.9143 |
| Train absolute lift | 0.0857 |
| Train observations | 105 |
| Train target observations | 96 |
| Train samples in box | 70 |
| Train targets in box | 70 |

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
- `JSD Mean`: [0.000, 0.018]
- `Total Clients`: [4.000, 5.999]
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
| Train precision / density | 0.5000 |
| Train recall / coverage | 0.3333 |
| Train target prevalence | 0.0571 |
| Train absolute lift | 0.4429 |
| Train observations | 105 |
| Train target observations | 6 |
| Train samples in box | 4 |
| Train targets in box | 2 |

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
