# Team Involvement in Demonstration

## Contribution Summary

| Name | Reg. No. | Primary Epics/Stories Owned | Demo Responsibility |
|---|---|---|---|
| Ravuri Kavya Sri | AP24110011426 | Data preprocessing, BiLSTM classifier, mixed-emotion detection, session/CSV logging, end-to-end validation, deployment readiness | Narrates model & analytics details; backup presenter |
| Villa Veera Venkata Manoj | AP24110011400 | Environment setup, BiLSTM training/fine-tuning, BERT classifier integration, Gemini prompt engineering, response regeneration, UI layout & implementation | Primary presenter — walks through the live app |
| Md Usman Patel | AP24110011687 | Requirement analysis, documentation consolidation, cross-epic testing support | Handles requirement/scope questions during Q&A |
| V.S. Venkata Reddy V | AP24110011256 | BERT model fine-tuning on Kaggle, training evaluation reporting | Handles technical questions on BERT training methodology |
| T. Abhishek Shalom | AP24110011337 | Demo planning, scalability & future-plan authoring, QA support | Handles scalability/future-plan questions |

## Collaboration Highlights
- Model training (Epic 2) and pipeline development (Epic 3) were built in
  parallel by the modeling-focused and pipeline-focused sub-teams, then
  integrated behind the shared `predict.py` unified schema so no rework was
  needed on either side.
- UI work (Epic 5) proceeded against the rule-based fallback classifier
  before trained models were ready, which meant the interface could be
  fully built, tested, and demoed independently of training completion.
- Documentation (this folder set) was maintained incrementally per epic
  rather than written retroactively, keeping it aligned with what was
  actually built.

## Acknowledgement
This project was completed as a team effort. Each member's specific
contribution is also reflected in `04_Project_Planning_Phase/Project_Planning.md`.
