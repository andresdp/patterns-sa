# FL platform snapshot (campaign runner)

This folder is a reduced, anonymized snapshot of the Flower-based FL platform that produced the run data in `federatedlearning/compact/`. It contains only what is needed to re-run the pattern-stress campaigns locally with Docker. It is **not** needed to reproduce the paper analyses, which use the bundled CSVs.

## Contents

| Path | Purpose |
|---|---|
| `run_adept_campaign.py` | Headless runner for the single-pattern campaign (baseline + Client Selector, Message Compressor, HDH; 1,380 runs) |
| `run_adept_campaign_combinedAP.py` | Runner for the combined-pattern campaign (CS+MC, CS+HDH, MC+HDH, CS+MC+HDH; 960 runs) |
| `Docker/` | Flower server/client code, pattern implementations, Dockerfiles and compose file used by the runner |
| `Local/` | Same code for Flower simulation mode; the runner also uses it to cache the datasets |
| `tests/` | Unit tests for the runner and the data partitioning |

## Requirements

Linux host, Docker with the Compose plugin, Python 3.12 or newer.

```bash
cd fl-platform
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the campaigns

Inspect the experiment matrix first (nothing is executed):

```bash
python run_adept_campaign.py --dry-run
python run_adept_campaign_combinedAP.py --dry-run
```

Run them (20 rounds per run, 10 repetitions/seeds per configuration):

```bash
python run_adept_campaign.py --continue-on-error
python run_adept_campaign_combinedAP.py --continue-on-error
```

Runs execute serially so that concurrent workloads do not affect the timing measurements. The campaign is resumable: re-running the same command skips completed runs. Useful options: `--only-wave N` (run only repetition/seed N), `--configurations "ON,OFF,OFF"` (filter, CS,MC,HDH order), `--output-dir`, `--rounds`.

Client resources are set with `--host-cpus`, `--server-cpus`, `--low-spec-cpus` and `--high-spec-cpus`. The bundled data was collected with 2 CPUs for the server, 7 for low-spec clients and 12 for high-spec clients on a 112-core host:

```bash
python run_adept_campaign.py --host-cpus 112 --server-cpus 2 --low-spec-cpus 7 --high-spec-cpus 12 --continue-on-error
```

On a smaller machine, scale these values down; absolute round times will then differ from the bundled data.

Results (one CSV row per run plus per-client, per-round metrics) are written under `pattern_stress_docker_results/` (or `--output-dir`). New results are not substituted into `federatedlearning/compact/` automatically; check settings and schema before using them in the notebooks.

## Tests

```bash
python -m unittest discover -s tests
```
