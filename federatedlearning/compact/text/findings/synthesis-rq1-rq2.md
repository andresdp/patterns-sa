# Text compact FL findings synthesis

This synthesis covers the 13 currently selected executed notebooks, as defined by [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md). It was derived from their current notebook outputs, matched box reports, and plots. The cases are related scope views, not a disjoint partition of the source dataset; do not add their row counts to estimate campaign totals.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

All cases use the shared accuracy × average total round-time S/M/L grid. In the combined-pattern stress family, the objective-space plots place observed runs primarily in lower/middle accuracy bins and lower/middle time bins; regions outside the observed cloud remain unobserved in that sampled slice. At 50% stress, the inspected image plot shows points in S-M, M-S, and M-M, with no sampled points in L accuracy or L time regions. The six stress leaves compare supported complete configurations at common stress, pooling client counts. The triple-pattern configuration is present only at 25%; the 50% and 75% scopes have six alternatives. Therefore differences across these leaves are not randomized pattern-dose estimates, and the client-count mix is pooled.

Stress-only leaves hold two pattern decisions OFF and vary only the named pattern stress setting, pooling clients. Profile leaves fix a single complete configuration and characterize its objective space; they cannot directly compare that policy against another profile. The client-count leaves retain all eight complete configurations within a fixed count. Pattern-instance and active-pattern-type counts are marginal descriptors and should not be treated as complete policy assignments. Across every family, environment conditions remain sampled and can co-vary with policy allocations.

The executed notebooks give these row supports (training/held-out counts are specific to each grouped partition):

- `analysis-fl-rq-baseline-text`: 180 total (126 train, 54 held out).
- `analysis-fl-rq-c10-text`: 390 total (273 train, 117 held out).
- `analysis-fl-rq-c4-text`: 390 total (273 train, 117 held out).
- `analysis-fl-rq-c8-text`: 390 total (273 train, 117 held out).
- `analysis-fl-rq-client_selector-text`: 150 total (105 train, 45 held out).
- `analysis-fl-rq-combined-patterns-stress-25-text`: 210 total (147 train, 63 held out).
- `analysis-fl-rq-combined-patterns-stress-50-text`: 180 total (126 train, 54 held out).
- `analysis-fl-rq-combined-patterns-stress-75-text`: 360 total (252 train, 108 held out).
- `analysis-fl-rq-hdh-text`: 150 total (105 train, 45 held out).
- `analysis-fl-rq-message_compressor-text`: 210 total (147 train, 63 held out).
- `analysis-fl-rq-stress-only-client_selector-text`: 150 total (105 train, 45 held out).
- `analysis-fl-rq-stress-only-hdh-text`: 150 total (105 train, 45 held out).
- `analysis-fl-rq-stress-only-message_compressor-text`: 210 total (147 train, 63 held out).

Current objective plots cluster at high accuracy, with both middle-time and fast-time observations. The combined 25%/50%/75% plots retain a dense high-accuracy/middle-time cloud and sparse faster runs. Use each notebook table for exact counts.

No between-case aggregation is warranted because the strata overlap in the original run population (for example, configuration profiles overlap with stress-only leaves and client-count views). The exact per-partition region counts and allocation tables are linked in each case report below.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

PRIM/CART feature rankings, rule conditions, and box metrics vary by task and scope; they are not transferable rules across cases. The six replacement combined-pattern cases specifically include client count as a varying predictor/context and exclude parsed stress features fixed or aliased within the selected stress. Elsewhere, the notebook's feature selection may remove fixed, constant, or exact-alias features. Read the listed feature set and box condition together, using the paired report's design prescription and operating envelope.

A box that concentrates a target in held-out runs still represents a restriction over already observed test rows. Assess precision together with unrestricted test prevalence, target coverage, and retained support. Sparse or absent held-out targets make evaluation weak or unavailable even when discovery found a rule. Policy-specific before/boxed/gain matrices are conditional summaries; a zero may mean no support or no retained runs, and `None` means no discovery box. The complete per-case held-out and policy matrices are in the current notebooks and their case reports.

## Scope-specific implications

**Practitioners:** use only a box with adequate held-out retained runs and target coverage as a candidate for further controlled evaluation. Keep policy choices distinct from context and run-level observed descriptors. The current evidence describes task-specific operating envelopes, not guarantees.

**Researchers:** report the evidence at each guide-defined scope, preserve grouped seed holdout, and avoid treating overlapping views, marginal pattern counts, or pooled client counts as independent controlled contrasts. Extend validation across seeds and client-level/round-level data before claiming transfer.

## Case coverage

- [analysis-fl-rq-baseline-text-findings.md](analysis-fl-rq-baseline-text-findings.md): Baseline profile (OFF,OFF,OFF); clients 4/8/10 pooled; all environments.
- [analysis-fl-rq-c10-text-findings.md](analysis-fl-rq-c10-text-findings.md): All eight configurations; 10 clients; all environments.
- [analysis-fl-rq-c4-text-findings.md](analysis-fl-rq-c4-text-findings.md): All eight configurations; 4 clients; all environments.
- [analysis-fl-rq-c8-text-findings.md](analysis-fl-rq-c8-text-findings.md): All eight configurations; 8 clients; all environments.
- [analysis-fl-rq-client_selector-text-findings.md](analysis-fl-rq-client_selector-text-findings.md): Client Selector profile (ON,OFF,OFF); clients 4/8/10 pooled; all environments.
- [analysis-fl-rq-combined-patterns-stress-25-text-findings.md](analysis-fl-rq-combined-patterns-stress-25-text-findings.md): All supported non-empty pattern configurations at common 25% stress; clients 4/8/10 pooled; all environments; baseline excluded.
- [analysis-fl-rq-combined-patterns-stress-50-text-findings.md](analysis-fl-rq-combined-patterns-stress-50-text-findings.md): All supported non-empty pattern configurations at common 50% stress; clients 4/8/10 pooled; all environments; baseline excluded.
- [analysis-fl-rq-combined-patterns-stress-75-text-findings.md](analysis-fl-rq-combined-patterns-stress-75-text-findings.md): All supported non-empty pattern configurations at common 75% stress; clients 4/8/10 pooled; all environments; baseline excluded.
- [analysis-fl-rq-hdh-text-findings.md](analysis-fl-rq-hdh-text-findings.md): HDH profile (OFF,OFF,ON); clients 4/8/10 pooled; all environments.
- [analysis-fl-rq-message_compressor-text-findings.md](analysis-fl-rq-message_compressor-text-findings.md): Message Compressor profile (OFF,ON,OFF); clients 4/8/10 pooled; all environments.
- [analysis-fl-rq-stress-only-client_selector-text-findings.md](analysis-fl-rq-stress-only-client_selector-text-findings.md): Exactly client selector ON and the other two patterns OFF; stress levels 25/50/75%; clients pooled; all environments.
- [analysis-fl-rq-stress-only-hdh-text-findings.md](analysis-fl-rq-stress-only-hdh-text-findings.md): Exactly hdh ON and the other two patterns OFF; stress levels 25/50/75%; clients pooled; all environments.
- [analysis-fl-rq-stress-only-message_compressor-text-findings.md](analysis-fl-rq-stress-only-message_compressor-text-findings.md): Exactly message compressor ON and the other two patterns OFF; stress levels 0/25/50/75/100%; clients pooled; all environments.

## Evidence and limits

All 26 task-local saved plots (two per notebook) and all matched box reports are recorded in the refreshed evidence manifest. Each case report links its notebook outputs, matching report, and plots. Existing historical findings were not used as evidence. Findings are observational and constrained to the current compact campaign's sampled conditions and shared discretization.
