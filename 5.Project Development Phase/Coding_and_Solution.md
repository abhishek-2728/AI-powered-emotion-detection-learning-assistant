# Coding & Solution

## Setup

```bash
git clone <your-repo-url>
cd 09_Programs_and_Codes
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then add your GOOGLE_API_KEY
```

## Running the App (works immediately, no trained models required)

```bash
streamlit run app.py
```

On first launch, if `models/bltsm/` and `models/bert_emotion_model_final/`
are empty, the app automatically uses the rule-based fallback classifier so
you can exercise the full flow (input → emotion detection → guidance →
analytics) immediately.

## Training the Real Models (optional, for full accuracy)

```bash
cd src
python train.py --model bilstm --data ../data/emotion_text_dataset.csv
python train.py --model bert   --data ../data/emotion_text_dataset.csv
```

This exports `models/bltsm/bilstm_student_adaptive.keras` +
`tokenizer.json`, and the full Hugging Face directory under
`models/bert_emotion_model_final/`. Restart the app afterward — both model
badges in the sidebar will flip from "🟡 fallback" to "✅ loaded".

## Key Solution Snippets

**Mixed-emotion detection** (`src/predict.py`):
```python
def detect_mixed_emotion(emotion_scores, threshold=MIXED_EMOTION_THRESHOLD):
    above = [(l, s) for l, s in emotion_scores.items() if s >= threshold]
    above.sort(key=lambda x: x[1], reverse=True)
    if len(above) <= 1:
        return max(emotion_scores, key=emotion_scores.get)
    return " + ".join(l for l, _ in above)
```

**Gemini prompt construction** (`app.py`):
```python
def build_gemini_prompt(field, problem, emotion, confidence):
    return (f"You are a supportive learning coach. A student studying {field} "
            f"is working on: \"{problem}\". Their detected emotional state is "
            f"'{emotion}' with {confidence*100:.0f}% confidence. ...")
```

## Solution Verification (done during development)
- `python3 -m py_compile` on every module — all pass.
- Ran `rule_based_predict()` on representative Confused/Frustrated and
  Confident phrasing — correctly identified primary emotion and a sensible
  mixed-emotion label ("Frustrated + Confused").
- Ran a full `predict_emotion()` → `save_interaction_to_csv()` →
  `load_csv_examples()` round trip — CSV rows persisted and read back
  correctly with headers intact.
