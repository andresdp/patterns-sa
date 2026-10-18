# Compact notebook stratification and scope

This guide maps each maintained notebook to the subset of the compact campaign it analyzes and explains why that slice exists. It currently covers **26 notebooks: 13 image and 13 text**. A **leaf is one notebook**. Each leaf applies its task, configuration, client-count, pattern-stress, and environment filters before computing outcomes, ranking features, discovering PRIM/CART boxes, and evaluating those boxes. All maintained notebooks use the all-environment view.

The three former broad-scope text stress notebooks have been retired so the two task sets have
matching experiment families. Their existing findings and generated reports remain historical
artifacts and are outside this maintained tree.

## Notebook tree

```text
Compact campaign (all available environment settings)
├── Image task: Dataset=CIFAR-10, Model=CNN 16k
│   ├── All configurations, one client-count stratum
│   │   ├── Total Clients=4  → image/analysis-fl-rq-c4-image.ipynb
│   │   ├── Total Clients=8  → image/analysis-fl-rq-c8-image.ipynb
│   │   └── Total Clients=10 → image/analysis-fl-rq-c10-image.ipynb
│   ├── Isolated pattern stress: exactly one pattern ON; client counts pooled
│   │   ├── Client Selector (25%, 50%, 75%) → image/analysis-fl-rq-stress-only-client_selector-image.ipynb
│   │   ├── HDH (25%, 50%, 75%) → image/analysis-fl-rq-stress-only-hdh-image.ipynb
│   │   └── Message Compressor (0%, 25%, 50%, 75%, 100%) → image/analysis-fl-rq-stress-only-message_compressor-image.ipynb
│   ├── Combined patterns at shared stress; clients pooled (4, 8, 10)
│   │   ├── 25%: all seven combinations, including three-pattern → image/analysis-fl-rq-combined-patterns-stress-25-image.ipynb
│   │   ├── 50%: three single- and three two-pattern combinations → image/analysis-fl-rq-combined-patterns-stress-50-image.ipynb
│   │   └── 75%: three single- and three two-pattern combinations → image/analysis-fl-rq-combined-patterns-stress-75-image.ipynb
│   └── One configuration, pooling client counts 4, 8, and 10
│       ├── No patterns ON       → image/analysis-fl-rq-baseline-image.ipynb
│       ├── Client Selector only → image/analysis-fl-rq-client_selector-image.ipynb
│       ├── Message Compressor only
│       │                       → image/analysis-fl-rq-message_compressor-image.ipynb
│       └── HDH only             → image/analysis-fl-rq-hdh-image.ipynb
└── Text task: Dataset=AG_NEWS, Model=MLP
    ├── All configurations, one client-count stratum
    │   ├── Total Clients=4  → text/analysis-fl-rq-c4-text.ipynb
    │   ├── Total Clients=8  → text/analysis-fl-rq-c8-text.ipynb
    │   └── Total Clients=10 → text/analysis-fl-rq-c10-text.ipynb
    ├── Isolated pattern stress: exactly one pattern ON; client counts pooled
    │   ├── Client Selector (25%, 50%, 75%) → text/analysis-fl-rq-stress-only-client_selector-text.ipynb
    │   ├── HDH (25%, 50%, 75%) → text/analysis-fl-rq-stress-only-hdh-text.ipynb
    │   └── Message Compressor (0%, 25%, 50%, 75%, 100%) → text/analysis-fl-rq-stress-only-message_compressor-text.ipynb
    ├── Combined patterns at shared stress; clients pooled (4, 8, 10)
    │   ├── 25%: all seven combinations, including three-pattern → text/analysis-fl-rq-combined-patterns-stress-25-text.ipynb
    │   ├── 50%: three single- and three two-pattern combinations → text/analysis-fl-rq-combined-patterns-stress-50-text.ipynb
    │   └── 75%: three single- and three two-pattern combinations → text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb
    └── One configuration, pooling client counts 4, 8, and 10
        ├── No patterns ON       → text/analysis-fl-rq-baseline-text.ipynb
        ├── Client Selector only → text/analysis-fl-rq-client_selector-text.ipynb
        ├── Message Compressor only
        │                       → text/analysis-fl-rq-message_compressor-text.ipynb
        └── HDH only             → text/analysis-fl-rq-hdh-text.ipynb
```

