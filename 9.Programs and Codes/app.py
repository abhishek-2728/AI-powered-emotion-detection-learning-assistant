"""
app.py
------
Emotion Detection & Learning Support Engine - Streamlit application.

Run with:
    streamlit run app.py

Features implemented (matching the project's Epics 3-5):
  - Field + problem input, 11 academic subjects, contextual placeholders
  - BiLSTM + BERT side-by-side prediction (or rule-based fallback demo mode)
  - Mixed-emotion detection & display ("Curious + Confused")
  - Gemini-powered empathetic responses with graceful template fallback
  - Session history + CSV persistence for continuous learning
  - Analytics dashboard: Emotions / Fields / Summary tabs with Plotly charts
"""

import os
import sys
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from preprocessing import EMOTION_LABELS  # noqa: E402
from predict import predict_emotion, save_interaction_to_csv, load_csv_examples  # noqa: E402

load_dotenv()

# --------------------------------------------------------------------------
# Static configuration
# --------------------------------------------------------------------------

FIELDS = [
    "Computer Science", "Mathematics", "Physics", "Chemistry", "Biology",
    "Electronics & Electrical Engineering", "Mechanical Engineering",
    "Business & Economics", "English & Literature", "History & Social Science",
    "Other",
]

FIELD_PLACEHOLDERS = {
    "Computer Science": "e.g. I don't understand how recursion actually works in this problem...",
    "Mathematics": "e.g. I keep getting the integration by parts formula backwards...",
    "Physics": "e.g. I can't visualize why torque depends on the angle like this...",
    "Chemistry": "e.g. Balancing this redox reaction is confusing me...",
    "Biology": "e.g. I'm mixing up mitosis and meiosis stages...",
    "Electronics & Electrical Engineering": "e.g. I don't get why we use Thevenin's theorem here...",
    "Mechanical Engineering": "e.g. This free-body diagram doesn't make sense to me...",
    "Business & Economics": "e.g. Why does the demand curve shift instead of move along itself...",
    "English & Literature": "e.g. I can't identify the theme in this passage...",
    "History & Social Science": "e.g. I'm having trouble connecting these two historical events...",
    "Other": "Describe what you're working on and where you're stuck...",
}

EMOTION_EMOJIS = {
    "Bored": "😐", "Confident": "💪", "Confused": "😕",
    "Curious": "🤔", "Frustrated": "😤",
}

TEMPLATE_RESPONSES = {
    "Bored": {
        "emoji": "😐",
        "response": "It sounds like this topic hasn't grabbed you yet — that's completely normal. "
                    "Sometimes a change in format (a short video, a real-world example, or teaching "
                    "it to someone else) can reignite interest.",
        "action": "Try connecting this topic to a real project or example you actually care about.",
    },
    "Confident": {
        "emoji": "💪",
        "response": "Great, you've clearly got a solid handle on this. That confidence is worth "
                    "building on — a good next step is testing it against a harder variation of the problem.",
        "action": "Challenge yourself with a slightly harder problem or explain the concept out loud.",
    },
    "Confused": {
        "emoji": "😕",
        "response": "Confusion here is a totally normal part of learning something new — it usually "
                    "means you're right at the edge of a concept, not far from it. Let's break it into "
                    "smaller pieces.",
        "action": "Re-read the concept in smaller chunks and try one worked example step-by-step.",
    },
    "Curious": {
        "emoji": "🤔",
        "response": "Love that curiosity — that's exactly the mindset that makes tricky topics stick. "
                    "Following that 'what if' thread is often the fastest way to deep understanding.",
        "action": "Follow up your question with one more 'why' or 'what if' before moving on.",
    },
    "Frustrated": {
        "emoji": "😤",
        "response": "That frustration is valid — this is genuinely hard. Take a short breather if you "
                    "need it; struggling with a concept is often the step right before it clicks.",
        "action": "Take a 5-minute break, then retry with just the first small step of the problem.",
    },
}

