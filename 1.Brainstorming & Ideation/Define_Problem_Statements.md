# Define Problem Statements

## Problem Statement 1 — Learner Perspective
"I am a student struggling silently with confusion or frustration while
studying alone, and I want a way to express how I feel about a specific
problem and immediately get guidance that matches my emotional state,
so that I don't disengage or give up."

## Problem Statement 2 — Educator Perspective
"I am an educator/tutor who cannot see how students are emotionally
reacting to course material in real time, and I want aggregated,
field-wise emotional analytics, so that I can identify topics or moments
where students consistently get confused, bored, or frustrated."

## Problem Statement 3 — Platform Perspective
"I am building a learning-support tool and I want a reliable, dual-model
emotion classification pipeline (with a safe fallback when models aren't
available) feeding into an AI response generator, so that the system
remains usable, explainable, and robust in production."

## Scope

| In Scope | Out of Scope |
|---|---|
| Text-based emotion detection (5 classes) | Facial/webcam emotion detection |
| BiLSTM + BERT dual-model comparison | Voice/audio emotion detection |
| Gemini-powered + template-fallback responses | Real-time multi-user classroom sync |
| Session + CSV-based analytics dashboard | Full LMS integration (see Future Plan) |
| Single-session Streamlit web app | Native mobile app |

## Success Criteria

- ≥90% classification accuracy on held-out academic-emotion text.
- Mixed-emotion detection surfaces secondary emotions ≥15% confidence.
- App remains functional even without trained model weights present
  (rule-based fallback).
- AI response generation degrades gracefully to templates if the Gemini
  API is unavailable.
