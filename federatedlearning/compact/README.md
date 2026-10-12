# Compact FL campaign: data, specs and notebooks

This folder holds the compact AP4FED experiment campaign and its ADEPT system definitions.
The analysis notebooks live one level up, in `federatedlearning/`, and load the specs from
here. This README explains what the data contains, which notebooks analyze it, and why each
notebook family slices the data the way it does.

**Current analysis scope:** Understand the compact run-level space first; general analysis of the detailed client/round records is deferred. ADEPT's configured aggregation averages selected numeric client fields over recorded values and counts distinct values for categorical fields. A mean describes that recorded population, not every client; usage means can include participants only. Equal averages can hide imbalance, joint conditions on a client, or behavior over rounds. The existing detailed-log HDH counts are a limited supporting measurement. See [the formalization's aggregation explanation](../../docs/paper_adept_formal_extension.md#21-observation-level-compact-summaries-first).

## 1. The data

| File | Runs | Configurations (`client_selector,message_compressor,hdh`) |
|:---|---:|:---|
| `adept_experiments_all_waves.csv` | 1,380 | `OFF,OFF,OFF` and each pattern alone (`ON,OFF,OFF`, `OFF,ON,OFF`, `OFF,OFF,ON`) |
| `adept_experiments_all_waves_combinedAP.csv` | 960 | pattern combinations (`ON,ON,OFF`, `ON,OFF,ON`, `OFF,ON,ON`, `ON,ON,ON`) |

Both files have the same 160 columns. Together they cover:

- **3 client counts:** 4, 8 and 10 clients (`Total Clients`), 780 runs each.
- **2 tasks:** image classification (CIFAR-10 + CNN 16k) and text classification
  (AG_NEWS + MLP). Dataset and model always go together, so each pair is one *task*.
- **8 configurations** of the three ON/OFF pattern decisions.
- **3 designed environment factors,** varied in waves: the shares of low-spec clients
  (`low_spec_percentage`), non-IID clients (`non_iid_percentage`) and delayed clients
  (`delay_percentage`). The Dirichlet α is constant (0.5).
- **10 partition seeds/repeats** (`partition_seed`, `repeat`, values 1–10). Each seed occurs
  once in each executed configuration-condition cell; `run_id` is unique per run. Include
  `partition_seed` in `MATCH_ON` to compare corresponding data partitions. This does not
  match hostname, scheduling, or other unrecorded conditions.
- The CSVs record **20 rounds**, `Epochs = 1`, learning rate `0.001`, and batch size `64`.
  Confirm the AP4FED meaning of `Epochs` before naming it local epochs. `avg_total_time` is
  documented as average total round time (training plus communication); the precise timing
  instrumentation and host hardware specifications are not in these CSVs.

The two quality objectives of the paper are **model accuracy** (`final_val_accuracy`,
maximize) and **total round time** (`avg_total_time`, minimize).

## 2. Specs

| Spec | Loads | Used by |
|:---|:---|:---|
| `FLsystem_compact_all.json` | both CSVs (`source_file` is a list; ADEPT concatenates them) | every notebook (the overview, the pattern and the stress notebooks) |
| `FLsystem_compact_individual.json` | `adept_experiments_all_waves.csv` | not used by the notebooks any more; kept to analyze the baseline and single patterns alone |
| `FLsystem_compact_combined.json` | `adept_experiments_all_waves_combinedAP.csv` | not used by the notebooks any more; kept to analyze the combinations alone |

All three declare the same parameters, objectives, client aggregations and column renames.
`FLsystem_compact_all.json` additionally declares:
- the pattern-stress parameters (§5), which the loader preprocessor derives;
- the three environment factors, as uncertainties.

It must therefore be loaded through `fl_slices.slice_filter(...)`, as every notebook does.

## 3. Notebooks and their rationale

The campaign mixes factors with very different effects: the task shifts accuracy (mean
0.88 for text vs. 0.51 for image classification), the number of clients changes the
system's structure, and the
environment was not varied in the same way for every configuration. One analysis of all
runs mixes these effects with the pattern effects. The notebooks therefore come in three
families. Each answers one question on the slice of data where that question has a clean
answer.

| Family | Notebooks | Data | Question |
|:---|:---|:---|:---|
| **Overview** | `analysis-fl.ipynb` | all 2,340 runs, all 8 configurations | What does the whole design space look like, and which factors dominate? |
| **Pattern** (ablation A1) | `analysis-fl-baseline.ipynb`, `analysis-fl-client-selector.ipynb`, `analysis-fl-message-compressor.ipynb`, `analysis-fl-hdh.ipynb` | one configuration each | What does each pattern do on its own, compared with the baseline? |
| **Stress** | `analysis-fl-stress-c{4,8,10}-{image,text}.ipynb` | one client count and one task, all 8 configurations, at the common environment point | For a fixed system structure and task, how do accuracy and round time change as more patterns (and pattern instances) are active? |

### Overview notebook

It is the reference for the whole campaign: the spec check, tradeoff regions, feature
importance and boxes over all runs. Its tradeoff edges are detected on all runs.
Because tasks, client counts and environments are mixed, its boxes are dominated by those
factors. Use it to see what dominates, not to conclude about individual patterns.
Its Section 7 (pattern stress) runs here too, but over mixed tasks and environments; the
stress notebooks give the controlled version.

### Pattern notebooks

Each keeps the runs of one configuration (the baseline, or one pattern alone), to
characterize that pattern in isolation: the base paper's single-pattern setting.

- They load all runs (`FLsystem_compact_all.json`) and keep their configuration, so the
  pattern-stress columns are available (Section 7: in a single-pattern notebook only the
  instance count varies; in the baseline nothing varies).
- They share **fixed tradeoff edges**, detected on all runs
  (`'final_val_accuracy': [0.2075, 0.4774, 0.7473, 1.0172]`,
  `'avg_total_time': [1.5625, 9.5065, 17.4505, 25.3945]`): the same edges the overview
  detects. A region therefore means the same in these four notebooks and in the overview,
  and densities can be compared across them.
- **Comparing a pattern with the baseline** uses shared task, client count, environment,
  and partition seed. The overview notebook does this for all three patterns at once; the
  generated `*-vs-baseline` notebooks isolate each direct comparison. The contrast API
  summarizes equally over matched seed-settings and, for `others='all'`, by the other
  pattern composition. These are descriptive seed-matched comparisons; sign changes by
  composition do not alone establish formal interactions.
- `--include-baseline` generates `*-vs-baseline` variants that keep the baseline runs next
  to one pattern's runs (their Section 5 then shows that pattern's matched contrast).
