#!/usr/bin/env bash
set -Eeuo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

run_question() {
  local question="$1"

  for task in image text; do
    local task_dir="federatedlearning/compact/$task"
    local notebooks=()

    case "$question" in
      RQ1)
        notebooks=("$task_dir"/analysis-fl-rq-stress-only-*-"$task".ipynb)
        ;;
      RQ2)
        notebooks=("$task_dir"/analysis-fl-rq-combined-patterns-stress-{25,50,75}-"$task".ipynb)
        ;;
      RQ3)
        notebooks=(
          "$task_dir/analysis-fl-rq-c4-$task.ipynb"
          "$task_dir/analysis-fl-rq-c10-$task.ipynb"
        )
        ;;
      RQ4)
        notebooks=("$task_dir/analysis-fl-rq-full-design-$task.ipynb")
        ;;
      supporting)
        notebooks=(
          "$task_dir/analysis-fl-rq-baseline-$task.ipynb"
          "$task_dir/analysis-fl-rq-c8-$task.ipynb"
        )
        ;;
      *)
        echo "Unknown analysis group: $question" >&2
        return 2
        ;;
    esac

    for notebook in "${notebooks[@]}"; do
      if [[ ! -f "$notebook" ]]; then
        echo "Missing expected notebook: $notebook" >&2
        return 1
      fi
      echo "[$question] Executing $notebook"
      python -m nbconvert \
        --execute --inplace --ExecutePreprocessor.timeout=1800 "$notebook"
    done
  done
}

selection="${1:-all}"
case "$selection" in
  RQ1|RQ2|RQ3|RQ4|supporting)
    run_question "$selection"
    ;;
  all)
    for question in RQ1 RQ2 RQ3 RQ4; do
      run_question "$question"
    done
    ;;
  -h|--help)
    cat <<'EOF'
Usage: ./federatedlearning/compact/run_paper_analyses.sh [RQ1|RQ2|RQ3|RQ4|all|supporting]

Run the image and text notebooks for one paper research question. The default
`all` runs RQ1 through RQ4. `supporting` runs baseline and c8 analyses that are
included with the precomputed data but are outside the paper's four RQs.
EOF
    ;;
  *)
    echo "Choose RQ1, RQ2, RQ3, RQ4, all, or supporting." >&2
    exit 2
    ;;
esac
