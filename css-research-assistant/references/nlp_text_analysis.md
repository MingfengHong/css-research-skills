# Text Analysis and NLP Reference

## Table of Contents
1. [Intent Routing](#1-intent-routing)
2. [Phase 1: Construct Validity](#2-phase-1-construct-validity)
3. [Phase 2: Preprocessing Rules](#3-phase-2-preprocessing-rules)
4. [Phase 3: Modeling Standards](#4-phase-3-modeling-standards)
5. [Phase 4: Validation Protocol](#5-phase-4-validation-protocol)
6. [Phase 5: Output and Diagnostics](#6-phase-5-output-and-diagnostics)

---

## 1. Intent Routing

Classify the user's NLP goal before writing code:

| Route | Condition | Toolchain |
|---|---|---|
| **Text-as-Frequency** | User asks "What is in the text?" — macro overview, topic discovery, agenda setting | `Gensim` (LDA), `BERTopic`, `sklearn` (TF-IDF) |
| **Text-as-Relations** | User asks "How are concepts related?" — cultural mapping, bias detection, semantic change | `Gensim` (Word2Vec, FastText), `GloVe` |
| **Text-as-Structure** | User asks "Who did what to whom?" — framing, agency, responsibility attribution | `spaCy` (dependency parsing, SRL, NER) |
| **Text-as-Dynamic-Context** | User needs nuanced classification, few-shot labeling, irony detection, or simulating human agents | `transformers` (Hugging Face), encoder (BERT) for discrimination, decoder (GPT) for generation |

---

## 2. Phase 1: Construct Validity

Before preprocessing, answer:
- What **latent construct** are we measuring? (e.g., political polarization, media framing, public sentiment)
- What **language and genre**? (English news, Chinese social media, academic abstracts)
- What **method-theory match**? Unsupervised for exploration; supervised or dictionary-based for specific constructs.

State the construct and its operationalization in a comment block at the top of the script.

---

## 3. Phase 2: Preprocessing Rules

### 3.1 All Routes — Universal Cleaning

- Force `encoding='utf-8'` on all file reads.
- Remove invisible characters (`\u200b`, zero-width spaces).
- Strip HTML tags and URLs with regex.

### 3.2 Route: Text-as-Frequency AND Text-as-Relations

**Rigorous cleaning required**:
- Tokenize with `spaCy` (use POS tagging; keep nouns, verbs, adjectives for topic modeling).
- Remove stopwords using an explicit stopword list.
- **Lemmatize** (do NOT stem). Use `token.lemma_` from `spaCy`.
- Filter by document frequency: `min_df >= 2` (or 5 for large corpora), `max_df <= 0.95`.

### 3.3 Route: Text-as-Dynamic-Context (Transformers)

**Minimal cleaning**:
- Do NOT remove stopwords, punctuation, or lowercase text (unless using an uncased model).
- Preserve syntax — attention mechanisms rely on it.
- Truncate at `max_length=512` (or model-specific limit). Use `truncation=True, padding=True`.

### 3.4 Route: Text-as-Structure

- Run full `spaCy` pipeline: tokenization, POS, dependency parsing, NER.
- Extract Subject-Verb-Object (SVO) triplets from dependency trees.
- Flag active vs. passive voice for agency analysis.

---

## 4. Phase 3: Modeling Standards

### 4.1 Baseline Requirement

Before using deep learning, establish a **TF-IDF + LinearSVC / LogisticRegression** baseline. Report its F1-macro. Only proceed to transformers if the baseline is insufficient.

### 4.2 Topic Modeling (Text-as-Frequency)

- Use `Gensim.LdaModel` or `BERTopic`.
- Do NOT choose topic count `K` arbitrarily. Compute **topic coherence score** (`C_v` or `u_mass`) across a range of `K` values and justify the choice.
- Output `pyLDAvis` or equivalent intertopic distance map to check topic overlap.

### 4.3 Embeddings (Text-as-Relations)

- Train Word2Vec / FastText with `Gensim`. Fix `seed` parameter.
- Report vector analogies or cosine similarities with explicit sociological interpretation.
- Acknowledge polysemy in comments: static embeddings average all token contexts.

### 4.4 Transformers (Text-as-Dynamic-Context)

- Use `transformers` pipeline or `AutoModelForSequenceClassification`.
- Fix all seeds:
  ```python
  import torch, numpy as np, random
  SEED = 42
  torch.manual_seed(SEED)
  np.random.seed(SEED)
  random.seed(SEED)
  ```
- For fine-tuning, use `TrainingArguments(seed=SEED)`.

---

## 5. Phase 4: Validation Protocol

### 5.1 Human-in-the-Loop

For any classification or labeling task, extract a **stratified random sample** (N=100–200) and format it for manual blind annotation. Save it as `output/annotation_sample.csv`.

### 5.2 Cross-Method Verification

If using dictionary-based sentiment, compare against a pretrained classifier (e.g., RoBERTa-sentiment) on a random subset. Report Pearson correlation. If r < 0.6, investigate divergence.

### 5.3 NER / IE Validation

For `spaCy`-extracted entities, sample the top 50 most frequent entities. Flag false positives and write post-processing rules to remove systematic errors (e.g., "Figure" misclassified as PERSON).

---

## 6. Phase 5: Output and Diagnostics

### 6.1 Classification Metrics

Never report accuracy alone. Use `sklearn.metrics.classification_report` to output:
- Precision, Recall, F1 per class
- Macro-averaged and weighted-averaged F1
- For imbalanced data, include PR curve

### 6.2 Visualization Rules

- Use `seaborn` with `sns.despine()`, Okabe-Ito or Viridis palettes.
- For high-dimensional embeddings, use t-SNE or UMAP with fixed `random_state`.
- **Avoid word clouds** in final outputs. Use bar charts of top TF-IDF weights or feature importances instead.

### 6.3 Validation Checklist

1. [ ] Construct validity: Text representation matches the social-science measurement target
2. [ ] Preprocessing defense: Strategy correctly matched to downstream model (DL text not over-cleaned)
3. [ ] Baseline: TF-IDF + linear model baseline reported before using BERT
4. [ ] Metrics: Full Precision, Recall, F1 matrix reported
5. [ ] Reproducibility: All random processes fixed with seed=42