The six **all-configuration** leaves retain all eight pattern ON/OFF configurations for the selected task and client count. They support within-client-count comparisons across complete configurations. Both tasks have three **stress-only** analysis views requiring exactly one named pattern ON and both other patterns OFF; they pool all client counts and compare the available stress levels without mixing co-activation. Their colors encode increasing stress severity: green/orange/red for Client Selector and HDH, and light-green/green/orange/red/dark-red for Message Compressor (shown in a horizontal legend row). Both tasks also have three **combined-pattern stress leaves**. Each fixes task and requires every enabled pattern to have the selected common stress level, while pooling clients 4, 8, and 10. The support table lists all seven possible non-empty combinations and marks combinations without matching campaign rows as unavailable. The three-pattern combination is supported at 25%, but not at 50% or 75%. The eight **configuration-profile** leaves retain exactly one configuration for the selected task, pooling all three client counts. They describe that policy's objective space and operating conditions; they do not directly compare it with another policy.

### Shared data between configuration profiles and stress-only views

The single-pattern **configuration-profile** notebook and the corresponding **stress-only** notebook select the **same rows** for each task. Both use the same single-pattern `SLICE`, pool clients 4, 8, and 10, and include all environments. The stress-only notebooks do not filter to one stress value: they need all available focal stress levels to compare them. As a result, these are distinct analysis views over one population, not separate dataset strata.

| Shared population | Profile notebook | Stress-only view | Rows per task |
|:---|:---|:---|---:|
| Client Selector only | `analysis-fl-rq-client_selector-{task}.ipynb` | `analysis-fl-rq-stress-only-client_selector-{task}.ipynb` | 150 |
| HDH only | `analysis-fl-rq-hdh-{task}.ipynb` | `analysis-fl-rq-stress-only-hdh-{task}.ipynb` | 150 |
| Message Compressor only | `analysis-fl-rq-message_compressor-{task}.ipynb` | `analysis-fl-rq-stress-only-message_compressor-{task}.ipynb` | 210 |

Here `{task}` is `text` or `image`. The duplicated source populations are retained for now; no notebook or result has been removed. The analytical emphasis differs: profile notebooks describe the single-pattern policy and omit parsed stress columns that alias environment measures, while stress-only views color by focal stress and retain its stress feature for importance ranking and scenario discovery. Keep this overlap in mind when counting distinct data subsets, interpreting notebook totals, and deciding later whether to merge or reformulate a pair. The exact row-value check is recorded in [`notebook_dataset_overlap_report.md`](notebook_dataset_overlap_report.md).

The 0% and 100% common-stress levels are omitted from the combined-pattern family to avoid duplicate or misleading leaves. At 0%, only Message Compressor alone is represented (compressor ON with no induced delay); the existing Message Compressor stress-only notebook already shows this point. At 100%, only Message Compressor alone is available because Client Selector and HDH have no 100% runs. That point is also covered by the Message Compressor stress-only notebook. Neither level supports a comparison across pattern combinations.

The filenames `c4`, `c8`, and `c10` mean **client count**. They do not mean pattern stress. The source CSV's `pattern_stress` column is parsed into the nullable pattern-specific percentage features described below; it is not a notebook filter. These parsed features are distinct from the derived measures `Pattern Types Active` and `Pattern Instances`; the latter may vary with run conditions even inside one configuration profile.

## Scope and feature roles

