"""
model.py  (BiLSTM classifier)
------------------------------
Defines the BiLSTM architecture used for the 5-class softmax emotion
classifier, plus helpers to load a trained model + tokenizer from
`models/bltsm/` and run inference.

If no trained artifacts are found, `load_bilstm()` returns None and
predict.py transparently falls back to the rule-based classifier in
preprocessing.py, so the rest of the app keeps working.

Expected artifacts in models/bltsm/:
    bilstm_student_adaptive.keras   (or bilstm_model.keras)
    tokenizer.json
    label_classes.json
"""

import os
import json
import numpy as np

from preprocessing import EMOTION_LABELS, clean_text, apply_keyword_boost

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models", "bltsm")
MAX_SEQUENCE_LENGTH = 80
VOCAB_SIZE = 30000
EMBEDDING_DIM = 128
LSTM_UNITS = 128


def build_bilstm_model(vocab_size=VOCAB_SIZE, embedding_dim=EMBEDDING_DIM,
                        max_len=MAX_SEQUENCE_LENGTH, lstm_units=LSTM_UNITS,
                        num_classes=len(EMOTION_LABELS)):
    """
    Build the BiLSTM architecture: Embedding -> Bidirectional LSTM -> Dense
    softmax. ~4.1M parameters at the default sizes, matching the trained
    checkpoint described in the project report.
    """
    from tensorflow import keras
    from tensorflow.keras import layers

    model = keras.Sequential([
        layers.Input(shape=(max_len,)),
        layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, mask_zero=True),
        layers.Bidirectional(layers.LSTM(lstm_units, return_sequences=False)),
        layers.Dropout(0.3),
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation="softmax"),
    ], name="bilstm_emotion_classifier")
    return model


def focal_loss(gamma=2.0, alpha=0.25):
    """
    Focal loss to counter class imbalance (minority classes: Bored, Frustrated),
    as used during BiLSTM training.
    """
    import tensorflow as tf

    def loss_fn(y_true, y_pred):
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)
        cross_entropy = -y_true * tf.math.log(y_pred)
        weight = alpha * tf.math.pow(1.0 - y_pred, gamma)
        return tf.reduce_sum(weight * cross_entropy, axis=-1)

    return loss_fn


def load_bilstm():
    """
    Load the trained BiLSTM model + tokenizer from disk.
    Returns (model, tokenizer) or (None, None) if artifacts are missing.
    """
    model_path_candidates = [
        os.path.join(MODEL_DIR, "bilstm_student_adaptive.keras"),
        os.path.join(MODEL_DIR, "bilstm_model.keras"),
    ]
    tokenizer_path = os.path.join(MODEL_DIR, "tokenizer.json")

    model_path = next((p for p in model_path_candidates if os.path.exists(p)), None)
    if model_path is None or not os.path.exists(tokenizer_path):
        return None, None

    try:
        from tensorflow import keras
        from tensorflow.keras.preprocessing.text import tokenizer_from_json

        model = keras.models.load_model(
            model_path, custom_objects={"loss_fn": focal_loss()}, compile=False
        )
        with open(tokenizer_path, "r", encoding="utf-8") as f:
            tokenizer = tokenizer_from_json(f.read())
        return model, tokenizer
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"[bilstm] Could not load model artifacts: {exc}")
        return None, None


def predict_bilstm(text: str, model, tokenizer) -> dict:
    """
    Run BiLSTM inference on a single text input and return the unified
    prediction schema (see predict.py:make_unified_schema).
    """
    from tensorflow.keras.preprocessing.sequence import pad_sequences

    cleaned = clean_text(text)
    seq = tokenizer.texts_to_sequences([cleaned])
    padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post")

    raw_probs = model.predict(padded, verbose=0)[0]
    probs = apply_keyword_boost(raw_probs, cleaned)

    top_idx = int(np.argmax(probs))
    scores = {label: float(p) for label, p in zip(EMOTION_LABELS, probs)}

    return {
        "emotion": EMOTION_LABELS[top_idx],
        "confidence": float(probs[top_idx]),
        "emotion_scores": scores,
        "cleaned_text": cleaned,
        "model_used": "BiLSTM",
    }
