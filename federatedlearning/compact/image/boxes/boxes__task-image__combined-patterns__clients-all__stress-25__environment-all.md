# Discovered scenario boxes — Image task — all available client counts (4, 8, 10) — 25% stress

## Analysis scope

- **Task:** image classification
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
| 1 | 1 | M-M | CART Box 1 | Evaluated | 0.7034 | 0.6957 | 0.0078 | 0.7000 | 0.7069 | 41 / 58 | 42 / 63 | 2 | — |
| 2 | 2 | M-M | PRIM Box 3 | Evaluated | 0.4322 | 0.5864 | -0.1541 | 0.4750 | 0.3966 | 23 / 58 | 24 / 63 | 2 | — |
| 3 | 1 | M-S | PRIM Box 2 | Evaluated | 0.3265 | 0.4496 | -0.1230 | 0.2759 | 0.4000 | 2 / 5 | 6 / 63 | 3 | — |
| — | — | S-M | PRIM Box 1 | Unvalidated: no held-out target examples | not available | 0.1319 | not available | not available | not available | 0 / 0 | 6 / 63 | 3 | — |

## PRIM

### Box 1 — S-M (S,M) — Unvalidated: no held-out target examples

**Learned box conditions**

- `Message Compressor Alg`: {(not selected)}
- `JSD Mean`: [0.001, 0.015]
- `Pattern Types Active`: [1.500, 3.000]
- **Includes NaN / not-selected values:** `Message Compressor Alg`

**Architectural interpretation**

- **Design prescription**:
  - Message Compressor = OFF
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (13/13)
  - HDH: ON (13/13)
  - Message Compressor: OFF (13/13)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: ON (6/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - JSD Mean [0.000833, 0.015]
- **Other design conditions**:
  - Pattern Types Active [1.5, 3]
- **Other parameter conditions**:
  - Algorithm {(not selected)}

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.0769 |
| Train recall / coverage | 1 |
| Train target prevalence | 0.0068 |
| Train absolute lift | 0.0701 |
| Train observations | 147 |
| Train target observations | 1 |
| Train samples in box | 13 |
| Train targets in box | 1 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.0769 |
| Coverage | 1 |
| Mean | 0.0769 |
| Mass | 0.0884 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 0 |
| Runs retained by box | 6 |
| Target runs inside box | 0 |
| Target prevalence before box | 0 |
| Precision inside box | 0 |
| Recall / target coverage | not available |
| Absolute lift over held-out prevalence | 0 |

### Box 2 — M-S (M,S)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Client Selector Criteria`: {CPU}
- `HDH Batch Size`: [30.400, 32.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
  - HDH = ON (HDH Batch Size = 32.0; HDH Beta 1 = 0.5; HDH Beta 2 = 0.999; HDH Discriminator = DCGANDiscriminator; HDH Epochs = 1.0; HDH Generator = DCGANGenerator; HDH Learning Rate = 0.0002; HDH Latent Dim = 100.0; HDH Optimizer = Adam)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: ON (14/14)
  - Message Compressor: OFF (7/14), ON (7/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: ON (6/6)
  - Message Compressor: OFF (3/6), ON (3/6)
- **Operating envelope**:
  - No uncertainty conditions in this box
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.4286 |
| Train recall / coverage | 0.5455 |
| Train target prevalence | 0.0748 |
| Train absolute lift | 0.3537 |
| Train observations | 147 |
| Train target observations | 11 |
| Train samples in box | 14 |
| Train targets in box | 6 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.4286 |
| Coverage | 0.5455 |
| Mean | 0.4286 |
| Mass | 0.0952 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 5 |
| Runs retained by box | 6 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.0794 |
| Precision inside box | 0.3333 |
| Recall / target coverage | 0.4000 |
| Absolute lift over held-out prevalence | 0.2540 |

### Box 3 — M-M (M,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Message Compressor Alg`: {zlib}
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - Message Compressor = ON (Algorithm = zlib)
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (28/56), ON (28/56)
  - HDH: OFF (28/56), ON (28/56)
  - Message Compressor: ON (56/56)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (12/24), ON (12/24)
  - HDH: OFF (12/24), ON (12/24)
  - Message Compressor: ON (24/24)
- **Operating envelope**:
  - No uncertainty conditions in this box
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4148 |
| Train target prevalence | 0.9184 |
| Train absolute lift | 0.0816 |
| Train observations | 147 |
| Train target observations | 135 |
| Train samples in box | 56 |
| Train targets in box | 56 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.4148 |
| Mean | 1 |
| Mass | 0.3810 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 58 |
| Runs retained by box | 24 |
| Target runs inside box | 23 |
| Target prevalence before box | 0.9206 |
| Precision inside box | 0.9583 |
| Recall / target coverage | 0.3966 |
| Absolute lift over held-out prevalence | 0.0377 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `JSD Mean`: (not selected) or <= 0.006
- `Total Clients`: [5.999, 10.000]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (30/72), ON (42/72)
  - HDH: OFF (42/72), ON (30/72)
  - Message Compressor: OFF (29/72), ON (43/72)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/42), ON (24/42)
  - HDH: OFF (18/42), ON (24/42)
  - Message Compressor: OFF (18/42), ON (24/42)
- **Operating envelope**:
  - JSD Mean [-0.0015, 0.00583]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.5333 |
| Train target prevalence | 0.9184 |
| Train absolute lift | 0.0816 |
| Train observations | 147 |
| Train target observations | 135 |
| Train samples in box | 72 |
| Train targets in box | 72 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 63 |
| Target runs before box | 58 |
| Runs retained by box | 42 |
| Target runs inside box | 41 |
| Target prevalence before box | 0.9206 |
| Precision inside box | 0.9762 |
| Recall / target coverage | 0.7069 |
| Absolute lift over held-out prevalence | 0.0556 |
