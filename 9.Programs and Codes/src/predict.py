"""
predict.py
----------
Orchestrates the full emotion-detection pipeline:

1. Load BiLSTM + BERT models (cached). If neither is available, fall back
   to the zero-dependency rule-based classifier so the app always runs.
2. Run inference through whichever model(s) are available.
3. Detect mixed emotions (secondary emotions with score >= 15%).
4. Persist every interaction to CSV for continuous learning / analytics.
"""

import os
import csv
from datetime import datetime

from preprocessing import EMOTION_LABELS, MIXED_EMOTION_THRESHOLD, rule_based_predict

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
EXAMPLES_CSV = os.path.join(BASE_DIR, "emotion_response_examples.csv")
MAPPING_CSV = os.path.join(BASE_DIR, "emotion_response_mapping.csv")

_MODEL_CACHE = {}


def get_models(use_streamlit_cache=True):
    """
    Load and cache BiLSTM + BERT models. When running inside Streamlit,
    wraps loading with st.cache_resource so models are loaded once per
    server process. Falls back to a plain in-memory cache otherwise
    (e.g. when called from tests or train.py).
    """
    if "bilstm" in _MODEL_CACHE and "bert" in _MODEL_CACHE:
        return _MODEL_CACHE["bilstm"], _MODEL_CACHE["bert"]

    def _load():
        from model import load_bilstm
        from bert_model import load_bert
        return load_bilstm(), load_bert()

    if use_streamlit_cache:
        try:
            import streamlit as st

            @st.cache_resource(show_spinner="Loading emotion detection models...")
            def _cached_load():
                return _load()

            (bilstm_model, bilstm_tok), (bert_model, bert_tok) = _cached_load()
        except Exception:
            (bilstm_model, bilstm_tok), (bert_model, bert_tok) = _load()
    else:
        (bilstm_model, bilstm_tok), (bert_model, bert_tok) = _load()

    _MODEL_CACHE["bilstm"] = (bilstm_model, bilstm_tok)
    _MODEL_CACHE["bert"] = (bert_model, bert_tok)
    return _MODEL_CACHE["bilstm"], _MODEL_CACHE["bert"]


def detect_mixed_emotion(emotion_scores: dict, threshold: float = MIXED_EMOTION_THRESHOLD) -> str:
    """
    Return a display string combining every emotion whose score exceeds the
    threshold (e.g. "Curious + Confused"), ordered by descending score.
    Falls back to the single top emotion when only one clears the bar.
    """
    above = [(label, score) for label, score in emotion_scores.items() if score >= threshold]
    above.sort(key=lambda x: x[1], reverse=True)
    if len(above) <= 1:
        top_label = max(emotion_scores, key=emotion_scores.get)
        return top_label
    return " + ".join(label for label, _ in above)


def predict_emotion(text: str, use_csv_examples: bool = False) -> dict:
    """
    Main entry point. Returns a dict with keys:
        bilstm (unified schema or None)
        bert (unified schema or None)
        primary (the schema used as the "main" result for downstream logic)
        mixed_emotion (display string, e.g. "Curious + Confused")
    """
    (bilstm_model, bilstm_tok), (bert_model, bert_tok) = get_models()

    bilstm_result = None
    bert_result = None

    if bilstm_model is not None and bilstm_tok is not None:
        from model import predict_bilstm
        bilstm_result = predict_bilstm(text, bilstm_model, bilstm_tok)

    if bert_model is not None and bert_tok is not None:
        from bert_model import predict_bert
        bert_result = predict_bert(text, bert_model, bert_tok)

    if bilstm_result is None and bert_result is None:
        # No trained artifacts on disk -> zero-dependency fallback so the
        # application remains fully functional out of the box.
        fallback = rule_based_predict(text)
        bilstm_result = fallback

    primary = bert_result if bert_result is not None else bilstm_result
    mixed_emotion = detect_mixed_emotion(primary["emotion_scores"])

    return {
        "bilstm": bilstm_result,
        "bert": bert_result,
        "primary": primary,
        "mixed_emotion": mixed_emotion,
    }


def save_interaction_to_csv(text: str, emotion: str, confidence: float,
                             response: str, field: str,
                             emotion_scores: dict = None, model_type: str = "primary"):
    """
    Append one interaction to emotion_response_examples.csv, and upsert the
    (field, emotion) -> response pair into emotion_response_mapping.csv for
    future reuse (the "use CSV examples" option in the UI).
    """
    file_exists = os.path.exists(EXAMPLES_CSV)
    with open(EXAMPLES_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "field", "text", "emotion", "confidence",
                              "response", "model_type"])
        writer.writerow([
            datetime.now().isoformat(), field, text, emotion,
            round(confidence, 4), response, model_type,
        ])

    _upsert_mapping(field, emotion, response)


def _upsert_mapping(field: str, emotion: str, response: str):
    rows = []
    header = ["field", "emotion", "response"]
    if os.path.exists(MAPPING_CSV):
        with open(MAPPING_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    key = (field, emotion)
    found = False
    for row in rows:
        if (row["field"], row["emotion"]) == key:
            row["response"] = response
            found = True
            break
    if not found:
        rows.append({"field": field, "emotion": emotion, "response": response})

    with open(MAPPING_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def load_csv_examples(field: str = None, emotion: str = None):
    """Read stored examples, optionally filtered by field and/or emotion."""
    if not os.path.exists(EXAMPLES_CSV):
        return []
    with open(EXAMPLES_CSV, "r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if field:
        rows = [r for r in rows if r["field"] == field]
    if emotion:
        rows = [r for r in rows if r["emotion"] == emotion]
    return rows
