# Compact FL campaign: data, specs and notebooks

This folder holds the compact AP4FED experiment campaign and its ADEPT system definitions.
The analysis notebooks live one level up, in `federatedlearning/`, and load the specs from
here. This README explains what the data contains, which notebooks analyze it, and why each
notebook family slices the data the way it does.

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

The two quality objectives of the paper are **model accuracy** (`final_val_accuracy`,
maximize) and **total round time** (`avg_total_time`, minimize).

## 2. Specs

| Spec | Loads | Used by |
|:---|:---|:---|
| `FLsystem_compact_all.json` | both CSVs (`source_file` is a list; ADEPT concatenates them) | `analysis-fl.ipynb` and the stress notebooks |
| `FLsystem_compact_individual.json` | `adept_experiments_all_waves.csv` | the pattern notebooks |
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
| **Pattern** (ablation A1) | `analysis-fl-baseline.ipynb`, `analysis-fl-client-selector.ipynb`, `analysis-fl-message-compressor.ipynb`, `analysis-fl-hdh.ipynb` | one configuration each (individual-pattern CSV) | What does each pattern do on its own, compared with the baseline? |
| **Stress** | `analysis-fl-stress-c{4,8,10}-{image,text}.ipynb` | one client count and one task, all 8 configurations, at the common environment point | For a fixed system structure and task, how do accuracy and round time change as more patterns (and pattern instances) are active? |

### Overview notebook

It is the reference for the whole campaign: the spec check, tradeoff regions, feature
importance and boxes over all runs. Its tradeoff edges are detected on all runs.
Because tasks, client counts and environments are mixed, its boxes are dominated by those
factors. Use it to see what dominates, not to conclude about individual patterns.
Its Section 6b (pattern stress) runs here too, but over mixed tasks and environments; the
stress notebooks give the controlled version.

### Pattern notebooks

Each keeps the runs of one configuration (the baseline, or one pattern alone), to
characterize that pattern in isolation: the base paper's single-pattern setting.

- They load the individual-pattern CSV.
- They share **fixed tradeoff edges**, detected on that full CSV
  (`'final_val_accuracy': [0.2075, 0.4774, 0.7473, 1.0172]`,
  `'avg_total_time': [1.693, 9.5935, 17.494, 25.3945]`). A region therefore means the same
  in all four notebooks, and densities can be compared across them.
- `--include-baseline` generates `*-vs-baseline` variants that keep the baseline runs, so
  a pattern is compared with not applying it.
- **Caveat:** within each notebook, client counts, tasks and environments still vary.

### Stress notebooks

Each fixes everything except the configuration, so differences between runs are pattern
effects:

| Fixed factor | Why |
|:---|:---|
| **Client count** | The system structure changes with the number of clients: more clients means more pattern instances, other round times (max ~25 s with 4 clients vs. ~17 s with 8 or 10), and a different effect of excluding clients. Comparing pattern stress across client counts would mix the two. |
| **Task** | Accuracy differs widely between the tasks (text: 0.52-0.92, mean 0.88; image: 0.31-0.60, mean 0.51), so the task would dominate every comparison, as `Model` did in the earlier FL data. |
| **Environment** (`ENVIRONMENT = 'common'`) | The waves did not run every configuration at every environment point: `ON,ON,ON`, for instance, was only run at 25% low-spec, 25% non-IID, 25% delay. That point is the only one shared by all 8 configurations, and there the design is a balanced full factorial: 10 runs per configuration (80 per notebook). |

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

- **`Pattern Types Active`** (S_types, 0-3): number of pattern decisions ON in `config_id`.
  It is fixed by the configuration and declared as a lever.
- **`Pattern Instances`** (S_inst): sum of `Client Selector Instances`,
  `Message Compressor Instances` and `HDH Instances`. The same pattern type can have
  several instances, so S_inst depends on the configuration *and* on the environment. The
  instance counts are declared as uncertainties; boxes on them read as conditional
  prescriptions.
- `Participating Clients` is added too (not declared in the spec: it is an effect of the
  client selector, not a factor).

### Assumptions (to confirm)

The CSVs record no pattern instances, so they are derived from per-client columns:

| ID | Assumption | Status |
|:---|:---|:---|
| A1 | The client selector has **one** instance, on the server. | Unconfirmed |
| A2 | The message compressor has **one instance per participating client**; the server-side decompression is not counted. | Unconfirmed |
| A3 | HDH has **one instance per participating non-IID client**. | Unconfirmed |
| A4 | A client participates iff it exists in the run (index ≤ `Total Clients`) and its `CPU Usage Avg` is recorded. | Verified on all 2,340 runs: with the selector ON, the participants are exactly the non-low-spec clients; with it OFF, all clients participate. |
| A5 | A client is non-IID iff its `Data Distribution` is `non-IID`. | Verified: the count equals `non_iid_clients` in every run. |
| A6 | Task = (Dataset, Model): CIFAR-10 + CNN 16k, AG_NEWS + MLP. | Verified: no other pairs occur. |

The rules live in `pattern_stress.INSTANCE_RULES`; changing an assumption is a one-line
change there.

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
- **The selector reduces instance stress.** With 10 clients, `ON,ON,ON` carries 9-11
  instances against 12-18 for `OFF,ON,ON`, because excluded clients take their compressor
  and HDH instances with them.

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
