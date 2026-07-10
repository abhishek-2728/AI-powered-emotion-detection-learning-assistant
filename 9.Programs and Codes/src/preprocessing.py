"""
preprocessing.py
----------------
Text preprocessing and keyword-enhancement utilities for the
Emotion Detection & Learning Support Engine.

Responsibilities
- Clean raw student input while preserving emotion-carrying punctuation
  (e.g. "!", "?", "...") because they carry signal for Bored/Frustrated/Curious.
- Provide a keyword lexicon per emotion class used to (a) boost model
  probabilities when explicit emotion words are present and (b) act as a
  zero-dependency rule-based fallback classifier when no trained model
  weights are available on disk (see predict.py).

Emotion classes (fixed order used everywhere in this project):
    0 -> Bored
    1 -> Confident
    2 -> Confused
    3 -> Curious
    4 -> Frustrated
"""

import re
import numpy as np

EMOTION_LABELS = ["Bored", "Confident", "Confused", "Curious", "Frustrated"]

# Keyword lexicon: emotion -> list of trigger words / phrases (lowercase).
# Used for the 10x keyword-scoring boost described in the project spec.
EMOTION_KEYWORDS = {
    "Bored": [
        "bored", "boring", "tedious", "dull", "monotonous", "uninterested",
        "sleepy", "nothing new", "same old", "pointless", "not engaging",
    ],
    "Confident": [
        "confident", "i understand", "i get it", "makes sense", "easy",
        "i can do this", "sure about", "comfortable with", "i've got this",
        "clear to me", "no problem",
    ],
    "Confused": [
        "confused", "don't understand", "do not understand", "lost",
        "unclear", "not sure", "puzzled", "what does this mean",
        "makes no sense", "stuck", "can't follow", "no idea",
    ],
    "Curious": [
        "curious", "wonder", "interesting", "what if", "how does",
        "why does", "want to know", "tell me more", "fascinated",
        "explore", "intrigued",
    ],
    "Frustrated": [
        "frustrated", "annoyed", "angry", "give up", "so hard", "difficult",
        "hate this", "fed up", "irritated", "sick of", "can't take it",
        "why is this so",
    ],
}

# Class weights applied to BERT logits, in EMOTION_LABELS order.
# (Bored, Confident, Confused, Curious, Frustrated)
BERT_CLASS_WEIGHTS = np.array([1.2, 1.8, 0.6, 1.0, 1.4])

# Confidence / confusion keyword boost multipliers used by the BERT classifier.
CONFIDENT_BOOST = 2.5
CONFUSED_BOOST = 2.0

# Explicit-emotion-word scoring weight used by the keyword enhancement pass.
KEYWORD_SCORE_WEIGHT = 10.0

# Mixed-emotion secondary-score threshold.
MIXED_EMOTION_THRESHOLD = 0.15

# Preserve these characters because they carry emotional signal.
_PRESERVE_PUNCT = "!?.…"
_CLEAN_RE = re.compile(r"[^a-zA-Z0-9\s" + re.escape(_PRESERVE_PUNCT) + r"]")
_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Normalize whitespace/casing while preserving emotion-carrying punctuation."""
    if not text:
        return ""
    text = text.strip()
    text = _CLEAN_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def keyword_scores(text: str) -> dict:
    """
    Return a raw keyword-match score per emotion for the given text.
    Each matched keyword contributes KEYWORD_SCORE_WEIGHT points.
    """
    lowered = text.lower()
    scores = {label: 0.0 for label in EMOTION_LABELS}
    for label, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if kw in lowered:
                scores[label] += KEYWORD_SCORE_WEIGHT
    return scores


def apply_keyword_boost(probs: np.ndarray, text: str) -> np.ndarray:
    """
    Boost a raw model probability vector (ordered per EMOTION_LABELS) using
    keyword evidence from the input text, then renormalize to sum to 1.0.
    """
    probs = np.array(probs, dtype=float)
    lowered = text.lower()
    boosted = probs.copy()

    for i, label in enumerate(EMOTION_LABELS):
        hits = sum(1 for kw in EMOTION_KEYWORDS[label] if kw in lowered)
        if hits:
            boosted[i] += (hits * KEYWORD_SCORE_WEIGHT) / 100.0

    # Extra targeted boosts described in the spec.
    if any(kw in lowered for kw in EMOTION_KEYWORDS["Confident"]):
        boosted[EMOTION_LABELS.index("Confident")] *= CONFIDENT_BOOST
    if any(kw in lowered for kw in EMOTION_KEYWORDS["Confused"]):
        boosted[EMOTION_LABELS.index("Confused")] *= CONFUSED_BOOST

    total = boosted.sum()
    if total <= 0:
        return probs
    return boosted / total


def rule_based_predict(text: str) -> dict:
    """
    Zero-dependency fallback classifier. Used automatically by predict.py
    when neither the BiLSTM nor the BERT model weights are present on disk,
    so the application is always runnable end-to-end.
    """
    cleaned = clean_text(text)
    raw = keyword_scores(cleaned)
    values = np.array(list(raw.values()))

    if values.sum() == 0:
        # Neutral fallback distribution when no keywords match at all.
        probs = np.array([0.15, 0.15, 0.15, 0.40, 0.15])
    else:
        probs = values / values.sum()
        # Smooth a little so no class ever collapses to exactly 0.
        probs = 0.85 * probs + 0.15 * (np.ones(5) / 5)
        probs = probs / probs.sum()

    scores = {label: float(p) for label, p in zip(EMOTION_LABELS, probs)}
    top_idx = int(np.argmax(probs))
    return {
        "emotion": EMOTION_LABELS[top_idx],
        "confidence": float(probs[top_idx]),
        "emotion_scores": scores,
        "cleaned_text": cleaned,
        "model_used": "RuleBasedFallback",
    }
