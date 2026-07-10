# Problem-Solution Fit

## Problem
Learners can't easily signal *how* they feel about a specific academic
struggle, so the help they receive (from peers, generic chatbots, or static
material) rarely matches their emotional state — leaving Confused students
without structure, Frustrated students without a breather, and Bored
students without re-engagement.

## Solution
A text-input pipeline that classifies the learner's emotional state across
5 academically-relevant categories (not generic sentiment), detects mixed
emotions, and routes the result into an emotion-aware response generator
(Gemini, with template fallback) — wrapped in a dashboard that also gives
longitudinal insight.

## Fit Validation

| Problem Signal (from Empathy Map) | Solution Feature |
|---|---|
| "I don't know how to express what I don't understand" | Free-text problem input + field context (FR-2) |
| "Generic advice doesn't match how I actually feel" | 5-class + mixed-emotion detection (FR-3, FR-4) |
| "I don't want to feel judged for asking again" | Non-judgmental templates/AI tone (Epic 4) |
| "I want to see if I'm improving over time" | Analytics dashboard, confidence timeline (FR-10) |
| "Sometimes there's no internet/API access" | Rule-based + template fallback (NFR-1, FR-7) |

## Early Validation Approach
- Manually tested phrasing patterns across all 5 classes to confirm keyword
  lexicon coverage (see `src/preprocessing.py::EMOTION_KEYWORDS`).
- Verified mixed-emotion detection surfaces realistic combinations (e.g.
  "Confused + Frustrated") rather than always defaulting to one label.
- Confirmed the pipeline still functions with zero trained model weights
  present, validating the "always demonstrable" design goal.
