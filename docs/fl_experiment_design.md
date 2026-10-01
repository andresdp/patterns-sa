# FL Experiment Design: Extending the AP4FED Dataset for ADEPT

**Status:** Draft design (2026-09-29), to be run with AP4FED (Compagnucci, Pinciroli, Trubiani, JSS 232, 2026)
**Serves:** [paper_jss_extension_plan.md](paper_jss_extension_plan.md), §4.3 (hypotheses H1-H5) and RQ2-RQ4
**Current data:** `federatedlearning/FLwithAP_MLdata_split.csv`, analyzed in `federatedlearning/analysis-fl.ipynb`

## 1. Why New Data Is Needed

| Property | Current dataset | Needed for the paper |
|:---|:---|:---|
| Runs | 32 | ~300-400 (enough runs per tradeoff region in a 70/30 split) |
| Decision combinations | 4 of 8 (baseline and each pattern alone) | all 8 (pattern interactions, H5) |
| Models | `CNN 16k`, `squeezenet1_1` | same |
| Client environment | **constant**: 5 clients, CPUs {3,3,3,3,1}, RAM 2 GB, 2 of 5 clients non-IID, α ∈ {0.5, 1} | **varied**: number of clients, resource spread, data heterogeneity |
| Pattern settings | one fixed value per pattern | the client selector threshold varies (a numeric constraint within the ON policy) |
| Replication | 5 runs per cell (2 for `squeezenet1_1` + HDH), no seed/repetition column | explicit repetition and seed columns |

With a constant environment, ADEPT can only produce prescriptive boxes (conditions on decisions). Varying the environment makes operating-envelope and conditional boxes possible, which is the paper's main claim (plan §2.1).

### Response variables: model accuracy × total round time

The campaign targets one tradeoff, the classic one in FL (plan §4.1):

| Role | Metric | Column | Direction |
|:---|:---|:---|:---|
| **Primary** | Model accuracy after the last round | `Final Val Accuracy` | maximize |
| **Primary** | Total round time (training + communication, per round; × `N Rounds` = total wall-clock time) | `Avg Total Round Time` | minimize |
| Explanatory | Round-time components | `Avg Training Time`, `Avg Communication Time` | — |
| Robustness check | F1 (last round and best) | `Final Val F1 (Last Round)`, `Final Val F1 (Best)` | — |
| **Needed if missing** | Accuracy at the 25/50/75% checkpoints (today only F1 is logged there) | suggested: `Val Accuracy 25%`, `Val Accuracy 50%`, `Val Accuracy 75%` | — |

The checkpoint accuracies allow a *time-to-accuracy* view (an open question in plan §9). Runs that crash or time out must still produce a row, with the missing metrics left empty: ADEPT labels them `FAILURE` (formal doc §3.6).

The factors below are chosen because each is expected to move configurations along one or both axes of this plane (§4).

## 2. Factors and Levels

All factors map onto AP4FED configuration parameters (AP4FED paper, Table 1).

### Decisions (architectural patterns)

| Factor | AP4FED setting | Levels |
|:---|:---|:---|
| D1 Client selector | `client_selector.enabled` (`selection_strategy`: Resource-based, `selection_criteria`: CPU) | OFF, ON |
| D2 Message compressor | `message_compressor.enabled` | OFF, ON |
| D3 Heterogeneous data handler | `heterogeneous_data_handler.enabled` | OFF, ON |
| P1 Selector threshold (only when D1 = ON) | `criteria_value` | ">1", ">2" (recorded numerically as 1, 2; §5) |

D1 × D2 × D3 is run **full factorial** (8 combinations). P1 varies a numeric constraint within the ON policy, as in the base paper's sweeps.

### Levers (fixed per model family)

| Factor | Levels | Notes |
|:---|:---|:---|
| L1 Model | `CNN 16k`, `squeezenet1_1` | budget tiers below |
| `num_Rounds` | 10 | fixed, comparable with current data |
| Dataset, optimizer, learning rate, batch size, epochs | CIFAR-10, Adam, 0.001, 64, 1 | fixed, as in current data |

### Uncertainties (client environment)

| Factor | AP4FED setting | Levels | Targets hypothesis |
|:---|:---|:---|:---|
| U1 Number of clients | `nC` | 4, 6, 8 | H3, H4 |
| U2 Share of low-resource clients | per-client `n_CPU` = 1 (others 2 or 3) | 0%, 25%, 50% | H1, H4 |
| U3 RAM per client | per-client `RAM` | 1, 2, 4 GB | H4 |
| U4 Share of non-IID clients | per-client `data_Distribution` | 0%, 25%, 50%, 75% | H2, H5 |
| U5 Heterogeneity of non-IID clients | Dirichlet α | 0.1, 0.5, 1.0 (lower = more skewed) | H2 |

