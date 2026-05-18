# File: frontend/pages/3_Generate.py

import streamlit as st
import requests
import json

st.header("🧠 Generate Study Materials")

res = requests.get("http://localhost:8000/upload/list")
files = res.json().get("files", []) if res.status_code == 200 else []

if not files:
    st.warning("Upload a document first.")
    st.stop()

selected_file = st.selectbox("Select document", files)

tab1, tab2, tab3 = st.tabs(["📋 Summary", "❓ Quiz", "🃏 Flashcards"])

# ── Summary Tab ───────────────────────────────────────────────────────────────
with tab1:
    if st.button("Generate Summary", type="primary"):
        with st.spinner("Summarizing..."):
            res = requests.post(
                "http://localhost:8000/generate/summary",
                json={"filename": selected_file}
            )
        if res.status_code == 200:
            st.markdown(res.json()["summary"])
        else:
            st.error(res.text)

# ── Quiz Tab ──────────────────────────────────────────────────────────────────
with tab2:
    num_q = st.slider("Number of questions", 3, 10, 5)

    if st.button("Generate Quiz", type="primary"):
        with st.spinner("Creating quiz..."):
            res = requests.post(
                "http://localhost:8000/generate/quiz",
                json={"filename": selected_file, "num_questions": num_q}
            )

        if res.status_code == 200:
            questions = res.json()["questions"]
            st.session_state.quiz = questions
            st.session_state.quiz_answers = {}

    # Display quiz if it exists
    if "quiz" in st.session_state:
        score = 0
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            answer = st.radio(
                f"q_{i}", q["options"],
                key=f"q_{i}", label_visibility="collapsed"
            )
            st.session_state.quiz_answers[i] = answer

        if st.button("Submit Quiz"):
            for i, q in enumerate(st.session_state.quiz):
                user_ans = st.session_state.quiz_answers.get(i)
                if user_ans == q["answer"]:
                    score += 1
                    st.success(f"Q{i+1}: ✅ Correct!")
                else:
                    st.error(f"Q{i+1}: ❌ Correct: {q['answer']}")
                st.caption(f"*{q.get('explanation', '')}*")

            pct = round(score / len(st.session_state.quiz) * 100)
            st.metric("Your Score", f"{score}/{len(st.session_state.quiz)} ({pct}%)")

            # Save to progress tracker
            requests.post("http://localhost:8000/progress/quiz-result", json={
                "filename": selected_file,
                "score": score,
                "total": len(st.session_state.quiz)
            })

# ── Flashcards Tab ────────────────────────────────────────────────────────────
with tab3:
    num_cards = st.slider("Number of flashcards", 5, 20, 10)

    if st.button("Generate Flashcards", type="primary"):
        with st.spinner("Creating flashcards..."):
            res = requests.post(
                "https://companion-buddy-backend.onrender.com/flashcards",
                json={"filename": selected_file, "num_cards": num_cards}
            )

        if res.status_code == 200:
            cards = res.json()["flashcards"]
            for i, card in enumerate(cards):
                with st.expander(f"Card {i+1}: {card['front']}"):
                    st.info(card["back"])
        else:
            st.error(res.text)