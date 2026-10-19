# Specification context for ADEPT box explanations

**Date:** 2026-10-12. **Status:** initial implementation available. **Scope:** a syntactic explanation of a decoded box, using relationships declared in the system specification and ADEPT's conceptual model.

## 1. Purpose

An ADEPT box is a conjunction of parameter conditions. Showing each condition in a list gives its value, but may omit how pattern-setting values relate to decisions and their policies. Add a small specification-aware layer that traces the conditions through the declared design model and presents them together.

This layer explains only what the specification says. It does not read the campaign records, infer mechanisms, causal effects, measurement-availability relationships, or unstated applicability rules. It does not claim that a condition contributed independently to the outcome. ADEPT's existing box metrics remain a separate empirical result.

## 2. The syntactic model

Use only these declared entities and relationships:

- A **component** declares parameters and decisions.
- A **decision** offers named **policies**.
- A policy can bind values to declared parameters.
- A **system configuration** selects policies, through its declared policy references.
- Each parameter has a declared role, such as lever, uncertainty, or constraint.
- A box condition constrains a parameter to a decoded value, set, or range.

The resulting trace is:

```text
box condition ──constrains──> parameter ──declared in──> component
                                      ▲
                                      └──── bound by ─── policy <── selected by ── configuration

parameter ──has declared role──> lever | uncertainty | constraint
```

The arrows represent specification structure. In particular, a parameter's `uncertainty` role does not create an arrow from that parameter to a decision or policy. If the specification declares no such link, the explanation says so.

### What can be concluded from each link

| Declared link | Explanation may say | Explanation must not add |
|:---|:---|:---|
| Component declares parameter | The condition concerns a parameter declared for that component | That the component's policy caused an outcome |
| Policy binds parameter to value | The policy specifies a value that matches, conflicts with, or is not covered by the box condition | That the box necessarily requires this policy (the reverse implication may not be declared) |
| Configuration selects policy | This configuration includes the named policy | That unlisted configurations are infeasible or unobserved configurations are impossible |
| Parameter role is lever | ADEPT classifies it as a design lever | Any further parentage not in the specification |
| Parameter role is uncertainty | ADEPT classifies it as an uncertainty/operating condition | A parent decision, mechanism, or policy requirement |
| Parameter role is constraint | ADEPT classifies it as a constraint | A controllability interpretation not declared by the model |

## 3. Interpret the whole box

First decode conditions with the fitted encoder, as ADEPT already does. Resolve each decoded parameter by its declared identity and component. Then inspect all conditions together against policy bindings and configuration references.

For a binding such as `CS ON → Client Selector Criteria = CPU`, if the box says `Client Selector Criteria in {CPU}`, the explanation can report:

> This condition matches a value bound by the Client Selector ON policy.

For an optional pattern setting that is bound by a decision's policies, this implementation interprets its absence from a selected policy as the declared optional “not selected” state. This allows the explanation to distinguish a matching ON policy from a conflicting OFF policy for a condition such as `Criteria = CPU`. This is a syntactic reading of the JSON and the optional setting declaration; it does not assert that the policy caused the target outcome. For settings without this structural relationship, applicability remains unresolved.

For each explicitly declared system configuration, compare its selected policies and bindings with the **joint** box conditions. Report the result as:

- **matches declared bindings**: every relevant declared binding satisfies the box;
- **conflicts with declared bindings**: at least one relevant binding violates a box condition;
- **not determined by the specification**: a required value/applicability relationship is missing or a relevant parameter is unbound.

These labels describe specification consistency. They do not assert that the configuration was run, that an absent configuration is infeasible, or that a matched configuration achieves the target. Keep empirical support and target metrics in the existing box report; they are outside this syntactic layer.

A condition on a lever or uncertainty remains a condition on that variable. It can be grouped with other conditions in the human-readable sentence, but it should not be assigned a policy parent unless a policy binding actually exists. Thus `non_iid_percentage in [a,b]` is reported as an uncertainty condition. The JSON does not make it a requirement to enable HDH merely because both concern data heterogeneity.

### Compact FL examples

