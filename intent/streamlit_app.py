import streamlit as st
import pandas as pd
import io
import csv
import os
import json
import textwrap
from datetime import datetime

try:
    import openai
except Exception:
    openai = None

st.set_page_config(page_title="Intent AI", layout="wide", initial_sidebar_state="collapsed")

st.title("🎯 Intent AI — Decision Intelligence")
st.markdown("Predict risks and identify opportunities with an embedded analysis engine")

def _call_openai_analyze(prompt_text: str):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or openai is None:
        return None
    try:
        openai.api_key = api_key
        system_msg = (
            "You are an analyst that outputs a single JSON object describing "
            "risk_level, summary, predictions (list of {metric,trend,status}), and recommendations (list of strings). Respond with JSON only."
        )
        resp = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt_text}],
            max_tokens=600,
            temperature=0.2,
        )
        text = resp['choices'][0]['message']['content']
        parsed = json.loads(text)
        parsed['status'] = parsed.get('status', 'success')
        return parsed
    except Exception:
        return None

def analyze_text_local(user_input: str):
    # Try live OpenAI then fallback to deterministic mock
    parsed = _call_openai_analyze(user_input)
    if parsed:
        return parsed

    # Fallback mock response
    risk_level = "Medium"
    if user_input and ("churn" in user_input.lower() or "loss" in user_input.lower()):
        risk_level = "Critical"

    return {
        "status": "success",
        "risk_level": risk_level,
        "summary": "Analysis indicates volatility in operational metrics. Primary concern is linked to retention and stability.",
        "predictions": [
            {"metric": "Employee Attrition", "trend": "+12%", "status": "High Risk"},
            {"metric": "Customer Churn", "trend": "+5%", "status": "Warning"},
        ],
        "recommendations": [
            "Initiate immediate retention program for top 10% talent.",
            "Automate support workflows to reduce customer friction.",
        ],
    }

def process_csv_bytes(content: bytes, selected_col=None, selected_x=None):
    text = content.decode('utf-8', errors='ignore')
    if not text.strip():
        return {"status": "error", "message": "CSV file is empty"}

    lines = text.splitlines()
    if len(lines) > 10000:
        return {"status": "error", "message": "CSV exceeds 10,000 rows limit"}

    stream = io.StringIO(text)
    sample = stream.getvalue().splitlines()
    headers = None
    if sample:
        first_row = sample[0]
        possible = [h.strip() for h in first_row.split(',')]
        if any([not h.replace('.', '', 1).isdigit() for h in possible]):
            headers = possible

    labels = []
    values = []

    stream.seek(0)
    if headers:
        reader = csv.DictReader(stream)
        col_name = None
        if selected_col:
            try:
                idx = int(selected_col)
                if 0 <= idx < len(headers):
                    col_name = headers[idx]
            except Exception:
                if selected_col in headers:
                    col_name = selected_col
        if not col_name:
            col_name = headers[-1]

        col_name_x = None
        if selected_x:
            try:
                idx = int(selected_x)
                if 0 <= idx < len(headers):
                    col_name_x = headers[idx]
            except Exception:
                if selected_x in headers:
                    col_name_x = selected_x

        row_index = 0
        for row in reader:
            row_index += 1
            cell = row.get(col_name)
            if cell is None:
                continue
            try:
                num = float(cell)
            except Exception:
                continue
            label_val = None
            if col_name_x:
                label_val = row.get(col_name_x)
            labels.append(label_val if label_val is not None else str(row_index))
            values.append(num)
    else:
        reader = csv.reader(stream)
        row_index = 0
        for row in reader:
            row_index += 1
            if not row:
                continue
            num = None
            if selected_col:
                try:
                    idx = int(selected_col)
                    if 0 <= idx < len(row):
                        num = float(row[idx])
                except Exception:
                    num = None
            if num is None:
                for cell in row:
                    try:
                        num = float(cell)
                        break
                    except Exception:
                        continue
            if num is None:
                continue
            label_val = None
            if selected_x:
                try:
                    idx_x = int(selected_x)
                    if 0 <= idx_x < len(row):
                        label_val = row[idx_x]
                except Exception:
                    label_val = None
            labels.append(label_val if label_val is not None else str(row_index))
            values.append(num)

    if not values:
        return {"status": "error", "message": "No numeric data found in CSV. Ensure at least one column contains numbers."}

    first = values[0]
    last = values[-1]
    trend_pct = ((last - first) / abs(first) * 100) if first != 0 else 0
    risk = "High Risk" if trend_pct > 10 else "Warning"

    response = {
        "status": "success",
        "headers": headers or [],
        "labels": labels,
        "values": values,
        "predictions": [
            {"metric": "Uploaded Metric", "trend": f"{trend_pct:.1f}%", "status": risk}
        ],
        "recommendations": [
            "Investigate root causes for rising metric.",
            "Run targeted interventions and measure impact over next quarter."
        ],
        "summary": f"Uploaded metric changed by {trend_pct:.1f}% over the observed period."
    }
    return response


