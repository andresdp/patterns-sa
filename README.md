# ADEPT-FL

![ADEPT-FL logo](docs/adept-fl-logo.svg)

**Architectural Decision Exploration and Pattern Tradeoffs in Federated Learning**

ADEPT-FL applies ADEPT’s design-space analysis to federated-learning (FL) systems. It combines run data and an FL system definition with pattern-aware preprocessing, tradeoff analysis, sensitivity analysis, and parameter-rule inference.

The analyzed patterns are Client Selector, Heterogeneous Data Handler (HDH), and Message Compressor. The main outcomes are model accuracy (maximize) and average total round time (minimize). Pattern decisions, stress levels, federation size, client heterogeneity, and delay describe the design space.

## Analysis workflow

![ADEPT-FL analysis workflow from Figure 2 of the paper](docs/adept-fl-workflow-fig2.png)

The workflow has three phases: **Data Exploration** configures the system, loads run data, and defines tradeoff regions; **Sensitivity Analysis** examines how design choices map to the target regions; **Scenario Discovery** infers parameter rules (boxes) for selected outcomes. The paper’s prose also describes the third phase as constraint inference. The paper labels the middle phase “Sensitive Analysis” in the diagram and “Sensitivity Analysis” in the text.

## Federated-learning round

![Federated-learning training loop from Figure 1 of the paper](docs/federated-learning-loop-fig1.png)

Figure 1 shows the underlying FL execution cycle: the server broadcasts global model parameters, clients train locally, clients return updated parameters, and the server aggregates them for the next round. Figure 2 above shows how ADEPT-FL analyzes the resulting run data.

## Reproduce the paper analyses

Precomputed FL run data is included, so reproducing the analyses does not require running FL training again. The two CSV inputs and the system definition are in `federatedlearning/compact/`.

Set up the Python environment from this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run a research question at a time, or run all four:

```bash
./federatedlearning/compact/run_paper_analyses.sh RQ1
./federatedlearning/compact/run_paper_analyses.sh RQ2
./federatedlearning/compact/run_paper_analyses.sh RQ3
./federatedlearning/compact/run_paper_analyses.sh RQ4
./federatedlearning/compact/run_paper_analyses.sh all
```

The runner executes the image and text notebooks for the selected question. To run one notebook manually, activate the environment, launch Jupyter from this directory, and open the notebook listed below:

```bash
jupyter lab
```

| Question | What it analyzes | Notebooks (for both `image` and `text`) |
|---|---|---|
| RQ1 | Each pattern enabled in isolation, across its stress levels | `analysis-fl-rq-stress-only-client_selector-*`, `analysis-fl-rq-stress-only-hdh-*`, `analysis-fl-rq-stress-only-message_compressor-*` |
| RQ2 | Supported two- and three-pattern combinations at 25%, 50%, and 75% stress | `analysis-fl-rq-combined-patterns-stress-{25,50,75}-*` |
| RQ3 | All pattern configurations at the smallest and largest federation sizes in the paper (4 and 10 clients) | `analysis-fl-rq-c4-*`, `analysis-fl-rq-c10-*` |
| RQ4 | Full-design constraint inference for the target tradeoff | `analysis-fl-rq-full-design-*` |

The `analysis-fl-rq-baseline-*` and `analysis-fl-rq-c8-*` notebooks are supporting analyses for the included data snapshot; they are not needed for the paper’s four RQs. Run them separately with `./federatedlearning/compact/run_paper_analyses.sh supporting`.

Notebook execution writes plots and box reports under the matching `image/` or `text/` directory. The two precomputed CSVs are `adept_experiments_all_waves.csv` and `adept_experiments_all_waves_combinedAP.csv`; `FLsystem_compact_all.json` declares their schema, aggregations, parameters, and outcome measures.

## FL data generation

The bundled CSVs are precomputed runs of a Flower-based FL platform and are the inputs used for the paper analyses. Reproducing the analyses does not require the platform or new FL runs.

To generate a new campaign, use the anonymized platform snapshot in [`fl-platform/`](fl-platform/README.md). It contains only the code needed to run the experiment matrices locally with Docker (Linux host, Docker with the Compose plugin, Python 3.12 or newer):

```bash
cd fl-platform
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_adept_campaign.py --dry-run            # single-pattern campaign, 1,380 runs
python run_adept_campaign_combinedAP.py --dry-run # combined-pattern campaign, 960 runs
```

Drop `--dry-run` to execute the campaigns. Runs are serial and resumable; [`fl-platform/README.md`](fl-platform/README.md) lists the options and the CPU settings used for the bundled data.

New campaign output is not substituted into the included precomputed inputs automatically. Confirm its settings and schema before using it in the notebooks.