**Host constraint:** AP4FED runs clients as containers on one host, and the AP4FED authors cap allocated cores at the host's capacity to avoid overcommitment. Every environment point must satisfy Σ `n_CPU` ≤ available cores (10 in the AP4FED paper's workstation). Points violating it are resampled. The current data allocates 13 CPUs, so check the host that produced it.

## 3. Sampling Plan

1. **Environment points.** Draw a Latin hypercube over U1-U5 (maximin), discretized to the levels above, rejecting points that violate the host constraint. Each environment point fixes the concrete per-client assignment (which clients are 1-CPU, which are non-IID, and their α).
2. **Crossed design.** Run every decision combination (8, plus the P1 variants for D1 = ON) on the **same** environment points, so pattern effects are compared under identical conditions (paired design).
3. **Replication.** Repeat each (decision combination, model, environment point) with different seeds, and record the seed. Replicates quantify the noise floor ADEPT cannot explain (RQ4).

### Budget tiers

Run time per run ≈ 10 rounds × average round time. Current data: `CNN 16k` 35-46 s per round (≈ 6-8 min per run); `squeezenet1_1` 266-513 s per round (≈ 45-85 min per run).

| Tier | Model | Environment points | Decision cells (D1×D2×D3, +P1) | Replicates | Runs | Sequential time |
|:---|:---|---:|---:|---:|---:|---:|
| **1 (minimum)** | `CNN 16k` | 12 | 12 (8 + 4 extra P1 variants) | 3 | 432 | ≈ 50 h |
| **2 (recommended add-on)** | `squeezenet1_1` | 6 | 8 | 2 | 96 | ≈ 100 h |
| 3 (optional) | `squeezenet1_1` | 12 | 12 | 3 | 432 | ≈ 450 h |

Tier 1 alone supports RQ2 and RQ4 for one model. Tier 2 keeps the model factor (RQ3) at a manageable cost. Runs can execute in parallel only as far as the host constraint allows.

### Support for the ablation studies (plan §4.4)

The ablations analyze subsets of the campaign, so they add requirements on how the runs are distributed rather than on the factors:

| Requirement | Serves | How the design meets it |
|:---|:---|:---|
| The baseline (`OFF,OFF,OFF`) is run at **every** environment point, for **each** model | A2-normalize (outcomes relative to the baseline of the same model and environment point); A1-vs-baseline | Full factorial over D1×D2×D3 at every point (§3, step 2) |
| **Tier 2 environment points are a subset of Tier 1's** | Comparing models at identical environments (A2-fix, A2-normalize) | Draw the 6 `squeezenet1_1` points from the 12 `CNN 16k` points (e.g. every other point of the maximin ordering), not as a new sample |
| Enough runs per **single-pattern slice** | A1-alone, A1-vs-baseline | Tier 1 gives 36 runs per single-pattern cell (72 for the selector, with two thresholds), i.e. about 25 training runs per slice: enough for Phase 3 densities, marginal for PRIM. **Recommended add-on (Tier 1+):** 2 extra replicates for the 5 cells baseline, selector `>1`, selector `>2`, compressor-only, HDH-only: 5 × 12 × 2 = **120 runs ≈ 14 h** (`CNN 16k`), giving 60 runs per cell. |
| Per-model slices large enough | A2-fix | Tier 1: 432 `CNN 16k` runs; Tier 2: 96 `squeezenet1_1` runs (A2-fix on `squeezenet1_1` supports prescriptive boxes, not fine envelopes) |

Single-pattern ablations on `squeezenet1_1` need Tier 3: in Tier 2 a single-pattern slice has only 12 runs.

## 4. Hypotheses and the Analyses That Test Them

