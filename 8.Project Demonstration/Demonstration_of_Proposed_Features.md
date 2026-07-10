# Demonstration of Proposed Features

## Demo Script

1. **Launch** — `streamlit run app.py`; show sidebar model-status badges
   (fallback mode is fine for live demos without GPU).
2. **Confused example** — Field: Computer Science, Problem: "I don't
   understand recursion at all, this makes no sense to me." Show detected
   emotion, confidence bars, and the generated guidance.
3. **Frustrated + Confused (mixed) example** — Problem: "I've tried this
   five times and I'm so frustrated, I don't even understand the error
   anymore." Show the mixed-emotion label and how the response acknowledges
   both.
4. **Confident example** — Problem: "I get it now, this makes total sense,
   I'm confident I can solve the rest." Show the Confident template/AI
   response with a "push further" style tip.
5. **Toggle Gemini off** — Demonstrate the template fallback response
   generating instantly with no API dependency.
6. **Analytics Dashboard** — After 4-5 interactions, open the Emotions,
   Fields, and Summary tabs to show the pie chart, confidence timeline, and
   field-wise bar chart populate live.
7. **Clear History** — Show the reset control and explain CSV logs persist
   independently of session state for longer-term analytics.

## Feature-to-Demo Mapping

| Feature | Demonstrated in Step |
|---|---|
| Dual-model comparison | 2 (when trained models are loaded) |
| Mixed-emotion detection | 3 |
| Gemini + template fallback | 3-5 |
| Analytics dashboard | 6 |
| Session management | 7 |

## Anticipated Q&A
- *"What if the models aren't trained yet?"* → Show the rule-based
  fallback still produces sensible, keyword-driven predictions.
- *"What if there's no internet for Gemini?"* → Toggle it off live to show
  the template response path.
- *"How is this different from plain sentiment analysis?"* → Point to the
  5 academically-relevant classes and mixed-emotion detection, which a
  binary positive/negative model cannot express.
