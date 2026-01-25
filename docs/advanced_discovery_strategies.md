# Advanced Box Discovery Strategies for ADEPT

This document expands on advanced algorithms and heuristics for inferring architectural "boxes" (hyper-rectangles) that characterize specific tradeoff regions.

## 1. Anchors (High-Precision Local Explanations)

**Concept:** Anchors represent a "sufficient" set of conditions (predicates) such that the outcome is almost always the same, regardless of the values of other parameters.

**Mechanism:**
- It uses a perturbation-based approach to find a rule that "anchors" a prediction.
- For a successful architectural configuration, an Anchor identifies the minimal constraints (e.g., `Memory > 16GB` and `Latency < 50ms`) that guarantee the target tradeoff with high precision (e.g., >95%).

**Why for ADEPT:**
- **Robustness vs. Brittleness:** Unlike Skope-rules, which can be brittle because they depend on the specific paths of an ensemble forest, Anchors are model-agnostic. They focus on the *stability* of the success region.
- **Local-to-Global:** Architects often have a "Gold Standard" design. Anchors mathematically define the "Safe Zone" around that design, showing how much you can deviate before the tradeoff is lost.

---

## 2. Genetic Algorithms (Direct Box Optimization)

**Concept:** Instead of using greedy heuristics (like the splitting in CART or the peeling in PRIM), Genetic Algorithms (GA) treat the box boundaries as a chromosome to be optimized.

**Mechanism:**
- **Population:** A set of candidate boxes.
- **Crossover/Mutation:** Boundary values (min/max) are swapped or slightly shifted.
- **Fitness Function:** A multi-objective score: `Fitness = w1*Density + w2*Coverage - w3*Complexity`.
- **Complexity Penalty:** You can explicitly favor boxes that restrict fewer parameters, making them more interpretable.

**Why for ADEPT:**
- **Global Search:** GAs can escape local optima that greedy algorithms might fall into. If the success region is non-convex or has "holes," a GA can find a box that captures the most significant cluster without being misled by a single bad split.
- **Custom Constraints:** You can force the algorithm to prioritize specific "expensive" parameters that the architect wants to keep unrestricted.

---

## 3. Bayesian Optimization (Data-Efficient Region Finding)

**Concept:** Uses a probabilistic surrogate model (typically a Gaussian Process) to map the parameter space to the probability of satisfying a tradeoff.

**Mechanism:**
- It builds a "landscape" of success probabilities.
- An acquisition function guides the search to find the boundaries (the "level sets") where the probability of success is high.
- It iteratively refines the estimate of the "Box" boundaries where the tradeoff target is reliably met.

**Why for ADEPT:**
- **Efficiency:** Ideal for cases where running simulations is expensive (e.g., a simulation takes 5 minutes). It finds the "Success Box" with significantly fewer samples than CART or PRIM.
- **Uncertainty Awareness:** It provides a confidence interval for the box boundaries, telling the architect: "I am 90% sure that if you stay within these bounds, you satisfy the tradeoff."

---

## 4. Implementation via the Optuna Framework

The Optuna framework, while traditionally used for Hyperparameter Optimization (HPO), is exceptionally well-suited for Scenario Discovery by "inverting" the problem: treating **box boundaries** as the variables to be optimized.

### Inverting the Objective Function
In an ADEPT context, the "objective function" is not a simulation run, but a **Box Evaluator** that runs against the existing `experiments_df`.
* **Search Space:** For each parameter $P_i$, Optuna suggests two values: $P_{i, min}$ and $P_{i, max}$.
* **Goal:** Maximize a fitness score derived from `Density` and `Coverage`.

### Bayesian Optimization via `TPESampler`
Optuna’s default **TPE (Tree-structured Parzen Estimator)** can be used for refined, data-efficient discovery.
* **Mechanism:** TPE learns the probability distribution of "good" vs "bad" box boundaries. It is highly effective at discovering correlations between parameters (e.g., how the required bound for `Memory` shifts as `CPU` constraints are tightened).
* **Mitigation of Brittleness:** By using a smooth probabilistic model (Parzen Estimators) rather than discrete tree splits, it identifies regions of stability rather than single paths.

### Genetic Algorithms via `NSGAIISampler`
The **NSGA-II (Non-dominated Sorting Genetic Algorithm II)** in Optuna is perhaps the most robust option for architectural analysis.
* **Multi-Objective Pareto Discovery:** Box discovery is inherently a conflict between `Density` (Precision) and `Coverage` (Recall). NSGA-II can optimize both simultaneously, returning a **Pareto Front of Boxes** instead of a single result.
    * *Example:** The architect can choose between a "Strict Box" (99% density, 10% coverage) and a "Flexible Box" (80% density, 70% coverage).
* **Interpretability Constraints:** GAs allow for custom penalties in the fitness function. We can explicitly penalize "complexity" (e.g., boxes that restrict too many parameters), favoring cleaner, more actionable architectural rules.

### Advantages of the Optuna Approach
1. **Constraint Handling:** Optuna naturally handles dependent constraints (e.g., ensuring $P_{max} \geq P_{min}$) and categorical levers.
2. **Parallelization:** Evaluating candidate boxes against a DataFrame is a "embarrassingly parallel" task; Optuna can test thousands of boxes across multiple cores in seconds.
3. **Persistence:** Discovery studies can be saved to a database (via SQLAlchemy), allowing architects to resume discovery or refine boxes as new simulation data becomes available.
4. **Visualization:** Optuna's built-in contour and importance plots can be repurposed to show which parameter boundaries are most sensitive for maintaining a tradeoff.

---

## 5. Semantic Discovery: LLM-Enhanced Bayesian Optimization (LLaMBO)

