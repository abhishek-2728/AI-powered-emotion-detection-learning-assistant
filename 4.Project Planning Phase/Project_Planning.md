# Project Planning

## Epics Overview

| Epic | Complexity | Duration |
|---|---|---|
| 1. Environment Setup & Dependency Configuration | Medium | 1h 30m |
| 2. Kaggle Model Training and Integration | Medium | 4h 30m |
| 3. Core Emotion Detection Pipeline Development | Medium | 4h 45m |
| 4. AI-Powered Guidance & Regeneration Engine | Medium | 3h 0m |
| 5. Streamlit UI Implementation | Medium | 2h 0m |
| 6. User Interaction (Validation & Deployment Readiness) | Easy | 1h 30m |
| **Total** | | **~17h 45m** |

## Story Breakdown & Ownership

### Epic 1 — Environment Setup and Dependency Configuration
| Story | Duration | Owner |
|---|---|---|
| Obtain Gemini API Key | 15m | Villa Veera Venkata Manoj |
| Install Python & Create Virtual Environment | 15m | Villa Veera Venkata Manoj |
| Install Project Dependencies | 15m | Villa Veera Venkata Manoj |
| Create the .env Configuration File | 15m | Ravuri Kavya Sri |
| Verify Model and Data Directories | 15m | Ravuri Kavya Sri |
| Prepare Project Folder Structure | 15m | Ravuri Kavya Sri |

### Epic 2 — Kaggle Model Training and Integration
| Story | Duration | Owner |
|---|---|---|
| Kaggle Setup (GPU + Dependencies + Data Loading) | 45m | Ravuri Kavya Sri |
| Data Preprocessing & Tokenization | 1h 0m | Ravuri Kavya Sri |
| BiLSTM Model Training | 45m | Villa Veera Venkata Manoj |
| Domain-Adaptive Fine-Tuning | 45m | Villa Veera Venkata Manoj |
| BERT Model Fine-Tuning | 45m | V.S. Venkata Reddy V |
| Model Export & Local Integration | 30m | Villa Veera Venkata Manoj |

### Epic 3 — Core Emotion Detection Pipeline Development
| Story | Duration | Owner |
|---|---|---|
| Text Preprocessing & Keyword Enhancement | 1h 0m | Villa Veera Venkata Manoj |
| BiLSTM Classifier (5-Class Softmax) | 45m | Ravuri Kavya Sri |
| BERT Classifier with Class Weighting & Keyword Adjustments | 1h 0m | Villa Veera Venkata Manoj |
| Mixed-Emotion Detection (≥15% Secondary Scores) | 45m | Ravuri Kavya Sri |
| Unified Prediction Schema | 30m | Villa Veera Venkata Manoj |
| CSV Persistence & Cached Model Loading | 45m | Villa Veera Venkata Manoj |

### Epic 4 — AI-Powered Guidance and Regeneration Engine
| Story | Duration | Owner |
|---|---|---|
| Capture Field + Problem, Build Gemini Prompt | 1h 0m | Villa Veera Venkata Manoj |
| Generate Empathetic Responses; Fallback to Templates | 45m | Ravuri Kavya Sri |
| Response Regeneration & Sync Mechanism | 45m | Villa Veera Venkata Manoj |
| Session History & CSV Logs | 30m | Ravuri Kavya Sri |

### Epic 5 — Streamlit UI Implementation
| Story | Duration | Owner |
|---|---|---|
| Responsive Layout & Session State Management | 30m | Villa Veera Venkata Manoj |
| Model Comparison, Mixed Emotions, Confidence Bars | 30m | Villa Veera Venkata Manoj |
| Form Controls, Settings Panel, Error Handling | 30m | Villa Veera Venkata Manoj |
| Analytics Charts (Plotly) with Caching | 30m | Ravuri Kavya Sri |

### Epic 6 — User Interaction
| Story | Duration | Owner |
|---|---|---|
| Validate UI Flow End-to-End | 1h 0m | Ravuri Kavya Sri |
| Optimization and Deployment Readiness | 30m | Ravuri Kavya Sri |

## Roles Not Tied to a Specific Story (Cross-cutting)
- **Md Usman Patel** — Requirement analysis, documentation consolidation, testing support.
- **T. Abhishek Shalom** — Demonstration planning, scalability & future-plan authoring, QA support.

## Milestones

| Milestone | Target |
|---|---|
| M1 — Environment ready | End of Epic 1 |
| M2 — Trained models exported | End of Epic 2 |
| M3 — Working inference pipeline | End of Epic 3 |
| M4 — AI guidance integrated | End of Epic 4 |
| M5 — Full UI + analytics | End of Epic 5 |
| M6 — Validated, deployment-ready | End of Epic 6 |
