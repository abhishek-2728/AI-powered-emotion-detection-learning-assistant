# Solution Architecture

## High-Level Component Architecture

```mermaid
flowchart TB
    subgraph Client
        UI[Streamlit UI - app.py]
    end
    subgraph Core Pipeline (src/)
        PP[preprocessing.py]
        BL[model.py - BiLSTM]
        BE[bert_model.py - BERT]
        PR[predict.py - orchestration]
    end
    subgraph External Services
        GEM[Gemini 2.5 Flash API]
    end
    subgraph Storage
        CSV1[emotion_response_examples.csv]
        CSV2[emotion_response_mapping.csv]
        DB[(Optional: Users / Emotion_Records - schema.sql)]
    end

    UI --> PR
    PR --> PP
    PR --> BL
    PR --> BE
    UI --> GEM
    PR --> CSV1
    PR --> CSV2
    PR -.future.-> DB
```

## Entity Relationship Diagram (Database — Future/Optional Path)

The current reference app persists to CSV for simplicity (Epic 3, Story 6).
For a hosted, multi-user deployment, the following relational schema
(implemented in `09_Programs_and_Codes/schema.sql`) is the designed path:

```
Users (1) ----< Emotion_Records (N)

Users:
  UserID (PK), Name, Email, Password, Role, Login_Count, Created_At

Emotion_Records:
  RecordID (PK), UserID (FK), Email, Field, Input_Text,
  Predicted_Emotion, Secondary_Emotion, Confidence_Score,
  Model_Used, AI_Response, Response_Type, Emotion_Scores,
  Timestamp, CSV_Logged
```

One user can generate many emotion records over time (1:N), enabling
per-user history and cross-user aggregate analytics.

## Module Responsibilities

| Module | Responsibility |
|---|---|
| `src/preprocessing.py` | Text cleaning, keyword lexicon, rule-based fallback classifier |
| `src/model.py` | BiLSTM architecture, focal loss, load/predict |
| `src/bert_model.py` | BERT load, class weighting, keyword adjustments, predict |
| `src/predict.py` | Model orchestration, mixed-emotion detection, CSV persistence |
| `src/train.py` | Offline training entry point for both models |
| `app.py` | Streamlit UI, Gemini integration, analytics dashboard |
| `schema.sql` | Optional relational schema for hosted multi-user deployment |

## Deployment View

Single-process Streamlit app; models cached in-process via
`st.cache_resource`. Stateless across restarts except for CSV files on
disk, making it trivially deployable to Streamlit Community Cloud, a VM,
or a container with a mounted volume for `data/`, `models/`, and the CSV
logs.
