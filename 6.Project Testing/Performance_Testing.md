# Performance Testing

## Test Environment
Python 3.9+, syntax/unit checks run without GPU (models trained separately
on Kaggle per Epic 2).

## 1. Static/Syntax Validation

All core modules compiled cleanly with `python3 -m py_compile`:

| Module | Result |
|---|---|
| `src/preprocessing.py` | ✅ OK |
| `src/model.py` | ✅ OK |
| `src/bert_model.py` | ✅ OK |
| `src/predict.py` | ✅ OK |
| `src/train.py` | ✅ OK |
| `app.py` | ✅ OK |

## 2. Functional Test — Rule-Based Fallback Classifier

Input: *"I am so confused and frustrated, I don't understand this at all,
why is this so hard!"*

```
{'emotion': 'Frustrated', 'confidence': 0.6675,
 'emotion_scores': {'Bored': 0.03, 'Confident': 0.03, 'Confused': 0.2425,
                     'Curious': 0.03, 'Frustrated': 0.6675}}
mixed_emotion -> "Frustrated + Confused"
```

Input: *"I get it now, this makes sense, I feel confident about it"*

```
{'emotion': 'Confident', 'confidence': 0.88, ...}
mixed_emotion -> "Confident"
```

**Result:** Correctly separates single-emotion vs. mixed-emotion cases,
and keyword boosts produce intuitively-ranked confidence scores.

## 3. Functional Test — CSV Persistence Round Trip

```
predict_emotion("I am so confused and frustrated with this recursion problem")
  -> primary emotion: Confused, mixed: "Confused + Frustrated"
save_interaction_to_csv(...) -> row appended successfully
load_csv_examples() -> returns the row back with all fields intact
```

`emotion_response_examples.csv` and `emotion_response_mapping.csv` were
verified to contain correctly formatted headers and rows after the round
trip, with no data loss or corruption on repeated writes.

## 4. Model Loading Resilience Test

With `models/bltsm/` and `models/bert_emotion_model_final/` both empty,
`predict.get_models()` correctly returns `(None, None)` for both, and
`predict_emotion()` transparently falls back to
`preprocessing.rule_based_predict()` — confirming NFR-1 (app must run
without trained weights).

## 5. Cross-Browser / UI Checks (manual)
- Verified layout renders consistently in Chrome and Edge (wide layout,
  sidebar collapse/expand, tab navigation).
- Verified progress bars, metrics, and Plotly charts render without
  console errors.

## 6. Load/Response-Time Observations
- Rule-based fallback: near-instant (<50ms) per prediction.
- BiLSTM/BERT inference (once trained and cached): expected sub-second on
  CPU for single-sentence inputs, consistent with model sizes reported in
  `PROJECT_ANALYSIS_REPORT.md` (4.1M params BiLSTM; base-sized BERT).

## Known Issues / Follow-ups
- Gemini API latency depends on network conditions; template fallback
  mitigates user-facing impact.
- Full BiLSTM/BERT inference timing should be re-measured after training
  on the target deployment hardware.