# --------------------------------------------------------------------------
# Gemini integration
# --------------------------------------------------------------------------

def build_gemini_prompt(field: str, problem: str, emotion: str, confidence: float) -> str:
    return (
        f"You are a supportive learning coach. A student studying {field} is working on: "
        f"\"{problem}\". Their detected emotional state is '{emotion}' with "
        f"{confidence * 100:.0f}% confidence. Write a short, warm, encouraging response that: "
        f"1) acknowledges how they feel, 2) gives one concrete, field-specific tip for their problem, "
        f"3) ends with an encouraging next step. Keep it under 120 words."
    )


def generate_ai_response(field: str, problem: str, emotion: str, confidence: float) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = build_gemini_prompt(field, problem, emotion, confidence)
        result = model.generate_content(prompt)
        return result.text.strip()
    except Exception as exc:
        st.warning(f"Gemini API unavailable, using template response instead. ({exc})")
        return None


def get_response(field: str, problem: str, emotion: str, confidence: float, use_ai: bool) -> tuple:
    """Returns (response_text, emoji)."""
    if use_ai:
        ai_text = generate_ai_response(field, problem, emotion, confidence)
        if ai_text:
            return ai_text, EMOTION_EMOJIS.get(emotion, "🙂")

    template = TEMPLATE_RESPONSES.get(emotion, TEMPLATE_RESPONSES["Curious"])
    text = f"{template['response']}\n\n**Suggested next step:** {template['action']}"
    return text, template["emoji"]


# --------------------------------------------------------------------------
# Streamlit page setup + session state
# --------------------------------------------------------------------------

st.set_page_config(
    page_title="Emotion Detection & Learning Support Engine",
    page_icon="🧠",
    layout="wide",
)

if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------

with st.sidebar:
    st.header("📊 Session Dashboard")

    bilstm_ready = os.path.exists(os.path.join("models", "bltsm", "tokenizer.json"))
    bert_ready = os.path.exists(os.path.join("models", "bert_emotion_model_final", "config.json"))

    st.caption("Model status")
    st.write(f"BiLSTM: {'✅ loaded' if bilstm_ready else '🟡 fallback (rule-based)'}")
    st.write(f"BERT: {'✅ loaded' if bert_ready else '🟡 fallback (rule-based)'}")

    st.divider()
    st.metric("Interactions this session", len(st.session_state.history))
    examples = load_csv_examples()
    st.metric("Total CSV examples", len(examples))

    if st.session_state.history:
        st.caption("Recent interactions")
        for item in st.session_state.history[-3:][::-1]:
            st.write(f"**{item['field']}** — {item['mixed_emotion']} "
                     f"({item['confidence'] * 100:.0f}%)")

    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    st.divider()
    st.header("⚙️ Settings")
    use_ai = st.checkbox("Use Gemini AI responses", value=True)
    save_to_csv = st.checkbox("Save interactions to CSV", value=True)
    show_details = st.checkbox("Show analysis details", value=True)
    use_csv_predictions = st.checkbox("Use CSV example responses when available", value=False)

    if use_csv_predictions and examples:
        st.info(f"{len(examples)} stored examples available for reuse.")

# --------------------------------------------------------------------------
# Main layout
# --------------------------------------------------------------------------

st.title("🧠 Emotion Detection & Learning Support Engine")
st.caption("Detect learning-related emotions from text and receive AI-powered, field-aware guidance.")

col_input, col_result = st.columns([1, 1.4])

with col_input:
    st.subheader("Tell us what you're working on")
    field = st.selectbox("Academic field", FIELDS)
    problem = st.text_area(
        "Describe your problem or how you're feeling about it",
        placeholder=FIELD_PLACEHOLDERS[field],
        height=160,
    )
    run = st.button("🎯 Get AI Learning Help", type="primary", use_container_width=True)

