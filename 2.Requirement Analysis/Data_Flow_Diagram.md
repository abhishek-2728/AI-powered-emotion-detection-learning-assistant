# Data Flow Diagram

## Level 0 — Context Diagram

```
                +-------------------+
   Student ---> |  Streamlit UI     | ---> Guidance + Analytics ---> Student
   (field,      |   (app.py)        |
   problem)     +-------------------+
```

## Level 1 — Detailed Flow

```mermaid
flowchart LR
    A[Student Input: field + problem text] --> B[preprocessing.py\nclean_text + keyword_scores]
    B --> C{Trained models\npresent on disk?}
    C -- Yes --> D[model.py: BiLSTM predict]
    C -- Yes --> E[bert_model.py: BERT predict\n+ class weighting + keyword boost]
    C -- No --> F[preprocessing.py\nrule_based_predict fallback]
    D --> G[predict.py: unify schema]
    E --> G
    F --> G
    G --> H[detect_mixed_emotion\n>=15% threshold]
    H --> I{Gemini API key\nconfigured & AI toggle on?}
    I -- Yes --> J[Gemini 2.5 Flash\nempathetic response]
    I -- No / error --> K[Template response\nby emotion]
    J --> L[app.py: Display results]
    K --> L
    L --> M[predict.py: save_interaction_to_csv]
    M --> N[emotion_response_examples.csv]
    M --> O[emotion_response_mapping.csv]
    L --> P[Session state history]
    P --> Q[Analytics Dashboard\nEmotions / Fields / Summary tabs]
```

## Data Stores

| Store | Written by | Read by |
|---|---|---|
| `emotion_response_examples.csv` | `predict.save_interaction_to_csv()` | `predict.load_csv_examples()`, sidebar metrics |
| `emotion_response_mapping.csv` | `predict._upsert_mapping()` | Optional "use CSV examples" mode in `app.py` |
| Streamlit `session_state.history` | `app.py` per interaction | Analytics dashboard (Plotly charts) |
| `Users` / `Emotion_Records` (future DB path) | Optional auth/API layer | Multi-user hosted deployment (see `schema.sql`) |
