# Text-as-Data and NLP Reference

Use this reference when text is evidence, a measurement instrument, a treatment/outcome, or a prediction target. Begin with the social-science task and construct; a model output is not automatically a valid measure.

## 1. Route by research task

| Task | Core question | Typical outputs |
|---|---|---|
| Selection and representation | Which texts enter the corpus, and how are they represented? | Corpus manifest, document units, features/embeddings |
| Discovery | What unanticipated themes, frames, or structures appear? | Candidate topics/clusters and close-reading evidence |
| Measurement | How much of a defined construct is present? | Validated labels, scores, dictionaries, or classifiers |
| Prediction | How well can text predict a target in the deployment setting? | Held-out performance, calibration, subgroup errors |
| Causal inference | How is text used as treatment, outcome, mediator, or confounder? | Identification strategy plus leakage-safe text measurement |

Do not collapse these tasks. Discovery can propose a construct but does not by itself validate a measure; predictive accuracy does not establish construct validity; a text-derived score does not identify a causal effect.

## 2. Corpus and construct contract

Before preprocessing, document:

- theoretical construct and what would count as positive, negative, ambiguous, or out-of-scope evidence;
- document and annotation unit (post, sentence, speaker-turn, article, organization-period, etc.);
- source platforms/archives, collection window, search terms, languages, genres, and inclusion/exclusion rules;
- target population and how the observed corpus differs from it;
- duplicates, reposts, quoted material, bots, missing/deleted content, OCR, and temporal drift;
- whether labels are descriptive, normative, inferred mental states, or proxies;
- who annotates, with what instructions, and whose standpoint the label scheme encodes.

Corpus construction is not value-free. Retain a manifest with source identifiers, retrieval timestamps, hashes where permitted, and exclusion reasons. Keep raw text separate from normalized representations.

## 3. Preprocessing is a model choice

Use the lightest transformation compatible with the task, language, and model. Preserve the raw text and implement preprocessing as a reproducible pipeline.

- Do not automatically strip URLs, hashtags, punctuation, case, emojis, named entities, or formatting; each can carry social meaning.
- Do not impose stopword removal, stemming/lemmatization, POS filtering, or fixed `min_df`/`max_df` thresholds as universal rules.
- For transformers and LLMs, generally preserve syntax and use the tokenizer/model's documented limits and truncation policy. Quantify what is truncated and whether truncation is socially patterned.
- For Chinese and other languages without whitespace token boundaries, use language-appropriate segmentation or character/subword representations and test dictionary/tokenizer coverage.
- For multilingual corpora, assess language detection, translation, and model equivalence; do not assume scores are comparable across languages.
- Remove markup or boilerplate only after checking whether it encodes source, genre, or interaction context.

For unsupervised analysis, vary consequential preprocessing choices and report how topics, clusters, or substantive conclusions change. A single coherence-maximizing pipeline is not enough.

## 4. Discovery

Discovery outputs are candidates for interpretation, not finished constructs.

- Choose topic/cluster granularity using interpretability, exclusivity/separation, stability, and usefulness for the research question, not one metric alone.
- Inspect representative, high-probability, borderline, and contradictory documents for every reported topic/cluster.
- Refit across seeds, preprocessing regimes, samples/time slices, and plausible numbers of topics. Align solutions before comparing stability.
- Document researcher decisions in labeling, merging, splitting, or discarding topics.
- Use word lists and two-dimensional maps as diagnostics; neither is sufficient validation by itself.

## 5. Measurement and annotation

Treat dictionaries, classifiers, embeddings, topic proportions, and LLM labels as measurement models.

Build validity evidence appropriate to the claim:

- **Substantive/content evidence:** coverage of the construct definition and close reading of cases.
- **Structural evidence:** expected internal relationships, dimensionality, and known-group patterns.
- **Convergent/discriminant evidence:** agreement with related measures and separation from distinct constructs.
- **External/criterion evidence:** association with independent outcomes or expert judgments when theoretically warranted.
- **Generalization evidence:** performance across time, sources, languages, genres, and socially relevant groups.

