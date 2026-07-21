# Social Network Analysis Reference

Use this reference when relationships, dependencies, paths, groups, or network-generating mechanisms are central. Define the network boundary and edge meaning before selecting metrics.

## 1. Network construction contract

Document:

- node population, inclusion/exclusion, and identity resolution;
- edge definition, direction, weight, sign, multiplicity, and time window;
- whether weights mean strength, frequency, probability, capacity, or distance/cost;
- directed/undirected, simple/multi-edge, bipartite/multimode, temporal, multiplex, or hypergraph structure;
- sampling/observation process, missing nodes/edges, censoring, and platform/API limits;
- projection, aggregation, thresholding, or symmetrization rules;
- the population or mechanism to which results are intended to generalize.

The observed graph is a measurement produced by these choices. Run boundary or threshold sensitivity when conclusions could change under another defensible construction.

Choose the graph class deliberately: `Graph`, `DiGraph`, `MultiGraph`, or `MultiDiGraph`. Preserve parallel edges or direction until the research question justifies collapsing them.

## 2. Descriptive quantities

### Components, paths, and distances

- Report isolates, weak/strong components, and the share of nodes in any analyzed giant component.
- Do not silently compute global path metrics only on the giant component. State the restricted population and consider harmonic closeness or reachability-aware alternatives.
- Convert strength weights to distances with a substantively justified transformation before shortest-path measures; raw strong-tie weights usually should not be treated as costs.

### Centrality

Tie each metric to a mechanism:

- degree/strength: local opportunity or activity;
- betweenness: potential brokerage on shortest paths;
- closeness/harmonic closeness: reachability under a path model;
- eigenvector/PageRank: recursive prominence under their flow assumptions.

Check direction, disconnectedness, weight semantics, and sensitivity to missing/duplicated edges. Centrality is not a generic measure of social importance. For costly measures such as betweenness, profile first and use documented approximation with uncertainty/seed when necessary.

### Bipartite and multimode networks

Analyze the two-mode network directly when possible. A one-mode projection creates cliques and loses event/context information. If projecting, state the projection rule, use an appropriate weighting/null model, and compare conclusions to the unprojected representation.

## 3. Community detection

Treat a community partition as an algorithm- and resolution-dependent summary, not discovered ground truth.

- Prefer Leiden over Louvain when supported because Louvain can return badly connected or internally disconnected communities; state the objective (modularity, CPM, etc.).
- Record algorithm/package version, weight/direction handling, resolution parameter, seed, stopping rule, and number/size of communities.
- Check internal connectedness and repeat across seeds. Explore a defensible resolution range; higher resolution usually yields more communities.
- Assess stability with an appropriate partition-similarity measure and inspect substantive membership changes.
- Compare against relevant metadata or external evidence without treating demographic correspondence as automatic validation.
- Report objective values for comparison, but do not select a partition by modularity alone or compare modularity across incompatible graphs/objectives.

If Leiden is unavailable or the project requires another method, explain the tradeoff and perform connectedness/stability checks rather than presenting Louvain as an unconditional default.

## 4. Degree distributions and power laws

A log-log plot or linear regression on logged frequencies is not evidence of a power law.

For a power-law claim:

1. State whether the distribution is discrete or continuous and what observations are independent enough for the model.
2. Estimate the lower cutoff `xmin` and exponent with maximum likelihood.
3. Use a simulation/bootstrap goodness-of-fit test based on a statistic such as KS.
4. Compare plausible alternatives (for example lognormal, exponential, stretched exponential, or truncated power law) with likelihood-based methods.
5. Report uncertainty, tail sample size, cutoff, and sensitivity to sampling, censoring, and degree definition.

Use CCDF/log-log plots as diagnostics and communication, not as the estimator. If evidence is weak, say the tail is heavy rather than declaring the network scale-free.

## 5. Null models and dependence

