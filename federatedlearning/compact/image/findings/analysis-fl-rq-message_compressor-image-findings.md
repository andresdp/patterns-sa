# Findings — ADEPT compact FL Message Compressor-only analysis: CIFAR-10/CNN 16k, all client counts

## Scope and data support

- **Task/configuration/client scope:** image classification (CIFAR-10 + CNN 16k); Message Compressor-only `OFF,ON,OFF`; all client counts (4, 8, 10); all sampled environments.
- **Rows:** 210 total; 147 train and 63 held out. The split is a grouped holdout by partition_seed (3/10 seeds), distribution-matched grouped stratification. Whole `partition_seed` groups remain together; target rates below are partition-specific.
- **Training regions (all nine, counts):** S-S: 0, S-M: 15, S-L: 0, M-S: 21, M-M: 111, M-L: 0, L-S: 0, L-M: 0, L-L: 0.
- **Held-out regions (all nine, counts):** S-S: 0, S-M: 7, S-L: 0, M-S: 9, M-M: 47, M-L: 0, L-S: 0, L-M: 0, L-L: 0.
- **RQ1 outcome allocation:** The shared outcome grid uses accuracy S/M/L (low/medium/high; maximize) and average total round time S/M/L (minimize); thus `L-S` is highest accuracy with fastest time and `S-L` lowest accuracy with slowest time. These symbols are value bins, not preference labels. The splits show the complete region support below; omitted areas are explicitly zero. Empty areas mean unobserved in this sampled slice, not infeasible. The all-configuration cases can compare complete configurations within one client count; one-pattern and baseline cases profile that single configuration over all client counts and do not estimate policy effects. The profile is Message Compressor-only `OFF,ON,OFF`; its train/test occupancy is shown in the split tables. There is no within-slice policy comparison. Pattern Types Active constant in the selected one-configuration slice.

## RQ1 — Tradeoffs and design relationships

The shared outcome grid uses accuracy S/M/L (low/medium/high; maximize) and average total round time S/M/L (minimize); thus `L-S` is highest accuracy with fastest time and `S-L` lowest accuracy with slowest time. These symbols are value bins, not preference labels. The splits show the complete region support below; omitted areas are explicitly zero. Empty areas mean unobserved in this sampled slice, not infeasible. The all-configuration cases can compare complete configurations within one client count; one-pattern and baseline cases profile that single configuration over all client counts and do not estimate policy effects. The profile is Message Compressor-only `OFF,ON,OFF`; its train/test occupancy is shown in the split tables. There is no within-slice policy comparison. Pattern Types Active constant in the selected one-configuration slice. Complete configuration and marginal pattern-count summaries are not interchangeable. Where the notebook reports pattern-stress groups, their denominators and normalized distributions are in Section 7; instance count mixes deployment configuration with run context and cannot be read as an assigned policy.

## RQ2 — Joint conditions and held-out what-if

Train feature scoring ranks (weighted): ['delay_percentage', 'Message Compressor Instances', 'Alpha Dirichlet Mean', 'non_iid_percentage', 'CPU Mean', 'low_spec_percentage']. These are model-relative predictive credits, not directions or effects. PRIM and CART boxes are conjunctions; the detailed report below lists the exact joint rule, specification context, discovery support, and held-out policy-specific matrices. Repeated target labels below correspond to distinct PRIM and CART rules in the order shown in the linked report.

