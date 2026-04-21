# Computational Social Science Skill for Claude

A Claude skill for rigorous, reproducible, publication-grade research software engineering in Computational Social Science (CSS). Covers causal inference, natural language processing, agent-based modeling, and social network analysis.

---

## What This Skill Does

This skill turns Claude into a Research Software Engineer that understands both social theory and code. It does not just write Python scripts — it enforces research-grade standards: fixed random seeds, structured logging, defensive assertions, algorithmic complexity annotations, and academic visualization conventions.

Before writing any code, the skill routes the user's request to the correct analytical domain and loads domain-specific constraints, toolchains, and validation protocols.

## Repository Structure

```
css-research-skills/
│
├── README.md
├── LICENSE
│
└── css-research-assistant/
    ├── SKILL.md
    └── references/
        ├── packages.md
        ├── causal_inference.md
        ├── nlp_text_analysis.md
        ├── abm_simulation.md
        └── network_analysis.md
```

**Note:** Per the [official Claude skill guidelines](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md), the skill folder itself (`css-research-assistant/`) must not contain a `README.md`. The human-facing documentation lives at the repository root.

## How It Works

### Progressive Disclosure

The skill uses a three-level loading system to avoid context overload:

1. **SKILL.md** (~160 lines) — Always loaded. Contains the domain router, universal coding standards, and the Definition of Done checklist.
2. **Domain references** (~140–165 lines each) — Loaded on demand when the router identifies the user's analytical domain.
3. **Package reference** (~90 lines) — Loaded when a specific package is central to the task.

### Domain Router

Before writing code, Claude classifies the request into one of four domains and loads the corresponding reference:

| Domain | Trigger | Reference |
|---|---|---|
| **Causal Inference** | Regression, DiD, RDD, IV, fixed effects, matching | `references/causal_inference.md` |
| **Text Analysis / NLP** | Topic modeling, sentiment, embeddings, parsing, classification | `references/nlp_text_analysis.md` |
| **ABM / Simulation** | Agent-based models, Mesa, diffusion, opinion dynamics | `references/abm_simulation.md` |
| **Network Analysis** | Graphs, centrality, community detection, ERGMs | `references/network_analysis.md` |

### Universal Standards (All Domains)

- **Theory First**: State the identification strategy or theoretical mechanism before coding.
- **Reproducibility**: Fix all random seeds (`seed=42`) and log them.
- **Defensive Coding**: Assert domain constraints (e.g., `assert 0 <= p <= 1.0`).
- **Complexity Awareness**: Annotate Big-O for loop-heavy operations; warn if O(N^2) or worse.
- **Pipeline Integrity**: Centralize paths in a `PATHS` dict; verify downstream compatibility.
- **Output Persistence**: Every table, plot, and report is saved to `output/`, not just printed.
- **Publication-Grade Visuals**: Nature/Science style — no chart junk, Okabe-Ito or Viridis colors, `dpi=300`.
- **Error Handling**: No bare `except:`; use `raise ... from e` to preserve chains.
- **No Emojis / No Filler**: Structured logs only (`[INFO] YYYY-MM-DD HH:MM:SS - message`).

## Installation

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- `ANTHROPIC_API_KEY` exported, or Claude Code will prompt on first run

### Via GitHub (recommended)

**Global installation** (available across all projects):

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/MingfengHong/css-research-skills.git ~/.claude/skills/css-research-skills
cp -r ~/.claude/skills/css-research-skills/css-research-assistant ~/.claude/skills/css-research-assistant
```

**Project installation** (recommended for per-project use):

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git clone https://github.com/MingfengHong/css-research-skills.git .claude/skills/css-research-skills
cp -r .claude/skills/css-research-skills/css-research-assistant .claude/skills/css-research-assistant
```

> **No Git?** Go to <https://github.com/MingfengHong/css-research-skills>, click **Code** → **Download ZIP**, extract it, then copy the `css-research-assistant/` folder to the target location above.

### Via ModelScope

Alternatively, install via ModelScope:

**Global installation:**

```bash
npx skills add https://github.com/MingfengHong/css-research-skills
```

Or via the ModelScope SDK:

```bash
pip install --upgrade modelscope
modelscope skills add MingfengHong/css-research-skills
```

Or via bash:

```bash
curl -fsSL https://modelscope.cn/skills/install.sh | bash -s -- MingfengHong/css-research-skills
```

**Project installation:**

```bash
cd /path/to/your/project
npx skills add https://github.com/MingfengHong/css-research-skills
```

### Post-installation

Restart Claude Code. The skill will auto-trigger when you mention topics related to social networks, regression, text modeling, agent simulation, or causal inference.

## Usage Example

**User**: "I want to run a difference-in-differences regression on this panel dataset with clustered standard errors."

**Claude (with skill)**:
1. Routes to **Causal Inference** domain.
2. Reads `references/causal_inference.md`.
3. Asks: "What is your treatment variable, outcome variable, entity identifier, and time variable?"
4. Writes `did_analysis.py` with:
   - Identification strategy stated in comments
   - `linearmodels.PanelOLS` with `cov_type='clustered'`
   - Event-study plot for parallel-trend validation
   - Multi-model Markdown table saved to `output/regression_table.md`
   - Completion checklist printed at the end

## Domain-Specific Highlights

### Causal Inference
- **Toolchain lock**: `statsmodels` / `linearmodels` (Python); `fixest` (R for high-dim FE).
- **Standard errors**: Robust/Clustered/HAC mandatory; spherical SEs forbidden.
- **The Cunningham Verification**: Cross-language coefficient check (Python vs R) for benchmark models.

### NLP / Text Analysis
- **Preprocessing split**: Classical NLP (stopwords, lemmatization) for LDA; minimal cleaning for Transformers.
- **Baseline requirement**: TF-IDF + LinearSVC before BERT.
- **Construct validity**: Explicit operationalization of latent constructs (polarization, framing, etc.).

### ABM / Simulation
- **OOP strictness**: Mandatory `mesa.Model` / `mesa.Agent` inheritance.
- **Randomness lock**: Use Mesa's `self.random`, never Python `random`.
- **Performance**: Spatial lookup via Mesa native methods; O(N^2) neighbor loops forbidden.

### Network Analysis
- **Complexity gates**: Betweenness centrality O(N^3) warning for N > 10,000.
- **Bipartite defense**: Weighted projection + information-loss warning.
- **Language lock**: ERGMs switch to R (`statnet` / `ergm`) with MCMC degeneracy checks.

## Development

This skill was built following the Anthropic [Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) workflow:
1. Draft skill from domain expertise and academic best practices.
2. Run parallel evals (with-skill vs without-skill) on realistic CSS tasks.
3. Grade outputs with programmatic assertions (reproducibility, paths, visualization quality).
4. Iterate based on quantitative benchmarks and qualitative code review.

## License

This work is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to share and adapt this material for **non-commercial** purposes, provided you give appropriate credit. See `LICENSE` for the full legal text.