# Tabs
analysis_tab, upload_tab, demo_tab = st.tabs(["📝 Text Analysis", "📊 CSV Upload", "📈 Demo Data"])

with analysis_tab:
    st.subheader("Business Context Analysis")
    text = st.text_area("Describe your business situation:", placeholder="e.g., We are facing high employee churn and revenue is flat...", height=150)
    col1, col2 = st.columns([1, 1])
    with col1:
        analyze_btn = st.button("🔍 Run Analysis", key="analyze", use_container_width=True)
    with col2:
        st.info("⏳ Takes ~2 seconds (includes AI latency)")

    if analyze_btn:
        if text:
            with st.spinner("Analyzing..."):
                result = analyze_text_local(text)
            risk = result.get('risk_level', 'Unknown')
            risk_color = "🔴" if risk == "Critical" else "🟡" if risk == "Warning" else "🟢"
            st.success(f"{risk_color} **Risk Level: {risk}**")
            st.markdown("**Summary:**")
            st.write(result.get('summary', 'No summary available'))
            if result.get('predictions'):
                st.markdown("**Predictions:**")
                for pred in result['predictions']:
                    st.metric(label=pred.get('metric', 'Metric'), value=pred.get('trend', 'N/A'), delta=pred.get('status', ''))
            if result.get('recommendations'):
                st.markdown("**Recommendations:**")
                for i, rec in enumerate(result['recommendations'], 1):
                    st.write(f"{i}. {rec}")
        else:
            st.warning("Please enter business context first")

with upload_tab:
    st.subheader("CSV Data Upload & Analysis")
    uploaded = st.file_uploader("Upload CSV file", type=['csv'])
    if uploaded:
        try:
            content = uploaded.read()
            df = pd.read_csv(io.BytesIO(content))
            st.success(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
            col1, col2 = st.columns(2)
            with col1:
                y_col = st.selectbox("Select Y Column (metric)", df.columns)
            with col2:
                x_col = st.selectbox("Select X Column (labels)", df.columns, index=0 if len(df.columns) > 1 else 0)

            if st.button("📈 Analyze CSV", key="upload", use_container_width=True):
                with st.spinner("Processing CSV..."):
                    result = process_csv_bytes(content, selected_col=y_col, selected_x=x_col)
                if result.get('status') == 'success':
                    chart_df = pd.DataFrame({'Label': result.get('labels', []), y_col: result.get('values', [])})
                    st.line_chart(chart_df.set_index('Label'))
                    st.success(result.get('summary', ''))
                    if result.get('predictions'):
                        st.markdown("**Trend Predictions:**")
                        for pred in result['predictions']:
                            status_icon = "🔴" if 'High Risk' in pred.get('status', '') else "🟡" if 'Warning' in pred.get('status', '') else "🟢"
                            st.write(f"{status_icon} **{pred.get('metric')}**: {pred.get('trend')} ({pred.get('status')})")
                    if result.get('recommendations'):
                        st.markdown("**Recommendations:**")
                        for i, rec in enumerate(result['recommendations'], 1):
                            st.write(f"{i}. {rec}")
                else:
                    st.error(result.get('message', 'Upload failed'))

            with st.expander("📋 Preview Data"):
                st.dataframe(df.head(10))
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")

with demo_tab:
    st.subheader("Sample Datasets")
    col1, col2, col3 = st.columns(3)
    demo_files = [
        ("📈 Growth Trend", "demo_data/demo_growth.csv"),
        ("📉 Decline Trend", "demo_data/demo_decline.csv"),
        ("⚡ Volatile Data", "demo_data/demo_noise.csv"),
    ]
    for (label, path), btn_col in zip(demo_files, (col1, col2, col3)):
        with btn_col:
            if st.button(label, use_container_width=True):
                try:
                    with open(path, 'rb') as f:
                        content = f.read()
                    result = process_csv_bytes(content)
                    if result.get('status') == 'success':
                        chart_df = pd.DataFrame({'Time': result['labels'], 'Value': result['values']})
                        st.line_chart(chart_df.set_index('Time'))
                        st.json(result.get('predictions'))
                    else:
                        st.error(result.get('message', 'Demo failed'))
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.divider()
st.caption(f"Intent AI v1.0 MVP — Last updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
