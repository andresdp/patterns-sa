# RQ notebook findings — 10 clients, image

**Notebook:** [analysis-fl-rq-c10-image.ipynb](../../federatedlearning/analysis-fl-rq-c10-image.ipynb)  
**Scenario:** CIFAR-10 paired with CNN 16k, 10 clients. The common view has 80 runs (56 train/24 test); the all-environment view has 390 runs (273 train/117 test). The notebook executed in `perfmodels` without code-cell errors.

Tradeoff labels are `<accuracy bin>-<round-time bin>` (`M-S` is medium accuracy/fast rounds). `S/M/L` mean small/medium/large values, not quality. Both views use fixed campaign-wide edges. The common-environment and all-environment views overlap.

## RQ1 — Observed tradeoffs and design associations

Every common-environment run falls in `M-M` (56/56 train, 24/24 test). The pattern-count table also shows 100% `M-M` for 0, 1, and 2–3 instances. At this shared operating point, the discretized outcomes do not distinguish configurations or instance levels.

The all-environment test set contains 53.0% `M-M`, 28.2% `S-M`, 13.7% `M-S`, and 5.1% `S-S`. By pattern-count group, `M-M` is 50.0% with 0 instances, 51.8% with 1, and 56.2% with 2–3; `M-S` is 16.7%, 8.2%, and 18.8%, respectively. There is no simple monotonic pattern. Pattern-type composition is more suggestive: the 3-type group is 67% `M-M` and 33% `M-S`, but it is a smaller group and does not isolate a single policy.

**Design reading:** use the all-environment contingency table to compare complete policy combinations; pattern count alone does not identify a reliable direction. The common point is robustly `M-M` at the bin level, but offers no basis for choosing a configuration when the goal is to move to another region.

## RQ2 — Box rules and what-if robustness

The common view has only one populated tradeoff, and neither PRIM nor CART found a non-empty box. This is a discovery limitation due to no outcome contrast, not a failure of execution.

For all environments, feature ranking repeatedly puts Alpha Dirichlet Mean and delay percentage at the top, with CPU Mean, CS Criteria, JSD Mean, and pattern stress also prominent. This is consistent with operating conditions shaping the pooled outcome map. Rankings show model reliance, not direction or cause.

| Target/method | Architectural reading | Held-out what-if result |
|---|---|---|
| `S-S`, PRIM | CS ON, Resource-Based/CPU/value 2.0; CPU Mean 8.0–8.75; Alpha Dirichlet Mean 0.600–0.825. | 3/6 hits (50%); 3/6 target cases captured. Baseline 5.1%; gain +44.9 pp. |
| `S-S`, CART | Same CS policy; CPU Mean 8.0–8.75, JSD Mean ≤0.010, Alpha 0.600–0.825. | 1/3 hits (33.3%); captures 1/6 target cases. Baseline 5.1%; gain +28.2 pp. |
| `S-M`, PRIM/CART | CS OFF; Alpha Dirichlet Mean 0.600–0.825. | 27/27 hits; 81.8% coverage. Baseline 28.2%; gain +71.8 pp. |
| `M-S`, PRIM/CART | No pattern policy required; Alpha Dirichlet Mean 0.825–0.900 and delay percentage 0–12.5%. | 15/15 hits; captures 15/16 target cases (93.8%). Baseline 13.7%; gain +86.3 pp. |
| `M-M`, PRIM | CPU Mean 10.25–11, Alpha 0.675–0.900, JSD Mean ≤0.013, delay 12.5–100%. No pattern policy selected. | 45/45 hits; 72.6% coverage. Baseline 53.0%; gain +47.0 pp. |
| `M-M`, CART | CPU Mean 10.25–11, Alpha 0.825–0.900, delay 12.5–100%. No pattern policy selected. | 45/45 hits; 72.6% coverage. Same baseline and gain. |

For `M-S`, low delay plus the higher alpha range is the strongest actionable operating-envelope association: 15 of 16 held-out targets lie inside the box, with no pattern policy required. For `S-M`, CS OFF and the lower alpha range produce a broad high-precision rule. The `S-S` boxes retain few runs and have lower coverage; use them as search leads rather than acceptance criteria.

**Limits:** Although held-out support is better for the broad target boxes, all results remain sample-conditional. Low-support targets are unstable; the all-environment view also mixes environment distributions across configurations. Compact run averages hide client-level distributions.
