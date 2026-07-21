# Reproducibility, Data Stewardship, and Responsible Research

Read this reference for durable empirical or simulation results and whenever data concern people, platforms, organizations, or restricted sources. Scale the requirements to the claim: an exploratory notebook needs fewer artifacts than a publication replication package, but it still needs enough provenance to avoid misleading results.

## 1. Reproducibility contract

Treat reproducibility as the ability of an independent researcher to obtain the reported results from the stated data, code, environment, and execution instructions.

For a publication-grade project, provide or document:

1. A data-availability statement covering source and derived data, how access is obtained, legal or contractual restrictions, expected access cost/time, and a persistent identifier when available.
2. Immutable source data or an exact retrieval recipe. Keep source, intermediate, and analysis data distinct.
3. Metadata or a codebook with meaningful variable names, units, allowed values, missing-value codes, identifiers, and transformation provenance.
4. All code that produces analysis data and reported tables, figures, estimates, and simulations.
5. A master script or exact ordered commands that run with minimal manual intervention.
6. A dependency lockfile or environment specification, software versions, relevant hardware details, RNG information, and expected runtime.
7. A README that maps each program to its inputs/outputs and each reported artifact to the paper, appendix, or claim it supports.
8. Data and software citations plus an explicit license for redistributable materials.

When data cannot be shared, still release code when permitted, document provenance and access conditions, provide a synthetic or schema-compatible test fixture when safe, and explain which verification steps require authorized data. Never place restricted data in a public or draft deposit.

## 2. File and workflow design

A useful default layout is:

```text
project/
├── README.md
├── data/
│   ├── raw/          # immutable or retrieval manifests
│   ├── interim/      # reproducible transformations
│   └── analysis/     # model-ready data
├── src/ or scripts/
├── tests/
├── environment.yml, requirements.lock, renv.lock, or equivalent
└── results/          # generated, with a result-to-claim map
```

Do not impose this layout on an established project. Preserve its conventions while ensuring the same separation and traceability.

At consequential pipeline boundaries, validate:

- row/entity/document/node/edge counts and uniqueness;
- join cardinality and unmatched keys;
- types, units, ranges, missingness, and timestamps;
- stable identifiers and source-to-derived lineage;
- exclusions and their effect on the analysis population;
- output schemas consumed downstream.

## 3. Randomness and computational environments

- Seed only stochastic components. Pass a seed or RNG object through APIs rather than relying on hidden global state.
- Record the seed sequence, RNG implementation, number of replicates, package versions, and any nondeterministic accelerator settings.
- For stochastic findings, estimate Monte Carlo uncertainty and show robustness across justified seeds or replicates. One repeated seed checks determinism, not scientific stability.
- Pin exact versions for frozen replication artifacts. For active development, use constrained versions plus tests and record the resolved environment.
- Capture the command, working directory, input version/hash, output location, runtime, and exit status for long or expensive runs.

## 4. FAIR and reusable research objects

Apply FAIR principles to data, code, models, and metadata where appropriate:

- **Findable:** persistent identifiers, rich searchable metadata, and explicit links between objects.
- **Accessible:** documented protocols and authentication/authorization conditions; retain metadata even when data cannot remain accessible.
- **Interoperable:** open formats, explicit schemas, standard vocabularies, and qualified links among objects.
- **Reusable:** provenance, licenses, community standards, units, codebooks, and enough context to interpret the object correctly.

FAIR does not mean unrestricted public release. Restricted access can be FAIR when the access procedure and metadata are clear.

## 5. Testing and independent verification

Use the smallest relevant stack:

- unit tests for deterministic transformations and metrics;
- fixture-based integration tests for the raw-to-result path;
- schema and invariant checks at boundaries;
- smoke tests that run on a small sample;
- regression tests for established outputs, with justified tolerances;
- a clean-environment rerun of the master entry point before release.

Separate software correctness from scientific validity. Passing tests cannot establish exchangeability, construct validity, model adequacy, or ethical acceptability.

## 6. Responsible-research screen

Before collecting, linking, modeling, or publishing data about people or communities, document:

1. **Purpose and stakeholders:** who benefits, who bears risk, who is missing, and who has power to shape or contest the research.
2. **Consent and expectations:** whether the use is consistent with consent, terms, community norms, and reasonable expectations. Publicly visible data are not automatically ethically unrestricted.
3. **Privacy and security:** direct identifiers, quasi-identifiers, linkage/re-identification risk, access controls, retention, and disclosure review.
4. **Representation and bias:** coverage, platform selection, language, historical exclusions, labeler standpoint, subgroup error, and downstream distributional effects.
5. **Potential harms:** material, reputational, political, psychological, group-level, and institutional harms, including harms caused by absence or misclassification.
6. **Dual use and deployment:** plausible misuse, surveillance, targeting, or automation beyond the research setting; who can access models and outputs.
7. **Governance:** ethics/IRB review where applicable, data-use agreements, incident response, community consultation, and limitations on release.

When values conflict, surface the tradeoff and mitigation rather than converting ethics into a checkbox or a single fairness metric.

## 7. Release checklist

- [ ] Data-availability statement and access conditions are accurate.
- [ ] Raw, derived, and analysis layers are distinguishable and traceable.
- [ ] Metadata, licenses, software citations, and persistent identifiers are present where possible.
- [ ] Master entry point or exact run order reproduces reported outputs.
- [ ] Environment, runtime, hardware-sensitive settings, RNG, and replicates are recorded.
- [ ] Programs map to outputs and outputs map to claims.
- [ ] Restricted data and sensitive outputs have an explicit release decision.
- [ ] Stakeholders, privacy, representation, harms, and dual use have been assessed.

## Primary sources

- [American Economic Association, Data and Code Availability Policy (February 2026)](https://www.aeaweb.org/journals/data/data-code-policy)
- [The Turing Way, Guide for Reproducible Research](https://book.the-turing-way.org/reproducible-research/reproducible-research/)
- [Wilkinson et al. (2016), FAIR Guiding Principles](https://doi.org/10.1038/sdata.2016.18)
- [National Academies (2022), Fostering Responsible Computing Research](https://doi.org/10.17226/26507)
- Salganik (2018), *Bit by Bit: Social Research in the Digital Age*, especially the ethics chapter; an English and Chinese edition were supplied as local reference copies for this revision.