with col_result:
    st.subheader("Emotion Analysis & Guidance")

    if run:
        if not problem.strip():
            st.warning("Please describe your problem first.")
        else:
            with st.spinner("Analyzing emotional state..."):
                result = predict_emotion(problem)

            primary = result["primary"]
            mixed_emotion = result["mixed_emotion"]

            with st.spinner("Generating personalized guidance..."):
                response_text, emoji = get_response(
                    field, problem, primary["emotion"], primary["confidence"], use_ai
                )

            st.markdown(f"### {emoji} Detected: **{mixed_emotion}**  "
                        f"({primary['confidence'] * 100:.1f}% confidence)")

            if result["bilstm"] and result["bert"]:
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**BiLSTM prediction**")
                    st.write(f"{result['bilstm']['emotion']} — "
                             f"{result['bilstm']['confidence'] * 100:.1f}%")
                with c2:
                    st.markdown("**BERT prediction**")
                    st.write(f"{result['bert']['emotion']} — "
                             f"{result['bert']['confidence'] * 100:.1f}%")

            if show_details:
                st.markdown("**Emotion score breakdown**")
                sorted_scores = sorted(
                    primary["emotion_scores"].items(), key=lambda x: x[1], reverse=True
                )
                for label, score in sorted_scores:
                    st.progress(score, text=f"{EMOTION_EMOJIS.get(label, '')} {label}: {score * 100:.1f}%")

            st.markdown("### 💬 Learning Guidance")
            st.info(response_text)

            entry = {
                "timestamp": datetime.now().isoformat(),
                "field": field,
                "problem": problem,
                "emotion": primary["emotion"],
                "mixed_emotion": mixed_emotion,
                "confidence": primary["confidence"],
                "emotion_scores": primary["emotion_scores"],
                "response": response_text,
                "model_type": "BERT" if result["bert"] else "BiLSTM/Fallback",
            }
            st.session_state.history.append(entry)

            if save_to_csv:
                save_interaction_to_csv(
                    text=problem, emotion=primary["emotion"],
                    confidence=primary["confidence"], response=response_text,
                    field=field, model_type=entry["model_type"],
                )
    else:
        st.markdown("_Fill in the form and click **Get AI Learning Help** to see your results here._")

# --------------------------------------------------------------------------
# Analytics dashboard
# --------------------------------------------------------------------------

st.divider()
st.header("📈 Analytics Dashboard")

if not st.session_state.history:
    st.caption("Your analytics will appear here once you've had at least one interaction this session.")
else:
    df = pd.DataFrame(st.session_state.history)

    tab_emotions, tab_fields, tab_summary = st.tabs(["Emotions", "Fields", "Summary"])

    with tab_emotions:
        c1, c2 = st.columns(2)
        with c1:
            emotion_counts = df["emotion"].value_counts().reset_index()
            emotion_counts.columns = ["emotion", "count"]
            fig_pie = px.pie(emotion_counts, names="emotion", values="count",
                              title="Emotion Distribution", hole=0.35)
            st.plotly_chart(fig_pie, use_container_width=True)
        with c2:
            fig_line = px.line(
                df, x="timestamp", y="confidence", color="emotion", markers=True,
                title="Emotional Journey (Confidence Over Time)",
            )
            st.plotly_chart(fig_line, use_container_width=True)

    with tab_fields:
        field_counts = df.groupby(["field", "emotion"]).size().reset_index(name="count")
        fig_bar = px.bar(
            field_counts, x="field", y="count", color="emotion", barmode="group",
            title="Emotion Distribution by Field",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab_summary:
        st.metric("Total interactions", len(df))
        st.metric("Most common emotion", df["emotion"].mode()[0])
        st.metric("Average confidence", f"{df['confidence'].mean() * 100:.1f}%")
        st.dataframe(
            df[["timestamp", "field", "emotion", "confidence"]].sort_values(
                "timestamp", ascending=False
            ),
            use_container_width=True,
        )
