# Proposed Solution

## Title
**Emotion Detection & Learning Support Engine** — an AI-powered learning
assistant that detects learning-related emotions from student text and
delivers personalized, empathetic academic guidance.

## Solution Summary

1. **Input** — Student selects their academic field (11 options) and
   describes their problem/feeling in free text.
2. **Preprocessing** — Text is cleaned while preserving emotion-carrying
   punctuation; keyword lexicon scoring is computed per emotion class.
3. **Dual-Model Classification** —
   - *BiLSTM*: Embedding → Bidirectional LSTM → Dense softmax over 5 classes,
     trained with Focal Loss for class imbalance, further domain-adapted on
     student-specific text.
   - *BERT*: Fine-tuned `bert-base-uncased`, with class weighting
     `[1.2, 1.8, 0.6, 1.0, 1.4]` and keyword-based confidence/confusion
     boosts.
   - If neither trained model is present, a transparent rule-based
     fallback (same keyword lexicon) keeps the app fully functional.
4. **Mixed-Emotion Detection** — Any emotion scoring ≥15% is surfaced
   alongside the primary label (e.g. "Curious + Confused").
5. **Guidance Generation** — A field- and emotion-aware prompt is sent to
   Gemini 2.5 Flash; if unavailable, a curated template (emoji + supportive
   message + concrete next step) is used instead.
6. **Persistence & Analytics** — Every interaction is logged to CSV and to
   Streamlit session state, feeding a 3-tab analytics dashboard (Emotions,
   Fields, Summary) built with Plotly.

## Differentiators

- **Never fails silently**: rule-based fallback + template fallback mean
  the demo/production app works with zero external dependencies configured.
- **Dual-model transparency**: showing both BiLSTM and BERT predictions
  builds trust and enables model comparison rather than a black box.
- **Mixed-emotion nuance**: avoids forcing a single label on genuinely
  mixed emotional states, which is common in real academic struggle.

## Target Users
Individual learners (primary), tutors/educators (secondary, via analytics),
and institutions evaluating emotion-aware EdTech tooling (tertiary).
