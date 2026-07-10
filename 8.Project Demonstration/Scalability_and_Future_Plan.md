# Scalability & Future Plan

## Current Architecture Limits
- Single-session Streamlit app; analytics reset when the session ends
  (CSV logs persist, but there's no per-user login yet).
- CPU inference is fine for single-user demos but would need batching or
  a model-serving layer (e.g. TorchServe, TensorFlow Serving, or a small
  FastAPI wrapper) for concurrent multi-user load.

## Near-Term Scalability Steps
1. **Adopt the relational schema** already designed in `schema.sql`
   (`Users` 1—N `Emotion_Records`) to move from CSV to a real database,
   enabling per-user login, history, and multi-device access.
2. **Separate inference service** — extract `predict.py` behind a small
   FastAPI/Flask service so multiple Streamlit (or other) frontends can
   share cached, GPU-backed model instances.
3. **Batch inference** for classroom-scale use (an educator submitting many
   students' reflections at once).

## Feature Roadmap
| Feature | Value |
|---|---|
| Multilingual emotion detection | Broader accessibility beyond English learners |
| Voice / multimodal input | Captures tone in addition to text |
| LMS integration (Moodle/Canvas) | Emotion signals surface directly where coursework happens |
| Adaptive learning paths | Recommend content difficulty based on detected emotional trend |
| Instructor dashboards | Aggregate, anonymized class-wide emotional analytics |
| Authentication & per-user history | Long-term tracking of a learner's emotional trajectory |

## Model Improvements
- Expand training data specifically for the Bored vs. Frustrated boundary,
  the two classes with the most observed confusion.
- Periodic re-fine-tuning using the growing `emotion_response_examples.csv`
  corpus collected from real usage (continuous learning loop already
  designed in Epic 3/4).

## Non-Functional Scalability Targets (Future)
- Support 100+ concurrent users with sub-2-second inference latency once
  moved to a dedicated model-serving layer.
- 99.5% uptime for the guidance layer via the existing Gemini + template
  fallback pattern, extended with retries/circuit breaking.
