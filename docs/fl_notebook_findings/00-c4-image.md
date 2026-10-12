# RQ notebook findings — 4 clients, image

**Notebook:** [analysis-fl-rq-c4-image.ipynb](../../federatedlearning/analysis-fl-rq-c4-image.ipynb)  
**Execution:** `perfmodels`; common-environment and all-environment views completed without cell errors.  
**Scenario:** CIFAR-10/CNN 16k, 4 clients. The common view has 80 runs (8 configurations × 10 partition seeds); the all-environment view has 390 runs.

## How to read the tradeoffs

Tradeoff labels are **accuracy bin – round-time bin**. `S`, `M`, and `L` mean small, medium, and large values; they do not mean good or bad. Here, higher accuracy and lower time are preferable, so `M-S` means medium accuracy and fast rounds. Both environment views use the same campaign-wide edges: accuracy 0.2075/0.4774/0.7473/1.0172 and average total time 1.5625/9.5065/17.4505/25.3945. The common view fixes the environment at the point shared by all configurations. The all-environment view includes all sampled settings, whose mix varies by configuration. They are complementary descriptions of this campaign, not independent replications.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

### Common-environment view

Only `M-M` and `M-S` are populated. `M-M` is the dominant outcome; `M-S` appears more often in configurations with Client Selector (CS) enabled. The pattern-count table gives the same directional signal:

| Configured pattern instances | `M-M` | `M-S` |
|---:|---:|---:|
| 0 | 100.0% | 0.0% |
| 1 | 86.7% | 13.3% |
| 2–3 | 72.5% | 27.5% |

The exact pattern-type view is consistent: `M-S` share rises from 0% for type 0 to 13% for type 1, 23% for type 2, and 40% for type 3. The configuration table points to CS as the clearest association: with CS OFF, `M-S` is 0–10%; with CS ON it is 30–40% across the four MC/HDH combinations. This supports treating CS as a candidate for exploring faster rounds in this fixed environment. It does not show that adding a pattern instance causes the shift: pattern count combines distinct decisions and settings.

### All-environment view

All four populated regions occur: `S-S`, `S-M`, `M-S`, and `M-M`. `M-M` remains the largest region for every exact pattern type, but its share declines as the number of configured instances increases (77% at type 0, 72% at type 1, 63% at type 2, and 53% at type 3). `M-S` grows from 17% at type 0 to 47% at type 3. The grouped pattern-count table shows a similar trend: `M-M` falls from 76.7% with no patterns to 61.2% with 2–3, while `M-S` rises from 16.7% to 33.8%.

Configuration shares sharpen the design reading. CS-enabled alternatives have substantially more `M-S` runs (43–47% for CS+MC and CS+MC+HDH; 34–46% for CS alone or CS+HDH) than most CS-OFF alternatives (2–20%). However, this broad view mixes environment settings. It therefore supports a screening hypothesis—CS-enabled designs are associated with faster-round tradeoffs across the sampled campaign—not a pattern-only explanation. The operating conditions and feature-ranking results below help describe that context.

### Designer takeaway

- To explore faster rounds in the common environment, include CS-enabled configurations in the candidate set and compare their accuracy against the project’s minimum acceptable level.
- Treat the number of pattern instances as a descriptive stress indicator, not as a control knob with a proven monotonic effect. Compare the complete configurations and their operating conditions.
- Use continuous accuracy/time values alongside bins when choosing between alternatives; bin membership hides differences within a region.

## RQ2 — Which joint conditions identify target tradeoffs, and what changes inside a box?

Feature importance screens for candidate drivers; PRIM and CART boxes describe conjunctions associated with a selected region. A box condition is a joint rule: omitted variables are unrestricted. The architectural explanation translates relevant low-level parameters to policies and their operating context. These are observed associations, not causal prescriptions.

### Feature-importance pattern

| View | Highest-ranked variables (weighted ranking) | Reading for a designer |
|---|---|---|
| Common environment | Client Selector Criteria, Pattern Instances, Pattern Types Active, HDH Batch Size | With environment held fixed, the ranking emphasizes architecture choices and their configured parameters. |
| All environments | Alpha Dirichlet Mean, delay percentage, Client Selector Criteria, CPU Mean, JSD Mean | Across environment variation, non-IID and delay/resource descriptors become prominent alongside CS. |

This shift is consistent with environment conditions contributing to the broader tradeoff map. Importance is a model ranking, not effect direction or a percentage of outcome explained; correlated variables can share or exchange rank. Use it to choose what to inspect in boxes and plots, not to make a standalone configuration decision.

### Common-environment boxes

