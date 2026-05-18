# File: frontend/pages/1_Upload.py

import streamlit as st
import requests

st.header("📤 Upload Study Material")
st.markdown("Upload a PDF and we'll index it for AI-powered study features.")

uploaded = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded:
    st.info(f"Ready to upload: **{uploaded.name}**")

    if st.button("Upload & Index PDF", type="primary"):
        with st.spinner("Processing your PDF... this takes ~10-20 seconds"):
            res = requests.post(
                "http://localhost:8000/upload/pdf",
                files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
            )

        if res.status_code == 200:
            data = res.json()
            st.success(f"✅ Indexed **{data['chunks_indexed']}** text chunks!")
            st.json(data)
        else:
            st.error(f"Upload failed: {res.text}")