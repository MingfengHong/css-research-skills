---
name: css-research-skills
description: >-
  Design, implement, audit, and reproduce computational social science research. Use for causal inference and econometrics (including modern DiD, RDD, IV, matching, and longitudinal analyses), text-as-data and NLP measurement, agent-based modeling and Mesa simulations, social-network analysis and ERGMs, or any research workflow where social-science claims depend on data and code. Route mixed tasks to every relevant domain reference. Do not use for generic coding or data cleaning with no social-science question.
license: CC-BY-NC-4.0
compatibility: Designed for coding agents that can read bundled Markdown and run project tools. Method and package APIs must be checked against the installed version and current official documentation.
metadata:
  author: MingfengHong
  version: "2.0.0"
  category: academic-research
---

# Computational Social Science Research Engineering

Translate a social-science question into a claim-linked, inspectable, and reproducible analysis. Code that runs is not by itself evidence that the scientific claim is supported.

## Start with the research contract

Before choosing a model or editing code:

1. Inspect the supplied data, code, documentation, environment files, and prior outputs. Preserve existing project conventions unless they undermine validity.
2. Route the task to one or more domains below and read every selected reference before making method or API choices.
3. Resolve only decision-critical ambiguity. Typical missing items are the unit of analysis, target population, time origin, estimand or construct, treatment timing, network boundary, simulation purpose, and required artifact.
4. State a concise research contract:
   - question and intended claim;
   - units, population, sample, and observation window;
   - estimand, text construct, network quantity, or emergent pattern;
   - identifying or modeling assumptions;
   - data provenance and access constraints;
   - primary analysis, diagnostics, sensitivity analyses, and outputs.
5. Implement the smallest change that satisfies that contract, then validate the claim-to-result chain.

Use [the research-design template](assets/research_design_template.md) when the user asks for a protocol, preregistration, analysis plan, or replication plan. Adapt it; do not print irrelevant empty sections.

## Domain router

A task may span several rows. Read all that apply rather than forcing it into exactly one domain.

| Route | Typical questions | Required reference |
|---|---|---|
| Causal inference | Potential outcomes, DAGs, experiments, regression adjustment, panel FE, DiD/event studies, RDD, IV, matching/weighting, longitudinal treatment | [references/causal_inference.md](references/causal_inference.md) |
| Text as data / NLP | Corpus construction, discovery, topic models, dictionaries, annotation, classification, embeddings, LLM coding, text-derived treatments or outcomes | [references/nlp_text_analysis.md](references/nlp_text_analysis.md) |
| ABM / simulation | Agent rules, micro-macro mechanisms, Mesa, calibration, validation, policy experiments, sensitivity and uncertainty | [references/abm_simulation.md](references/abm_simulation.md) |
| Network analysis | Network construction, centrality, communities, diffusion, bipartite or temporal networks, null models, ERGM/TERGM | [references/network_analysis.md](references/network_analysis.md) |
| Research integrity | Any durable empirical/simulation result; human, platform, proprietary, or restricted data | [references/reproducibility_and_ethics.md](references/reproducibility_and_ethics.md) |

Read [references/packages.md](references/packages.md) when a package API is central. Read [references/source_guide.md](references/source_guide.md) when checking the evidence behind a rule or refreshing a dynamic reference such as Mesa or NetworkX.

## Universal validity gates

### Claim-method alignment

- Distinguish description, prediction, measurement, causal identification, and simulation explanation. Do not let a convenient algorithm silently change the question.
- Define the target quantity before estimation. Report the population and aggregation weights to which it applies.
- Treat assumptions as claims requiring argument and diagnostics, not boilerplate that a statistical test can prove.

### Data and provenance

- Keep source data immutable when feasible. Derive analysis data with code and retain stable identifiers from raw to derived records.
- Record provenance, collection window, inclusion/exclusion rules, units, missing-data handling, transformations, licenses, and access restrictions.
- Check joins, duplicates, types, ranges, attrition, and sample counts at consequential pipeline boundaries.

### Reproducibility

- Control randomness where stochasticity exists; accept a seed or RNG object and record it. Do not inject `seed=42` into deterministic tasks or mistake one fixed seed for robustness.
- For stochastic estimators or simulations, use justified repeated seeds and summarize the distribution of results. Record RNG, package versions, environment, hardware-sensitive settings, and commands when they can affect reproduction.
- Prefer a master entry point or exact ordered commands, dependency lock or environment specification, and a README mapping code to results.

### Validation

Validate at four levels as relevant:

1. **Software:** unit/smoke tests, schema checks, invariants, and expected failures.
2. **Method:** overlap, convergence, fit, balance, residual or simulation diagnostics, and estimator-specific checks.
3. **Substantive:** face-valid cases, close reading, known patterns, negative controls, or external benchmarks.
4. **Robustness:** reasonable alternative specifications, preprocessing choices, seeds, samples, network boundaries, or parameter ranges.

Do not add a cross-language coefficient comparison, a 300-dpi figure, a regression table, or an `output/` directory unless it serves the user's deliverable or a real validation need.

### Responsible research

For data about people or communities, assess consent and reasonable expectations, privacy and re-identification risk, representativeness and exclusions, stakeholder impacts and power, data rights, potential harms, and dual-use or deployment risk. Public availability does not by itself establish ethical permission or scientific validity.

### Performance and engineering

- Preserve downstream schemas and interfaces when modifying a pipeline.
- Measure before optimizing. Explain the complexity of non-obvious bottlenecks; do not annotate every loop mechanically.
- Prefer sparse or streaming operations when scale requires them, but keep a clear and testable baseline.
- Catch exceptions only where the code can add context, recover, or clean up. Preserve exception chains and never hide failed analyses.

## High-value gotchas

- A non-significant pre-treatment coefficient does not prove parallel trends.
- Staggered-adoption DiD with heterogeneous effects is not a routine two-way fixed-effects regression.
- Robust or clustered standard errors must follow the assignment and sampling structure; they are not interchangeable defaults.
- Winsorization, VIF thresholds, stopword removal, lemmatization, and document-frequency cutoffs are analysis choices, not universal cleaning rules.
- Automated text labels are measurements of constructs, not the constructs themselves.
- Mesa APIs, NetworkX interfaces, and statistical-package defaults change. Inspect the installed version and current official docs before writing version-sensitive code.
- Louvain modularity alone does not establish stable or well-connected communities.
- A straight line on a log-log plot does not establish a power law.
- Calibration data cannot also serve as independent validation evidence without qualification.
- A reproducible pipeline can still be biased, unethical, or causally unidentified.

## Finish with an evidence report

Before claiming completion, report only the items relevant to the task:

- files or system state changed;
- exact commands/tests run and their results;
- analysis sample and important exclusions;
- estimand/construct/model and assumptions;
- diagnostics and sensitivity checks completed;
- provenance, environment, and seed/replicate information;
- ethics or access constraints;
- output paths and mapping to claims;
- unresolved limitations or unverified external state.

For maintenance of this skill, run `python scripts/validate_skill.py` from the skill root and execute the realistic cases in `evals/evals.json` against both the current skill and the saved prior version.