**Client Selector Criteria.** The system JSON declares this as a pattern parameter and the Client Selector ON policy binds it to `CPU`. A matching box condition can therefore be annotated with that binding and the configurations that explicitly select the ON policy. Since OFF has no corresponding explicit value binding, describe its setting applicability as unspecified unless the schema is extended to state it. Other ON bindings, such as the threshold, can be listed as declared policy context when useful; do not imply that they were themselves conditions in the box.

**Non-IID percentage.** Its declared role is uncertainty. Display the box's range and role; no decision-to-uncertainty link is added. This provides more context while keeping the architectural interpretation within the declared model.

**Several related conditions.** If a box constrains both selector criteria and selector strategy, display both under the same component/decision trace. State which conditions match the ON policy's bindings and which remain additional box restrictions. Do not present them as separate effects or erase a condition just because a policy binds a related value.

## 4. Minimal result shape and presentation

The rendered explanation lists the full settings for each required policy; the operating envelope keeps uncertainty conditions separate. Box conditions are evaluated jointly. The plain text or Markdown rendering is selected with `output_format="plain"` or `output_format="markdown"`. The compact output keeps the explanation on one line:

```text
Architectural interpretation • Design prescription: • Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0) • Message Compressor = ON (Algorithm = zlib) • Operating envelope: • non-IID percentage [25, 75] (%) • delay percentage [0, 50] (%)
```

The raw rule and existing box metrics remain visible in the notebook; this syntactic explanation adds grouped conditions and paths to the JSON locations that support each statement. Data-to-specification mismatches belong in a separate dataset/configuration audit, not in the specification-only trace.

## 5. ADEPT integration

The implementation is exposed as `PatternAnalysis.explain_box_context(box)`, delegated through `ArchSpaceCore` to `ExplanationManager` and `BoxContextExplainer`. It returns structured traces and rendered text. The implementation uses:

- `Box.readable_limits()` decodes numeric and categorical limits.
- `SystemDefinition` contains parameter roles, component parameters, policy bindings, system-configuration references, and column-renaming metadata.
- `ExplanationManager` currently renders a generic dictionary summary.
- `PatternAnalysis` has the loaded system definition and analysis context; `ArchSpaceCore.explain()` delegates to the explanation manager.

Proposed components:

| Addition | Responsibility |
|:---|:---|
| `BoxContextExplainer` | Join decoded conditions to declared parameters and policy bindings; group related settings and check declared configurations |
| `explain_box_context()` entry point | Supply the box and loaded specification, then return structured traces plus rendered text |

Keep this API separate from the existing generic `explain()` contract initially. An illustrative use is:

```python
explanation = analysis.explain_box(box)
print(explanation.text)
explanation.model_dump()
```

No causal graph, ontology, data-driven parent links, or detailed client-level analysis is used. The compact configuration set is checked by enumerating configurations explicitly declared in JSON.

### Configuration check semantics

Evaluate declared bindings condition by condition and then report the joint result for each declared configuration. For an optional pattern setting with policy bindings under the same decision, a selected policy that omits the setting is read as the optional “not selected” state. For other unbound parameters, mark the relationship as unspecified. Do not enumerate theoretical policy combinations unless the specification declares them feasible; distinguish explicitly declared configurations from possible combinations.

The direction matters. The optional-setting convention above applies only to a pattern setting with bindings under that decision. ADEPT may then report that a condition such as `x=CPU` is consistent with ON and excludes configurations whose selected policy leaves `x` not selected. It does not infer a causal effect or extend this reverse interpretation to unrelated parameters.

## 6. Acceptance criteria

- Every original decoded box condition remains present in the explanation.
- Each added statement traces to a declared JSON field or a named conceptual-model role.
- Conditions are grouped and checked jointly; the explanation does not claim separate condition effects.
- A binding is not reversed into a requirement without explicit support in the specification.
- Uncertainties remain uncertainties unless the specification explicitly links them elsewhere.
- Declared configurations are distinct from configurations merely observed in the CSVs.
- Specification consistency is distinct from box membership, target attainment, and held-out support.
- Missing or conflicting specification metadata is shown as such; dataset/specification discrepancies remain in the separate data audit.
- The prose adds context without changing box membership or its computed metrics.

This extension makes the basic box explanation more architectural and traceable while remaining a syntactic reading of ADEPT's declared design model. All performance findings remain observational.