- **Caveat:** within each notebook, client counts, tasks and environments still vary.

### Stress notebooks

Each fixes everything except the configuration, so differences between runs are pattern
effects:

| Fixed factor | Why |
|:---|:---|
| **Client count** | The system structure changes with the number of clients: more clients means more pattern instances, other round times (max ~25 s with 4 clients vs. ~17 s with 8 or 10), and a different effect of excluding clients. Comparing pattern stress across client counts would mix the two. |
| **Task** | Accuracy differs widely between the tasks (text: 0.52-0.92, mean 0.88; image: 0.31-0.60, mean 0.51), so the task would dominate every comparison, as `Model` did in the earlier FL data. |
| **Environment** (`ENVIRONMENT = 'common'`) | The waves did not run every configuration at every environment point: `ON,ON,ON`, for instance, was only run at 25% low-spec, 25% non-IID, 25% delay. That point is the only one shared by all 8 configurations, and there the design is a balanced full factorial: 10 runs per configuration (80 per notebook), one for each partition seed. |

- Tradeoff edges are **detected per notebook**. Comparisons happen inside a notebook,
  across stress levels and configurations; regions are not comparable across notebooks.
- `--environment all` generates `*-allenv` variants over every environment point (390
  runs each). There stress and environment effects are mixed, but the environment varies,
  which is what operating-envelope analyses need.

