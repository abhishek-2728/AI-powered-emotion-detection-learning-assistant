# models/bltsm/

Place the trained BiLSTM artifacts exported from the Kaggle training notebook here:

| File | Description |
|---|---|
| `bilstm_student_adaptive.keras` | Domain-adapted BiLSTM model weights |
| `tokenizer.json` | Keras `Tokenizer` fitted on the training vocabulary (30,000 words) |
| `label_classes.json` | Ordered emotion label list matching the model's output layer |

If this folder is empty, `predict.py` automatically falls back to the
zero-dependency rule-based classifier in `src/preprocessing.py`, so the
Streamlit app (`app.py`) still runs and demonstrates the full pipeline
without requiring the trained weights.

To generate these files, run:

```bash
python src/train.py --model bilstm --data data/emotion_text_dataset.csv
```
