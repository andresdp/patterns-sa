# Discovered scenario boxes — Image task — hdh

## Analysis scope

- **Task:** image classification
- **Configuration slice:** hdh
- **Client-count scope:** All client counts (4, 8, 10)
- **Environment scope:** all
- **Outcomes:** final_val_accuracy and avg_total_time

## How to read the metrics

- **Discovery metrics = training partition.** ADEPT uses these training runs to rank parameters and fit the PRIM/CART boxes. The table describes how well each learned rule matches the data it was discovered from.
- **Held-out metrics = test partition.** Each fixed rule is applied to separate runs set aside by `partition_seed`; those runs were not used to discover the box. These metrics show whether the observed association carries over to unseen data partitions.
- Compare the two sets: a drop in test precision or lift can indicate that the training association is less stable out of sample. Test recall/coverage shows how many target runs the rule still captures.
- Precision is the share of runs inside the box that reach the target; recall/coverage is the share of target runs captured by the box. Absolute lift is precision minus the target prevalence in the same partition, reported as a proportion.
- These are observational performance measures, not causal effects or guarantees for future deployments.

The architectural interpretation traces conditions through declared system-spec relationships.

## PRIM

### Box 1 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [6.000, 10.000]
- `Alpha Dirichlet Mean`: [0.600, 0.812]
- `JSD Mean`: [0.019, 0.081]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.6, 0.812]
  - JSD Mean [0.0194, 0.081]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.9500 |
| Train recall / coverage | 0.7600 |
| Train target prevalence | 0.5429 |
| Train absolute lift | 0.4071 |
| Train samples in box | 20 |
| Train targets in box | 19 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 25 |
| Runs retained by box | 20 |
| Target runs inside box | 19 |
| Target prevalence before box | 0.5556 |
| Precision inside box | 0.9500 |
| Recall / target coverage | 0.7600 |
| Absolute lift over held-out prevalence | 0.3944 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `Total Clients`: [4.000, 6.000]
- `Alpha Dirichlet Mean`: [0.613, 0.900]
- `JSD Mean`: [0.000, 0.057]
- `HDH Instances`: [0.500, 2.000]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.613, 0.9]
  - JSD Mean [0, 0.0575]
  - HDH Instances [0.5, 2]
- **Other design conditions**:
  - Total Clients [4, 6]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.6667 |
| Train recall / coverage | 0.1000 |
| Train target prevalence | 0.4286 |
| Train absolute lift | 0.2381 |
| Train samples in box | 3 |
| Train targets in box | 2 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 20 |
| Runs retained by box | 3 |
| Target runs inside box | 2 |
| Target prevalence before box | 0.4444 |
| Precision inside box | 0.6667 |
| Recall / target coverage | 0.1000 |
| Absolute lift over held-out prevalence | 0.2222 |

## CART

### Box 1 — S-M (S,M)

**Learned box conditions**

- `Total Clients`: [5.999, 10.000]
- `JSD Mean`: [0.018, 0.081]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - JSD Mean [0.0181, 0.081]
- **Other design conditions**:
  - Total Clients [6, 10]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 0.9500 |
| Train recall / coverage | 0.7600 |
| Train target prevalence | 0.5429 |
| Train absolute lift | 0.4071 |
| Train samples in box | 20 |
| Train targets in box | 19 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 25 |
| Runs retained by box | 20 |
| Target runs inside box | 19 |
| Target prevalence before box | 0.5556 |
| Precision inside box | 0.9500 |
| Recall / target coverage | 0.7600 |
| Absolute lift over held-out prevalence | 0.3944 |

### Box 2 — M-M (M,M)

**Learned box conditions**

- `JSD Mean`: [0.001, 0.014]
- **Includes NaN / not-selected values:** No

**Architectural interpretation**

- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Operating envelope**:
  - JSD Mean [0.000991, 0.0144]

**Discovery metrics (training partition)**

| Metric | Value |
|:---|---:|
| Train precision / density | 1 |
| Train recall / coverage | 0.4000 |
| Train target prevalence | 0.4286 |
| Train absolute lift | 0.5714 |
| Train samples in box | 8 |
| Train targets in box | 8 |

**Held-out metrics (test partition)**

| Metric | Value |
|:---|---:|
| Test runs | 45 |
| Target runs before box | 20 |
| Runs retained by box | 8 |
| Target runs inside box | 8 |
| Target prevalence before box | 0.4444 |
| Precision inside box | 1 |
| Recall / target coverage | 0.4000 |
| Absolute lift over held-out prevalence | 0.5556 |
