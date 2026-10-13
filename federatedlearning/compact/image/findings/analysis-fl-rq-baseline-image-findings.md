# Findings — ADEPT compact FL baseline analysis: CIFAR-10/CNN 16k, all client counts

## Scope and data support

- **Task/configuration/client scope:** image classification (CIFAR-10 + CNN 16k); baseline `OFF,OFF,OFF`; all client counts (4, 8, 10); all sampled environments.
- **Rows:** 180 total; 126 train and 54 held out. The split is a grouped holdout by partition_seed (3/10 seeds), distribution-matched grouped stratification. Whole `partition_seed` groups remain together; target rates below are partition-specific.
- **Training regions (all nine, counts):** S-S: 0, S-M: 31, S-L: 0, M-S: 21, M-M: 74, M-L: 0, L-S: 0, L-M: 0, L-L: 0.
- **Held-out regions (all nine, counts):** S-S: 0, S-M: 13, S-L: 0, M-S: 9, M-M: 32, M-L: 0, L-S: 0, L-M: 0, L-L: 0.
- **RQ1 outcome allocation:** The shared outcome grid uses accuracy S/M/L (low/medium/high; maximize) and average total round time S/M/L (minimize); thus `L-S` is highest accuracy with fastest time and `S-L` lowest accuracy with slowest time. These symbols are value bins, not preference labels. The splits show the complete region support below; omitted areas are explicitly zero. Empty areas mean unobserved in this sampled slice, not infeasible. The all-configuration cases can compare complete configurations within one client count; one-pattern and baseline cases profile that single configuration over all client counts and do not estimate policy effects. The profile is baseline `OFF,OFF,OFF`; its train/test occupancy is shown in the split tables. There is no within-slice policy comparison. Pattern Types Active=0 and Pattern Instances constant; no stress contrast exists.

## RQ1 — Tradeoffs and design relationships

The shared outcome grid uses accuracy S/M/L (low/medium/high; maximize) and average total round time S/M/L (minimize); thus `L-S` is highest accuracy with fastest time and `S-L` lowest accuracy with slowest time. These symbols are value bins, not preference labels. The splits show the complete region support below; omitted areas are explicitly zero. Empty areas mean unobserved in this sampled slice, not infeasible. The all-configuration cases can compare complete configurations within one client count; one-pattern and baseline cases profile that single configuration over all client counts and do not estimate policy effects. The profile is baseline `OFF,OFF,OFF`; its train/test occupancy is shown in the split tables. There is no within-slice policy comparison. Pattern Types Active=0 and Pattern Instances constant; no stress contrast exists. Complete configuration and marginal pattern-count summaries are not interchangeable. Where the notebook reports pattern-stress groups, their denominators and normalized distributions are in Section 7; instance count mixes deployment configuration with run context and cannot be read as an assigned policy.

## RQ2 — Joint conditions and held-out what-if

Train feature scoring ranks (weighted): ['delay_percentage', 'Alpha Dirichlet Mean', 'Total Clients', 'CPU Mean']. These are model-relative predictive credits, not directions or effects. PRIM and CART boxes are conjunctions; the detailed report below lists the exact joint rule, specification context, discovery support, and held-out policy-specific matrices. Repeated target labels below correspond to distinct PRIM and CART rules in the order shown in the linked report.