- **S-M (S,M):** - `Message Compressor Instances`: [6.000, 10.000] - `non_iid_percentage`: [50.000, 75.000] - **Includes NaN / not-selected values:** No. Discovery: 14 target rows in 14 retained, from 15 target rows / 147 train rows. Held out: unrestricted target rate 7/63; retained 6/63 (9.5%); target-in-box 6; precision 1, coverage 0.8571, absolute lift 0.8889 (+88.89 pp).
- **M-S (M,S):** - `Alpha Dirichlet Mean`: [0.750, 0.900] - `delay_percentage`: [0.000, 12.500] - **Includes NaN / not-selected values:** No. Discovery: 21 target rows in 21 retained, from 21 target rows / 147 train rows. Held out: unrestricted target rate 9/63; retained 9/63 (14.3%); target-in-box 9; precision 1, coverage 1, absolute lift 0.8571 (+85.71 pp).
- **M-M (M,M):** - `Alpha Dirichlet Mean`: [0.750, 0.900] - `delay_percentage`: [12.500, 100.000] - **Includes NaN / not-selected values:** No. Discovery: 105 target rows in 105 retained, from 111 target rows / 147 train rows. Held out: unrestricted target rate 47/63; retained 45/63 (71.4%); target-in-box 45; precision 1, coverage 0.9574, absolute lift 0.2540 (+25.40 pp).
- **M-M (M,M):** - `delay_percentage`: [12.485, 100.000] - `Alpha Dirichlet Mean`: [0.750, 0.900] - **Includes NaN / not-selected values:** No. Discovery: 105 target rows in 105 retained, from 111 target rows / 147 train rows. Held out: unrestricted target rate 47/63; retained 45/63 (71.4%); target-in-box 45; precision 1, coverage 0.9574, absolute lift 0.2540 (+25.40 pp).
- **M-S (M,S):** - `delay_percentage`: [0.000, 12.485] - **Includes NaN / not-selected values:** No. Discovery: 21 target rows in 21 retained, from 21 target rows / 147 train rows. Held out: unrestricted target rate 9/63; retained 9/63 (14.3%); target-in-box 9; precision 1, coverage 1, absolute lift 0.8571 (+85.71 pp).
- **S-M (S,M):** - `delay_percentage`: [12.485, 100.000] - `Alpha Dirichlet Mean`: [0.600, 0.750] - `Message Compressor Instances`: [5.999, 10.000] - **Includes NaN / not-selected values:** No. Discovery: 14 target rows in 14 retained, from 15 target rows / 147 train rows. Held out: unrestricted target rate 7/63; retained 6/63 (9.5%); target-in-box 6; precision 1, coverage 0.8571, absolute lift 0.8889 (+88.89 pp).

Targets populated in training but absent from both reported box sets (no discovery box): none. Targets with zero held-out target rows remain unevaluable on test even when a box was discovered.

For each box, the unrestricted test prevalence is `target runs before box / test runs`; precision is target rows among retained runs; coverage is target rows retained divided by target rows in test; absolute lift is precision minus test prevalence and is shown in both proportion and percentage points. No reported `not available` value should be read as zero. A target with 0 held-out target rows has no test-evaluable recall even if the rule retains non-target rows. The full Section 11 policy-specific before/boxed/gain and target-coverage matrices are preserved in the notebook output. RQ2 all-target support and exact rule conditions: [box report](../boxes/boxes__task-image__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.md); scoring, PRIM/CART and what-if outputs: [notebook Sections 8–12](../analysis-fl-rq-message_compressor-image.ipynb#research-question-2).

## Implications

- **Practitioners:** Treat any high-precision rule as a candidate operating envelope for this image task and stated client/configuration scope. Validate it with additional partition seeds before deployment; do not use the box as evidence of an intervention effect.
- **Researchers:** The ten-seed grouped holdout and sparse target counts limit stability claims. The compact run-level client averages can hide client imbalance and round variation. Pattern activation/context allocation is observational, with uneven environment coverage; pattern-stress instance assumptions require the campaign README caveats.

## Limitations and evidence

# ADEPT compact FL Message Compressor-only analysis: CIFAR-10/CNN 16k, all client counts reports only the selected scope; results do not transfer automatically across client counts or single-pattern profiles. Shared bins mean empty regions are sample gaps.

- Notebook: [analysis-fl-rq-message_compressor-image.ipynb](../analysis-fl-rq-message_compressor-image.ipynb) (split cell 18; RQ1 Sections 4–7; RQ2 Sections 8–12).
- Box report: [boxes__task-image__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.md](../boxes/boxes__task-image__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.md).
- Objective space: [quality-space plot](../plots/quality-space__task-image__message_compressor-only_OFF_ON_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png).
- Feature ranking: [feature-importance plot](../plots/feature-importance__task-image__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.png).
- Shared definitions and scope: [compact campaign README](../../README.md).
