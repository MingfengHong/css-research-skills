# Computational Social Science Package Guide

Use this file only when a package API is central. It is a routing guide, not a frozen API reference.

## Version-first workflow

1. Inspect the project's environment/lockfile and installed version.
2. Preserve the pinned major version unless migration is requested.
3. Consult the matching official documentation and migration/release notes for version-sensitive code.
4. Record resolved versions in the research output or replication README.
5. Run a minimal API smoke test before building the full analysis.

Examples:

```bash
python -c "import importlib.metadata as m; print(m.version('networkx'))"
python -c "import mesa; print(mesa.__version__)"
Rscript -e "packageVersion('fixest'); packageVersion('did'); packageVersion('ergm')"
```

Do not copy an API example from `latest` documentation into an older pinned project without checking compatibility.

## Causal inference and econometrics

| Purpose | Preferred starting point | Official documentation | Notes |
|---|---|---|---|
| General regression/GLM | Python `statsmodels`; R base or `fixest` | [statsmodels](https://www.statsmodels.org/stable/), [fixest](https://lrberge.github.io/fixest/) | Match variance estimation to the design; inspect defaults |
| Panel models | R `fixest`; Python `linearmodels` where appropriate | [fixest](https://lrberge.github.io/fixest/), [linearmodels](https://bashtage.github.io/linearmodels/) | Fixed effects do not by themselves identify a causal effect |
| Staggered DiD | R `did` or a validated heterogeneity-robust implementation; `fixest::sunab` for Sun-Abraham designs | [`did`](https://bcallaway11.github.io/did/), [`sunab`](https://lrberge.github.io/fixest/reference/sunab.html) | State control group, estimand, aggregation, and inference |
| RDD | R/Python `rdrobust` ecosystem | [rdpackages](https://rdpackages.github.io/) | Use local-polynomial, bandwidth, manipulation, and sensitivity diagnostics |
| Matching/weighting | R `MatchIt`, `WeightIt`; project-validated Python alternatives | [MatchIt](https://kosukeimai.github.io/MatchIt/), [WeightIt](https://ngreifer.github.io/WeightIt/) | Report balance, overlap, weights, ESS, and target population |

Do not force Python/R cross-checks unless they add value. If used, align sample, formula, fixed effects, weights, dropped categories, and variance estimator before comparing numbers.

## Text as data and machine learning

| Purpose | Preferred starting point | Official documentation | Notes |
|---|---|---|---|
| Reproducible ML pipelines | scikit-learn | [scikit-learn](https://scikit-learn.org/stable/) | Put learned preprocessing inside the pipeline/fold |
| Linguistic processing | spaCy | [spaCy usage](https://spacy.io/usage) | Use `nlp.pipe` for corpora; pin model package and language |
| Transformers | Hugging Face Transformers | [Transformers](https://huggingface.co/docs/transformers/) | Match tokenizer/model; record revision and truncation policy |
| Topic/embedding workflows | Gensim, BERTopic, or validated project tools | [Gensim](https://radimrehurek.com/gensim/auto_examples/), [BERTopic](https://maartengr.github.io/BERTopic/) | Validate stability and substantive meaning, not one score |
| Deep learning | PyTorch | [PyTorch](https://pytorch.org/docs/stable/) | Record device/determinism settings; use repeated runs when stochastic |

Do not hardcode `max_length=512`; read the selected model/tokenizer limits. A simple linear baseline is valuable when it is a meaningful comparator, not a universal prerequisite.

## Agent-based modeling

| Purpose | Preferred starting point | Official documentation | Notes |
|---|---|---|---|
| Python ABM | Mesa | [Mesa stable](https://mesa.readthedocs.io/stable/), [migration guide](https://mesa.readthedocs.io/latest/migration_guide.html) | Version 3+ requires `super().__init__`; AgentSet replaces old schedulers |
| Parameter sweeps | Mesa batch utilities or a small project-specific runner | [Mesa API](https://mesa.readthedocs.io/stable/apis/api_main.html) | Store scenario, parameters, replicate, seed, and status |
| Sensitivity/uncertainty | SALib or project-validated alternatives | [SALib](https://salib.readthedocs.io/) | Choose method from parameter distributions and interactions |

Do not use `RandomActivation`, `SimultaneousActivation`, or `BatchRunner` from old examples without confirming that the pinned Mesa version supports them.

## Network analysis

| Purpose | Preferred starting point | Official documentation | Notes |
|---|---|---|---|
| Flexible Python graph analysis | NetworkX | [NetworkX stable](https://networkx.org/documentation/stable/) | Choose graph class and weight semantics explicitly |
| Larger graphs / Leiden | igraph plus `leidenalg`, or supported NetworkX community APIs | [python-igraph](https://python.igraph.org/en/stable/), [leidenalg](https://leidenalg.readthedocs.io/) | Record objective, resolution, seed, and connectedness |
| ERGM/TERGM and valued networks | R `statnet` / `ergm` ecosystem | [statnet](https://statnet.org/), [`ergm`](https://cran.r-project.org/package=ergm) | Inspect terms/vignettes for installed version; run MCMC and simulation GOF |
| Power-law diagnostics | `powerlaw` or a transparent MLE/bootstrap implementation | [`powerlaw`](https://pythonhosted.org/powerlaw/) | Verify discrete/continuous support, `xmin`, GOF, and alternatives |

## Data, storage, and visualization

- Use pandas, data.table, DuckDB, or Arrow according to scale and existing project conventions. Declare types and validate join cardinality at consequential boundaries.
- Use sparse matrices for large sparse features or graphs; avoid dense conversion that changes feasible sample size.
- Use Matplotlib/Seaborn/ggplot2 with accessible labels, uncertainty, units, and color choices. Export format and resolution should follow the destination (paper, slide, web, exploratory review), not a universal DPI rule.
- Record fonts, locale, timezone, and renderer when they affect reproducibility.

Official references: [pandas](https://pandas.pydata.org/docs/), [DuckDB](https://duckdb.org/docs/stable/), [Apache Arrow](https://arrow.apache.org/docs/), [Matplotlib](https://matplotlib.org/stable/users/index.html), [Seaborn](https://seaborn.pydata.org/), and [ggplot2](https://ggplot2.tidyverse.org/).
