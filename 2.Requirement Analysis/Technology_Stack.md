# Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.9+ | Core implementation language |
| Web UI | Streamlit | Interactive learning-assistant interface |
| Deep Learning (baseline) | TensorFlow / Keras | BiLSTM emotion classifier |
| Deep Learning (transformer) | PyTorch + Hugging Face Transformers | Fine-tuned BERT (`bert-base-uncased`) classifier |
| NLP utilities | NLTK, regex | Text cleaning, keyword lexicon matching |
| Data handling | pandas, NumPy | Dataset loading, CSV persistence, score aggregation |
| Visualization | Plotly Express | Emotion distribution, confidence timeline, field breakdown charts |
| Generative AI | Google Gemini 2.5 Flash (`google-generativeai`) | Empathetic, field-aware response generation |
| Config management | `python-dotenv` | Loading `GOOGLE_API_KEY` and settings from `.env` |
| Persistence (current) | CSV (`emotion_response_examples.csv`, `emotion_response_mapping.csv`) | Continuous learning / analytics data store |
| Persistence (future path) | SQLite/PostgreSQL (`schema.sql`: `Users`, `Emotion_Records`) | Multi-user hosted deployment |
| Training environment | Kaggle (dual-GPU) | Model training for BiLSTM and BERT |
| IDEs | VS Code, PyCharm Community | Development and debugging |
| Version control | Git + GitHub | Source control, collaboration |

## Why this stack

- **Streamlit** was chosen over a custom frontend for fast iteration and
  built-in widgets (progress bars, tabs, caching) that map directly onto
  the app's requirements (FR-5, FR-9, FR-10).
- **Dual-model design (BiLSTM + BERT)** trades off compute cost vs.
  contextual understanding — BiLSTM is lightweight and fast; BERT is more
  accurate on nuanced phrasing. Running both provides a comparison view.
- **Gemini + template fallback** ensures the guidance layer is never a
  single point of failure (NFR-1 style resilience extended to the AI layer).
