# Discovered scenario boxes — Text task — all available client counts (4, 8, 10) — 25% stress

## Analysis scope

- **Task:** text classification
- **Configuration slice:** all supported non-empty combinations with every active pattern at target stress
- **Target stress:** 25%
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
| 1 | 1 | L-M | CART Box 1 | Evaluated | 0.8317 | 0.8270 | 0.0047 | 1 | 0.7119 | 42 / 59 | 42 / 63 | 1 | Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | 2 | L-M | PRIM Box 2 | Evaluated | 0.8317 | 0.8270 | 0.0047 | 1 | 0.7119 | 42 / 59 | 42 / 63 | 1 | Representative for CART Box 1 |
| 3 | 1 | L-S | PRIM Box 1 | Evaluated | 0.4163 | 0.3858 | 0.0305 | 0.2881 | 0.7500 | 3 / 4 | 9 / 63 | 3 | — |

## PRIM

### Box 1 — L-S (L,S)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Client Selector Criteria`: {CPU}
- `Pattern Instances`: [1.500, 12.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (20/20)
  - HDH: OFF (7/20), ON (13/20)
  - Message Compressor: OFF (6/20), ON (14/20)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (9/9)
  - HDH: OFF (3/9), ON (6/9)
  - Message Compressor: OFF (3/9), ON (6/9)
- **Operating envelope**:
  - Pattern Instances [1.5, 12]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.3000 |
| Train recall / coverage | 0.7500 |
| Train target prevalence | 0.0544 |
| Train absolute lift | 0.2456 |
| Train observations | 147 |
| Train target observations | 8 |
| Train samples in box | 20 |
| Train targets in box | 6 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.3000 |
| Coverage | 0.7500 |
| Mean | 0.3000 |
| Mass | 0.1361 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 4 |
| Runs retained by box | 9 |
| Target runs inside box | 3 |
| Target prevalence before box | 0.0635 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.7500 |
| Absolute lift over held-out prevalence | 0.2698 |

### Box 2 — L-M (L,M) — Representative for CART Box 1

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (42/98), ON (56/98)
  - HDH: OFF (42/98), ON (56/98)
  - Message Compressor: OFF (42/98), ON (56/98)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/42), ON (24/42)
  - HDH: OFF (18/42), ON (24/42)
  - Message Compressor: OFF (18/42), ON (24/42)
- **Operating envelope**:
  - No uncertainty conditions in this box
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7050 |
| Train target prevalence | 0.9456 |
| Train absolute lift | 0.0544 |
| Train observations | 147 |
| Train target observations | 139 |
| Train samples in box | 98 |
| Train targets in box | 98 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.7050 |
| Mean | 1 |
| Mass | 0.6667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 59 |
| Runs retained by box | 42 |
| Target runs inside box | 42 |
| Target prevalence before box | 0.9365 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7119 |
| Absolute lift over held-out prevalence | 0.0635 |

## CART

### Box 1 — L-M (L,M) — Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (42/98), ON (56/98)
  - HDH: OFF (42/98), ON (56/98)
  - Message Compressor: OFF (42/98), ON (56/98)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/42), ON (24/42)
  - HDH: OFF (18/42), ON (24/42)
  - Message Compressor: OFF (18/42), ON (24/42)
- **Operating envelope**:
  - No uncertainty conditions in this box
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.7050 |
| Train target prevalence | 0.9456 |
| Train absolute lift | 0.0544 |
| Train observations | 147 |
| Train target observations | 139 |
| Train samples in box | 98 |
| Train targets in box | 98 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 59 |
| Runs retained by box | 42 |
| Target runs inside box | 42 |
| Target prevalence before box | 0.9365 |
| Precision inside box | 1 |
| Recall / target coverage | 0.7119 |
| Absolute lift over held-out prevalence | 0.0635 |
