# File: frontend/pages/4_Progress.py

import streamlit as st
import requests

st.header("📊 Study Progress")

res = requests.get("http://localhost:8000/progress/summary")

if res.status_code != 200:
    st.error("Couldn't load progress data.")
    st.stop()

data = res.json()

if not data:
    st.info("No progress yet. Take a quiz first!")
    st.stop()

for filename, stats in data.items():
    st.subheader(f"📄 {filename}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sessions", stats["sessions"])
    col2.metric("Avg Score", f"{stats['avg_score']}%")
    col3.metric("Best Score", f"{stats['best_score']}%")
    col4.metric("Last Studied", stats["last_studied"][:10])
    st.divider()