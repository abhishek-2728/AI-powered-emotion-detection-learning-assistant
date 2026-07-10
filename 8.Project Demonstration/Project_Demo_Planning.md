# Project Demo Planning

## Pre-Demo Checklist
- [ ] `pip install -r requirements.txt` completed in a clean virtual environment
- [ ] `.env` populated with a valid `GOOGLE_API_KEY` (or explicitly plan to
      demo the template-fallback path)
- [ ] Confirm `models/bltsm/` and `models/bert_emotion_model_final/` are
      populated if a "real model" demo is desired, otherwise rehearse the
      fallback-mode narrative
- [ ] Clear `emotion_response_examples.csv` / `emotion_response_mapping.csv`
      to header-only state for a clean analytics dashboard demo
- [ ] Rehearse the 7-step demo script from `Demonstration_of_Proposed_Features.md`
- [ ] Prepare 3-4 example inputs per emotion in advance (avoid live typing delays)

## Timeline

| Time | Activity |
|---|---|
| T-1 day | Full rehearsal with the team, timing each step |
| T-1 hour | Environment sanity check, restart Streamlit fresh |
| Demo | Follow script; keep buffer for Q&A |
| T+1 day | Collect feedback, log follow-up issues |

## Roles During Demo
| Name | Role |
|---|---|
| Villa Veera Venkata Manoj | Primary presenter — walks through UI and pipeline |
| Ravuri Kavya Sri | Narrates model/analytics details, backup presenter |
| Md Usman Patel | Handles Q&A on requirements/scope |
| V.S. Venkata Reddy V | Handles technical questions on BERT training |
| T. Abhishek Shalom | Handles scalability/future-plan questions |

## Contingency Plans
- If Gemini API is unreachable during the live demo, immediately toggle
  "Use Gemini AI responses" off — the template path is designed to be
  indistinguishable in structure (emoji + message + action) for a smooth
  demo.
- If a trained model fails to load, the app already degrades to the
  rule-based fallback automatically — no manual intervention needed.
