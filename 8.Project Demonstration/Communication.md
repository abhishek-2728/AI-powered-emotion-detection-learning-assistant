# Communication

## Team Communication Channels
| Channel | Purpose |
|---|---|
| Team WhatsApp/Discord group | Daily coordination, quick blockers |
| Shared Kanban board (Overview/Workspace/Kanban) | Epic/story tracking, ownership, status |
| Weekly sync call | Progress review, integration checkpoints between model team and UI team |
| GitHub repository | Code reviews, issue tracking, version history |

## Roles in Communication
| Name | Communication Responsibility |
|---|---|
| Ravuri Kavya Sri | Data/testing updates, documentation consolidation |
| Villa Veera Venkata Manoj | Model + backend integration updates, sprint coordination |
| Md Usman Patel | Requirement clarifications, stakeholder-facing summaries |
| V.S. Venkata Reddy V | BERT training status reports |
| T. Abhishek Shalom | Demo scheduling, cross-team scalability discussions |

## Stakeholder Update Cadence
- **End of each Epic**: a short written status update (what's done, what's
  blocked, what's next) shared with the full team.
- **Pre-demo**: a walkthrough rehearsal at least one day before any
  external demonstration.

## Communication Principles Followed
- Every model change (BiLSTM/BERT) is communicated with its accuracy
  numbers so the UI team knows what the app should display.
- Any fallback behavior change (e.g. rule-based classifier logic) is
  flagged, since it directly affects what "no models present" demos show.
