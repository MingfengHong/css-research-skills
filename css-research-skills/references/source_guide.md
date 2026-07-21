# Source Guide and Update Policy

Use this guide to audit or refresh the rules in this skill. Prefer live official documentation for changing APIs, original papers/books for methodological claims, and local reference copies only as reading aids. Do not redistribute supplied PDFs with the skill.

## Evidence hierarchy

1. **Specifications and current official docs** govern file formats, frontmatter, installation, and versioned APIs.
2. **Original methods papers and authoritative books** govern estimands, assumptions, validation, and scientific interpretation.
3. **Journal/repository policies** govern replication-package expectations.
4. **Tutorials and local guides** are implementation aids; check them against the sources above.

Refresh dynamic sources (Claude Code, Mesa, NetworkX, package docs, AEA policy) before version-sensitive changes. Stable conceptual sources should still be checked for corrections or newer editions when a rule is contested.

## A. Skill design and evaluation

1. **Agent Skills, [Agent Skills Specification](https://agentskills.io/specification).**
   Governs directory structure, YAML frontmatter, name-directory equality, description/compatibility limits, optional directories, relative references, progressive disclosure, and `skills-ref` validation.

2. **Agent Skills, [Best Practices for Skill Creators](https://agentskills.io/skill-creation/best-practices).**
   Supports coherent scope, omission of generic knowledge, calibrated instruction strength, defaults rather than menus, gotchas, templates, and validate-fix loops.

3. **Agent Skills, [Evaluating Skill Output Quality](https://agentskills.io/skill-creation/evaluating-skills).**
   Defines realistic cases in `evals/evals.json`, current-vs-baseline runs, objective expectations, grading evidence, aggregation, and human review.

4. **Agent Skills, [Using Scripts in Skills](https://agentskills.io/skill-creation/using-scripts).**
   Supports deterministic scripts for repeated/fragile work, relative paths, noninteractive interfaces, `--help`, useful errors, structured output, and dependency/version documentation.

5. **Anthropic, [Extend Claude with Skills](https://code.claude.com/docs/en/skills).**
   Dynamic Claude Code reference for installation scopes, automatic/explicit invocation, frontmatter extensions, permissions, dynamic context, and forked/subagent execution.

6. **Anthropic, [Skill Creator](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/skill-creator/skills/skill-creator/SKILL.md).**
   Primary workflow for extracting skills from real tasks, running old-vs-new evaluations, writing expectations, and iterating on trigger descriptions.

7. **Anthropic, [`anthropics/skills`](https://github.com/anthropics/skills).**
   Production examples for separating concise instructions, references, scripts, and assets. Inspect current repository structure rather than copying an old snapshot.

Additional local reading supplied for this revision:

- *The Complete Guide to Building Skills for Claude* (33 pages): progressive disclosure, frontmatter/description, scripts, and testing/iteration.
- *Claude Code for Academics* (76 pages, March 2026): plan-first academic workflows, project memory, permissions, skills, and subagents. Treat as a practical presentation rather than a normative specification.

## B. Research software engineering and responsibility

8. **American Economic Association, [Data and Code Availability Policy](https://www.aeaweb.org/journals/data/data-code-policy) (February 2026).**
   Supports data-availability statements, source/analysis data, metadata, transformation and analysis code, master scripts, environments, README/output maps, restricted-data procedures, ethics approvals, and repositories.

9. **The Turing Way Community, [Guide for Reproducible Research](https://book.the-turing-way.org/reproducible-research/reproducible-research/).**
   Supports version control, testing, reproducible environments, research data management, collaboration, code/software citation, risk assessment, and open research.

10. **Wilkinson et al. (2016), [FAIR Guiding Principles](https://doi.org/10.1038/sdata.2016.18).**
    Supports findability, accessibility (including authenticated access), interoperability, reusability, persistent identifiers, rich metadata, provenance, licenses, and community standards.

11. **National Academies (2022), [Fostering Responsible Computing Research](https://doi.org/10.17226/26507).**
    Supports sociotechnical analysis, divergent stakeholder values and power, privacy, unjust bias, potential harms, uncertainty, governance, and impacts beyond individuals.

Also reviewed in English and Chinese local editions: Matthew J. Salganik, *Bit by Bit: Social Research in the Digital Age*, especially the chapter on ethics, informed consent, informational risk, and privacy.

## C. Causal inference

12. **Hernán and Robins (2020), [*Causal Inference: What If*](https://miguelhernan.org/whatifbook).**
    Core source for potential outcomes, consistency, exchangeability, positivity, standardization, IPW, longitudinal g-methods, target trials, and time-zero alignment. The official page may publish corrected versions; check it before quoting page numbers.

13. **Roth, Sant'Anna, Bilinski, and Poe (2023), [What's Trending in Difference-in-Differences?](https://doi.org/10.1016/j.jeconom.2023.03.008).**
    DiD overview organized around multiple periods/treatment timing, potential parallel-trend violations, and alternative inference frameworks.

14. **Sun and Abraham (2021), [Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects](https://doi.org/10.1016/j.jeconom.2020.09.006).**
    Establishes contamination of conventional lead/lag TWFE coefficients under staggered timing and heterogeneous effects; motivates interaction-weighted alternatives.

15. **Callaway and Sant'Anna (2021), [Difference-in-Differences with Multiple Time Periods](https://doi.org/10.1016/j.jeconom.2020.12.001).**
    Supports group-time ATT, conditional parallel trends, outcome-regression/IPW/doubly robust estimation, aggregation schemes, and simultaneous inference. Pair with current [`did` documentation](https://bcallaway11.github.io/did/).

Additional local reading supplied: Scott Cunningham, *Causal Inference: The Mixtape*, for accessible design intuition and worked examples. It supplements rather than overrides the modern DiD sources above.

## D. Text as data and NLP

16. **Grimmer, Roberts, and Stewart (2022), [*Text as Data*](https://press.princeton.edu/books/hardcover/9780691207544/text-as-data).**
    Organizes text research around selection/representation, discovery, measurement, prediction, and causal inference; stresses question-specific corpus construction and iterative research design. A local PDF was reviewed.

17. **Grimmer and Stewart (2013), [The Promise and Pitfalls of Automatic Content Analysis](https://doi.org/10.1093/pan/mps028).**
    Supports method-task matching, close reading, extensive problem-specific validation, and avoiding direct equivalence between algorithmic output and theoretical construct.

18. **Denny and Spirling (2018), [Text Preprocessing for Unsupervised Learning](https://doi.org/10.1017/pan.2017.44).**
    Supports sensitivity analysis across preprocessing regimes instead of unconditional stopword, lemmatization, or frequency-threshold rules.

19. **Egami et al. (2022), [How to Make Causal Inferences Using Texts](https://doi.org/10.1126/sciadv.abg2652).**
    Supports explicit roles for text in the causal design and split-sample/cross-fitting workflows to address overfitting and identification risks in discovered measures.

20. **Birkenmaier, Wagner, and Lechner (2023), [ValiText](https://arxiv.org/abs/2307.02863).**
    Supplementary preprint framework for substantive, structural, and external validity evidence. Label it as a preprint and do not treat it as settled consensus.

## E. Agent-based modeling

21. **Grimm et al. (2020), [ODD Protocol, second update](https://doi.org/10.18564/jasss.4259).**
    Core standard for Overview, Design Concepts, Details, model rationale, code links, evaluation/fitness for purpose, and simulation-experiment descriptions.

22. **Railsback and Grimm (2019), [*Agent-Based and Individual-Based Modeling*, 2nd ed.](https://press.princeton.edu/books/hardcover/9780691190822/agent-based-and-individual-based-modeling).**
    Supports question formulation, conceptual models, implementation/testing, pattern-oriented modeling, calibration, prediction, scheduling, and sensitivity/uncertainty/robustness analysis.

23. **Mesa Project, [Migration Guide](https://mesa.readthedocs.io/latest/migration_guide.html).**
    Dynamic source for mandatory model initialization, automatic IDs, reserved attributes, AgentSet activation, time/event advancement, visualization changes, and deprecated APIs.

24. **Mesa Project, [Working with AgentSets](https://mesa.readthedocs.io/latest/tutorials/1_agentset.html).**
    Dynamic source for `get`, `select`, `agg`, `groupby`, `set`, sorting, and activation patterns. Match examples to the installed version rather than `latest` blindly.

## F. Social network analysis

25. **Newman (2018), [*Networks*, 2nd ed.](https://global.oup.com/academic/product/networks-9780198805090).**
    Foundation for graph representation, centrality, mixing, communities, random graphs, network processes, and generative mechanisms.

26. **Traag, Waltman, and van Eck (2019), [From Louvain to Leiden](https://doi.org/10.1038/s41598-019-41695-z).**
    Supports the warning that Louvain can produce badly connected communities, Leiden refinement, explicit connectivity guarantees, and reporting resolution dependence.

27. **Clauset, Shalizi, and Newman (2009), [Power-Law Distributions in Empirical Data](https://doi.org/10.1137/070710111).**
    Supports maximum-likelihood fitting, cutoff estimation, KS/bootstrap goodness of fit, and likelihood-based comparison with competing distributions instead of log-log regression.

28. **Krivitsky, Hunter, Morris, and Klumb (2023), [`ergm` 4](https://doi.org/10.18637/jss.v105.i06).**
    Supports flexible covariates/term operators, constraints, valued networks, missing-edge handling, extension packages, and the current `statnet` workflow.

29. **NetworkX Developers, [Stable Documentation](https://networkx.org/documentation/stable/).**
    Dynamic source for `Graph`, `DiGraph`, `MultiGraph`, `MultiDiGraph`, algorithms, I/O, backends, and version compatibility.

Additional local reading supplied: Wang Xiaofan et al., *Introduction to Network Science*. The copy is image-based; its front matter was visually inspected and it is retained as foundational Chinese-language context, not as the source for changing package APIs.

## Maintenance checklist

- [ ] Check Agent Skills and Claude Code specification changes.
- [ ] Check AEA policy version and repository/README requirements.
- [ ] Check Mesa and NetworkX installed/current versions before changing API guidance.
- [ ] Check current `did`, `fixest`, `ergm`, and related package documentation before adding syntax.
- [ ] Distinguish original methods, later syntheses, current software docs, and preprints.
- [ ] Add a source only when it changes a rule, default, gotcha, validation step, or evaluation case.
- [ ] Run `scripts/validate_skill.py` and the old-vs-new cases in `evals/evals.json` after substantive revisions.
