# Text task synthesis: RQ1 and RQ2

### Recurring findings

Across the seven text slices, populated regions are concentrated at high accuracy: L-S (high accuracy, short time) and L-M (high accuracy, medium time) recur in the baseline, compressor-only, client-count slices and much of HDH-only. Low-accuracy regions are consistently empty. L-M generally dominates the observed run mix. The all-configuration c4/c8/c10 slices add sparse medium-accuracy outcomes and, at c4, a small L-L tail. Empty cells are sample gaps, not feasibility claims. [c4 plot](../plots/quality-space__task-text__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png), [c8 plot](../plots/quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png), [c10 plot](../plots/quality-space__task-text__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png).

The baseline (180 runs) splits into L-M 150/180 and L-S 30/180. Fixed-client all-configuration samples each contain 390 runs: L-M is 263/390 at c4, 307/390 at c8, 305/390 at c10. Single-pattern profiles are distinct slices: selector 78/150 L-M and 68/150 L-S; HDH 138/150 L-M and 9/150 L-L; compressor 180/210 L-M and 30/210 L-S. These are profile summaries, not matched policy effects.

### Configuration/client-count-specific findings

At c4, M-S/M-M/L-L appear (small support); c8 and c10 emphasize L-S/L-M, with M-S/M-M rare. The baseline and single-pattern notebooks pool clients 4/8/10 and cannot replace fixed-count comparisons. Within c4 the L-M allocation spans configurations; c8 has one deterministic configuration in L-M; c4 and c10 have none. Pattern-count strata combine policies and context: neither active-type count nor instance count is a randomized dose.

### Evidence gaps

The environment design is uneven, and run-level client averages hide imbalance. Rare and absent held-out targets limit comparisons: c4 M-M absent, c10 M-S absent, HDH-only M-M absent, and several medium tradeoffs have one or two test rows. Grouped splits use only 3 of 10 partition seeds for test.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

### Recurring findings

Delay percentage repeatedly separates high-accuracy short-time from medium-time boxes: low delay (roughly 0–12.5%) is associated with L-S, while higher delay (12.5–100%) aligns with L-M in the compressor-only and several fixed-client slices. This is an operating-context association, not evidence that manipulating delay or a pattern would cause a tradeoff. Box-restricted held-out purity is often high, but coverage varies: at c4 L-S coverage is 19.4%; c8 it is 65.2%; c10 it is 62.5%. L-M coverage is about 57–72% across fixed client counts. [Text case reports](.) link each exact rule and support to its notebook and box report.

### Configuration/client-count-specific findings

In c4, the L-S rule includes Client Selector ON/CPU criterion jointly with low delay; L-M is associated with higher delay and low pattern/HDH instance bounds, with selector not selected. In c8 and c10, low/high delay rules dominate. Baseline and compressor-only rules mainly separate delay because their pattern configuration is fixed. Selector-only and HDH-only boxes instead profile context under a fixed pattern choice; they cannot validate the choice against OFF. Feature rankings shift by slice, though delay, Alpha Dirichlet Mean, CPU/client summaries, pattern instances, and selector criteria recur. Treat importance as relative predictive credit; zero scores can reflect constants/correlation pruning.

### Evidence gaps

Some discovered boxes have no held-out target rows (unavailable evaluation), while others are based on tiny test supports. A 100% precision from a handful of retained runs does not imply broad robustness. Section 11 policy matrices are conditional on each policy group; zeros can indicate unsupported cells. Box restrictions filter existing held-out rows, and STARR-style results describe discretized tradeoff membership only.

## Task conclusions and implications

For AG_NEWS/MLP under the sampled compact campaign, high accuracy is common, with round-time category varying most visibly with operating conditions, particularly delay. The evidence supports using the boxes to prioritize validation scenarios within the same configuration and client scope. It does not support causal claims about CS, MC, or HDH, generalization beyond the sampled seed/environment mix, or treating an empty region as impossible.

**Practitioner implication:** use the delay/context envelopes as candidate run filters for further evaluation; preserve the stated policy and client scope and gather more held-out seeds for rare targets. **Research implication:** add balanced policy-by-environment coverage and larger independent seed holdouts, then test whether the observed associations persist. The case reports cite each notebook, box report, and plot; the refreshed [evidence manifest](evidence-manifest.json) fingerprints the inputs.
