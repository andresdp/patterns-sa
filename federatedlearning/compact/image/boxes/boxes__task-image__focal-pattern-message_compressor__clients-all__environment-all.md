# Discovered scenario boxes — Image task — Message Compressor ON

## Analysis scope

- **Task:** image classification
- **Configuration slice:** all configurations with Message Compressor ON
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
| 1 | 1 | M-S | CART Box 2 | Evaluated | 0.9014 | 0.8982 | 0.0032 | 1 | 0.8205 | 32 / 39 | 32 / 180 | 2 | — |
| 2 | 1 | M-M | CART Box 1 | Evaluated | 0.7817 | 0.7852 | -0.0035 | 1 | 0.6417 | 77 / 120 | 77 / 180 | 4 | — |
| 3 | 1 | S-M | PRIM Box 2 | Evaluated | 0.7500 | 0.7568 | -0.0068 | 1 | 0.6000 | 12 / 20 | 12 / 180 | 2 | — |
| 4 | 2 | S-M | CART Box 3 | Evaluated | 0.7097 | 0.7568 | -0.0471 | 1 | 0.5500 | 11 / 20 | 11 / 180 | 3 | — |
| 5 | 2 | M-S | PRIM Box 3 | Evaluated | 0.6316 | 0.6269 | 0.0047 | 1 | 0.4615 | 18 / 39 | 18 / 180 | 2 | — |
| 6 | 2 | M-M | PRIM Box 4 | Evaluated | 0.4615 | 0.4615 | 0 | 1 | 0.3000 | 36 / 120 | 36 / 180 | 5 | — |
| 7 | 1 | S-S | PRIM Box 1 | Evaluated | 0.0957 | 0.0369 | 0.0589 | 0.0503 | 1 | 1 / 1 | 18 / 180 | 1 | — |

## PRIM

### Box 1 — S-S (S,S)

**Learned box conditions**

