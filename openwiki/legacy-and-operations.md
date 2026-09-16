---
type: operations guide
title: Operations, CI, and repository boundaries
description: Runtime prerequisites and repository automation for legacy simulations, conductor artifacts, bundled assets, and scheduled OpenWiki updates.
tags: [operations, ci, jmt, openwiki]
---

# Operations, CI, and repository boundaries

The repository contains three operational layers: current ADEPT Python analysis, legacy/JMT replication, and repository documentation automation. `requirements.txt` pins the primary Python stack (pandas, NumPy, scikit-learn, SciPy, Pydantic, plotting, discovery, notebooks, and pytest). JMT runners additionally require Java/OpenJDK, a JMT single-jar runtime, configured paths, and writable temporary/output directories. `lib/` contains static third-party web assets (`bindings`, `tom-select`, `vis-9.1.2`) rather than Python runtime ownership. `conductor/` contains planning/product/workflow artifacts, not an application server.

## OpenWiki automation

`.github/workflows/openwiki-update.yml` runs manually or daily at cron `0 8 * * *`. It checks out full Git history (`fetch-depth: 0`), installs Node 22 and globally installs `openwiki@0.3.0`, Mermaid, and jsdom, then runs `openwiki code --update --print`. The command receives provider/model configuration and secret-backed integration credentials from GitHub Actions environment variables; secrets are operational inputs and are not part of this wiki.

The job has `contents: write` and `pull-requests: write`, and `peter-evans/create-pull-request` creates/updates branch `openwiki/update` with paths `openwiki`, `AGENTS.md`, `CLAUDE.md`, and the workflow. It uses commit title/message `docs: update OpenWiki`. Generated wiki output should therefore be reviewed as an automated PR and not hand-edited in source directories. The local equivalent is the narrowest available OpenWiki command for the installed CLI; validate Mermaid and links before accepting the PR.

Operational debugging: confirm full Git history, Node 22, package installation, repository secrets/permissions, and the workflow's generated diff. A failed provider/API run is not a source-code failure. A failed link or Mermaid validation is a generated-doc repair. Never copy secret values into logs, wiki pages, or source fixtures.

Safe boundaries: do not modify the bundled JAR or third-party `lib` assets for ADEPT changes; do not treat stale `docs/usage.md` references to absent Toy/tools modules as current runtime truth; do not execute large JMT grids without checking their Cartesian-product size. See [legacy case studies](./legacy/overview.md), [simulation recipes](./patterns/simulation-recipes.md), and [testing](./testing-and-development.md).
