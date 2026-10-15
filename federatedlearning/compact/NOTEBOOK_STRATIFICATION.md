# Compact notebook stratification and scope

This guide maps each maintained notebook to the subset of the compact campaign it analyzes and explains why that slice exists. A **leaf is one notebook**. Each leaf applies its task, configuration, client-count, pattern-stress, and environment filters before computing outcomes, ranking features, discovering PRIM/CART boxes, and evaluating those boxes. All maintained notebooks use the all-environment view.

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
│   ├── Combined patterns at shared settings (defaults: 8 clients, 50% stress)
│   │   └── All seven non-empty combinations, supported rows only → image/analysis-fl-rq-combined-patterns-c8-stress-50-image.ipynb
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
    ├── Focal pattern ON, other pattern decisions vary; client counts pooled
    │   ├── Client Selector stress → text/analysis-fl-rq-stress-client_selector-text.ipynb
    │   ├── Message Compressor stress → text/analysis-fl-rq-stress-message_compressor-text.ipynb
    │   └── HDH stress → text/analysis-fl-rq-stress-hdh-text.ipynb
    ├── Isolated pattern stress: exactly one pattern ON; client counts pooled
    │   ├── Client Selector (25%, 50%, 75%) → text/analysis-fl-rq-stress-only-client_selector-text.ipynb
    │   ├── HDH (25%, 50%, 75%) → text/analysis-fl-rq-stress-only-hdh-text.ipynb
    │   └── Message Compressor (0%, 25%, 50%, 75%, 100%) → text/analysis-fl-rq-stress-only-message_compressor-text.ipynb
    ├── Combined patterns at shared settings (defaults: 8 clients, 50% stress)
    │   └── Supported single- and two-pattern combinations → text/analysis-fl-rq-combined-patterns-c8-stress-50-text.ipynb
    └── One configuration, pooling client counts 4, 8, and 10
        ├── No patterns ON       → text/analysis-fl-rq-baseline-text.ipynb
        ├── Client Selector only → text/analysis-fl-rq-client_selector-text.ipynb
        ├── Message Compressor only
        │                       → text/analysis-fl-rq-message_compressor-text.ipynb
        └── HDH only             → text/analysis-fl-rq-hdh-text.ipynb