### Generating and editing

The pattern and stress notebooks are **generated** from `analysis-fl.ipynb` by
`make_slice_notebooks.py`. Only their `parameters` cell differs, plus a header. Their
markdown is the overview's, unchanged: it explains what each step computes and how to read
it, but never describes particular results (counts, ranges, boxes), so it stays valid for
any slice and after the data changes. The results are the cell outputs. Cells tagged
`reading-guide` are the ones that explain how to read a result. Edit the overview notebook
and regenerate, rather than editing a generated notebook:

```bash
# from federatedlearning/
python make_slice_notebooks.py --execute                  # pattern notebooks
python make_slice_notebooks.py --stress --execute         # stress notebooks
python make_slice_notebooks.py --stress --environment all # ...-allenv variants
```

Regenerating overwrites the generated notebooks, including any text written in them.

## 4. Filters (`fl_slices.slice_filter`)

| Argument | Keeps |
|:---|:---|
| `name` (+ `include_baseline`) | `'all'`, `'baseline'`, or one pattern alone (`'client_selector'`, `'message_compressor'`, `'hdh'`) |
| `clients` | runs with that `Total Clients` (4, 8 or 10) |
| `task` | `'image'` = CIFAR-10 + CNN 16k, `'text'` = AG_NEWS + MLP |
| `environment` | `'common'`: only the environment points at which **every** configuration left after the other filters was run |

```python
session.load(preprocessor=fl_slices.slice_filter(clients=8, task='image', environment='common'))
```

In the notebooks these are the parameters `SLICE`, `INCLUDE_BASELINE`, `CLIENTS`, `TASK`
and `ENVIRONMENT`.

## 5. Pattern stress (`pattern_stress.py`)

- **`Pattern Instances`** (S_inst), the **primary stress measure**: sum of `Client Selector Instances`,
  `Message Compressor Instances` and `HDH Instances`. The same pattern type can have
  several instances, so S_inst depends on the configuration *and* on the environment. The
  instance counts are declared as uncertainties; boxes on them read as conditional
  prescriptions. `HDH Instances` is **measured** from the per-round data when
  `detailed/` is available (participating clients with `HDH Time > 0`), and assumed (A3)
  otherwise; the other two counts are assumed (A1, A2). The loader prints which source
  was used. `fl_slices.slice_filter(..., measured_instances=False)` forces A3.
- **`Pattern Types Active`** (S_types, 0-3), a secondary measure: number of pattern
  decisions ON in `config_id`. It is exact, fixed by the configuration, and declared as a
  lever.
- See "Choosing the stress parameters" below for the options considered and the decision.
- `Participating Clients` is added too (not declared in the spec: it is an effect of the
  client selector, not a factor).

### Assumptions (to confirm)

The compact CSVs record no pattern instances, so they are derived from per-client columns
(HDH is measured instead when the per-round data is available):

| ID | Assumption | Status |
|:---|:---|:---|
| A1 | The client selector has **one** instance, on the server. | Unconfirmed |
| A2 | The message compressor has **one instance per participating client**; the server-side decompression is not counted. | Unconfirmed |
| A3 | HDH has **one instance per participating non-IID client**. | **Contradicted for the image task** by the per-round data (below): HDH work is recorded on every participating non-IID client in text runs, but almost never in image runs. Holds for the text task. |
| A4 | A client participates iff it exists in the run (index ≤ `Total Clients`) and its `CPU Usage Avg` is recorded. | Verified on all 2,340 runs: with the selector ON, the participants are exactly the non-low-spec clients; with it OFF, all clients participate. The per-round data confirms it, and shows that participation never changes between rounds. |
| A5 | A client is non-IID iff its `Data Distribution` is `non-IID`. | Verified: the count equals `non_iid_clients` in every run. |
| A6 | Task = (Dataset, Model): CIFAR-10 + CNN 16k, AG_NEWS + MLP. | Verified: no other pairs occur. |

