# Compact FL findings synthesized by research question

This synthesis uses the six executed RQ1/RQ2 notebooks for the compact campaign. Each slice pairs a dataset with its model and fixes one client count: 4, 8, or 10. Every notebook contains a common-environment view followed by an all-environment view. The views share runs and are complementary, not independent replications.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

### Conclusions across the six slices

1. **The shared environment gives a useful controlled comparison, but often too little outcome variety for discovery.** The common view has one populated tradeoff in 3 of 6 slices: 8-client text is entirely `L-M`, 10-client image entirely `M-M`, and 10-client text entirely `L-M`. The 8-client image test set is entirely `M-M`; only two training rows fall elsewhere. These settings can show what occurred at the shared operating point, but they cannot rank designs for reaching absent regions or support a meaningful box for a region that never varies.

2. **The task/model pair and client count matter to the observed outcome map.** Common-environment image runs center on `M-M` at 8 and 10 clients, while 4-client image also has `M-S`. Text runs center on `L-M`; 4-client text additionally has a visible `L-S` subset. These labels are discretized regions, not direct evidence that one task or client count is intrinsically better. Compare continuous accuracy and time values before transferring a configuration between slices.

3. **Pattern-count groups are useful summaries, but they do not define a universal monotonic tradeoff.** In common 4-client text, `L-S` grows from 0% with no active instances to 22.5% with 2–3; common 4-client image shows a similar shift toward `M-S`. Across all environments, text slices show smaller increases in `L-S` at 2–3 instances (21.9% for 8 clients; 25.0% for 10 clients), while image slices differ: 8-client image remains mostly `M-M`, and 10-client image has a slight `M-M` rise but no consistent movement in fast regions. Pattern count combines different policy decisions, participating-client counts, and estimated pattern instances. It is a load/stress descriptor, not a single controllable architectural lever.

4. **The complete configuration remains the right design alternative to compare.** Marginal tables and objective-versus-instance plots describe associations; they do not isolate a pattern’s effect. For a design choice, compare the full CS/MC/HDH configuration under the intended operating envelope, check both objectives, and use the pattern-count table as context. Any apparent pattern-count gradient should be verified against the actual policy combinations and run support that form each group.

### Implications for software architects/designers

- Pick a target region that meets the product’s accuracy floor and time budget, then shortlist complete configurations that reach it in the matching dataset/model and client-count slice.
- Use common-environment results to compare designs at the same sampled environment point. Use all-environment results to see how that shortlist behaves as non-IID, delay, CPU, and JSD conditions vary.
- Do not turn an observed rise in `*-S` shares by pattern count into a recommendation to add instances. Identify the specific policy and its deployment constraints first.

### Implications for researchers

- Report populated and empty quadrants for each task/model and client-count slice. An empty quadrant is a boundary of the sampled design space, not evidence that the outcome is impossible.
- Keep the campaign-wide objective grid fixed when crosschecking slices, as these notebooks do, and report run counts with every pattern-count percentage. Avoid interpreting `Pattern Instances` as a randomized treatment: it combines policy, participation, and execution-derived activity.
- Separate common-environment comparisons from all-environment summaries in figures and prose. The former controls the sampled environment point; the latter may reweight environments differently by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

### Consistent findings

1. **Broadening to all environments consistently elevates uncertainty/resource descriptors.** Alpha Dirichlet Mean and delay percentage appear at or near the top of the feature rankings in every all-environment slice. CPU Mean and JSD Mean also recur. Common-environment rankings instead emphasize CS criteria, pattern types/instances, compressor algorithm, and HDH settings. This consistency says which variables the fitted models use to organize the observations; it does not establish causal importance or the direction of a change.

2. **Low delay is the clearest recurring operating-envelope condition for fast-round targets.** CART/PRIM rules repeatedly associate delay ≤12.5% with `L-S` in 8- and 10-client text, and with fast-round image regions in 4-, 8-, and 10-client image. Held-out target shares inside those boxes are 100% in the reported samples. Support and coverage differ: the 10-client image `M-S` box captures 15/16 target runs; 8-client text `L-S` captures 15/23; c4 image CART `M-S` captures 15/30. A designer can treat low delay as a strong condition to test for a faster-round operating mode, while choosing the rule by its coverage and retained scenario count.

3. **CS rules are conditional on the target, not universal.** The 4-client text common-view `L-S` box maps `Client Selector Criteria = CPU` to CS ON with Resource-Based strategy and value 2.0; its `L-M` box maps “not selected” to CS OFF. In broader views, CS OFF is part of some text/image rules, while several fast-round boxes require no pattern policy at all. The architecture explanation should therefore be read as a joint prescription: use the stated design policy only with the operating envelope listed under the same box.

4. **Box restrictions can increase target stability, but precision gains trade against coverage and retained design space.** Examples include 8-client text `L-S` rising from 19.7% to 100% while retaining 15/117 test runs and 65.2% of target cases, and 10-client image `M-S` rising from 13.7% to 100% while retaining 15/117 and 93.8% of targets. For common 8-client image, the baseline is already 100% `M-M`; PRIM/CART restrictions retain half or one quarter of test rows but add no target-rate improvement. A no-gain result is still useful: it shows the extra restriction is unnecessary for the measured objective in that view.

5. **Some target regions are not discoverable in some slices.** When every common-environment run occupies one bin, PRIM/CART may return no non-empty box. That is a scope/support limit, not a failed run. Similarly, a high precision from a one-row rule or a target represented by one held-out case is weak evidence. Prefer rules that preserve a meaningful fraction of target cases and have enough retained rows to assess.

### Implications for software architects/designers

- Translate each box into two checks: **design prescription** (which policies the JSON relationships entail) and **operating envelope** (the delay, alpha, CPU, JSD, or instance ranges that co-occur with the target).
- For a faster-round target, test whether delay can be held at or below 12.5%; use the specific notebook rule to decide whether CS or another condition is also part of the observed envelope.
- For any rule, compare baseline target rate, in-box target rate, retained run count/fraction, and target coverage. Do not accept a 100% box rate without checking how many target cases it captures.
- Treat “no pattern policy required by the box conditions” literally: the fitted rule did not need a policy condition. It does not prove that pattern choices have no influence.

### Implications for researchers

- Present every box as a joint observational rule and include its architectural translation, test support, target prevalence, precision, coverage, gain, and retained-space fraction. This lets readers distinguish a useful operating envelope from a narrow high-precision pocket.
- Do not pool test rows across the common and all-environment views as if they were independent. Use the all-environment view for envelope discovery and the common view for a controlled descriptive comparison; neither identifies causal effects.
- Treat no-box outputs and low-support boxes as substantive evidence limits. Follow them with experiments that add support to the missing target region or independently vary the policy and uncertainty implicated by the box.

## Interpretation limits and reporting

These are observational compact-run analyses. Numeric client fields are averaged within runs, so client imbalance and round-level behavior are hidden. Grouped train/test splitting keeps `partition_seed` groups apart, but the held-out cases still come from the same campaign. PRIM/CART rules describe the sampled combinations of design and operating conditions and should guide follow-up experiments, not be stated as causal effects or deployment guarantees. Report exact box counts with percentages, especially for rare quadrants.

For the architect, the practical output is a shortlist of policy choices paired with conditions to monitor or constrain. For the researcher, it is a set of transparent, testable associations that identifies where the campaign has enough evidence, where it does not, and which additional crossed experiments would reduce ambiguity.

For per-slice evidence, see the [six notebook findings](fl_notebook_findings/README.md). The original notebooks are retained under [`federatedlearning/old-analysis`](../federatedlearning/old-analysis/README.md).