```

The six **all-configuration** leaves retain all eight pattern ON/OFF configurations for the selected task and client count. They support within-client-count comparisons across complete configurations. Both tasks have three **stress-ONLY** leaves requiring exactly one named pattern ON and both other patterns OFF; they pool all client counts to compare stress levels without mixing co-activation. Their colors encode increasing stress severity: green/orange/red for Client Selector and HDH, and light-green/green/orange/red/dark-red for Message Compressor (shown in a horizontal legend row). The three text focal-pattern leaves retain their broader scope: one named pattern must be ON, other patterns may vary, and client counts are pooled, so those views overlap. Both tasks also have a **combined-pattern** leaf fixing task, client count and target stress, then comparing every available non-empty pattern combination; it shows absent combinations in its support table but does not assign them outcomes. At text c8/50%, six single- and two-pattern combinations have ten rows each and the three-pattern combination has none. The eight **configuration-profile** leaves retain exactly one configuration for the selected task, pooling all three client counts. They describe that policy's objective space and operating conditions; they do not directly compare it with another policy.

The filenames `c4`, `c8`, and `c10` mean **client count**. They do not mean pattern stress. The source CSV's `pattern_stress` column is parsed into the nullable pattern-specific percentage features described below; it is not a notebook filter. These parsed features are distinct from the derived measures `Pattern Types Active` and `Pattern Instances`; the latter may vary with run conditions even inside one configuration profile.

## Scope and feature roles

| Notebook family | Fixed by its filter | Varies within the selected data | Excluded from feature ranking / scenario discovery |
|:---|:---|:---|:---|
| All configurations, c4/c8/c10 | Task, client count, all-environment view | Pattern configuration, sampled environment, outcomes | `Dataset`, `Model`, `Total Clients` |
| Image stress-ONLY | Task, exactly one pattern ON, other two OFF, all-environment view | Focal stress percentage, client count, sampled environment, outcomes | `Dataset`, `Model`, and the focal pattern's paired environment percentage (exact alias of its stress feature) |
| Text stress-ONLY | Task, exactly one pattern ON, other two OFF, all-environment view | Focal stress percentage, client count, sampled environment, outcomes | `Dataset`, `Model`, and the focal pattern's paired environment percentage (exact alias of its stress feature) |
| Text focal-pattern stress | Task, one required pattern ON, all-environment view | Focal stress percentage, client count, other pattern decisions, sampled environment, outcomes | `Dataset`, `Model`, and the focal pattern's paired environment percentage (exact alias of its stress feature) |
| Combined-pattern (image and text) | Task, client count, target stress, all-environment view; baseline excluded | Supported pattern configuration, sampled environment, outcomes | `Dataset`, `Model`, `Total Clients`, and all parsed pattern-stress features; configuration remains the design alternative |
| Baseline profile | Task, `OFF,OFF,OFF`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are all missing and excluded; other invariant features are auto-excluded |
| Client Selector profile | Task, `ON,OFF,OFF`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are excluded as aliases of existing environment features |
| Message Compressor profile | Task, `OFF,ON,OFF`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are excluded as aliases of existing environment features |
| HDH profile | Task, `OFF,OFF,ON`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are excluded as aliases of existing environment features |

In the all-configuration leaves, `Total Clients` is removed from candidate predictors because the notebook fixes it. These leaves include the three parsed stress features; each is missing when its pattern is OFF and otherwise matches its corresponding environment percentage. In profile leaves, client count remains a candidate because 4, 8, and 10 are pooled. Profile notebooks exclude parsed stress features because they duplicate the corresponding environment percentage in those single-configuration scopes. In each stress-ONLY leaf, the focal pattern's stress feature varies and is retained for ranking and PRIM/CART; its paired environment percentage is excluded as an exact duplicate. In the combined-pattern leaves, each enabled pattern is fixed at the selected stress, so all parsed stress features are excluded; `config_id` represents the design alternative. Text focal-pattern leaves continue to vary co-enabled pattern decisions. These are observational associations and do not isolate a causal stress effect.

## Notebook purpose and analysis goals

| Notebook | What it shows | Analysis goal |
|:---|:---|:---|
| `image/analysis-fl-rq-c4-image.ipynb` | All eight configurations at 4 clients | Compare objective-space allocations and identify conditions/boxes within this client-count stratum. |
| `image/analysis-fl-rq-c8-image.ipynb` | All eight configurations at 8 clients | Same RQ1/RQ2 comparison at the middle client count. |
| `image/analysis-fl-rq-c10-image.ipynb` | All eight configurations at 10 clients | Same RQ1/RQ2 comparison at the highest client count. |
| `image/analysis-fl-rq-stress-only-client_selector-image.ipynb` | Client Selector only at 25%, 50%, 75%, client counts pooled | Relate isolated Client Selector stress levels to objective tradeoffs and discover stress-aware operating envelopes. |
| `image/analysis-fl-rq-stress-only-hdh-image.ipynb` | HDH only at 25%, 50%, 75%, client counts pooled | Relate isolated HDH stress levels to objective tradeoffs and discover stress-aware operating envelopes. |
| `image/analysis-fl-rq-stress-only-message_compressor-image.ipynb` | Message Compressor only at 0%, 25%, 50%, 75%, 100%, client counts pooled | Compare the five compressor stress settings without co-activation and identify feasible tradeoffs/envelopes. |
| `image/analysis-fl-rq-combined-patterns-c8-stress-50-image.ipynb` | Every non-empty pattern combination at configurable clients/stress; defaults c8/50% | Compare single-, pair-, and triple-pattern alternatives under a common requested setting; distinguish absent campaign support from poor performance. |
| `text/analysis-fl-rq-stress-only-client_selector-text.ipynb` | Client Selector only at 25%, 50%, 75%, client counts pooled | Relate isolated Client Selector stress levels to text tradeoffs and stress-aware operating envelopes. |
| `text/analysis-fl-rq-stress-only-hdh-text.ipynb` | HDH only at 25%, 50%, 75%, client counts pooled | Relate isolated HDH stress levels to text tradeoffs and stress-aware operating envelopes. |
| `text/analysis-fl-rq-stress-only-message_compressor-text.ipynb` | Message Compressor only at 0%, 25%, 50%, 75%, 100%, client counts pooled | Compare the five compressor stress settings without co-activation and identify feasible tradeoffs/envelopes. |
| `text/analysis-fl-rq-combined-patterns-c8-stress-50-text.ipynb` | Every supported non-empty pattern combination at configurable clients/stress; defaults c8/50% | Compare single- and pair-pattern alternatives under a common setting; the support table marks the unsupported triple-pattern case. |
| `image/analysis-fl-rq-baseline-image.ipynb` | Image baseline, `OFF,OFF,OFF`, all clients | Provide the no-pattern reference objective space and operating conditions. |
| `image/analysis-fl-rq-client_selector-image.ipynb` | Client Selector only profile, all clients | Describe the single-pattern design's observed tradeoffs and conditions. |
| `image/analysis-fl-rq-message_compressor-image.ipynb` | Message Compressor only profile, all clients | Describe the single-pattern design's observed tradeoffs and conditions. |
| `image/analysis-fl-rq-hdh-image.ipynb` | HDH only profile, all clients | Describe the single-pattern design's observed tradeoffs and conditions. |
| `text/analysis-fl-rq-c4-text.ipynb` | All eight configurations at 4 clients | Compare objective-space allocations and conditions within the text task's 4-client stratum. |
| `text/analysis-fl-rq-c8-text.ipynb` | All eight configurations at 8 clients | Same RQ1/RQ2 comparison at the middle client count. |
| `text/analysis-fl-rq-c10-text.ipynb` | All eight configurations at 10 clients | Same RQ1/RQ2 comparison at the highest client count. |
| `text/analysis-fl-rq-stress-client_selector-text.ipynb` | Client Selector enabled; co-activation allowed; clients pooled | Describe observed Client Selector stress tradeoffs and associated joint boxes in the existing broader pattern mix. |
| `text/analysis-fl-rq-stress-hdh-text.ipynb` | HDH enabled; co-activation allowed; clients pooled | Describe observed HDH stress tradeoffs and associated joint boxes in the existing broader pattern mix. |
| `text/analysis-fl-rq-stress-message_compressor-text.ipynb` | Message Compressor enabled; co-activation allowed; clients pooled | Describe observed compressor stress tradeoffs and associated joint boxes in the existing broader pattern mix. |
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
| Image Client Selector stress-ONLY leaf | 150 | — |
| Image Message Compressor stress-ONLY leaf | 210 | — |
| Image HDH stress-ONLY leaf | 150 | — |
| Text Client Selector stress-ONLY leaf | — | 150 |
| Text Message Compressor stress-ONLY leaf | — | 210 |
| Text HDH stress-ONLY leaf | — | 150 |
| Each text Client Selector focal-pattern leaf | — | 480 |
| Each text Message Compressor focal-pattern leaf | — | 600 |
| Each text HDH focal-pattern leaf | — | 480 |
| Combined-pattern leaf at c8 / 50% stress | 60 | 60 |
| Baseline profile | 180 | 180 |
| Client Selector profile | 150 | 150 |
| Message Compressor profile | 210 | 210 |
| HDH profile | 150 | 150 |

Each stress-ONLY or focal-pattern subset spans all ten `partition_seed` groups. Current stress-ONLY level counts (client counts pooled) are CS: 25% = 30, 50% = 30, 75% = 90; MC: 0% = 30, 25% = 30, 50% = 30, 75% = 90, 100% = 30; HDH: 25% = 30, 50% = 30, 75% = 90, for both tasks. The text focal-pattern counts remain CS: 25% = 240, 50% = 90, 75% = 150; MC: 0% = 120, 25% = 120, 50% = 90, 75% = 150, 100% = 120; HDH: 25% = 240, 50% = 90, 75% = 150. At c8/50%, each task's combined-pattern leaf has ten rows for each of the three single-pattern and three pairwise combinations, and zero rows for all three patterns enabled. A client-count-by-level split would leave only 30 rows at most per stress-ONLY level and is not part of the maintained tree. Text focal-pattern views overlap because co-enabled runs appear in more than one leaf; their row counts must not be summed as unique campaign rows.

Use the notebook's fresh output as the authority after any data or filtering change.

## How to use this guide in a findings refresh

When running the [`adept-compact-findings` skill](../../../.claude/skills/adept-compact-findings/SKILL.md), use this tree to verify each case's scope and avoid treating overlapping focal-pattern leaves as independent campaign partitions. The executed notebook outputs, box reports, and plots remain authoritative for row counts, tradeoff support, split diagnostics, feature rankings, and box metrics. The campaign [README](README.md) has the broader data and methodology context.
