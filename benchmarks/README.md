# Comprehensive benchmark

The benchmark compares three conditions on the same eight computational social-science tasks:

1. no Skill;
2. Skill 1.0.0;
3. Skill 2.0.0.

The primary question is whether a Skill improves the coverage of claim-relevant research guidance—not whether an answer is long or contains runnable-looking code.

## Coverage

The benchmark spans design-sensitive causal inference, text analysis, agent-based modelling, network analysis, and research reproducibility. It includes both the areas emphasized by 1.0.0 and the broader validity guidance introduced in 2.0.0.

## Tasks

| # | Task | Why it is included |
|---:|---|---|
| 1 | Staggered-adoption DiD | Estimand, comparisons, heterogeneous effects, inference |
| 2 | Cross-language IV audit | R/Python parity, diagnostics, implementation contracts |
| 3 | Multilingual text → causal measurement | Construct validity, annotation, sample splitting |
| 4 | Imbalanced text classification | Baselines, metrics, thresholding, error analysis |
| 5 | Large spatial ABM | Architecture, performance, invariants, experiment design |
| 6 | Large bipartite network | Network construction, projection, scale, interpretation |
| 7 | Valued ERGM with missing dyads | Dependence-aware modeling, missingness, diagnostics |
| 8 | Restricted-data replication package | Provenance, executable workflow, access constraints |

## Rubric

Every task has one check in each of six dimensions:

| Dimension | Core question |
|---|---|
| Research framing | Does the response define the question, claim, units, and target quantity or construct? |
| Method fit | Does it select methods that match the design and explain their assumptions? |
| Implementation | Does it provide an actionable software or workflow contract? |
| Diagnostics | Does it include method-specific tests, invariants, or failure checks? |
| Reproducibility | Does it preserve provenance, environment, execution order, and outputs? |
| Responsible claims | Does it bound interpretation and address relevant access, privacy, or harm constraints? |

Each condition receives 48 checks in total.

## Overall results

| Condition | Checks passed | Pass rate | Difference from No Skill |
|---|---:|---:|---:|
| No Skill | 28/48 | 58.3% | — |
| Skill 1.0.0 | 31/48 | 64.6% | +6.3 pp |
| Skill 2.0.0 | 42/48 | 87.5% | +29.2 pp |

The broader result changes the interpretation of 1.0.0: it improves on the no-Skill condition overall and performs particularly well on cross-language IV and imbalanced text classification. The new version leads overall, but it does not win every task; 1.0.0 scores 5/6 on imbalanced text classification versus 4/6 for 2.0.0.

## Task-level results

| Condition | DiD | Cross-language IV | Text measurement | Text classification | Spatial ABM | Bipartite network | Valued ERGM | Replication package |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| No Skill | 5/6 | 3/6 | 3/6 | 4/6 | 3/6 | 4/6 | 4/6 | 2/6 |
| Skill 1.0.0 | 5/6 | 5/6 | 4/6 | 5/6 | 4/6 | 3/6 | 2/6 | 3/6 |
| Skill 2.0.0 | 6/6 | 6/6 | 6/6 | 4/6 | 5/6 | 5/6 | 5/6 | 5/6 |

## Dimension-level results

| Condition | Research framing | Method fit | Implementation | Diagnostics | Reproducibility | Responsible claims |
|---|---:|---:|---:|---:|---:|---:|
| No Skill | 37.5% | 87.5% | 100.0% | 62.5% | 12.5% | 50.0% |
| Skill 1.0.0 | 62.5% | 87.5% | 100.0% | 62.5% | 12.5% | 62.5% |
| Skill 2.0.0 | 87.5% | 100.0% | 100.0% | 87.5% | 50.0% | 100.0% |

Reproducibility remains the weakest dimension even for 2.0.0, while implementation is strong across all three conditions.
