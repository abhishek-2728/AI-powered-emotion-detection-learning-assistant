# Project Executable Files

## How to Run

```bash
cd 09_Programs_and_Codes
pip install -r requirements.txt
cp .env.example .env      # add GOOGLE_API_KEY if you want Gemini responses
streamlit run app.py
```

The app opens at `http://localhost:8501` by default.

## Executable / Entry-Point Inventory

| File | Type | How to Run |
|---|---|---|
| `app.py` | Streamlit web app (main deliverable) | `streamlit run app.py` |
| `src/train.py` | CLI training script | `python src/train.py --model bilstm --data data/emotion_text_dataset.csv` |
| `src/train.py` (BERT) | CLI training script | `python src/train.py --model bert --data data/emotion_text_dataset.csv` |
| `schema.sql` | Database schema (optional path) | `sqlite3 app.db < schema.sql` |

## Required Environment Variables

| Variable | Required | Purpose |
|---|---|---|
| `GOOGLE_API_KEY` | Optional | Enables Gemini-generated responses; app falls back to templates without it |

## Directory Prerequisites at Runtime

| Path | Required for |
|---|---|
| `models/bltsm/` | BiLSTM predictions (else rule-based fallback is used) |
| `models/bert_emotion_model_final/` | BERT predictions (else rule-based fallback is used) |
| `data/emotion_text_dataset.csv` | Only needed to run `train.py` |
| `emotion_response_examples.csv`, `emotion_response_mapping.csv` | Auto-created/appended at runtime if absent |

## Packaging Note
No compiled binaries are included — this is a pure-Python project. Trained
model weight files (`.keras`, `.safetensors`) are intentionally excluded
from version control (see `.gitignore`) due to size; regenerate them with
`train.py` or download them from your team's model storage location.
