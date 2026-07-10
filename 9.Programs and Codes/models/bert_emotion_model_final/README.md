# models/bert_emotion_model_final/

Place the fine-tuned BERT (`bert-base-uncased`) artifacts exported from the
Kaggle training notebook here (a standard Hugging Face `save_pretrained()`
directory):

| File | Description |
|---|---|
| `config.json` | Model architecture configuration |
| `model.safetensors` (or `pytorch_model.bin`) | Fine-tuned weights |
| `tokenizer.json`, `tokenizer_config.json`, `vocab.txt` | Tokenizer files |
| `special_tokens_map.json` | Tokenizer special-token configuration |
| `label_mapping.json` | `{emotion_label: class_index}` mapping |

If this folder is empty, `predict.py` automatically falls back to the
zero-dependency rule-based classifier in `src/preprocessing.py`, so the
Streamlit app (`app.py`) still runs and demonstrates the full pipeline
without requiring the trained weights.

To generate these files, run:

```bash
python src/train.py --model bert --data data/emotion_text_dataset.csv
```
