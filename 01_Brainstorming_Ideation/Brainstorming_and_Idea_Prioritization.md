# Brainstorming & Idea Prioritization

## Context
Educators and self-learners often can't tell, from text alone, whether a
student is Confident, Curious, Confused, Bored, or Frustrated — yet these
states strongly predict whether a learner disengages or pushes through.

## Ideation Session — Raw Ideas

| # | Idea | Champion |
|---|---|---|
| 1 | Sentiment-only (positive/negative) tagging of forum posts | Ravuri Kavya Sri |
| 2 | Facial-expression webcam emotion detection during study sessions | Villa Veera Venkata Manoj |
| 3 | Text-based, 5-class learning-emotion classifier (Bored/Confident/Confused/Curious/Frustrated) + AI coaching response | Md Usman Patel |
| 4 | Voice-tone based stress detection | V.S. Venkata Reddy V |
| 5 | Manual "how do you feel?" mood-picker widget, no ML | T. Abhishek Shalom |
| 6 | Combine dual models (BiLSTM + BERT) for robustness and comparison | Villa Veera Venkata Manoj |

## Prioritization (Impact vs. Feasibility)

| Idea | Impact | Feasibility | Priority |
|---|---|---|---|
| Idea 3 (text-based 5-class + AI coach) | High | High | **Selected** |
| Idea 6 (dual-model comparison) | High | Medium | **Folded into Idea 3** |
| Idea 2 (webcam) | Medium | Low (privacy, hardware) | Rejected |
| Idea 4 (voice) | Medium | Low (audio pipeline complexity) | Deferred to future work |
| Idea 1 (sentiment only) | Low | High | Rejected — too coarse, doesn't capture "Confused" vs "Frustrated" |
| Idea 5 (manual picker) | Low | High | Rejected — no automatic insight, defeats the purpose |

## Decision

Build a **text-input emotion detection engine** using two complementary
models — a BiLSTM baseline and a fine-tuned BERT model — feeding into a
Gemini-powered (with template fallback) supportive-response generator,
delivered through a Streamlit web app with an analytics dashboard.

## Team

| Name | Reg. No. | Email |
|---|---|---|
| Ravuri Kavya Sri | AP24110011426 | Kavyasri_ravuri@srmap.edu.in |
| Villa Veera Venkata Manoj | AP24110011400 | manoj_villa@srmap.edu.in |
| Md Usman Patel | AP24110011687 | usman_mohammad@srmap.edu.in |
| V.S. Venkata Reddy V | AP24110011256 | Veera_vippala@srmap.edu.in |
| T. Abhishek Shalom | AP24110011337 | abhishek_tullibilli@srmap.edu.in |
