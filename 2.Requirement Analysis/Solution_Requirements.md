# Solution Requirements

## Functional Requirements

| ID | Requirement |
|---|---|
| FR-1 | User can select an academic field from 11 predefined options |
| FR-2 | User can enter free-text describing their learning problem |
| FR-3 | System predicts one of 5 emotions: Bored, Confident, Confused, Curious, Frustrated |
| FR-4 | System detects and displays mixed emotions when secondary scores ≥ 15% |
| FR-5 | System shows BiLSTM and BERT predictions side-by-side when both models are available |
| FR-6 | System generates an empathetic, field-aware AI response via Gemini |
| FR-7 | System falls back to a predefined template response if Gemini is unavailable/disabled |
| FR-8 | System logs every interaction to CSV (examples + emotion-response mapping) |
| FR-9 | System maintains session history and displays recent interactions in a sidebar |
| FR-10 | System provides an analytics dashboard with Emotions/Fields/Summary tabs |
| FR-11 | User can toggle AI responses, CSV saving, detail visibility, and CSV-example reuse |
| FR-12 | User can clear session history on demand |

## Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-1 | Application must run even if trained model weights are absent (rule-based fallback) |
| NFR-2 | Model loading must be cached so repeated predictions don't reload weights |
| NFR-3 | End-to-end response time under typical load should stay under ~3 seconds |
| NFR-4 | API keys must be read from environment variables, never hardcoded |
| NFR-5 | UI must work consistently across major browsers (Chrome, Edge, Firefox) |
| NFR-6 | Codebase must be modular (preprocessing / model / bert_model / predict / app layers) |
| NFR-7 | All CSV writes must handle missing files gracefully (create-if-absent) |

## Assumptions & Constraints

- Model training happens offline on Kaggle (GPU); the local app only performs inference.
- A valid `GOOGLE_API_KEY` is optional — the app is fully demonstrable without one.
- Single-session, single-machine deployment for the current version; multi-user
  persistence is a documented future extension (`schema.sql`).