- Compare clustering, assortativity, motifs, or community structure to a null model that preserves the features irrelevant to the hypothesis (size/density, degree sequence, bipartite degrees, temporal activity, etc.).
- Generate enough null replicates to quantify Monte Carlo uncertainty and record their seeds.
- Respect network dependence. Node/edge observations are usually not iid, so ordinary regression standard errors or permutation schemes can be invalid.
- For homophily, distinguish preference/selection from opportunity, composition, and influence; assortativity alone does not identify the mechanism.

## 6. ERGM and related inferential models

Use the current R `statnet`/`ergm` ecosystem unless the project has a validated alternative. Define terms as hypotheses about tie formation and dependence, not as a feature shopping list.

Before fitting:

- verify directedness, loops, valued/binary response, missing dyads, constraints, sampling design, and network size;
- start from a defensible baseline such as edges plus required offsets/constraints;
- add nodal mixing/activity and dependence terms incrementally, guided by theory;
- use curved terms and decay parameters deliberately rather than as automatic anti-degeneracy fixes.

After fitting:

- inspect estimation/convergence messages and MCMC diagnostics;
- diagnose degeneracy and separation-like behavior;
- simulate networks from the fitted model and perform GOF on statistics not merely copied from the fitted sufficient statistics;
- compare observed and simulated degree, shared-partner, distance, mixing, and other substantively relevant distributions;
- report sensitivity to term specification, constraints, decay/fixed choices, and initialization/control settings;
- for valued networks, specify the reference distribution and response support; for missing edges, use supported missing-data handling rather than silently treating them as absent.

An ERGM coefficient is a conditional log-odds/change statistic under the full model, not a marginal tie probability. Do not interpret coefficients before convergence and GOF support the model.

## 7. Scale and software

- Use sparse representations for large sparse graphs and avoid dense adjacency matrices unless size permits.
- NetworkX prioritizes flexible Python workflows, not maximum scale. For large or repeatedly computed graphs, profile and consider igraph, graph-tool, specialized libraries, or backend dispatch.
- Consult the installed NetworkX version and [stable API documentation](https://networkx.org/documentation/stable/reference/index.html); do not rely on a frozen package cheat sheet.
- Record versions and seeds for stochastic layouts and algorithms. Layout coordinates are visual aids, not analytical evidence.
- For dense visualizations, filter or aggregate with a stated rule, use small multiples or matrix/summary views, and avoid implying that omitted edges do not exist.

## 8. Reporting checklist

- [ ] Nodes, edges, boundaries, time, weights, direction, multiplicity, and missingness are defined.
- [ ] Construction/projection/threshold decisions are reproducible and sensitivity-tested when consequential.
- [ ] Metrics are tied to mechanisms and handle components/weight semantics correctly.
- [ ] Community results report objective, resolution, seed, connectedness, and stability.
- [ ] Power-law claims use MLE, cutoff estimation, GOF, and competing distributions.
- [ ] Null models preserve the appropriate features and quantify Monte Carlo uncertainty.
- [ ] ERGM results include constraints, convergence/MCMC diagnostics, simulation GOF, and specification sensitivity.
- [ ] Code, versions, outputs, and network-construction provenance map to the reported claim.

## Primary sources

- Newman (2018), [*Networks*, 2nd ed.](https://global.oup.com/academic/product/networks-9780198805090), for representation, centrality, communities, random graphs, and generative mechanisms.
- Traag, Waltman, and van Eck (2019), [Leiden and well-connected communities](https://doi.org/10.1038/s41598-019-41695-z).
- Clauset, Shalizi, and Newman (2009), [power-law fitting, goodness of fit, and model comparison](https://doi.org/10.1137/070710111).
- Krivitsky et al. (2023), [`ergm` 4 features](https://doi.org/10.18637/jss.v105.i06), including flexible terms, constraints, valued networks, and missing edges.
- NetworkX Developers, current [stable documentation](https://networkx.org/documentation/stable/). Treat it as a dynamic API reference.
- Wang Xiaofan et al., *Introduction to Network Science*, supplied as a scanned local reference copy for foundational Chinese-language context.
