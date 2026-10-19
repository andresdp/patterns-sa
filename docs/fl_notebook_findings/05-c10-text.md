# RQ notebook findings — 10 clients, text

**Notebook:** [analysis-fl-rq-c10-text.ipynb](../../federatedlearning/analysis-fl-rq-c10-text.ipynb)  
**Scenario:** AG_NEWS paired with MLP, 10 clients. The common view has 80 runs (56 train/24 test); the all-environment view has 390 runs (273 train/117 test). Execution in `perfmodels` completed without code-cell errors.

Tradeoff labels are `<accuracy bin>-<round-time bin>`; `L-S` is large accuracy/fast rounds and `L-M` large accuracy/medium rounds. `S/M/L` are numeric bins, not quality labels. The notebook uses the shared campaign grid. The two environment views overlap.

## RQ1 — Observed tradeoffs and design associations

All common-environment runs are `L-M` (56 train and 24 test). In this setting, pattern-count group does not separate the outcomes and there is no tradeoff contrast to learn a configuration preference from.

In all environments, the test set is 78.6% `L-M`, 20.5% `L-S`, and 0.9% `M-M`; the `M-S` region has no held-out rows. Pattern-count shares show a modest shift: `L-S` rises from 16.7% at 0 instances to 18.2% at 1 and 25.0% at 2–3, while `L-M` falls from 83.3% to 81.2% and 73.1%. `L-L` appears in the 2–3 group (1.9%), and some medium-accuracy cases remain rare. Pattern count is associated with a more diverse/faster outcome mix but cannot identify a configuration that causes it.

**Design reading:** treat `L-M` as the prevalent result and `L-S` as a viable faster-round alternative. Use the low-delay operating envelope below to assess whether `L-S` is achievable in the intended deployment; do not infer that increasing the number of instances alone will produce it.

## RQ2 — Box rules and what-if robustness

The common view has only `L-M`, and neither PRIM nor CART discovers a box. Under all environments, Alpha Dirichlet Mean and delay percentage rank first, followed by Client Selector Criteria, JSD, CPU, HDH, and pattern-instance measures. This feature ranking agrees with the other slices that the broader environment contributes strongly to observed tradeoffs; it is not a causal effect ranking.

| Target/method | Architectural reading | Held-out what-if result |
|---|---|---|
| `L-S`, PRIM/CART | No pattern policy required; delay percentage 0–12.5%. PRIM additionally limits HDH Instances to 0–4.5; CART uses only delay. | PRIM 15/15 hits, 62.5% coverage; CART 15/15 hits, 62.5% coverage. Baseline 20.5%; gain +79.5 pp. |
| `L-M`, PRIM/CART | No pattern policy required; CPU Mean 10.25–11 and delay percentage 12.5–100%. | 66/66 hits, 71.7% coverage. Baseline 78.6%; gain +21.4 pp. |
| `M-M`, PRIM | No pattern policy required; CPU Mean 8–10.25 and HDH Instances 0.5–8. | 1/9 hits (11.1%); captures the only held-out target case. Baseline 0.9%; gain +10.3 pp. |
| `L-L`, PRIM/CART | PRIM bounds Alpha 0.625–0.688, Pattern Instances 2.5–7 and HDH Instances 0.5–3. CART requires CS OFF, 1.5–3 active types, 2.5–3 HDH instances, and delay 50–100%. | PRIM 5/12 hits (41.7%), 100% coverage; CART 3/3 hits, 60% coverage. Baseline 4.3%. |

The strongest choices are the two higher-support envelopes: delay ≤12.5% for `L-S`, and delay ≥12.5% plus the CPU-mean range for `L-M`. Both have full in-box target share in held-out runs without a required pattern policy. The rare `M-M` box is not precise enough to guide a design. For `L-L`, CART’s 3/3 precision requires a narrow rule and has only three retained cases; PRIM covers all five target cases but includes seven non-targets. Pick based on whether operational coverage or a tighter observed pocket matters, then validate on more runs.

**Limits:** Only one `M-M` target exists in the held-out sample, so its box rate is especially unstable. Split rows are grouped by `partition_seed` but still come from this campaign. Per-client averages do not show client imbalance.