| Method and target | Discovered rule and architectural reading | Held-out result |
|---|---|---|
| PRIM `M-S` | `Client Selector Criteria = CPU` **and** `HDH Batch Size` 30.4–32. Architecture: CS ON, Resource-Based strategy, CPU criterion, value 2.0; HDH ON with its declared settings (batch size 32). No uncertainty condition is selected. | 2/6 test runs in the box hit `M-S` (precision 33.3%); it captures 2/4 test `M-S` runs (recall/coverage 50%). Baseline test prevalence is 4/24 (16.7%); gain +16.7 pp. |
| PRIM `M-M` | CS criterion not selected and HDH batch size not selected or ≤30.4. Architecture: CS OFF and HDH OFF; no further policy is prescribed. | 6/6 in-box test runs hit `M-M` (100% precision); captures 6/20 target runs (30% recall). Baseline prevalence 83.3%; gain +16.7 pp. |
| CART `M-M` | `Pattern Instances` 2–4 and CS criterion not selected. Architecture: CS OFF, with the additional configured-instance condition. | 6/6 hits (100% precision); 6/20 target runs captured (30% recall). Baseline prevalence 83.3%; gain +16.7 pp. |

The `M-M` rules make an already common outcome more concentrated, but retain only 6 of 24 test runs. The `M-S` PRIM rule is less precise and has modest support. In this fixed environment there is no uncertainty envelope to interpret. These are narrow, low-support filters, so validate them on further runs before using them as acceptance rules.

### All-environment boxes

| Method and target | Discovered rule and architectural reading | Held-out result |
|---|---|---|
| PRIM `S-S` | CS criterion = CPU and Alpha Dirichlet Mean 0.625–0.688. Architecture: CS ON, Resource-Based/CPU/2.0; operating envelope has the stated alpha range. | 4/6 box runs hit; precision 66.7%, recall 100% (4/4 target runs); baseline 3.4%, gain +63.2 pp. |
| PRIM `S-M` | CS criterion not selected, CPU Mean 8.25–9.5, Alpha Dirichlet Mean 0.625–0.688. Architecture: CS OFF; CPU and alpha conditions define the operating envelope. | 1/6 hit; precision 16.7%, recall 25%; baseline 3.4%, gain +13.2 pp. Weak concentration. |
| PRIM `M-S` | JSD Mean not selected or ≤0.019, delay percentage 0–12.5%. Architecture: no pattern policy required; low delay and low JSD define the operating envelope. | 6/6 hit; precision 100%, recall 20% (6/30 target runs); baseline 25.6%, gain +74.4 pp. |
| CART `M-S` | Delay percentage 0–12.5%; no pattern policy required. | 15/15 hit; precision 100%, recall 50% (15/30 target runs); baseline 25.6%, gain +74.4 pp. |
| PRIM/CART `M-M` | CS OFF, alpha mean 0.688–0.875, JSD within the method-specific upper limit, and delay percentage at least 37.5%. Architecture: CS policy OFF; alpha, JSD, and delay define the operating envelope. | 6/6 hit; precision 100%, recall 7.6% (6/79 target runs); baseline 67.5%, gain +32.5 pp. |

The clearest what-if result is CART’s low-delay rule for `M-S`: restricting to delay ≤12.5% raises target share from 25.6% to 100% in the held-out sample, retaining 15/117 runs and half of the observed target cases. PRIM adds a low-JSD condition but retains only six runs and captures 20% of target cases, so that extra restriction is not useful if coverage matters. For `M-M`, the box also reaches 100% precision but captures only 6 of 79 target runs; it describes a narrow reliable pocket rather than the general recipe for `M-M`.

### Designer takeaway

- If `M-S` is the chosen target, test low-delay operation first; CART finds a simpler, broader envelope than PRIM, with the same observed precision and greater target coverage.
- If the deployment cannot constrain delay, these results do not support expecting the same `M-S` stability. Explore configurations and environments outside the box before adopting the rule.
- For `M-M`, the CS-OFF/operating-envelope box identifies a highly concentrated but narrow subset. Decide whether the 7.6% target coverage is acceptable before treating it as a useful operating restriction.
- Keep the architecture explanation hierarchical: policy-level decisions (such as CS OFF) provide design context, while alpha, delay, CPU, and JSD limits describe the conditions under which the box was observed.

## Scope and limits

The grouped split holds out `partition_seed` values, keeping all rows from a given partition seed on one side. The common view has 56 training and 24 test runs; the all-environment view has 273 training and 117 test runs. Held-out rows are still from the same campaign. Boxes are observational filters: the what-if tables quantify target concentration and the share of scenarios retained, not guaranteed improvement from applying a rule. Compact data averages selected client-level measures within each run, so client-to-client imbalance is not visible here. The common and all-environment subsets overlap and should not be counted as independent evidence.
