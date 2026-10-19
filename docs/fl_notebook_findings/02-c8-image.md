# RQ notebook findings — 8 clients, image

**Notebook:** [analysis-fl-rq-c8-image.ipynb](../../federatedlearning/analysis-fl-rq-c8-image.ipynb)  
**Scenario:** CIFAR-10 paired with CNN 16k, 8 clients. The common view has 80 runs (56 train/24 test); the all-environment view has 390 (273 train/117 test). Execution in `perfmodels` completed without code-cell errors.

Labels are `<accuracy bin>-<round-time bin>`, so `M-S` means medium accuracy and fast rounds. `S/M/L` are value bins, not good/bad labels. Both views use the fixed campaign-wide edges. The common view fixes the shared environmental point; the all-environment view adds the varied environment mix. The views overlap.

## RQ1 — Observed tradeoffs and design associations

In the common environment, `M-M` dominates: it accounts for 54/56 training rows and all 24 held-out rows. The other two training observations are singleton `S-M` and `M-S` cases, so they do not support stable configuration guidance. By configured pattern-count group, 0 and 1 instances are 100% `M-M`; the 2–3 group is 95% `M-M`, with one `M-S` and one `S-M` run. A designer cannot select a reliably different tradeoff from this fixed-environment evidence.

In the all-environment view, all four regions `S-S`, `S-M`, `M-S`, and `M-M` appear. The test distribution is 5.1% `S-S`, 26.5% `S-M`, 15.4% `M-S`, and 53.0% `M-M`. `M-M` stays the largest single region across pattern-count groups (50.0% with 0 instances, 51.8% with 1, 55.6% with 2–3), while the combined fast-round share (`M-S`) rises from 16.7% at 0 instances to 19.4% at 2–3. The groups also vary in low-accuracy `S-M`/`S-S` outcomes, so pattern count alone does not define a preferred direction.

**Design reading:** the shared environment produces a stable `M-M` outcome, while broader conditions expose the tradeoff space. For deployment planning, use all-environment results to identify the conditions that move a candidate away from `M-M`; use common-environment results to compare policies at the shared point.

## RQ2 — Box rules and what-if robustness

The common-environment feature ranking is led by JSD Mean, Pattern Types Active, Client Selector Criteria, and Pattern Instances. Under all environments, Alpha Dirichlet Mean, delay percentage, JSD Mean, CPU Mean, and Client Selector Criteria lead. This repeated shift toward environment measures suggests that operating conditions matter to the pooled outcome map. Feature importance is a ranking, not effect direction or causal attribution.

### Common-environment boxes

| Target/method | Architectural reading | Held-out what-if result |
|---|---|---|
| `M-M`, PRIM | No pattern policy required; Pattern Types Active is 0–1.5 (effectively at most one active type in observed levels). | 12/12 retained runs hit `M-M`; coverage 50%. Baseline already 24/24 (100%); gain 0 pp. |
| `M-M`, CART | No pattern policy required; JSD Mean ≤0.006 and Pattern Types Active 0–2.5. | 6/6 hits; coverage 25%. Baseline 100%; gain 0 pp. |

These boxes do not improve target attainment because every test run is already `M-M`. They only describe narrower subsets. There is no observed robustness benefit from imposing these restrictions in the common view.

### All-environment boxes

| Target/method | Architectural reading | Held-out what-if result |
|---|---|---|
| `S-S`, PRIM | CS ON, Resource-Based strategy, CPU criterion, value 2.0; CPU Mean 8.25–10.125 and JSD Mean 0.003–0.090. | 2/4 hits (50%); captures 2/6 target runs (33.3%). Baseline 5.1%; gain +44.9 pp. |
| `S-S`, CART | Same CS policy; JSD Mean 0.014–0.090 and Alpha Dirichlet Mean 0.625–0.688. | 1/1 hit; captures 1/6 target runs (16.7%). Baseline 5.1%; gain +94.9 pp, but one retained row is fragile evidence. |
| `S-M`, PRIM/CART | CS OFF (Criteria is not selected); Alpha Dirichlet Mean 0.625–0.688. | PRIM 21/21 hits, 67.7% coverage; CART 21/21 hits, 67.7% coverage. Baseline 26.5%; gain +73.5 pp. |
| `M-S`, PRIM | CS OFF; Alpha Dirichlet Mean 0.688–0.875 and delay percentage 0–12.5%. | 9/9 hits; 50% coverage. Baseline 15.4%; gain +84.6 pp. |
| `M-S`, CART | No pattern policy required; JSD Mean ≤0.006, Alpha Dirichlet Mean 0.813–0.875, delay percentage 0–12.5%. | 13/13 hits; 72.2% coverage. Same baseline; gain +84.6 pp. |
| `M-M`, PRIM/CART | CS OFF; Alpha Dirichlet Mean 0.812–0.875 and delay percentage 12.5–100%. | 33/33 hits; 53.2% coverage. Baseline 53.0%; gain +47.0 pp. |

The useful operating-envelope signal is the paired delay distinction: `M-S` boxes select delay ≤12.5%, while `M-M` boxes select delay ≥12.5%, with CS OFF in the PRIM versions. For `M-S`, CART captures 13/18 held-out target cases versus PRIM’s 9/18; the additional JSD condition in CART still yields full precision in this split. For `S-M`, CS OFF plus the lower alpha band gives a high-retention rule. Treat the single-row CART `S-S` result as a lead to validate, not a design rule.

**Limits:** All-environment box gains are observational and conditional on the sampled distribution. Low-support targets and overlapping views limit generalization. Compact per-run averages hide differences between clients.