| Notebook family | Fixed by its filter | Varies within the selected data | Excluded from feature ranking / scenario discovery |
|:---|:---|:---|:---|
| All configurations, c4/c8/c10 | Task, client count, all-environment view | Pattern configuration, sampled environment, outcomes | `Dataset`, `Model`, `Total Clients` |
| Image stress-only | Task, exactly one pattern ON, other two OFF, all-environment view | Focal stress percentage, client count, sampled environment, outcomes | `Dataset`, `Model`, and the focal pattern's paired environment percentage (exact alias of its stress feature) |
| Text stress-only | Task, exactly one pattern ON, other two OFF, all-environment view | Focal stress percentage, client count, sampled environment, outcomes | `Dataset`, `Model`, and the focal pattern's paired environment percentage (exact alias of its stress feature) |
| Combined-pattern stress (image and text) | Task, common enabled-pattern stress, all-environment view; baseline excluded; clients pooled | Supported pattern configuration, client count, sampled environment, outcomes | `Dataset`, `Model`, and parsed pattern-stress features (fixed/aliased in this slice); retain `Total Clients` as context and a candidate predictor |
| Baseline profile | Task, `OFF,OFF,OFF`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are all missing and excluded; other invariant features are auto-excluded |
| Client Selector profile | Task, `ON,OFF,OFF`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are excluded as aliases of existing environment features |
| Message Compressor profile | Task, `OFF,ON,OFF`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are excluded as aliases of existing environment features |
| HDH profile | Task, `OFF,OFF,ON`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are excluded as aliases of existing environment features |

In the all-configuration leaves, `Total Clients` is removed from candidate predictors because the notebook fixes it. These leaves include the three parsed stress features; each is missing when its pattern is OFF and otherwise matches its corresponding environment percentage. In profile leaves, client count remains a candidate because 4, 8, and 10 are pooled. Profile notebooks exclude parsed stress features because they duplicate the corresponding environment percentage in those single-configuration scopes. In each stress-only leaf, the focal pattern's stress feature varies and is retained for ranking and PRIM/CART; its paired environment percentage is excluded as an exact duplicate. In the combined-pattern stress leaves, every enabled pattern's stress feature is fixed at the selected level (disabled-pattern features remain missing), so parsed stress features are excluded; `config_id` represents the design alternative. `Total Clients` remains because the notebooks pool clients 4, 8, and 10. These are observational associations and do not isolate causal pattern or client-count effects.

## Notebook purpose and analysis goals