The rules live in `pattern_stress.INSTANCE_RULES`; changing an assumption is a one-line
change there.

### Evidence from the per-round data (`detailed/`)

`federatedlearning/detailed/` (not in git: 71 MB and 48 MB) holds one row per client and
round for the same 2,340 runs (343,200 rows), with `participated`, `HDH Time`,
`Communication Time`, `JSD` and the list of active patterns per round. It settles part of
the assumptions:

| Question | What the data shows |
|:---|:---|
| Do active patterns change during a run? | No. The active-pattern list (`AP List`, 6 slots: client selector, client cluster, message compressor, model co-versioning registry, multi-task model trainer, HDH) is the same in every round of a run and matches `config_id` in all 2,340 runs: patterns are activated statically. |
| Does participation change between rounds? | No. Each client participates in all rounds or in none (0 of 17,160 run-client pairs change). The selector excludes clients once, at the start. |
| Where does HDH run (A3)? | Only in round 1 (augmentation happens once), only on participating non-IID clients, never on IID or excluded clients. **Text task:** on every participating non-IID client (1,371 of 1,371). **Image task:** on almost none (48 of 1,371). |
| Message compressor instances (A2)? | Not observable: no compression column per client. Communication time per client and round is higher with the compressor ON (mean 4.9 s vs. 4.0 s), so compression adds overhead rather than saving time in this setup. |
| Client selector instances (A1)? | Not observable. |

Consequences for the stress measures:
- `HDH Instances` overstates HDH in image runs, where HDH rarely does any work. An
  observed alternative is the number of clients with `HDH Time > 0` in the per-round data.
- Because HDH works only in round 1, its cost is a one-off per client, not a per-round
  load. Instance counts treat both kinds of pattern the same way.

### Open questions

1. **Client selector instances (A1):** one server-side component, or does the selection
   logic also run on each client (e.g. a resource report per client)?
2. **Message compressor (A2):** should the server's decompressor (or compression of the
   global model sent back to clients) count as an instance? With it, S_inst would add 1 per
   run with the compressor ON.
3. **HDH (A3):** is HDH deployed only on non-IID clients, or on every participating client
   (augmenting only where needed)? Is it deployed on a non-IID client the selector excludes?
4. **Weights:** should S_inst count instances equally, or weight them by cost (e.g. an HDH
   instance trains a GAN, a compressor instance only compresses messages)?
5. **Logging:** can AP4FED record the instance counts per run, so they no longer need to
   be inferred?
6. **HDH on images:** why does HDH record no work on almost every non-IID client in the
   CIFAR-10 runs (48 of 1,371)? Is it skipped by a trigger (e.g. a heterogeneity threshold),
   failing silently, or logged differently? Until this is known, HDH results on the image
   task should be read as "HDH configured", not "HDH applied".

### Choosing the stress parameters (for discussion)

**Question.** Which run attributes should be declared as "pattern stress", so that ADEPT can
relate the amount of patterning in a run to the tradeoffs?

**Options considered**

| Option | Stress parameters | Pros | Cons |
|:---|:---|:---|:---|
| 1. Pattern types only | `Pattern Types Active` (0-3), as a **lever** | Exact (read from `config_id`); controlled by the architect, so boxes on it are prescriptive; needs no assumption | Ignores the size of a deployment: one HDH on 2 clients and one on 8 clients count the same |
| 2. Instance counts, measured where possible | per-pattern instance counts and their sum, as **uncertainties** | Captures deployment size, and how the selector removes instances from the other patterns | Only HDH is observable (per-round `HDH Time`); selector and compressor counts rest on A1-A2; needs the 119 MB per-round data, which is not in git |
| 3. Pattern activity | e.g. excluded clients, total HDH time, extra communication time | Measures what the patterns actually did | These are **effects** of the patterns that correlate directly with round time; declared as parameters, they would partly restate the objective in the boxes (leakage) |

