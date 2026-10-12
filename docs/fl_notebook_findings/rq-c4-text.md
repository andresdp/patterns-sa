# RQ notebook findings — 4 clients, text

**Notebook:** [analysis-fl-rq-c4-text.ipynb](../../federatedlearning/analysis-fl-rq-c4-text.ipynb)  
**Scenario:** AG_NEWS paired with MLP, 4 clients. Each view contains 80 runs; the common view has 56 training and 24 test runs, while the all-environment view has 273 training and 117 test runs. All code cells completed in `perfmodels` without execution errors.

Tradeoff labels are `<accuracy bin>-<round-time bin>`: `L-S` is large accuracy with fast rounds; `L-M` is large accuracy with medium round time. `S/M/L` describe value ranges, not quality ranks. This view uses the fixed campaign-wide grid. The common-environment runs hold sampled environment shares constant; the all-environment runs include the broader mix, so the views overlap and are not independent.

## RQ1 — Observed tradeoffs and design associations

In the common environment, 48/56 training runs and 20/24 held-out runs are `L-M`; the remainder are `L-S`. The pattern-count table shows a consistent association within this small slice: `L-S` share rises from 0% with zero pattern instances to 10% with one and 22.5% with 2–3, while `L-M` falls from 100% to 90% and 77.5%. Pattern-count levels combine different policies, so this is a stress-space association, not evidence that adding instances causes faster rounds.

Across all environments, training runs are 67.4% `L-M`, 25.3% `L-S`, and 4.4% `L-L`; the held-out set is 67.5%, 26.5%, and 4.3%, respectively. By pattern-count group, `L-S` increases from 16.7% (0 instances) to 21.2% (1) and 33.8% (2–3), while `L-M` decreases from 83.3% to 70.6% and 58.1%. The 2–3 group also includes 5% `L-L`, so “faster” is not a single uniform shift. More active pattern types also trend toward `L-S`, but the changes are modest and multiple configurations contribute to each group.

**Design reading:** retain both `L-M` and `L-S` as candidate outcomes. If lower round time is a priority, compare the complete configurations that enable CS and inspect their operating envelope; the instance-count plot alone cannot identify which decision accounts for the association.

## RQ2 — Box rules and what-if robustness

Feature ranking changes with scope. In the common view, the leading variables are Client Selector Criteria, Pattern Types Active, Message Compressor Algorithm, and HDH Batch Size. In the all-environment view, Alpha Dirichlet Mean and delay percentage rank first, followed by Client Selector Criteria, HDH/CPU measures, and pattern-instance descriptors. Treat the ranking as a screen for candidate conditions; it gives neither direction nor a causal effect, and pattern-bound values can act as proxies for whether a pattern is enabled.

### Common-environment boxes

| Target/method | Architectural reading | Held-out what-if result |
|---|---|---|
| `L-S`, PRIM | CS ON, Resource-Based strategy, CPU criterion, value 2.0; no uncertainty condition selected. | 4/12 retained runs hit `L-S` (33.3% precision); captures 4/4 target runs (100% coverage). Baseline 4/24 (16.7%); gain +16.7 pp. |
| `L-M`, PRIM/CART | CS OFF; no additional design or uncertainty condition selected. | 12/12 retained runs hit `L-M` (100% precision); captures 12/20 target runs (60% coverage). Baseline 83.3%; gain +16.7 pp. |

For this fixed setting, the rules separate two observed policy states: CPU-based CS is associated with some `L-S` cases, while CS OFF yields a compact, high-precision `L-M` subset. The latter removes 12 of 24 test runs and misses 40% of the `L-M` cases, so it is a selective option rather than a general requirement for `L-M`.

### All-environment boxes

| Target/method | Architectural reading | Held-out what-if result |
|---|---|---|
| `L-S`, PRIM | CS ON (Resource-Based/CPU/value 2.0) and delay percentage 0–12.5%. | 6/6 hits; 19.4% of `L-S` cases captured. Baseline 26.5%; box share 100%. |
| `L-S`, CART | No pattern policy required; delay percentage 0–12.5%. | 15/15 hits; 48.4% coverage. Same 26.5% baseline; box share 100%. |
| `L-M`, PRIM/CART | CS OFF; 12.5–100% delay, 0–5.5 pattern instances, and 0–2.5 HDH instances. | 45/45 hits; 57.0% coverage. Baseline 67.5%; box share 100%. |
| `L-L`, PRIM | Alpha Dirichlet Mean 0.625–0.688, 2.5–7 pattern instances, and 0.5–3 HDH instances; no single pattern policy required. | 5/12 hits (41.7%); captures all 5 target cases. Baseline 4.3%; gain +37.4 pp. |
| `L-L`, CART | CS OFF, 1.5–3 active pattern types, 2.5–3 HDH instances, and 50–100% delay. | 3/3 hits; 60% coverage. Baseline 4.3%; box share 100%. |

For a faster `L-S` target, low delay is the most portable observed restriction: CART needs no pattern policy and captures more than twice as many target runs as PRIM. For `L-M`, the box combines CS OFF with a high-delay operating envelope and modest pattern-instance limits. These are conditional associations: a designer should check whether the delay and pattern-activity limits match deployment constraints before using the target-rate gain.

**Limits:** The `L-L` boxes rely on five held-out target runs, so their apparent gains are fragile. Compact outcomes average selected per-client measurements within each run. The split holds out `partition_seed` groups, but remains within this campaign; none of the box rates is a deployment guarantee.