- **S-M (S,M):** - `Total Clients`: [6.000, 10.000] - `Alpha Dirichlet Mean`: [0.600, 0.750] - **Includes NaN / not-selected values:** No. Discovery: 28 target rows in 28 retained, from 31 target rows / 126 train rows. Held out: unrestricted target rate 13/54; retained 12/54 (22.2%); target-in-box 12; precision 1, coverage 0.9231, absolute lift 0.7593 (+75.93 pp).
- **M-S (M,S):** - `delay_percentage`: [0.000, 12.500] - **Includes NaN / not-selected values:** No. Discovery: 21 target rows in 21 retained, from 21 target rows / 126 train rows. Held out: unrestricted target rate 9/54; retained 9/54 (16.7%); target-in-box 9; precision 1, coverage 1, absolute lift 0.8333 (+83.33 pp).
- **M-M (M,M):** - `Alpha Dirichlet Mean`: [0.750, 0.900] - `delay_percentage`: [12.500, 100.000] - **Includes NaN / not-selected values:** No. Discovery: 63 target rows in 63 retained, from 74 target rows / 126 train rows. Held out: unrestricted target rate 32/54; retained 27/54 (50.0%); target-in-box 27; precision 1, coverage 0.8438, absolute lift 0.4074 (+40.74 pp).
- **M-M (M,M):** - `Alpha Dirichlet Mean`: [0.750, 0.900] - `delay_percentage`: [12.488, 100.000] - **Includes NaN / not-selected values:** No. Discovery: 63 target rows in 63 retained, from 74 target rows / 126 train rows. Held out: unrestricted target rate 32/54; retained 27/54 (50.0%); target-in-box 27; precision 1, coverage 0.8438, absolute lift 0.4074 (+40.74 pp).
- **S-M (S,M):** - `Alpha Dirichlet Mean`: [0.600, 0.750] - `Total Clients`: [5.999, 10.000] - `delay_percentage`: [12.488, 100.000] - **Includes NaN / not-selected values:** No. Discovery: 28 target rows in 28 retained, from 31 target rows / 126 train rows. Held out: unrestricted target rate 13/54; retained 12/54 (22.2%); target-in-box 12; precision 1, coverage 0.9231, absolute lift 0.7593 (+75.93 pp).
- **M-S (M,S):** - `delay_percentage`: [0.000, 12.488] - **Includes NaN / not-selected values:** No. Discovery: 21 target rows in 21 retained, from 21 target rows / 126 train rows. Held out: unrestricted target rate 9/54; retained 9/54 (16.7%); target-in-box 9; precision 1, coverage 1, absolute lift 0.8333 (+83.33 pp).

Targets populated in training but absent from both reported box sets (no discovery box): none. Targets with zero held-out target rows remain unevaluable on test even when a box was discovered.

For each box, the unrestricted test prevalence is `target runs before box / test runs`; precision is target rows among retained runs; coverage is target rows retained divided by target rows in test; absolute lift is precision minus test prevalence and is shown in both proportion and percentage points. No reported `not available` value should be read as zero. A target with 0 held-out target rows has no test-evaluable recall even if the rule retains non-target rows. The full Section 11 policy-specific before/boxed/gain and target-coverage matrices are preserved in the notebook output. RQ2 all-target support and exact rule conditions: [box report](../boxes/boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md); scoring, PRIM/CART and what-if outputs: [notebook Sections 8–12](../analysis-fl-rq-baseline-image.ipynb#research-question-2).

## Implications

- **Practitioners:** Treat any high-precision rule as a candidate operating envelope for this image task and stated client/configuration scope. Validate it with additional partition seeds before deployment; do not use the box as evidence of an intervention effect.
- **Researchers:** The ten-seed grouped holdout and sparse target counts limit stability claims. The compact run-level client averages can hide client imbalance and round variation. Pattern activation/context allocation is observational, with uneven environment coverage; pattern-stress instance assumptions require the campaign README caveats.

## Limitations and evidence

# ADEPT compact FL baseline analysis: CIFAR-10/CNN 16k, all client counts reports only the selected scope; results do not transfer automatically across client counts or single-pattern profiles. Shared bins mean empty regions are sample gaps.

- Notebook: [analysis-fl-rq-baseline-image.ipynb](../analysis-fl-rq-baseline-image.ipynb) (split cell 18; RQ1 Sections 4–7; RQ2 Sections 8–12).
- Box report: [boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md](../boxes/boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md).
- Objective space: [quality-space plot](../plots/quality-space__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png).
- Feature ranking: [feature-importance plot](../plots/feature-importance__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.png).
- Shared definitions and scope: [compact campaign README](../../README.md).
