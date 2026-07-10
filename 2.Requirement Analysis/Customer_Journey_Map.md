# Customer Journey Map

| Stage | Action | Thoughts/Feelings | Touchpoint | Opportunity |
|---|---|---|---|---|
| 1. Arrival | Opens the Streamlit app | "Let's see if this actually helps" | Landing page, title + caption | Clear, low-friction first impression |
| 2. Input | Selects field, describes problem | Slightly vulnerable, hopeful | Field dropdown + problem text area | Contextual placeholder text per field |
| 3. Analysis | Clicks "Get AI Learning Help" | Anticipation | Spinner: "Analyzing emotional state..." | Fast (<3s) response, transparent about what's happening |
| 4. Recognition | Sees detected emotion(s) + confidence | "Yes, that's exactly how I feel" (validation) | Emotion badge + emoji + progress bars | Mixed-emotion detection avoids oversimplifying |
| 5. Guidance | Reads AI/template response | Reassured, given a concrete next step | Gemini or template response card | Field-specific, emotion-aware tone |
| 6. Reflection | Checks sidebar / analytics tabs | Curious about patterns over time | Sidebar dashboard, Emotions/Fields/Summary tabs | Session history builds self-awareness |
| 7. Return | Comes back for another problem | Comfortable, trusts the tool | Persistent session + CSV logging | Continuity across interactions |

## Key Moment of Truth
Step 4 (Recognition) — if the detected emotion feels wrong or generic, trust
in the entire system collapses. This is why keyword-boosted scoring and
mixed-emotion detection (≥15% threshold) were prioritized over a single
best-guess label.
