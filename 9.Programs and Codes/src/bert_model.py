"""
bert_model.py
-------------
Fine-tuned BERT (bert-base-uncased) classifier wrapper: loading, class
weighting, and keyword-based confidence/confusion adjustments.

Expected artifacts in models/bert_emotion_model_final/:
    config.json, model.safetensors (or pytorch_model.bin),
    tokenizer.json, tokenizer_config.json, vocab.txt,
    special_tokens_map.json, label_mapping.json
"""

import os
import numpy as np

from preprocessing import (
    EMOTION_LABELS,
    BERT_CLASS_WEIGHTS,
    CONFIDENT_BOOST,
    CONFUSED_BOOST,
    clean_text,
)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models", "bert_emotion_model_final")
MAX_LENGTH = 128
LEARNING_RATE = 2e-5
EPOCHS = 3


def load_bert():
    """
    Load the fine-tuned BERT model + tokenizer from disk.
    Returns (model, tokenizer) or (None, None) if artifacts are missing.
    """
    required = ["config.json", "tokenizer_config.json"]
    if not all(os.path.exists(os.path.join(MODEL_DIR, f)) for f in required):
        return None, None

    try:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        model.eval()
        return model, tokenizer
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"[bert] Could not load model artifacts: {exc}")
        return None, None


def _apply_class_weights(probs: np.ndarray) -> np.ndarray:
    weighted = probs * BERT_CLASS_WEIGHTS
    return weighted / weighted.sum()


def _apply_keyword_adjustments(probs: np.ndarray, text: str) -> np.ndarray:
    lowered = text.lower()
    from preprocessing import EMOTION_KEYWORDS

    adjusted = probs.copy()
    if any(kw in lowered for kw in EMOTION_KEYWORDS["Confident"]):
        adjusted[EMOTION_LABELS.index("Confident")] *= CONFIDENT_BOOST
    if any(kw in lowered for kw in EMOTION_KEYWORDS["Confused"]):
        adjusted[EMOTION_LABELS.index("Confused")] *= CONFUSED_BOOST
    return adjusted / adjusted.sum()


def predict_bert(text: str, model, tokenizer) -> dict:
    """
    Run BERT inference on a single text input, apply class weighting and
    keyword adjustments, and return the unified prediction schema.
    """
    import torch

    cleaned = clean_text(text)
    inputs = tokenizer(
        cleaned, return_tensors="pt", truncation=True,
        padding=True, max_length=MAX_LENGTH,
    )
    with torch.no_grad():
        logits = model(**inputs).logits
    raw_probs = torch.softmax(logits, dim=-1).numpy()[0]

    probs = _apply_class_weights(raw_probs)
    probs = _apply_keyword_adjustments(probs, cleaned)

    top_idx = int(np.argmax(probs))
    scores = {label: float(p) for label, p in zip(EMOTION_LABELS, probs)}

    return {
        "emotion": EMOTION_LABELS[top_idx],
        "confidence": float(probs[top_idx]),
        "emotion_scores": scores,
        "cleaned_text": cleaned,
        "model_used": "BERT",
    }
