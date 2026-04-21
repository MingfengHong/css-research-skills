# Causal Inference Reference

## Table of Contents
1. [Intent Routing](#1-intent-routing)
2. [Phase 1: Identification Strategy](#2-phase-1-identification-strategy)
3. [Phase 2: Data Preprocessing](#3-phase-2-data-preprocessing)
4. [Phase 3: Estimation Standards](#4-phase-3-estimation-standards)
5. [Phase 4: Diagnostics and Visualization](#5-phase-4-diagnostics-and-visualization)
6. [Phase 5: Output and Validation](#6-phase-5-output-and-validation)

---

## 1. Intent Routing

Before choosing a model, classify the user's goal:

| Route | Condition | Toolchain |
|---|---|---|
| **Cross-section / Pooled** | User has observational data without panel structure | `statsmodels` (Python) or `lm` / `fixest` (R) |
| **Panel Data / Fixed Effects** | User has repeated observations (e.g., country-year, firm-month) | `linearmodels.PanelOLS` (Python) or `fixest::feols` (R) |
| **Difference-in-Differences** | User compares treated vs control over time | `linearmodels.PanelOLS` with treatment interaction, or `did` / `fixest` (R) |
| **Regression Discontinuity** | User exploits a sharp cutoff | `rdrobust` (R) or manual local polynomial in Python |
| **Instrumental Variables** | User has endogeneity and a valid instrument | `linearmodels.IV2SLS` (Python) or `fixest::feols` with IV syntax (R) |
| **Matching / Propensity Score** | User wants to reduce selection bias via balancing | `MatchIt` (R) or `sklearn` + manual weighting (Python) |

**Language Lock**: For high-dimensional fixed effects (>10,000 groups) or ERGM-style inference, prefer R (`fixest`). For everything else, Python (`statsmodels` / `linearmodels`) is acceptable.

---

## 2. Phase 1: Identification Strategy

Before writing regression code, state the identification strategy in a comment block:

```python
"""
Identification Strategy: Difference-in-Differences (DiD)
Target Parameter: ATT (Average Treatment Effect on the Treated)
Key Assumption: Parallel trends — treated and control units would have followed
                parallel trajectories absent treatment.
Structure: Y_it = alpha_i + delta_t + beta * D_it + gamma * X_it + epsilon_it
"""
```

- Define the **target parameter** (ATE, ATT, LATE).
- List the **key assumptions** (parallel trends, continuity, exclusion restriction).
- Write the **structural equation** in comments.

---

## 3. Phase 2: Data Preprocessing

Run these checks before estimation:

1. **Panel balance**: If panel data, verify balance with `df.groupby('entity')['time'].count().describe()`.
2. **Missing values**: Do NOT let the estimator silently drop rows. Explicitly `dropna()` on the estimation sample and report the N before and after.
3. **Outliers**: Winsorize continuous variables at 1% and 99% if domain-appropriate. Log the operation.
4. **Collinearity**: Compute VIF for regressors. If any VIF > 10, flag multicollinearity.
5. **Treatment overlap**: For matching / propensity score, verify common support (propensity scores overlap between treated and control).

---

## 4. Phase 3: Estimation Standards

### 4.1 Standard Errors (Non-Negotiable)

**Never use spherical (homoskedastic) standard errors.** Always specify robust or clustered SEs:

- **Heteroskedasticity-robust**: `cov_type='HC3'` in `statsmodels` or `vcov = "hetero"` in `fixest`
- **Cluster-robust**: `cov_type='clustered', cluster_entity=True` in `linearmodels`, or `cluster = ~entity` in `fixest`
- **Two-way clustering**: `clusters=df[['firm', 'year']]` or `vcov = ~firm + year` in `fixest`

### 4.2 Model Output Requirements

Every regression output MUST include:
- Coefficients
- Standard errors (in parentheses)
- Significance stars (* p<0.1, ** p<0.05, *** p<0.01)
- Number of observations (N)
- R-squared or Adjusted R-squared
- Clustering level(s) noted in a footnote

### 4.3 Python Toolchain

| Task | Package | Function |
|---|---|---|
| OLS / Logit / Probit | `statsmodels.formula.api` | `smf.ols()`, `smf.logit()` |
| Panel FE / RE | `linearmodels.panel` | `PanelOLS`, `RandomEffects` |
| IV / 2SLS | `linearmodels.iv` | `IV2SLS` |
| Robust SE | `statsmodels` | `cov_type='HC3'` |
| Clustered SE | `linearmodels` | `cov_type='clustered'` |

### 4.4 R Toolchain (When Required)

| Task | Package | Function |
|---|---|---|
| High-dim FE | `fixest` | `feols(..., cluster = ~entity)` |
| Matching | `MatchIt` | `matchit()` |
| RDD | `rdrobust` | `rdrobust()` |

### 4.5 The Cunningham Verification (Cross-Language Check)

For any core benchmark regression that drives the paper's main claim, perform a cross-language verification:

1. Estimate the model in Python (`linearmodels` or `statsmodels`).
2. Generate equivalent R code (`fixest`) and run it.
3. Compare the key coefficient and standard error to at least 5 decimal places.
4. If they diverge, investigate data leakage, incorrect degrees of freedom, or SE specification before proceeding.

---

## 5. Phase 4: Diagnostics and Visualization

### 5.1 DiD — Event Study Plot

- Plot dynamic treatment effects (coefficients on leads and lags of treatment).
- Pre-treatment coefficients must have confidence intervals overlapping zero (parallel trends test).
- Use `seaborn` or `matplotlib` with `sns.despine()`, Okabe-Ito colors, and `dpi=300`.

### 5.2 RDD — Bin-Scatter Plot

- Plot outcome vs running variable with local polynomial fit on each side of cutoff.
- Draw a vertical dashed line at the cutoff.
- Include confidence bands.

### 5.3 Matching — Love Plot

- Plot standardized mean differences for all covariates before and after matching.
- Draw a horizontal line at 0.1 (common balance threshold).
- All post-matching points should fall below this line.

---

## 6. Phase 5: Output and Validation

### 6.1 Regression Tables

Use `statsmodels.iolib.summary2.summary_col` (Python) or `modelsummary` / `stargazer` (R) to produce multi-model comparison tables:
- Model 1: Baseline
- Model 2: + Controls
- Model 3: + Fixed Effects
- Model 4: + Robust SE / Clustered SE

Save the table as `.md` (Markdown) or `.tex` (LaTeX) in the `output/` directory.

### 6.2 Validation Checklist

1. [ ] **Theory**: Identification strategy and assumptions stated in comments
2. [ ] **Inference**: Robust or clustered SEs explicitly set (not default spherical)
3. [ ] **Sample**: N reported and stable across model specifications
4. [ ] **Cross-check**: Python and R coefficients match to 5 decimals (for benchmark models)
5. [ ] **Diagnostics**: Appropriate plot generated (event study, bin-scatter, or Love plot)
6. [ ] **Output**: Multi-model table saved to `output/` as Markdown or LaTeX