For human annotation:

- pilot the codebook on difficult cases and revise before the final holdout is labeled;
- use independent double coding for a justified subset; report disagreement and an appropriate reliability measure, not agreement alone;
- retain ambiguous/abstain options where the construct requires them;
- separate adjudication data from final evaluation data;
- report class prevalence, confusion matrices, per-class uncertainty, and examples of systematic error.

Do not mandate a fixed sample size such as 100-500. Choose annotation size from prevalence, desired precision, subgroup needs, and available resources.

## 6. Prediction

- Split data to match deployment: by time for future prediction, by author/organization/thread for group generalization, and before duplicated or near-duplicated content can cross folds.
- Keep preprocessing, feature selection, prompt/model selection, and threshold tuning inside the training/validation process.
- Use a simple interpretable baseline when it is a meaningful comparator, not as a ritual prerequisite for every pretrained model.
- Report task-relevant metrics with uncertainty: per-class precision/recall/F1, macro averages for imbalance, PR-AUC when appropriate, calibration, and subgroup error.
- Compare against prevalence, heuristic, or human baselines that expose whether the model adds value.
- Perform qualitative error analysis on false positives/negatives, low-confidence cases, and relevant subgroups.

## 7. LLM-assisted coding

- Record provider/model identifier, access date or version, prompt/system instructions, examples, decoding settings, tool/retrieval context, and preprocessing.
- Use structured outputs and schema validation for production coding. Preserve raw responses or hashes when allowed.
- Measure run-to-run and prompt sensitivity when the API is stochastic or the model is mutable.
- Keep a human-labeled evaluation set that was not used to write prompts or select examples. Report agreement and substantive failure modes.
- Do not send restricted or identifiable text to an external service without authorization and an appropriate data-handling agreement.

## 8. Text in causal inference

First identify the role of text: treatment, treatment component, outcome, confounder proxy, mediator, or effect modifier. Define the causal estimand before learning the text representation.

When the same data are used to discover a latent textual measure and estimate its causal relationship, overfitting and identification problems can arise. Use a design such as sample splitting or cross-fitting so that construct discovery/model selection is separated from causal-effect estimation. Freeze the mapping before estimating effects on the held-out sample, and propagate measurement uncertainty when feasible.

Avoid conditioning on post-treatment text or colliders. If text is a treatment, articulate the manipulable intervention/version; if text is an outcome, clarify which changes in language count as the outcome and validate the mapping independently.

## 9. Reporting checklist

- [ ] Task is labeled as representation, discovery, measurement, prediction, causal inference, or a justified combination.
- [ ] Corpus boundary, provenance, units, language/genre/time, exclusions, and ethical constraints are documented.
- [ ] Construct and annotation rules are explicit; automated outputs are not equated with theory by assertion.
- [ ] Preprocessing choices are reproducible and consequential alternatives are tested.
- [ ] Train/validation/test separation matches the generalization or causal design and prevents leakage.
- [ ] Quantitative metrics include uncertainty and are paired with close reading/error analysis.
- [ ] Text-derived causal variables use a leakage-safe workflow and an explicit estimand.
- [ ] Prompts, model versions, seeds/settings, code, and output provenance are retained where permitted.

## Primary sources

- Grimmer, Roberts, and Stewart (2022), [*Text as Data*](https://press.princeton.edu/books/hardcover/9780691207544/text-as-data), organized around representation, discovery, measurement, prediction, and causal inference; a local PDF was reviewed for this revision.
- Grimmer and Stewart (2013), [promise, pitfalls, close reading, and problem-specific validation](https://doi.org/10.1093/pan/mps028).
- Denny and Spirling (2018), [preprocessing sensitivity for unsupervised learning](https://doi.org/10.1017/pan.2017.44).
- Egami et al. (2022), [causal inference with text and split-sample workflows](https://doi.org/10.1126/sciadv.abg2652).
- Birkenmaier, Wagner, and Lechner (2023), [ValiText](https://arxiv.org/abs/2307.02863), used as a supplementary preprint framework for substantive, structural, and external validity evidence.