**Decision (2026-10-11, revised the same day).** The instance count (option 2) is the
primary stress measure, because it captures the size of a deployment, which the number of
pattern types ignores; `Pattern Types Active` (option 1) is kept as a secondary, exact
measure:
- Section 7 of the notebooks groups robustness by `Pattern Instances` and then by
  `Pattern Types Active`, plots the objectives against `Pattern Instances`, and runs PRIM
  on both.
- Because the primary measure rests partly on assumptions (A1-A2) and on the per-round
  data, its caveats (points 2-5 below) matter more than they would for option 1.
- `HDH Instances` comes from the per-round data (participating clients with
  `HDH Time > 0`) when `detailed/` is present, with A3 as the fallback. On the compact data
  the measured count equals A3 in every text run, and is almost always 0 in image runs.
- Option 3 is not used for stress; activity measures could instead be reported as
  diagnostics (outcomes), never as parameters.

**Points for the co-authors**

1. Instances are now the primary stress notion ("how much patterning is deployed"), with
   the number of composed pattern types as a secondary, exact measure. Is this the notion
   the paper wants?
2. Confirm or correct A1-A2 (see the open questions above). If AP4FED can log instance
   counts per run (open question 5), option 2 no longer needs assumptions.
3. HDH on images (open question 6): if HDH really does not run on CIFAR-10, the image
   notebooks measure "HDH configured" rather than "HDH applied", and the paper should say
   so, or the image runs with HDH should be re-run.
4. Should instances be weighted by cost (open question 4)? HDH works once, in round 1,
   while the compressor works in every round, so equal counts compare unlike things.
5. Reproducibility: the measured counts depend on `detailed/`, which is not versioned.
   Options: Git LFS, an archived dataset (e.g. Zenodo) cited in the paper, or a small
   derived file (`run_id` -> HDH instances) committed next to the compact CSVs.

### Observations about the campaign design

- **The environment is not crossed with the configurations.** Each configuration was run
  at a different set of (low-spec, non-IID, delay) points; `ON,ON,ON` only at
  (25%, 25%, 25%). Differences between stress levels over all runs therefore mix pattern
  effects and environment effects.
- **The common environment point is (25%, 25%, 25%),** at every client count, where the
  design is a balanced full factorial (10 runs per configuration and task).
- **Stress levels are mixtures of configurations** (level 1: 3 configurations, level 2: 3,
  level 3: 1). On the common point every configuration has the same number of runs, so each
  level weights its configurations equally; on all runs it does not.
- **The selector reduces instance stress.** With 10 clients in the text task, `ON,ON,ON`
  carries 9-11 instances against 12-18 for `OFF,ON,ON`, because excluded clients take their
  compressor and HDH instances with them. In the image task the gap is small (9-10 against
  10-11), because HDH adds almost no measured instances there.

## 6. Technical notes

- Both CSVs are comma-delimited; the specs set `dataspace.discovery_options.csv_delimiter`
  to `,`.
- Configurations are identified from `config_id` in the order
  `client_selector_pattern,message_compressor_pattern,hdh_pattern`. Each spec declares
  exactly the configuration IDs present in its data.
- The per-client aggregation rules, column renames (e.g. `Final Val Accuracy` →
  `final_val_accuracy`) and objectives are those of the earlier FL spec.
  `Final Agent Time` is not a quality objective.
- Tradeoff edges are notebook settings (`TRADEOFF_LABELS`, `TRADEOFF_EDGES` in the
  `parameters` cell), not part of the specs. `TRADEOFF_EDGES = None` detects them from the
  loaded runs; explicit edges need labels for the same objectives.
