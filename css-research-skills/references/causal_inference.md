# Causal Inference Reference

Use this reference when the requested claim is causal or when a regression may be interpreted causally. Begin with the estimand and design; an estimator cannot repair an unidentified question.

## 1. Causal design contract

State the following before implementation:

- target population and unit of analysis;
- treatment strategies, timing, and versions;
- outcome, follow-up window, and time zero;
- causal contrast and estimand: ATE, ATT, group-time ATT, LATE, per-protocol effect, or another explicit quantity;
- assignment mechanism or source of identifying variation;
- confounders, mediators, colliders, spillovers/interference, attrition, and measurement error;
- assumptions needed for identification and the evidence available for each.

For longitudinal observational analyses, emulate the relevant parts of a target trial: eligibility, treatment strategies, assignment procedure, start of follow-up, outcome, causal contrast, and analysis plan. Align eligibility, treatment assignment, and time zero to avoid immortal-time and selection biases.

Use potential outcomes and/or a DAG to clarify:

- **Consistency:** the observed treatment corresponds to a well-defined intervention and links observed to counterfactual outcomes.
- **Exchangeability:** treated and comparison outcomes would be comparable, marginally or conditional on measured covariates.
- **Positivity:** each relevant treatment strategy has support within covariate strata used for the target population.
- **Interference:** whether one unit's treatment can affect another unit's outcome; redefine the estimand if spillovers are part of the question.

Diagnostics can reveal violations but cannot prove these assumptions.

## 2. Route by design, not by package

| Design | Primary target | Key requirements |
|---|---|---|
| Randomized experiment | Assignment-policy-specific ATE/ITT or treatment-received effect | Preserve assignment, account for noncompliance/attrition, analyze at the assignment level |
| Covariate adjustment / standardization | ATE/ATT under conditional exchangeability | Pre-treatment covariates, overlap, correct or flexible outcome model, uncertainty |
| Matching / weighting | ATE/ATT/ATO for a stated population | Propensity/selection model, balance, overlap, weight diagnostics, outcome analysis |
| Instrumental variables | LATE or another IV estimand | Relevance, independence, exclusion, monotonicity where invoked; first-stage and weak-IV diagnostics |
| Regression discontinuity | Local effect at a cutoff | Running-variable integrity, bandwidth/kernel/order choices, density and covariate checks |
| Panel fixed effects | Within-unit conditional association; causal only with additional assumptions | Timing, strict/sequential exogeneity, dynamic confounding, serial dependence |
| Difference-in-differences | ATT under a stated parallel-trends condition | Treatment timing, comparison group, anticipation, heterogeneity, inference structure |
| Time-varying treatment | Longitudinal regime effect | Time-varying confounding, positivity, g-method such as IPW/g-formula when needed |

Do not label a design causal merely because it uses fixed effects, matching, controls, or a familiar package.

## 3. Modern difference-in-differences

### 3.1 Diagnose the design

Before estimation, report:

- treatment adoption cohorts and whether treatment is absorbing, reversible, or repeated;
- never-treated and not-yet-treated observations available as comparisons;
- event-time support by cohort and any anticipation window;
- outcome observations before and after treatment for each cohort;
- clustering and the number of treated clusters;
- the precise parallel-trends assumption: unconditional or conditional, and relative to which comparison group.

### 3.2 Choose an estimator that targets interpretable effects

- For a canonical two-group/two-period design, the ordinary DiD contrast may be appropriate when its assumptions and inference are justified.
- With multiple periods and staggered adoption, do not default to a vanilla two-way fixed-effects treatment coefficient or lead/lag event study when effects may vary across cohorts or event time.
- Use group-time ATT methods such as Callaway-Sant'Anna, or interaction-weighted/event-study methods such as Sun-Abraham, when their control-group and parallel-trends assumptions fit the design.
- State whether controls are never-treated, not-yet-treated, or another group. The choice changes the estimand and assumptions.
- Report cohort/event-time effects before aggregating. For summaries, state the aggregation weights and show how cohort size, calendar time, and event-time support affect them.
- Use simultaneous confidence bands when making joint statements about an event-study path; pointwise intervals do not control simultaneous coverage.