While traditional Bayesian Optimization (BO) relies on Gaussian Processes or TPE, a new paradigm involves using Large Language Models (LLMs) to guide the search. A prominent example is **LLaMBO** (Large Language Models to Enhance Bayesian Optimization), now available via **OptunaHub**.

### The LLaMBO Perspective
LLaMBO treats the discovery process as a conversation between the optimizer and the architectural context. Instead of seeing parameters as anonymous vectors, it understands their semantics.

1.  **Zero-shot Warmstarting:** 
    *   Instead of starting with random boxes, the LLM analyzes the pattern name (e.g., *Anti-Corruption Layer*) and the quality goals. It proposes a "Warmstart" box based on its internal knowledge of common architectural bottlenecks.

2.  **Few-shot Surrogate Modeling:** 
    *   Traditional models (GPs) require many points to "understand" the success region. LLaMBO uses the LLM's few-shot learning capability to predict the performance of a candidate box after seeing only a handful of examples.

3.  **Candidate Suggestion via Natural Language:** 
    *   The optimizer describes the current results in natural language: *"We found that lower server counts lead to high latency, but very high counts cause contention."* The LLM then suggests a refined box boundary to test next.

### Why LLaMBO for ADEPT?
*   **Mitigating Brittleness:** By grounding the search in architectural concepts, LLaMBO is less likely to get lost in "noisy" regions of the data that might confuse a purely numerical algorithm like CART or Skope-rules.
*   **Domain-Aware Priors:** It injects "Architectural Common Sense" into the discovery process. For example, it knows that `CacheSize` usually has a diminishing return, helping the optimizer focus on the most impactful regions.
*   **Interpretability by Design:** Because the "surrogate model" is a language model, the reason for choosing a specific box can be extracted in plain English: *"I am testing this box because it balances the parallelization benefits of the Backend component with the increased coordination costs of the Gateway."*

### Integration with OptunaHub
LLaMBO is implemented as a custom `Sampler` in Optuna. In an ADEPT session, this would look like:

```python
import optunahub
# Load the LLaMBO sampler from the community hub
sampler = optunahub.load_module("samplers/llambo").LLaMBOSampler()

study = optuna.create_study(sampler=sampler, direction="maximize")
# The LLM-guided search for box boundaries begins here...
```

---

## 6. The LLM as an Architectural Explainer

Beyond inferring box boundaries, Large Language Models provide a **"Semantic Bridge"** that transforms mathematical findings into actionable architectural knowledge. This fundamentally changes the ADEPT workflow in four key ways:

### 1. From "What" to "Why" (Causal Hypothesis)
While algorithms like PRIM identify *what* the bounds are (e.g., "Servers between 5 and 8"), an LLM can synthesize this with the architectural pattern (e.g., *CQRS*) to hypothesize *why*:
* **LLM Perspective:** *"The restricted upper bound on servers (8) suggests a synchronization bottleneck in the Command-side bus. In a CQRS pattern, adding more command-side nodes likely increases consensus overhead beyond the benefits of parallelization."*
* **Value:** It turns a mathematical "box" into a grounded **design rationale**.

### 2. Semantic Parameter Prioritization
Currently, discovery algorithms treat all parameters as anonymous numbers. An LLM understands their semantic meaning and can guide the optimization.
* **LLM Perspective:** *"You are analyzing a 'Database' component. Historically, 'Connection Pool Size' and 'Disk I/O' are the most critical bottlenecks for 'Response Time'. I recommend prioritizing the search in these subspaces for box discovery."*
* **Value:** It reduces the search space for Genetic Algorithms or Bayesian Optimization by injecting **architectural intuition**, making the process faster and less "brittle."

### 3. Rule Synthesis (Simplifying the Union of Boxes)
Discovery processes like CART often identify multiple disjoint success regions (leaves) that are difficult for a human to memorize or apply as a single policy.
* **LLM Perspective:** It can take 10 sets of disjoint rules and synthesize them into a single, cohesive human policy: *"To satisfy the High-Availability tradeoff, you must either scale vertically (using 'Type B' instances) or ensure the 'Load Balancer Timeout' is under 500ms when scaling horizontally."*
* **Value:** It **compresses** complex mathematical regions into actionable, easy-to-communicate architectural policies.

### 4. Cross-Project Knowledge Retrieval
The LLM can cross-reference discovered boxes with an architectural corpus (e.g., the papers in `papers/`) to provide external validation.
* **LLM Perspective:** *"The box you found for the Anti-Corruption Layer matches the performance profile described in the 2023 ICSA paper on Microservices Gateways. That study indicates this specific constraint is usually caused by excessive serialization overhead."*
* **Value:** It connects local simulation results to **industry-wide patterns and pitfalls**.

---

## Comparison Summary

| Strategy | Primary Strength | Mitigation for "Brittleness" | Perspective |
| :--- | :--- | :--- | :--- |
| **Anchors** | Guaranteed Precision | Focuses on local stability. | Local/Sufficient |
| **Genetic (NSGA-II)** | Global Optimality | Does not rely on greedy splits. | Exploratory/Pareto |
| **Bayesian (TPE)** | Sample Efficiency | Uses smooth probabilistic models. | Refined/Probabilistic |
| **LLaMBO** | Semantic Intuition | Grounded in architectural meaning. | Contextual/Knowledge-Rich |

### Note on Skope-rules
Skope-rules often feel brittle because they are highly sensitive to the diversity of the underlying Random Forest. If the forest is overfitted or biased, the extracted rules inherit that fragility. The strategies above (especially GA, BO, and LLaMBO) offer a more "holistic" search for boundaries that is less dependent on the vagaries of a specific decision tree ensemble.