| Notebook | What it shows | Analysis goal |
|:---|:---|:---|
| `image/analysis-fl-rq-c4-image.ipynb` | All eight configurations at 4 clients | Compare objective-space allocations and identify conditions/boxes within this client-count stratum. |
| `image/analysis-fl-rq-c8-image.ipynb` | All eight configurations at 8 clients | Same RQ1/RQ2 comparison at the middle client count. |
| `image/analysis-fl-rq-c10-image.ipynb` | All eight configurations at 10 clients | Same RQ1/RQ2 comparison at the highest client count. |
| `image/analysis-fl-rq-stress-only-client_selector-image.ipynb` | Client Selector only at 25%, 50%, 75%, client counts pooled | Relate isolated Client Selector stress levels to objective tradeoffs and discover stress-aware operating envelopes. |
| `image/analysis-fl-rq-stress-only-hdh-image.ipynb` | HDH only at 25%, 50%, 75%, client counts pooled | Relate isolated HDH stress levels to objective tradeoffs and discover stress-aware operating envelopes. |
| `image/analysis-fl-rq-stress-only-message_compressor-image.ipynb` | Message Compressor only at 0%, 25%, 50%, 75%, 100%, client counts pooled | Compare the five compressor stress settings without co-activation and identify feasible tradeoffs/envelopes. |
| `image/analysis-fl-rq-combined-patterns-stress-25-image.ipynb` | All seven combinations at 25%, clients 4/8/10 pooled | Compare single-, pair-, and triple-pattern alternatives at common stress while treating client count as a varying context factor. |
| `image/analysis-fl-rq-combined-patterns-stress-50-image.ipynb` | Six supported combinations at 50%, clients pooled | Compare three single- and three two-pattern alternatives; mark the triple-pattern combination unavailable. |
| `image/analysis-fl-rq-combined-patterns-stress-75-image.ipynb` | Six supported combinations at 75%, clients pooled | Compare three single- and three two-pattern alternatives; mark the triple-pattern combination unavailable. |
| `text/analysis-fl-rq-stress-only-client_selector-text.ipynb` | Client Selector only at 25%, 50%, 75%, client counts pooled | Relate isolated Client Selector stress levels to text tradeoffs and stress-aware operating envelopes. |
| `text/analysis-fl-rq-stress-only-hdh-text.ipynb` | HDH only at 25%, 50%, 75%, client counts pooled | Relate isolated HDH stress levels to text tradeoffs and stress-aware operating envelopes. |
| `text/analysis-fl-rq-stress-only-message_compressor-text.ipynb` | Message Compressor only at 0%, 25%, 50%, 75%, 100%, client counts pooled | Compare the five compressor stress settings without co-activation and identify feasible tradeoffs/envelopes. |
| `text/analysis-fl-rq-combined-patterns-stress-25-text.ipynb` | All seven combinations at 25%, clients 4/8/10 pooled | Compare single-, pair-, and triple-pattern alternatives at common stress while treating client count as a varying context factor. |
| `text/analysis-fl-rq-combined-patterns-stress-50-text.ipynb` | Six supported combinations at 50%, clients pooled | Compare three single- and three two-pattern alternatives; mark the triple-pattern combination unavailable. |
| `text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb` | Six supported combinations at 75%, clients pooled | Compare three single- and three two-pattern alternatives; mark the triple-pattern combination unavailable. |
| `image/analysis-fl-rq-baseline-image.ipynb` | Image baseline, `OFF,OFF,OFF`, all clients | Provide the no-pattern reference objective space and operating conditions. |
| `image/analysis-fl-rq-client_selector-image.ipynb` | Client Selector only profile, all clients | Describe the single-pattern design's observed tradeoffs and conditions. |
| `image/analysis-fl-rq-message_compressor-image.ipynb` | Message Compressor only profile, all clients | Describe the single-pattern design's observed tradeoffs and conditions. |
| `image/analysis-fl-rq-hdh-image.ipynb` | HDH only profile, all clients | Describe the single-pattern design's observed tradeoffs and conditions. |
| `text/analysis-fl-rq-c4-text.ipynb` | All eight configurations at 4 clients | Compare objective-space allocations and conditions within the text task's 4-client stratum. |
| `text/analysis-fl-rq-c8-text.ipynb` | All eight configurations at 8 clients | Same RQ1/RQ2 comparison at the middle client count. |
| `text/analysis-fl-rq-c10-text.ipynb` | All eight configurations at 10 clients | Same RQ1/RQ2 comparison at the highest client count. |
| `text/analysis-fl-rq-stress-only-client_selector-text.ipynb` | Client Selector only at 25%, 50%, 75%, client counts pooled | Relate isolated Client Selector stress levels to text tradeoffs and stress-aware operating envelopes. |
| `text/analysis-fl-rq-stress-only-hdh-text.ipynb` | HDH only at 25%, 50%, 75%, client counts pooled | Relate isolated HDH stress levels to text tradeoffs and stress-aware operating envelopes. |
| `text/analysis-fl-rq-stress-only-message_compressor-text.ipynb` | Message Compressor only at 0%, 25%, 50%, 75%, 100%, client counts pooled | Compare the five compressor stress settings without co-activation and identify feasible tradeoffs/envelopes. |
| `text/analysis-fl-rq-baseline-text.ipynb` | Text baseline, `OFF,OFF,OFF`, all clients | Provide the no-pattern reference objective space and operating conditions. |
| `text/analysis-fl-rq-client_selector-text.ipynb` | Client Selector only profile, all clients | Describe the single-pattern design's observed tradeoffs and conditions. |
| `text/analysis-fl-rq-message_compressor-text.ipynb` | Message Compressor only profile, all clients | Describe the single-pattern design's observed tradeoffs and conditions. |
| `text/analysis-fl-rq-hdh-text.ipynb` | HDH only profile, all clients | Describe the single-pattern design's observed tradeoffs and conditions. |

