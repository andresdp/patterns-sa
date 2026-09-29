# Policy Grouping in Robustness Analysis

**Status:** Implemented (2026-09-27)
**Code:** `PatternAnalysis` policy-grouping helpers in `adept/core/session.py` (`_policy_label_frame`, `_policy_labels`, `_policy_mask`)
**Tests:** `tests/test_policy_grouping.py`

## The Problem

Robustness results are reported per *policy*, but "policy" means two different things:

| Meaning | Example (Federated Learning) | Where it comes from |
|---|---|---|
| **Configuration**: the combination of policies chosen for every decision | `OFF,ON,OFF` | one value of the configuration column (`dataspace.configuration_identification.column`) |
| **Decision policy**: the policy chosen for a single decision | `ON` for `hdh_pattern` | the decision/policy references of each configuration |

In a **single-decision** system (CQRS, Gateway Offloading, ...) the two are the same:
configuration `no-offloading` *is* the policy `no-offloading`. The robustness API was
written under that assumption and mixed both meanings freely.

In a **multi-decision** system such as the Federated Learning example (three ON/OFF
decisions), mixing them broke in two ways:

1. **Crash.** `get_robustness_results` iterated configurations (`OFF,OFF,OFF`, ...) but
   looked each one up as a decision policy, raising `ValueError: Policy 'OFF,OFF,OFF' not found`.
2. **Silently wrong numbers.** Plain policy names repeat across decisions (`ON`, `OFF`).
   Lookups picked the *first* decision that had the name, so a baseline robustness report
   with rows `OFF`/`ON` actually described the client selector decision only, and was then
   compared against box-constrained matrices whose rows were configurations.

## The Resolution

Every robustness method now maps a policy label to experiment rows through one helper
(`_policy_mask`), and reports rows according to an explicit **grouping**, selected with a
`by` argument:

| `by` | Rows | FL example | Gateway Offloading |
|---|---|---|---|
| `'configuration'` (default) | one per configuration | `OFF,OFF,OFF`, `ON,OFF,OFF`, `OFF,ON,OFF`, `OFF,OFF,ON` | `no-offloading`, ... |
| `'decision'` | one per (decision, policy), labeled `decision:policy` | `client_selector_pattern:ON`, ..., `hdh_pattern:OFF` | `offloading_strategy:no-offloading`, ... |
| a decision key | one per policy of that decision, plain labels | `by='hdh_pattern'` gives `ON`, `OFF` | `by='offloading_strategy'` gives `no-offloading`, ... |

Decision keys may be written as `'Component:Decision'` or just `'Decision'` when unambiguous.

### Resolving a label without `by`

Methods that receive a single label (`compute_robustness`, `get_tradeoff_impact_matrix`,
`show_stability_radius`) accept `by=None`, in which case the label is resolved as:

1. a configuration (`'OFF,OFF,ON'`, `'no-offloading'`),
2. a qualified decision policy (`'hdh_pattern:ON'`),
3. a plain decision policy name, **only if exactly one decision has it**.

A plain name shared by several decisions (`'ON'` in FL) raises
`ValueError: Policy 'ON' is ambiguous ...`, suggesting `'hdh_pattern:ON'` or `by='hdh_pattern'`.
This is deliberate: the previous behavior silently answered for an arbitrary decision.

### Methods that take `by`

| Method | Default | Notes |
|---|---|---|
| `get_robustness_report` | `'configuration'` | `decision_key=X` is kept as shorthand for `by=X` |
| `get_policy_robustness_ranking`, `show_robustness_heatmap` | `'configuration'` | forwarded to `get_robustness_report` |
| `get_policy_robustness_improvement_matrix` | `'configuration'` | `'decision'` stacks one block per decision |
| `show_policy_robustness_comparison_heatmap` | `'configuration'` | used for the matrices it computes itself |
| `analyze_robustness_uplift` | `'configuration'` | `'decision'` gives one row per decision policy plus a single `GLOBAL` row |
| `get_robustness_results` | `'configuration'` | groups with no rows in the test subset are skipped with a warning |
| `compute_robustness`, `get_tradeoff_impact_matrix`, `show_stability_radius` | `None` (auto-resolve) | see above |

When a pre-computed baseline is passed (`get_robustness_results(baseline=...)`,
`show_policy_robustness_comparison_heatmap(baseline_matrix=...)`) and its rows do not match
the other matrix, a warning is printed: the two were built with different groupings.
Compute both with the same `by`.

## Choosing a Grouping

* **`'configuration'`** answers *"which system configuration is most robust?"*. Each row is
  one concrete configuration, so rows never overlap. With few experiments, each group is
  small (FL: ~10 test rows across 4 configurations), so values rest on very few points.
* **`'decision'` / a decision key** answers *"does enabling pattern X improve robustness?"*.
  Groups are larger (`OFF` pools every configuration where X is off), but rows overlap across
  decisions and each row mixes different states of the *other* decisions. This matches the
  per-decision contingency analysis (`show_policy_contingency(decision_key=...)`).

## Backward Compatibility

For single-decision systems all groupings select identical rows, and the default
`'configuration'` labels equal the former policy names in the same order. This was verified
on Gateway Offloading by snapshotting 156 robustness outputs (reports, rankings, per-policy
metrics, impact/coverage/improvement matrices, uplift, aggregates and `get_robustness_results`,
for STARR and REGRET) before the change and comparing them after it: all identical.

For multi-decision systems, results change by design: default reports now have configuration
rows instead of the ambiguous `OFF`/`ON` rows, and plain shared names raise instead of
matching the first decision. Notebooks that relied on `OFF`/`ON` rows should pass
`by='<decision>'` explicitly.
