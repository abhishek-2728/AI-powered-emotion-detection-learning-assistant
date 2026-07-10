# Sample Project Documentation

## Project Title
Emotion Detection & Learning Support Engine

## Team
| Name | Reg. No. | Email |
|---|---|---|
| Ravuri Kavya Sri | AP24110011426 | Kavyasri_ravuri@srmap.edu.in |
| Villa Veera Venkata Manoj | AP24110011400 | manoj_villa@srmap.edu.in |
| Md Usman Patel | AP24110011687 | usman_mohammad@srmap.edu.in |
| V.S. Venkata Reddy V | AP24110011256 | Veera_vippala@srmap.edu.in |
| T. Abhishek Shalom | AP24110011337 | abhishek_tullibilli@srmap.edu.in |

## One-line Summary
An AI-powered Streamlit app that detects a learner's emotional state
(Bored, Confident, Confused, Curious, Frustrated) from free text using
BiLSTM and BERT models, and responds with empathetic, field-aware, AI- or
template-generated learning guidance.

## Document Map
| Folder | Contents |
|---|---|
| `01_Brainstorming_Ideation/` | Idea generation, problem statements, empathy map |
| `02_Requirement_Analysis/` | Customer journey, data flow, requirements, tech stack |
| `03_Project_Design_Phase/` | Problem-solution fit, proposed solution, architecture + ER diagram |
| `04_Project_Planning_Phase/` | Epics, stories, durations, team ownership |
| `05_Project_Development_Phase/` | Code layout, coding guide, functional feature checklist |
| `06_Project_Testing/` | Performance & functional test results |
| `07_Project_Documentation/` | This folder — executable files & doc index |
| `08_Project_Demonstration/` | Demo planning, communication plan, scalability & future plan |
| `09_Programs_and_Codes/` | Full working source code, models, data, requirements |

## Architecture at a Glance
```
Student Input -> Preprocessing -> [BiLSTM | BERT | Rule-based fallback]
              -> Unified Schema -> Mixed-Emotion Detection
              -> Gemini (or Template) Response -> UI Display
              -> CSV Persistence + Session State -> Analytics Dashboard
```

## Where to Start Reading
1. `03_Project_Design_Phase/Solution_Architecture.md` — full system design + ER diagram
2. `09_Programs_and_Codes/PROJECT_ANALYSIS_REPORT.md` — model results and pipeline detail
3. `07_Project_Documentation/Project_Executable_Files.md` — how to actually run it