The objective-space discretization edges are held fixed across all notebooks. Empty objective regions mean no observed rows in that notebook's filtered subset; they do not establish that the outcome is impossible.

## Shared train/test partition

After filtering, each notebook performs the same grouped holdout procedure:

```text
Filtered subset for one notebook
└── Group rows by partition_seed (10 seed groups)
    ├── Training: 7 seed groups, about 70% of rows
    │   └── Feature scoring and PRIM/CART box discovery
    └── Held out: 3 seed groups, about 30% of rows
        └── Evaluation of the already-discovered boxes
```

All rows belonging to a `partition_seed` stay together, preventing runs from one data partition from appearing on both sides. The splitter searches grouped holdouts for a tradeoff distribution close to the full filtered subset. Rare tradeoff classes can trigger a stratification warning or fallback; this does not split seed groups. Use each notebook's printed diagnostics for the actual score, tradeoff counts, and any warning. A tradeoff absent from the held-out rows has no held-out target support for box validation.

The currently executed notebooks report these filtered row counts; they are a snapshot, not a permanent guarantee if the source CSVs change:

| Scope | Image rows | Text rows |
|:---|---:|---:|
| Each all-configuration client-count leaf | 390 | 390 |
| Image Client Selector stress-only leaf | 150 | — |
| Image Message Compressor stress-only leaf | 210 | — |
| Image HDH stress-only leaf | 150 | — |
| Text Client Selector stress-only leaf | — | 150 |
| Text Message Compressor stress-only leaf | — | 210 |
| Text HDH stress-only leaf | — | 150 |
| Combined-pattern, 25% stress; clients pooled | 210 | 210 |
| Combined-pattern, 50% stress; clients pooled | 180 | 180 |
| Combined-pattern, 75% stress; clients pooled | 360 | 360 |
| Baseline profile | 180 | 180 |
| Client Selector profile | 150 | 150 |
| Message Compressor profile | 210 | 210 |
| HDH profile | 150 | 150 |

Each stress-only subset spans all ten `partition_seed` groups. Current stress-only level counts (client counts pooled) are CS: 25% = 30, 50% = 30, 75% = 90; MC: 0% = 30, 25% = 30, 50% = 30, 75% = 90, 100% = 30; HDH: 25% = 30, 50% = 30, 75% = 90, for both tasks. In the combined-pattern stress leaves, 25% has 210 rows (30 for each of seven configurations), 50% has 180 rows (30 for each of six), and 75% has 360 rows (90 for each single-pattern configuration and 30 for each pairwise configuration). The three-pattern configuration is absent at 50% and 75%. Client count varies in these pooled views. The family omits 0% and 100% because each has only Message Compressor alone, already represented in the Message Compressor stress-only notebook.

Use the notebook's fresh output as the authority after any data or filtering change.

## How to use this guide in a findings refresh

When running the [`adept-compact-findings` skill](../../../.claude/skills/adept-compact-findings/SKILL.md), use this tree to verify each case's scope. The executed notebook outputs, box reports, and plots remain authoritative for row counts, tradeoff support, split diagnostics, feature rankings, and box metrics. The campaign [README](README.md) has the broader data and methodology context.

For a manual, family-by-family calibration process before updating the findings skill, see [`MANUAL_FINDINGS_CALIBRATION.md`](MANUAL_FINDINGS_CALIBRATION.md).
