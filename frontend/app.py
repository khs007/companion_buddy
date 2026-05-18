import streamlit as st

st.set_page_config(
    page_title="AI Study Companion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 AI Study Companion")
st.markdown("*Upload your notes and let AI supercharge your studying*")

st.markdown("""
### How to use:
1. **Upload** your PDF notes using the Upload page
2. **Chat** with your notes using the Chat page  
3. **Generate** summaries, quizzes, and flashcards
4. **Track** your progress over time

👈 Use the sidebar to navigate between features.
""")

# Show uploaded files in sidebar
import requests
try:
    res = requests.get("http://localhost:8000/upload/list", timeout=3)
    files = res.json().get("files", [])
    if files:
        st.sidebar.markdown("### 📄 Your Documents")
        for f in files:
            st.sidebar.markdown(f"- {f}")
except:
    st.sidebar.warning("Backend not running. Start FastAPI first.")