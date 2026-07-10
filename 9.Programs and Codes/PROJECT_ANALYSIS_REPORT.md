# Project Analysis Report — Emotion Detection & Learning Support Engine

## 1. Purpose

Detect learning-related emotions (Bored, Confident, Confused, Curious,
Frustrated) from free-text student input and respond with empathetic,
field-aware, AI-generated guidance — helping learners feel understood and
giving educators visibility into class-wide emotional patterns.

## 2. Data

Five sources were unified into a single 198,476-row dataset spanning the
five target classes: GoEmotions, EmpatheticDialogues, ISEAR, and two
supplementary academic-context sources. Text was cleaned with regex while
preserving emotion-carrying punctuation (`!`, `?`, `...`).

## 3. Models

| Model | Architecture | Accuracy | Notes |
|---|---|---|---|
| BiLSTM (baseline) | Embedding(128) + BiLSTM(128), 4.1M params | 95% | Focal loss (γ=2.0) for class imbalance |
| BiLSTM (student-adaptive) | Fine-tuned on 10K student samples | 100% (val, student domain) | Exported as `bilstm_student_adaptive.keras` |
| BERT (`bert-base-uncased`) | Fine-tuned, 3 epochs, AdamW, lr=2e-5 | 95% | Class-weighted logits + keyword adjustments |

Per-class F1 highlights: Curious 1.00, Confused 0.93–0.99 across both
models, reflecting strong separability of these two classes versus the
more overlapping Bored/Frustrated pair.

## 4. Inference Pipeline

1. `preprocessing.py` — cleaning + keyword lexicon (10x scoring weight per hit).
2. `model.py` / `bert_model.py` — per-model inference, class weighting
   `[1.2, 1.8, 0.6, 1.0, 1.4]` for BERT, keyword boosts (Confident ×2.5,
   Confused ×2.0).
3. `predict.py` — unifies both outputs into one schema, detects mixed
   emotions at a ≥15% secondary-score threshold, persists to CSV.
4. `app.py` — Streamlit UI: input → prediction → Gemini/template response →
   analytics dashboard.

## 5. Reliability & Fallback Design

Trained model weights are large binaries and are intentionally **not**
committed to this repository (see `models/*/README.md`). `predict.py`
detects their absence and transparently swaps in a rule-based classifier
built from the same keyword lexicon, so the application is always runnable
end-to-end — this was verified during development (see
`06_Project_Testing/Performance_Testing.md`).

## 6. Known Limitations

- Bored vs. Frustrated show the most class confusion (adjacent negative
  affect states in academic text).
- Rule-based fallback is a reasonable demo substitute but is less nuanced
  than the trained models on ambiguous phrasing.
- Gemini responses depend on an external API key and network access;
  template fallback exists precisely for this reason.

## 7. Future Work

See `08_Project_Demonstration/Scalability_and_Future_Plan.md`.
