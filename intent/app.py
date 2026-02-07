import streamlit as st
import time
import csv
import io
import os
import json
import logging
import base64
import textwrap
import random
import openai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# -----------------------
# LOGGING (same as yours)
# -----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")

st.title("Intent AI")

# =====================================================
# SAME ANALYZE LOGIC (copied from your Flask version)
# =====================================================
def analyze_logic(user_input):

    time.sleep(2)

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        openai.api_key = api_key
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role":"system","content":"You are an analyst."},
                    {"role":"user","content":user_input}
                ]
            )
            return resp["choices"][0]["message"]["content"]
        except:
            pass

    # fallback (your mock)
    risk = "Medium"
    if "loss" in user_input.lower():
        risk = "Critical"

    return {
        "risk_level": risk,
        "summary": "Analysis indicates volatility in operational metrics.",
        "recommendations": [
            "Initiate retention program",
            "Automate support",
            "Improve workflows"
        ]
    }


# =====================================================
# UI PART (replaces Flask pages)
# =====================================================

tab1, tab2 = st.tabs(["Text Analysis", "CSV Upload"])

# -------------------
# TEXT ANALYSIS TAB
# -------------------
with tab1:
    user_input = st.text_area("Enter business context")

    if st.button("Analyze"):
        result = analyze_logic(user_input)
        st.json(result)


# -------------------
# CSV UPLOAD TAB
# -------------------
with tab2:

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        text = file.read().decode("utf-8")

        stream = io.StringIO(text)
        reader = csv.reader(stream)

        values = []

        for row in reader:
            for cell in row:
                try:
                    values.append(float(cell))
                    break
                except:
                    pass

        if values:
            st.line_chart(values)

            first = values[0]
            last = values[-1]

            trend = ((last-first)/abs(first))*100 if first!=0 else 0

            st.success(f"Trend: {trend:.1f}%")

        else:
            st.error("No numeric data found")
