"""
train.py
--------
Training entry point for both models described in the project report.
Designed to run on Kaggle (dual-GPU) or any machine with TensorFlow /
PyTorch + Transformers installed. Expects a unified dataset CSV with
columns: text, emotion  (emotion in EMOTION_LABELS).

Usage:
    python train.py --model bilstm --data ../data/emotion_text_dataset.csv
    python train.py --model bert   --data ../data/emotion_text_dataset.csv

Outputs:
    ../models/bltsm/bilstm_student_adaptive.keras + tokenizer.json + label_classes.json
    ../models/bert_emotion_model_final/  (full HF save_pretrained() directory)
"""

import argparse
import json
import os

import numpy as np
import pandas as pd

from preprocessing import EMOTION_LABELS, clean_text

DATA_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "data", "emotion_text_dataset.csv")
BILSTM_OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "models", "bltsm")
BERT_OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "models", "bert_emotion_model_final")


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna(subset=["text", "emotion"])
    df["text"] = df["text"].astype(str).apply(clean_text)
    df = df[df["emotion"].isin(EMOTION_LABELS)]
    return df.reset_index(drop=True)


def train_bilstm(df: pd.DataFrame, epochs: int = 12, batch_size: int = 64,
                  max_len: int = 80, vocab_size: int = 30000):
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.utils import to_categorical
    from tensorflow.keras.callbacks import EarlyStopping
    from sklearn.model_selection import train_test_split

    from model import build_bilstm_model, focal_loss

    tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(df["text"])
    sequences = tokenizer.texts_to_sequences(df["text"])
    X = pad_sequences(sequences, maxlen=max_len, padding="post", truncating="post")

    label_to_idx = {label: i for i, label in enumerate(EMOTION_LABELS)}
    y = to_categorical(df["emotion"].map(label_to_idx), num_classes=len(EMOTION_LABELS))

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=df["emotion"]
    )

    model = build_bilstm_model(vocab_size=vocab_size, max_len=max_len)
    model.compile(optimizer="adam", loss=focal_loss(gamma=2.0), metrics=["accuracy"])

    early_stop = EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True)
    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs, batch_size=batch_size,
        callbacks=[early_stop], verbose=2,
    )

    os.makedirs(BILSTM_OUT_DIR, exist_ok=True)
    model.save(os.path.join(BILSTM_OUT_DIR, "bilstm_student_adaptive.keras"))
    with open(os.path.join(BILSTM_OUT_DIR, "tokenizer.json"), "w", encoding="utf-8") as f:
        f.write(tokenizer.to_json())
    with open(os.path.join(BILSTM_OUT_DIR, "label_classes.json"), "w", encoding="utf-8") as f:
        json.dump(EMOTION_LABELS, f)

    print(f"BiLSTM model + tokenizer saved to {BILSTM_OUT_DIR}")


def train_bert(df: pd.DataFrame, epochs: int = 3, batch_size: int = 16,
               learning_rate: float = 2e-5, base_model: str = "bert-base-uncased"):
    import torch
    from torch.utils.data import Dataset
    from sklearn.model_selection import train_test_split
    from transformers import (
        AutoTokenizer, AutoModelForSequenceClassification,
        Trainer, TrainingArguments,
    )

    label_to_idx = {label: i for i, label in enumerate(EMOTION_LABELS)}
    df["label"] = df["emotion"].map(label_to_idx)

    train_df, val_df = train_test_split(
        df, test_size=0.15, random_state=42, stratify=df["emotion"]
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model)

    class EmotionDataset(Dataset):
        def __init__(self, frame):
            self.encodings = tokenizer(
                list(frame["text"]), truncation=True, padding=True, max_length=128
            )
            self.labels = list(frame["label"])

        def __len__(self):
            return len(self.labels)

        def __getitem__(self, idx):
            item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item

    model = AutoModelForSequenceClassification.from_pretrained(
        base_model, num_labels=len(EMOTION_LABELS)
    )

    args = TrainingArguments(
        output_dir=os.path.join(BERT_OUT_DIR, "checkpoints"),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_steps=50,
    )

    trainer = Trainer(
        model=model, args=args,
        train_dataset=EmotionDataset(train_df),
        eval_dataset=EmotionDataset(val_df),
    )
    trainer.train()

    os.makedirs(BERT_OUT_DIR, exist_ok=True)
    model.save_pretrained(BERT_OUT_DIR)
    tokenizer.save_pretrained(BERT_OUT_DIR)
    with open(os.path.join(BERT_OUT_DIR, "label_mapping.json"), "w", encoding="utf-8") as f:
        json.dump(label_to_idx, f)

    print(f"BERT model + tokenizer saved to {BERT_OUT_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Train BiLSTM or BERT emotion classifier.")
    parser.add_argument("--model", choices=["bilstm", "bert"], required=True)
    parser.add_argument("--data", default=DATA_DEFAULT)
    parser.add_argument("--epochs", type=int, default=None)
    args = parser.parse_args()

    df = load_dataset(args.data)
    print(f"Loaded {len(df)} labeled rows from {args.data}")

    if args.model == "bilstm":
        train_bilstm(df, epochs=args.epochs or 12)
    else:
        train_bert(df, epochs=args.epochs or 3)


if __name__ == "__main__":
    main()
