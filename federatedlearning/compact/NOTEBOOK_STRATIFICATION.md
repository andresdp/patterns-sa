# Compact notebook stratification and scope

This guide maps each maintained notebook to the subset of the compact campaign it analyzes. A **leaf is one notebook**. Each leaf applies its task, configuration, client-count, required-pattern, and environment filters before computing outcomes, ranking features, discovering PRIM/CART boxes, and evaluating those boxes.

## Notebook tree

```text
Compact campaign (all available environment settings)
├── Image task: Dataset=CIFAR-10, Model=CNN 16k
│   ├── All configurations, one client-count stratum
│   │   ├── Total Clients=4  → image/analysis-fl-rq-c4-image.ipynb
│   │   ├── Total Clients=8  → image/analysis-fl-rq-c8-image.ipynb
│   │   └── Total Clients=10 → image/analysis-fl-rq-c10-image.ipynb
│   ├── Focal pattern ON, other pattern decisions vary; client counts pooled
│   │   ├── Client Selector stress → image/analysis-fl-rq-stress-client_selector-image.ipynb
│   │   ├── Message Compressor stress → image/analysis-fl-rq-stress-message_compressor-image.ipynb
│   │   └── HDH stress → image/analysis-fl-rq-stress-hdh-image.ipynb
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
    └── One configuration, pooling client counts 4, 8, and 10
        ├── No patterns ON       → text/analysis-fl-rq-baseline-text.ipynb
        ├── Client Selector only → text/analysis-fl-rq-client_selector-text.ipynb
        ├── Message Compressor only
        │                       → text/analysis-fl-rq-message_compressor-text.ipynb
        └── HDH only             → text/analysis-fl-rq-hdh-text.ipynb
```

The six **all-configuration** leaves retain all eight pattern ON/OFF configurations for the selected task and client count. They support within-client-count comparisons across complete configurations. The six **focal-pattern stress** leaves require one named pattern to be ON, allow the other two decisions to vary, and pool all three client counts and all observed values of that pattern's stress feature. These are overlapping analysis views: runs with multiple patterns ON appear in more than one focal-pattern branch. The eight **configuration-profile** leaves retain exactly one configuration for the selected task, pooling all three client counts. They describe that policy's objective space and operating conditions; they do not directly compare it with another policy.

The filenames `c4`, `c8`, and `c10` mean **client count**. They do not mean pattern stress. The source CSV's `pattern_stress` column is parsed into the nullable pattern-specific percentage features described below; it is not a notebook filter. These parsed features are distinct from the derived measures `Pattern Types Active` and `Pattern Instances`; the latter may vary with run conditions even inside one configuration profile.

## Scope and feature roles

| Notebook family | Fixed by its filter | Varies within the selected data | Excluded from feature ranking / scenario discovery |
|:---|:---|:---|:---|
| All configurations, c4/c8/c10 | Task, client count, all-environment view | Pattern configuration, sampled environment, outcomes | `Dataset`, `Model`, `Total Clients` |
| Focal-pattern stress | Task, one required pattern ON, all-environment view | Its stress percentage, client count, other pattern decisions, sampled environment, outcomes | `Dataset`, `Model`, and the focal pattern's paired environment percentage (exact alias of its stress feature) |
| Baseline profile | Task, `OFF,OFF,OFF`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are all missing and excluded; other invariant features are auto-excluded |
| Client Selector profile | Task, `ON,OFF,OFF`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are excluded as aliases of existing environment features |
| Message Compressor profile | Task, `OFF,ON,OFF`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are excluded as aliases of existing environment features |
| HDH profile | Task, `OFF,OFF,ON`, all-environment view | Client count, sampled environment, outcomes | `Dataset`, `Model`; parsed pattern-stress features are excluded as aliases of existing environment features |

In the all-configuration leaves, `Total Clients` is removed from the candidate predictors because the notebook fixes it. These leaves include the three parsed stress features as candidates; each is missing when its pattern is OFF and otherwise exactly matches its corresponding environment percentage. In the profile leaves, client count remains a candidate because 4, 8, and 10 are pooled. Profile notebooks exclude the parsed stress features from candidate predictors for now because they are duplicate representations of the corresponding environment percentage in those single-configuration scopes. In a focal-pattern stress leaf, the required pattern's stress feature is present and varies. It is retained for feature ranking and PRIM/CART, while its paired environment percentage is excluded from those candidate inputs to avoid duplicate predictors. Client count and the other pattern decisions remain variable. These choices are associative; they do not isolate a stress effect from the observed configuration and environment mix.

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
| Each Client Selector focal-pattern leaf | 480 | 480 |
| Each Message Compressor focal-pattern leaf | 600 | 600 |
| Each HDH focal-pattern leaf | 480 | 480 |
| Baseline profile | 180 | 180 |
| Client Selector profile | 150 | 150 |
| Message Compressor profile | 210 | 210 |
| HDH profile | 150 | 150 |

Each value in a focal-pattern view spans all ten `partition_seed` groups. Current stress-level counts per task (client counts pooled) are CS: 25% = 240, 50% = 90, 75% = 150; MC: 0% = 120, 25% = 120, 50% = 90, 75% = 150, 100% = 120; HDH: 25% = 240, 50% = 90, 75% = 150. A client-count-by-level split would leave only 30–80 rows per task/value and is not part of the maintained tree. Because focal-pattern views overlap, their row counts must not be summed as unique campaign rows.

Use the notebook's fresh output as the authority after any data or filtering change.

## How to use this guide in a findings refresh

When running the [`adept-compact-findings` skill](../../../.claude/skills/adept-compact-findings/SKILL.md), use this tree to verify each case's scope and avoid treating overlapping focal-pattern leaves as independent campaign partitions. The executed notebook outputs, box reports, and plots remain authoritative for row counts, tradeoff support, split diagnostics, feature rankings, and box metrics. The campaign [README](README.md) has the broader data and methodology context.