| ID | Hypothesis | Factors | Expected ADEPT output |
|:---|:---|:---|:---|
| H1 | The client selector's accuracy gain grows with the share of low-resource clients, and vanishes when all clients are capable. | D1, P1, U2 | conditional box: D1 = ON ∧ U2 ≥ x → high-accuracy region |
| H2 | HDH improves accuracy only under high heterogeneity (low α, many non-IID clients); otherwise it only costs training time. | D3, U4, U5 | conditional box on D3, U4, U5 |
| H3 | The message compressor pays off only when communication is a significant share of the round (more clients, larger model). | D2, U1, L1 | conditional box on D2, U1 |
| H4 | For a fixed configuration, round time stays in the fast tier while the number of clients and the resource spread stay within bounds. | U1-U3 | operating-envelope box per configuration |
| H5 | Selector and HDH interact: excluding weak non-IID clients removes the data HDH would repair. | D1 × D3, U4 | boxes on combinations; configuration-level robustness (`by='configuration'`); A1 transfer check (an A1-alone box loses density when the pattern is composed) |
| A1 | Each pattern alone has an operating envelope over the environment (the base paper's setting, per FL pattern). | one of D1-D3, P1, U1-U5 | envelope boxes per single-pattern slice |
| A2 | Once the model is fixed or normalized away, pattern and environment factors pass the standard key-parameter threshold. | D1-D3, U1-U5, L1 | key-parameter sets per model (A2-fix) and on relative outcomes (A2-normalize) |

## 5. Output Schema (compatible with `FLsystem_split.json`)

Keep the current CSV layout so the existing specification, aggregation and notebook apply:

- **One row per run** (not averaged over repetitions).
- **Decision columns:** `client_selector_pattern`, `message_compressor_pattern`, `hdh_pattern` (ON/OFF) and `config_id` (`<selector>,<compressor>,<hdh>`).
- **Pattern settings:** as now (`Client Selector Strategy/Criteria/Value`, `Message Compressor Alg`, `HDH ...`), empty when the pattern is OFF. `Client Selector Value` carries P1 and must stay **numeric** (`1`, `2`), as in the current data (2.0), not strings such as `">2"`. Strings are encoded in alphabetical order, which would put `">10"` before `">2"` and break the threshold's order in the boxes (formal doc §4.1; alternatively, declare the order in the spec, TODO T4). The same applies to any other ordered setting (RAM, CPUs).
- **Per-client columns:** `Client <N> <field>` for N = 1..nC (fields `ID`, `CPU`, `RAM`, `Data Distribution`, `Data Persistence`, `Alpha Dirichlet`, `JSD`, `CPU Usage Avg`, `RAM Usage Avg`). Columns of clients beyond nC stay empty; the declared aggregation skips them.
- **New columns:** `Run ID`, `Environment Point`, `Repetition`, `Seed`, and optionally `Host Cores`.
- **Run-level settings and metrics:** unchanged (`N Rounds`, `Total Clients`, `Model`, ..., accuracy/F1, round/training/communication times, 25/50/75% checkpoints, adding accuracy at the checkpoints; see §1).

Keep clients that the selector excludes in the CSV with empty usage columns, as in the current data: this is how their exclusion becomes observable.

## 6. ADEPT Preparation for the New Data

| Task | Where | Status |
|:---|:---|:---|
| Declare all 8 configurations in `configuration_identification` (the linter's coverage warning should then disappear) | `FLsystem_split.json` (or a new `FLsystem_env.json`) | To do |
| Move `Total Clients` from lever to uncertainty | spec | To do |
| Declare spread statistics as uncertainties: `CPU Min`, `CPU Std`, `RAM Min`, `Alpha Dirichlet Min` | spec `aggregations` (`numeric: ["mean", "std", "min"]`) | Supported |
| Share of non-IID clients (and of 1-CPU clients) | new categorical statistic in `adept/utils/aggregation.py`, e.g. `share:non-IID` | To do |
| Give `Client Selector Value` `bounds` (it now varies within ON), as a numeric parameter | spec | To do |
| Declared category order for any ordered setting delivered as strings (formal doc T4) | `Parameter` model, `FeatureEncoder` | To do (only if the data keeps strings) |
| Declare `Repetition`/`Seed` as non-analyzed columns; noise-floor analysis per cell | notebook | To do |
| Stratified analyses (per model, per decision) next to pooled ones | `discover_scenarios` option (plan §6.2) + notebook | To do |
| Slices with pooled tradeoff labels (A1, A2-fix) | today: row filter in the `preprocessor` + `create_tradeoffs(ranges=...)`; later a `restrict` option | Workaround available |
| Relative outcomes: accuracy gain and time ratio over the baseline of the same model and `Environment Point`, averaged over its replicates (A2-normalize) | `preprocessor` (derived columns declared as objectives) | To do |

## 7. Acceptance Checks on Delivered Data

- All 8 decision combinations present for each model tier, on the same environment points.
- The linter reports no coverage warning and no low-variance warnings on U1-U5 aggregates.
- Every row has a `Seed`, `Repetition` and `Environment Point`; replicates of one cell differ only in `Seed`.
- Every (`Model`, `Environment Point`) has at least one baseline run, and the `squeezenet1_1` environment points are a subset of the `CNN 16k` ones.
- For every run with D1 = ON, clients below the threshold record no usage.
- Σ `n_CPU` ≤ host cores for every environment point (or `Host Cores` recorded for runs that exceed it).