Traditional lead coefficients can be contaminated by heterogeneous post-treatment effects. A failure to reject pre-treatment coefficients is low-power evidence, not proof of parallel trends. Complement plots/tests with design knowledge, pre-period fit, placebo outcomes/timings, and sensitivity analyses for plausible trend violations.

### 3.3 Inference and robustness

- Cluster at the level of treatment assignment or dependence justified by the design. If the number of treated or total clusters is small, consider small-sample corrections, wild-cluster bootstrap, randomization inference, or design-specific alternatives.
- Avoid controls affected by treatment. If conditional parallel trends is invoked, define and justify the pre-treatment covariates.
- Check sensitivity to anticipation windows, comparison groups, cohort composition, event-time binning, covariate adjustment, and alternative heterogeneity-robust estimators.
- Diagnose negative or unintuitive weighting when presenting TWFE as a comparison; do not treat that comparison as the preferred causal result by default.

## 4. Data and estimation discipline

- Build the analysis sample explicitly and report counts before/after exclusions and missing-data handling. Do not let model-specific row dropping create incomparable samples silently.
- Do not require a balanced panel unless the estimand/design needs one. Investigate whether observation and attrition are affected by treatment.
- Do not winsorize automatically. If outliers are influential, explain their provenance and report transparent sensitivity analyses.
- VIF is not a general identification diagnostic and a threshold such as 10 is not a universal deletion rule.
- Select standard errors from the sampling and assignment structure. Heteroskedasticity-robust, one-way clustered, multiway clustered, spatial/HAC, randomization-based, and bootstrap inference answer different dependence problems.
- Preserve treatment timing and identifiers through joins; assert uniqueness and time ordering before estimation.

## 5. Method-specific minimum diagnostics

### Matching and weighting

- Show covariate balance with standardized differences and distributions, not p-values alone.
- Plot propensity/weight overlap; report extreme weights, effective sample size, trimming rules, and changed target population.
- Prefer doubly robust estimation when justified, but do not describe it as immune to joint misspecification or positivity violations.

### Instrumental variables

- Explain the instrument mechanism and exclusion restriction in context.
- Report first-stage strength with an appropriate weak-instrument diagnostic; do not use one F-statistic threshold mechanically for every design.
- Interpret the IV estimand for the population/compliers supported by the assumptions.

### Regression discontinuity

- Inspect manipulation/heaping around the cutoff and predetermined-covariate continuity.
- Use local polynomial methods with data-driven bandwidths and bias-aware uncertainty; show sensitivity to bandwidth, kernel, and polynomial order.
- Interpret the result locally unless additional generalization assumptions are supplied.

### Longitudinal treatment

- If time-varying covariates both predict treatment and are affected by prior treatment, ordinary regression adjustment can be biased. Consider inverse-probability weighting, the g-formula, or related g-methods.
- Check treatment/censoring weights, positivity, model specification, and longitudinal alignment.

## 6. Validation and reporting

Report:

- estimand, target population, analysis sample, and treatment/control timing;
- effect estimate with uncertainty and scale, not only p-values or stars;
- identifying assumptions and evidence/limitations for each;
- diagnostics specific to the design;
- robustness and sensitivity results, including changes in estimand or population;
- code/data/environment provenance and an output-to-claim map.

A cross-language or cross-package comparison is useful only when both implementations use the same sample, estimand, weights, fixed effects, degrees-of-freedom correction, and variance estimator. Numerical disagreement can reflect different defaults rather than an implementation bug; agreement does not validate identification.

## Primary sources

- Hernán and Robins (2020), [*Causal Inference: What If*](https://miguelhernan.org/whatifbook), especially consistency, exchangeability, positivity, standardization/IPW, target trials, and longitudinal g-methods.
- Cunningham (2021), *Causal Inference: The Mixtape*, supplied as a local reference copy for design intuition and reproducible examples.
- Roth, Sant'Anna, Bilinski, and Poe (2023), [modern DiD synthesis](https://doi.org/10.1016/j.jeconom.2023.03.008).
- Sun and Abraham (2021), [heterogeneous dynamic effects in event studies](https://doi.org/10.1016/j.jeconom.2020.09.006).
- Callaway and Sant'Anna (2021), [DiD with multiple periods](https://doi.org/10.1016/j.jeconom.2020.12.001), with the current [`did` package documentation](https://bcallaway11.github.io/did/).
