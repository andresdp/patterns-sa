
* **Architectural Pattern**: It defines a predefined vocabulary of design elements for a system or a portion of it. It can belong a specific domain (e.g., microservices). A pattern comes with variants (decisions), parameters and design assumptions that define the pattern behavior. A pattern is usually instantiated (or embodied) in a given system, and the variants and parameters are bound to concrete values.

* **System Architecture**: It's an instantiation of either a single architectural pattern or a composition of architectural patterns. It is the main artifact to be analyzed quantitavely and explained.

* **Quality Objective**: It refers to a non-functional property of the system, which is often evaluated quantitatively by a given metric (e.g., latency for the quality of performance). The value of the metric is affected by the system behavior, which is directly influenced by the pattern(s) embodied in the system.

* **Quality Tradeoff**: It refers to a joint analysis of two or more quality objectives (or two metrics for the same quality objective). Generally, improving (e.g., maximizing) one objective comes at the cost of degrading other objective(s), but there can be cases in which two (or more) objectives can be simultaenously improved.

* **Configuration Space**: It the set of all the possible instances or candidates for a system architecture. These candidates are often obtained based on the degrees of freedom of the patterns embodied in the system or additional system parameters.

* **Quality Space**: It defines a set of quality objectives for the system, and maps every instance in the configuration space to a multi-valued vector based on the metrics for the quality objectives. The mapping is usually implemented by an external analyzer.

* **Architecture Space**: It is an abstraction that encompases both the configuration space and the quality space.

* **Architecture Analysis**: It refers to performing a particular data-driven investigation on a predefined architecture space or any of its sub-parts. The investigation should be oriented to get insights about: tradeoffs, key decisions, key parameters, best candidates, or robustness of certain candidates for quality objectives of interest, among others.