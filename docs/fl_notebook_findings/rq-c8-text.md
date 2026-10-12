# RQ notebook findings — 8 clients, text

**Notebook:** [analysis-fl-rq-c8-text.ipynb](../../federatedlearning/analysis-fl-rq-c8-text.ipynb)  
**Scenario:** AG_NEWS paired with MLP, 8 clients. Each view has 80 common-environment or 390 all-environment runs; grouped splits are 56/24 and 273/117, respectively. Execution in `perfmodels` completed without code-cell errors.

Tradeoffs are labeled `<accuracy bin>-<round-time bin>`; `L-S` means large accuracy and fast rounds. `S/M/L` denote bin size, not desirability. Shared campaign-wide edges are used. Common and all-environment views overlap; environmental mixes differ in the broader view.

## RQ1 — Observed tradeoffs and design associations

The common environment is entirely `L-M` (56/56 training and 24/24 test). Pattern-count groups 0, 1, and 2–3 are also all `L-M`. The common setting therefore provides no evidence to rank configurations by these coarse tradeoff bins and no target variety for box discovery.

Across all environments, held-out runs are 78.6% `L-M`, 19.7% `L-S`, and 0.9% each `M-S` and `M-M`. `L-M` remains dominant in each pattern-count group, but its share decreases from 83.3% with 0 instances to 81.2% with 1 and 74.4% with 2–3; `L-S` increases from 16.7% to 18.2% and 21.9%. More instances are associated with a modest shift toward fast rounds, while low-support medium-accuracy regions appear only rarely. Pattern-count groups mix several policies and instance assumptions; this is not a causal effect.

**Design reading:** preserve `L-M` as the default observed tradeoff and consider `L-S` when faster rounds are needed. The common view cannot distinguish which configuration best supports that choice; use the environmental rules from the all-environment analysis and verify them under the expected delay conditions.

## RQ2 — Box rules and what-if robustness

Common-view feature importance emphasizes Pattern Instances, JSD Mean, Client Selector Criteria, Pattern Types Active, and HDH Batch Size. In the all-environment view, Alpha Dirichlet Mean and delay percentage rank first, followed by CS, HDH/CPU measures, and pattern counts. The environment-first ranking recurs in the other client/task slices as well; it is useful for deciding which operating variables to monitor, not as a causal ranking.

### Common-environment boxes

PRIM and CART discovered no non-empty box for the sole observed target, `L-M`. This is not a notebook failure: all runs already fall into one tradeoff bin and the discovery methods found no sufficiently selective rule. No box-based robustness gain is supported in this view.

### All-environment boxes

| Target/method | Architectural reading | Held-out what-if result |
|---|---|---|
| `L-S`, PRIM/CART | No pattern policy required; delay percentage 0–12.5%. | PRIM 15/15 hits and 65.2% coverage; CART 15/15 hits and 65.2% coverage. Baseline 19.7%; gain +80.3 pp. |
| `L-M`, PRIM/CART | No pattern policy required; CPU Mean 10.125–10.75 and delay percentage 12.5–100%. | 66/66 hits; 71.7% coverage. Baseline 78.6%; gain +21.4 pp. |
| `M-S`, PRIM | No pattern policy required; CPU Mean 8.25–10.125 and HDH Instances 0.5–4.5. | 1/6 hits; captures the sole held-out target case, but precision is 16.7%. Baseline 0.9%; apparent gain +15.8 pp. |

The high-support rules give a practical operating split: low delay is associated with `L-S`; higher delay combined with a narrower CPU-mean band is associated with `L-M`. Both have full in-box target share in the held-out sample, while retaining roughly two-thirds to three-quarters of target cases. The rare `M-S` box is not a dependable prescription despite capturing its one test target.

**Limits:** The train/test split is grouped by partition seed but still uses the same compact campaign. CPU, delay, and configured pattern measures co-vary; the boxes describe combinations, not isolated causal levers. Compact averages do not expose client-level imbalance.