- `Client Selector Stress Percentage`: [37.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (42/42)
  - HDH: OFF (42/42)
  - Message Compressor: ON (42/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (18/18)
  - HDH: OFF (18/18)
  - Message Compressor: ON (18/18)
- **Operating envelope**:
  - Client Selector Stress Percentage [37.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.0238 |
| Train recall / coverage | 0.5000 |
| Train target prevalence | 0.0048 |
| Train absolute lift | 0.0190 |
| Train observations | 420 |
| Train target observations | 2 |
| Train samples in box | 42 |
| Train targets in box | 1 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 0.0238 |
| Coverage | 0.5000 |
| Mean | 0.0238 |
| Mass | 0.1000 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 1 |
| Runs retained by box | 18 |
| Target runs inside box | 1 |
| Target prevalence before box | 0.0056 |
| Precision inside box | 0.0556 |
| Recall / target coverage | 1 |
| Absolute lift over held-out prevalence | 0.0500 |

### Box 2 — S-M (S,M)

**Learned box conditions**

- `Message Compressor Instances`: [6.000, 10.000]
- `non_iid_percentage`: [62.500, 75.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (28/28)
  - HDH: OFF (14/28), ON (14/28)
  - Message Compressor: ON (28/28)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (12/12)
  - HDH: OFF (6/12), ON (6/12)
  - Message Compressor: ON (12/12)
- **Operating envelope**:
  - Message Compressor Instances [6, 10]
  - non-IID percentage [62.5, 75] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6087 |
| Train target prevalence | 0.1095 |
| Train absolute lift | 0.8905 |
| Train observations | 420 |
| Train target observations | 46 |
| Train samples in box | 28 |
| Train targets in box | 28 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.6087 |
| Mean | 1 |
| Mass | 0.0667 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 20 |
| Runs retained by box | 12 |
| Target runs inside box | 12 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6000 |
| Absolute lift over held-out prevalence | 0.8889 |

### Box 3 — M-S (M,S)

**Learned box conditions**

- `Client Selector Stress Percentage`: (not selected) or <= 22.500
- `Message Compressor Stress Percentage`: [0.000, 12.500]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (42/42)
  - HDH: OFF (21/42), ON (21/42)
  - Message Compressor: ON (42/42)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (18/18)
  - HDH: OFF (9/18), ON (9/18)
  - Message Compressor: ON (18/18)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 22.5] (%)
  - Message Compressor Stress Percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4565 |
| Train target prevalence | 0.2190 |
| Train absolute lift | 0.7810 |
| Train observations | 420 |
| Train target observations | 92 |
| Train samples in box | 42 |
| Train targets in box | 42 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.4565 |
| Mean | 1 |
| Mass | 0.1000 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 39 |
| Runs retained by box | 18 |
| Target runs inside box | 18 |
| Target prevalence before box | 0.2167 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4615 |
| Absolute lift over held-out prevalence | 0.7833 |

### Box 4 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.887, 0.900]
- `JSD Mean`: (not selected) or <= 0.014
- `Message Compressor Instances`: [3.500, 10.000]
- `Client Selector Stress Percentage`: (not selected) or <= 62.500
- `Message Compressor Stress Percentage`: [12.500, 100.000]
- **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (49/84), ON (35/84)
  - HDH: OFF (56/84), ON (28/84)
  - Message Compressor: ON (84/84)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (21/36), ON (15/36)
  - HDH: OFF (24/36), ON (12/36)
  - Message Compressor: ON (36/36)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.887, 0.9]
  - JSD Mean [-0.0081, 0.0142]
  - Message Compressor Instances [3.5, 10]
  - Client Selector Stress Percentage [20, 62.5] (%)
  - Message Compressor Stress Percentage [12.5, 100] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.3000 |
| Train target prevalence | 0.6667 |
| Train absolute lift | 0.3333 |
| Train observations | 420 |
| Train target observations | 280 |
| Train samples in box | 84 |
| Train targets in box | 84 |

**Algorithm fit diagnostics**

| Diagnostic | Value |
|:---|---:|
| Density | 1 |
| Coverage | 0.3000 |
| Mean | 1 |
| Mass | 0.2000 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 120 |
| Runs retained by box | 36 |
| Target runs inside box | 36 |
| Target prevalence before box | 0.6667 |
| Precision inside box | 1 |
| Recall / target coverage | 0.3000 |
| Absolute lift over held-out prevalence | 0.3333 |

## CART

### Box 1 — M-M (M,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.812, 0.900]
- `JSD Mean`: (not selected) or <= 0.003
- `Message Compressor Stress Percentage`: [12.508, 100.000]
- `Message Compressor Instances`: [3.499, 10.000]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (131/181), ON (50/181)
  - HDH: OFF (147/181), ON (34/181)
  - Message Compressor: ON (181/181)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (57/77), ON (20/77)
  - HDH: OFF (63/77), ON (14/77)
  - Message Compressor: ON (77/77)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.812, 0.9]
  - JSD Mean [-0.0081, 0.00316]
  - Message Compressor Stress Percentage [12.5, 100] (%)
  - Message Compressor Instances [3.5, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6464 |
| Train target prevalence | 0.6667 |
| Train absolute lift | 0.3333 |
| Train observations | 420 |
| Train target observations | 280 |
| Train samples in box | 181 |
| Train targets in box | 181 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 120 |
| Runs retained by box | 77 |
| Target runs inside box | 77 |
| Target prevalence before box | 0.6667 |
| Precision inside box | 1 |
| Recall / target coverage | 0.6417 |
| Absolute lift over held-out prevalence | 0.3333 |

### Box 2 — M-S (M,S)

**Learned box conditions**

- `JSD Mean`: (not selected) or <= 0.006
- `Message Compressor Stress Percentage`: [0.000, 12.508]
- **Includes NaN / not-selected values:** `JSD Mean`

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (38/75), ON (37/75)
  - HDH: OFF (42/75), ON (33/75)
  - Message Compressor: ON (75/75)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (16/32), ON (16/32)
  - HDH: OFF (18/32), ON (14/32)
  - Message Compressor: ON (32/32)
- **Operating envelope**:
  - JSD Mean [-0.0081, 0.00584]
  - Message Compressor Stress Percentage [0, 12.5] (%)

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.8152 |
| Train target prevalence | 0.2190 |
| Train absolute lift | 0.7810 |
| Train observations | 420 |
| Train target observations | 92 |
| Train samples in box | 75 |
| Train targets in box | 75 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 39 |
| Runs retained by box | 32 |
| Target runs inside box | 32 |
| Target prevalence before box | 0.2167 |
| Precision inside box | 1 |
| Recall / target coverage | 0.8205 |
| Absolute lift over held-out prevalence | 0.7833 |

### Box 3 — S-M (S,M)

**Learned box conditions**

- `Alpha Dirichlet Mean`: [0.600, 0.688]
- `Message Compressor Stress Percentage`: [12.508, 100.000]
- `Pattern Instances`: [7.000, 10.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (28/28)
  - HDH: OFF (14/28), ON (14/28)
  - Message Compressor: ON (28/28)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (11/11)
  - HDH: OFF (6/11), ON (5/11)
  - Message Compressor: ON (11/11)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.688]
  - Message Compressor Stress Percentage [12.5, 100] (%)
  - Pattern Instances [7, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.6087 |
| Train target prevalence | 0.1095 |
| Train absolute lift | 0.8905 |
| Train observations | 420 |
| Train target observations | 46 |
| Train samples in box | 28 |
| Train targets in box | 28 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 180 |
| Target runs before box | 20 |
| Runs retained by box | 11 |
| Target runs inside box | 11 |
| Target prevalence before box | 0.1111 |
| Precision inside box | 1 |
| Recall / target coverage | 0.5500 |
| Absolute lift over held-out prevalence | 0.8889 |
