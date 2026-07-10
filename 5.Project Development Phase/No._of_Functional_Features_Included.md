# Number of Functional Features Included

| # | Feature | Status |
|---|---|---|
| 1 | Field selection (11 academic subjects) | ✅ Implemented |
| 2 | Contextual placeholder text per field | ✅ Implemented |
| 3 | Free-text problem/feeling input | ✅ Implemented |
| 4 | Text cleaning preserving emotion punctuation | ✅ Implemented |
| 5 | Keyword lexicon scoring (10x weight per hit) | ✅ Implemented |
| 6 | BiLSTM 5-class softmax classifier | ✅ Implemented (trainable via `train.py`) |
| 7 | BERT classifier with class weighting | ✅ Implemented (trainable via `train.py`) |
| 8 | Keyword-based Confident/Confused boosting | ✅ Implemented |
| 9 | Rule-based zero-dependency fallback classifier | ✅ Implemented |
| 10 | Unified prediction schema across models | ✅ Implemented |
| 11 | Mixed-emotion detection (≥15% threshold) | ✅ Implemented |
| 12 | Side-by-side BiLSTM vs BERT comparison view | ✅ Implemented |
| 13 | Confidence progress bars per emotion | ✅ Implemented |
| 14 | Gemini 2.5 Flash empathetic response generation | ✅ Implemented |
| 15 | Template-response fallback (5 emotions, emoji + tip) | ✅ Implemented |
| 16 | AI response toggle (Gemini on/off) | ✅ Implemented |
| 17 | Session history tracking | ✅ Implemented |
| 18 | CSV persistence (examples + emotion-response mapping) | ✅ Implemented |
| 19 | "Use CSV examples" reuse option | ✅ Implemented |
| 20 | Clear-history control | ✅ Implemented |
| 21 | Sidebar model-status indicators | ✅ Implemented |
| 22 | Sidebar session statistics | ✅ Implemented |
| 23 | Analytics — Emotion distribution pie chart | ✅ Implemented |
| 24 | Analytics — Confidence timeline chart | ✅ Implemented |
| 25 | Analytics — Field-wise emotion bar chart | ✅ Implemented |
| 26 | Analytics — Summary tab with key metrics table | ✅ Implemented |
| 27 | Cached model loading (`st.cache_resource`) | ✅ Implemented |
| 28 | Optional relational DB schema for multi-user deployment | ✅ Provided (`schema.sql`) |

**Total functional features: 28**
