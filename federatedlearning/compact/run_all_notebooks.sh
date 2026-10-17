#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
SCOPE_GUIDE="$SCRIPT_DIR/NOTEBOOK_STRATIFICATION.md"
CLEAN_OUTPUTS=""

usage() {
  cat <<'EOF'
Usage: ./federatedlearning/compact/run_all_notebooks.sh [--clean | --keep]

Execute every maintained compact image and text notebook sequentially with the
perfmodels conda environment. By default, ask whether to clear each task's
plots/ and boxes/ folders before execution.

  --clean  Clear existing contents of image/text plots/ and boxes/ first
  --keep   Keep existing contents; notebooks may overwrite their own outputs
  -h       Show this help
EOF
}

while (($#)); do
  case "$1" in
    --clean|--keep)
      if [[ -n "$CLEAN_OUTPUTS" ]]; then
        echo "Choose only one of --clean or --keep." >&2
        exit 2
      fi
      CLEAN_OUTPUTS="$1"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ -z "$CLEAN_OUTPUTS" ]]; then
  if [[ -t 0 ]]; then
    printf 'Clear prior contents of image/text plots/ and boxes/ before regenerating? [y/N] '
    IFS= read -r answer || answer=""
    case "$answer" in
      y|Y|yes|YES|Yes) CLEAN_OUTPUTS="--clean" ;;
      *) CLEAN_OUTPUTS="--keep" ;;
    esac
  else
    CLEAN_OUTPUTS="--keep"
    echo "Non-interactive input detected; keeping existing outputs. Use --clean to clear them." 
  fi
fi

if [[ "$CLEAN_OUTPUTS" == "--clean" ]]; then
  for task in image text; do
    for output_dir in "$SCRIPT_DIR/$task/plots" "$SCRIPT_DIR/$task/boxes"; do
      mkdir -p -- "$output_dir"
      find "$output_dir" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
    done
  done
  echo "Cleared prior plots and box reports."
fi

for task in image text; do
  task_dir="$SCRIPT_DIR/$task"
  notebooks=("$task_dir"/analysis-fl-rq-*-"$task".ipynb)
  if ((${#notebooks[@]} == 0)) || [[ ! -e "${notebooks[0]}" ]]; then
    echo "No matching $task notebooks found in $task_dir" >&2
    exit 1
  fi

  echo "Executing ${#notebooks[@]} $task notebooks..."
  for notebook in "${notebooks[@]}"; do
    echo "[$task] ${notebook##*/}"
    conda run --no-capture-output -n perfmodels python -m nbconvert \
      --execute --inplace --ExecutePreprocessor.timeout=1800 "$notebook"
  done
done

for task in image text; do
  echo "Validating $task notebook artifacts and refreshing its evidence manifest..."
  conda run --no-capture-output -n perfmodels python \
    "$REPO_ROOT/.claude/skills/adept-compact-findings/scripts/inventory_inputs.py" \
    --task "$task" \
    --scope-guide "federatedlearning/compact/NOTEBOOK_STRATIFICATION.md" \
    --notebook "federatedlearning/compact/$task/analysis-fl-rq-*-$task.ipynb"
done

echo "All compact notebooks executed and artifact inventories validated."
