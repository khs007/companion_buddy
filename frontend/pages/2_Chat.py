# File: frontend/pages/2_Chat.py

import streamlit as st
import requests

st.header("💬 Chat with Your Notes")

# Document selector
res = requests.get("https://companion-buddy-backend.onrender.com/upload/list")
files = res.json().get("files", []) if res.status_code == 200 else []

if not files:
    st.warning("No documents uploaded yet. Go to the Upload page first.")
    st.stop()

selected_file = st.selectbox("Which document to query?", files)

# Chat history stored in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("📎 Sources"):
                for s in msg["sources"]:
                    st.caption(s)

# Input
question = st.chat_input("Ask anything about your notes...")

if question:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # Get AI answer
    with st.chat_message("assistant"):
        with st.spinner("Searching your notes..."):
            res = requests.post(
                "https://companion-buddy-backend.onrender.com/chat/ask",
                json={"question": question, "filename": selected_file}
            )

        if res.status_code == 200:
            data = res.json()
            st.write(data["answer"])
            if data.get("sources"):
                with st.expander("📎 Sources"):
                    for s in data["sources"]:
                        st.caption(s)
            st.session_state.messages.append({
                "role": "assistant",
                "content": data["answer"],
                "sources": data.get("sources", [])
            })
        else:
            st.error("Failed to get answer. Is the backend running?")