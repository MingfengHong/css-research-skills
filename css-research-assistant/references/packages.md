# Computational Social Science Core Package Reference

This document collects official documentation links and typical usage conventions for Python packages commonly used in CSS research. When a task involves deep interaction with a specific package, consult the corresponding official docs for the latest API.

## Data Processing

### Pandas
- **Docs**: https://pandas.pydata.org/docs/
- **Typical use**: Survey data cleaning, panel data reshaping (`melt`/`pivot`), grouped aggregation (`groupby`), missing-value strategies
- **Convention**: Use `pd.read_csv(..., dtype={...})` to declare types explicitly; avoid `inplace=True`

## Network Analysis

### NetworkX
- **Docs**: https://networkx.org/documentation/stable/
- **Typical use**: Social-network construction (nodes=individuals, edges=relationships), centrality metrics (betweenness, eigenvector), community detection (`community` module), small-world and scale-free network generation
- **Convention**: For large networks (>1e5 nodes), export to edge lists and process with sparse matrices; always report modularity after community partitioning

### PyTorch Geometric (PyG)
- **Docs**: https://pytorch-geometric.readthedocs.io/en/latest/
- **Typical use**: Graph neural networks (GCN, GAT, GraphSAGE) for node classification, link prediction, and graph-level tasks
- **Convention**: Build datasets with `Data` objects; distinguish `edge_index` from `edge_weight`; fix `torch.manual_seed()` before training

## Simulation

### Mesa
- **Docs**: https://mesa.readthedocs.io/en/stable/
- **Typical use**: Agent-based social simulation (opinion dynamics, diffusion models, organizational evolution)
- **Convention**:
  - `Model` subclasses handle global scheduling and environment; `Agent` subclasses handle individual rules
  - Explicitly create `random.Random(seed)` in `Model.__init__` and pass it to all Agents
  - Use `DataCollector` to record time-series data centrally; avoid manual log-file writes inside `step()`

## Machine Learning and Statistics

### Scikit-Learn
- **Docs**: https://scikit-learn.org/stable/
- **Typical use**: Baseline classification/regression, cross-validation, feature scaling, dimensionality reduction (PCA, t-SNE, UMAP)
- **Convention**: Always wrap preprocessing and models in a `Pipeline`; report `classification_report` and confusion matrices for classification tasks

### Statsmodels
- **Docs**: https://www.statsmodels.org/stable/index.html
- **Typical use**: OLS / Logit / Probit regression, time series (ARIMA), panel data (`linearmodels` extension)
- **Convention**: Output must include coefficients, standard errors, t-values, p-values, and R-squared; use `HC3` for heteroskedasticity-robust standard errors; report first-stage F-statistics for IV regression

### PyTorch
- **Docs**: https://pytorch.org/docs/stable/
- **Typical use**: Custom neural networks, deep-learning text/graph model training
- **Convention**:
  - Fix all random seeds at the top of training scripts (including `torch.backends.cudnn.deterministic = True` if strict reproducibility is required)
  - Explicitly print loss functions and evaluation metrics before training begins
  - Wrap inference code in `torch.no_grad()`

## Natural Language Processing

### Hugging Face Transformers
- **Docs**: https://huggingface.co/docs/transformers/index
- **Typical use**: Pretrained language-model fine-tuning (BERT, RoBERTa, LLaMA), sentiment analysis, named entity recognition, text classification
- **Convention**:
  - Load `AutoTokenizer` and `AutoModel` as a pair
  - Explicitly set `padding=True, truncation=True, max_length=512`
  - Fix `training_args.seed` during fine-tuning

### Spacy
- **Docs**: https://spacy.io/usage
- **Typical use**: Dependency parsing, named entity recognition, POS tagging, text-preprocessing pipelines
- **Convention**: Use language-specific models like `spacy.load("en_core_web_sm")`; for large corpora use `nlp.pipe()` instead of looping over `nlp()`

### Gensim
- **Docs**: https://radimrehurek.com/gensim/auto_examples/index.html
- **Typical use**: LDA topic modeling, Word2Vec / Doc2Vec training, TF-IDF vectorization
- **Convention**:
  - Tune `num_topics` via perplexity or coherence score
  - Fix the `seed` parameter when training Word2Vec
  - Save/load models with `model.save()` and `LdaModel.load()`; do not manually serialize internal matrices

## Visualization

### Matplotlib
- **Docs**: https://matplotlib.org/stable/users/index.html
- **Convention**:
  - Use `plt.rcParams` to set publication-grade styles globally (sans-serif fonts, removed borders)
  - For network plots, use `spring_layout` or `kamada_kawai_layout`; avoid drawing all node labels directly with `nx.draw_networkx` on large networks

### Seaborn
- **Docs**: https://seaborn.pydata.org/
- **Convention**:
  - Set `ci=95` or `errorbar=("ci", 95)` for statistical plots (regression lines, distributions)
  - Default context: `sns.set_context("paper")` and `sns.set_style("ticks")`
  - Heatmap format `fmt=".2f"`, use colorblind-friendly cmaps (`viridis`, `cividis`, `rocket_r`)
