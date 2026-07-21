# Agent-Based Modeling and Simulation Reference

Use this reference for models in which heterogeneous agents, interactions, environments, and timing generate macro-level outcomes. An ABM is a scientific model, not only an object-oriented program.

## 1. Define purpose and micro-macro mechanism

Before implementation, state:

- the question and purpose: explanation, theory development, prediction, policy exploration, or method demonstration;
- entities/agents, state variables, scales, and environment;
- decision rules, adaptation, learning, interaction, and information;
- spatial/network structure and boundary conditions;
- scheduling/time representation and why order matters;
- exogenous inputs and stochastic processes;
- macro patterns or outcomes the micro rules are intended to generate;
- empirical patterns used for calibration and separate evidence used for validation.

Keep the conceptual model independent of the software API. Implement the smallest model capable of testing the mechanism before adding realism.

## 2. Document with ODD

Maintain an ODD description alongside the code:

### Overview

1. Purpose and patterns
2. Entities, state variables, and scales
3. Process overview and scheduling

### Design concepts

Address only relevant concepts: basic principles, emergence, adaptation, objectives, learning, prediction, sensing, interaction, stochasticity, collectives, and observation.

### Details

1. Initialization
2. Input data
3. Submodels

ODD 2020 also calls for explicit model rationale, evaluation of fitness for purpose, links from the description to code, and a standardized description of simulation experiments. Give parameter units/ranges, update order, equations or pseudocode, and enough detail for reimplementation; a class list is not an ODD.

## 3. Scientific workflow

1. **Conceptualize:** define the mechanism and discriminating patterns.
2. **Implement:** translate rules one at a time with traceable parameter names and units.
3. **Verify:** test whether the code implements the conceptual model.
4. **Calibrate:** estimate or constrain parameters using declared data/patterns and an objective function.
5. **Validate:** compare against independent patterns/data at several aggregation levels when possible.
6. **Analyze:** run replicated experiments, sensitivity/uncertainty analyses, and mechanism-removal or alternative-rule tests.
7. **Report:** link ODD, code version, parameters, seeds, experiment design, and outputs.

Calibration fit is not independent validation. If the same pattern must serve both roles, state that limitation and use cross-validation, held-out periods/locations, or additional patterns where feasible.

## 4. Mesa version gate

Mesa is a dynamic dependency. Before generating or modifying Mesa code:

1. Inspect the installed version (`python -c "import mesa; print(mesa.__version__)"`).
2. Check the matching official documentation and [migration guide](https://mesa.readthedocs.io/latest/migration_guide.html).
3. Preserve the project's pinned major version unless migration is requested.
4. Do not mix examples from incompatible versions.

For Mesa 3.x and later:

- call `super().__init__(seed=seed)` in the model constructor;
- let the model manage agents and automatically assign `unique_id`; do not overwrite reserved `model.agents`;
- replace deprecated `mesa.time` schedulers with explicit AgentSet activation such as `self.agents.do("step")`, `self.agents.shuffle_do("step")`, or staged `do` calls;
- use AgentSet operations such as `select`, `get`, `agg`, and `groupby` when they express the operation clearly;
- check the installed version before relying on newer time/event APIs such as `model.run_for`, `run_until`, or scheduled events.

For an older pinned project, either use its supported API consistently or propose a separate migration. Do not silently rewrite the model to the latest alpha documentation.

## 5. Randomness and experiment design

- Route stochastic draws through the model's documented RNGs. Avoid hidden module-level randomness inside agents.
- Record seed sequences and RNG versions. A same-seed rerun should match within the declared environment when the implementation promises determinism.
- Scientific conclusions require replicated runs. Choose the number of replications using Monte Carlo error/precision or a sequential stopping rule, not a single conventional number.
- For policy comparisons, consider common random numbers or paired seeds to reduce comparison noise, while preserving independence assumptions in inference.
- Separate parameter uncertainty, stochastic (aleatory) variability, structural uncertainty, and observation error where the claim requires it.

Store experiment results in tidy/long form with at least scenario, parameter set, replicate, seed, time, metric, model/code version, and status.

## 6. Verification

Test the implementation before interpreting emergent patterns:

- deterministic toy cases with analytically known outcomes;
- unit tests for agent decisions and environment transitions;
- invariants (population/accounting conservation, bounds, legal state transitions);
- boundary and empty-neighborhood cases;
- schedule/order sensitivity when simultaneous and sequential activation represent different mechanisms;
- same-seed repeatability and controlled different-seed variation;
- small-run smoke tests and data-collector schema checks;
- performance profiling for genuinely large runs.

Use assertions for true invariants, not uncertain empirical expectations. Explain any O(N²) interaction and use spatial indexing, neighbor lists, sparse networks, or sampling when the mechanism does not require all-pairs interaction.

## 7. Calibration, validation, and sensitivity

- Define calibration targets, loss/distance function, parameter bounds, optimization/search method, and identifiability limits.
- Use pattern-oriented modeling: prefer multiple patterns at different scales that jointly constrain mechanisms.
- Validate against independent temporal, spatial, subgroup, or distributional patterns; report both successes and mismatches.
- Run global sensitivity analysis when interactions/nonlinearity matter; one-at-a-time changes can miss interaction effects.
- Explore structural sensitivity by replacing or removing key mechanisms and schedules.
- Report uncertainty intervals/distributions across replications, not only a mean trajectory.
- Avoid policy optimization against an unvalidated model or a single parameterization. Present scenarios as conditional on model assumptions.

## 8. Reporting checklist

- [ ] Purpose, mechanism, scales, schedule, and intended macro patterns are explicit.
- [ ] ODD includes Overview, Design Concepts, Details, rationale, evaluation, and experiment design.
- [ ] Mesa version is recorded and code uses one compatible API generation.
- [ ] Verification covers toy cases, invariants, boundaries, schedules, and reproducibility.
- [ ] Calibration and validation evidence are distinguished.
- [ ] Experiments use recorded replicated seeds and quantify Monte Carlo uncertainty.
- [ ] Parameter, stochastic, and structural sensitivity are addressed at the level required by the claim.
- [ ] Results retain scenario/parameter/replicate/seed/time provenance and map to claims.

## Primary sources

- Grimm et al. (2020), [ODD second update](https://doi.org/10.18564/jasss.4259).
- Railsback and Grimm (2019), [*Agent-Based and Individual-Based Modeling*, 2nd ed.](https://press.princeton.edu/books/hardcover/9780691190822/agent-based-and-individual-based-modeling), especially model design, testing, pattern-oriented modeling, calibration, and sensitivity/robustness analysis.
- Mesa Project, current [migration guide](https://mesa.readthedocs.io/latest/migration_guide.html) and [AgentSet tutorial](https://mesa.readthedocs.io/latest/tutorials/1_agentset.html). Treat these as dynamic references and verify against the installed version.
