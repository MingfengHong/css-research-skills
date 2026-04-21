# Network Analysis Reference

## Table of Contents
1. [Intent Routing](#1-intent-routing)
2. [Phase 1: Graph Construction](#2-phase-1-graph-construction)
3. [Phase 2: Analytical Standards](#3-phase-2-analytical-standards)
4. [Phase 3: Visualization Rules](#3-phase-3-visualization-rules)
5. [Phase 4: Performance and Scale](#4-phase-4-performance-and-scale)
6. [Phase 5: Output and Validation](#5-phase-5-output-and-validation)

---

## 1. Intent Routing

Classify the network analysis goal before writing code:

| Route | Condition | Toolchain |
|---|---|---|
| **Micro-Positional** | "Who is most important?" — centrality, brokerage, structural holes, ego-networks | `NetworkX` or `igraph` |
| **Meso-Clustering** | "What are the groups?" — communities, echo chambers, polarization, triad census | `networkx.algorithms.community`, `python-louvain`, `leidenalg` |
| **Macro-Topological** | "What does the whole network look like?" — small world, scale-free, bipartite projection | `NetworkX` + `scipy.stats` for degree distribution fitting |
| **Inferential-Generative** | "Why does the network form this way?" — tie formation mechanisms, homophily, transitivity | R `statnet` / `ergm` (language lock: Python lacks robust ERGM support) |

---

## 2. Phase 1: Graph Construction

### 2.1 Directionality

Explicitly assert graph type:
```python
G = nx.Graph()      # Undirected
G = nx.DiGraph()    # Directed
G = nx.MultiGraph() # Multigraph (parallel edges)
```

If computing PageRank, In/Out-Degree, or reciprocity, use `DiGraph`. If the user implies undirected ties (friendship, collaboration), use `Graph`.

### 2.2 Bipartite Networks

If the data is two-mode (e.g., people-events, users-hashtags):
- Verify with `nx.is_bipartite(G)`.
- When projecting to a one-mode network, use **weighted projection**:
  ```python
  G_proj = nx.bipartite.weighted_projected_graph(G, nodes=people_nodes)
  ```
- **Warn the user** in comments about information loss and artificial clique inflation.

### 2.3 Isolates and Components

Before computing global metrics (average path length, diameter, clustering coefficient):
- Extract the **Giant Connected Component (GCC)**:
  ```python
  GCC = G.subgraph(max(nx.connected_components(G), key=len)).copy()
  ```
- Report the fraction of nodes in the GCC.

---

## 3. Phase 2: Analytical Standards

### 3.1 Centrality (Micro-Positional)

| Metric | Use When | Complexity | Warning |
|---|---|---|---|
| Degree Centrality | Local influence | O(N) | Safe |
| Betweenness Centrality | Brokerage / structural holes | O(N*E) or O(N^3) dense | For N > 10,000, use `k=50` approximation or switch to `igraph` |
| Eigenvector / PageRank | Global influence | O(N*E) iterative | Safe for most networks |
| Closeness Centrality | Information speed | O(N*E) | Exclude isolates |

### 3.2 Community Detection (Meso-Clustering)

- Prefer **Louvain** or **Leiden** over Girvan-Newman for speed and modularity quality.
- Always report the **modularity score** `Q`:
  ```python
  import community as community_louvain
  partition = community_louvain.best_partition(G, weight='weight', random_state=42)
  Q = community_louvain.modularity(partition, G, weight='weight')
  ```
- Report the number of communities and community size distribution.

### 3.3 Assortativity

If testing homophily, compute assortativity coefficients:
- Categorical attribute: `nx.attribute_assortativity_coefficient(G, 'attribute')`
- Numeric attribute: `nx.numeric_assortativity_coefficient(G, 'attribute')`

### 3.4 Inferential Models (ERGM)

**Language Lock**: For ERGMs, switch to R.

```r
library(ergm)
model <- ergm(net ~ edges + nodematch("gender") + gwesp(0.25, fixed=TRUE))
```

- Check **MCMC degeneracy** with `mcmc.diagnostics(model)` before interpreting coefficients.
- Report AIC, BIC, and goodness-of-fit statistics.

---

## 4. Phase 3: Visualization Rules

### 4.1 Forbidden Pattern

Do NOT use bare `nx.draw(G)` for networks with N > 50. The result is a meaningless "hairball."

### 4.2 Layout Seeding

Network layouts are stochastic. Lock the seed:
```python
pos = nx.spring_layout(G, weight='weight', seed=42, k=0.8, iterations=50)
```

### 4.3 Aesthetic Mapping

- **Node size**: Map to a structural metric (degree, betweenness, or PageRank).
- **Node color**: Map to communities or categorical attributes. Use Okabe-Ito palette.
- **Edge width / alpha**: Map to weight. Use `alpha=0.3` to `0.5` for dense networks.
- **Labels**: Show only top-N nodes by centrality to avoid clutter.
- **Spines**: Remove all spines (`ax.spines[spine].set_visible(False)`).

### 4.4 Large Networks (N > 1,000)

- Use `kamada_kawai_layout` or `spring_layout` with reduced iterations.
- Do not draw all edges. Sample or filter edges by weight.
- Consider plotting the degree distribution (log-log) instead of the full graph.

---

## 5. Phase 4: Performance and Scale

Pure Python `NetworkX` is slow. If the user implies N > 100,000:
- Recommend `igraph` (C-backed) or `graph-tool`.
- Only use NetworkX if explicitly requested.

For sparse matrix operations (adjacency matrix powers, spectral methods):
- Use `scipy.sparse` instead of dense `numpy` arrays.

---

## 6. Phase 5: Output and Validation

### 6.1 Metrics Export

Save centrality and community assignments to `output/network_metrics.csv`:
```csv
node,degree_centrality,betweenness_centrality,community
A,0.25,0.10,0
B,0.15,0.05,1
```

### 6.2 Visualization Export

Save network plots at `dpi=300` to `output/network_viz.png` (or `.pdf`).

### 6.3 Validation Checklist

1. [ ] Graph type asserted (directed/undirected, bipartite status checked)
2. [ ] GCC extracted before global metrics if graph is disconnected
3. [ ] Modularity score reported for community detection
4. [ ] Layout seed fixed for reproducibility
5. [ ] Complexity of most expensive operation declared in comments
6. [ ] For ERGMs: MCMC diagnostics checked before coefficient interpretation
7. [ ] Metrics and visualization saved to `output/`
