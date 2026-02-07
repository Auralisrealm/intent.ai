import streamlit as st
import pandas as pd
import time
import random
import io

# try/except blocks to prevent crashing if libraries are missing
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    st.error("⚠️ Library 'reportlab' not found. Please add it to requirements.txt")

try:
    import plotly.graph_objects as go
    import plotly.express as px
except ImportError:
    st.error("⚠️ Library 'plotly' not found. Please add it to requirements.txt")

# =========================
# 1. APP CONFIGURATION
# =========================
st.set_page_config(
    page_title="RiskAnalytics AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Injection
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Stylish Cards */
    div.stMetric {
        background-color: #262730;
        border: 1px solid #4C4C4C;
        padding: 15px;
        border-radius: 8px;
    }
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 2. HELPER FUNCTIONS
# =========================

def generate_pdf(risk_level, summary):
    """Generates a PDF report in memory"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, 750, "RiskAnalytics AI - Confidential Report")
    c.line(40, 740, 550, 740)
    
    # Body
    c.setFont("Helvetica", 12)
    c.drawString(40, 710, f"Detected Risk Level: {risk_level}")
    c.drawString(40, 690, "Analysis Summary:")
    
    text_object = c.beginText(40, 670)
    text_object.setFont("Helvetica", 11)
    # Simple wrapping
    words = summary.split()
    line = ""
    for word in words:
        if len(line + word) > 80:
            text_object.textLine(line)
            line = ""
        line += word + " "
    text_object.textLine(line)
    c.drawText(text_object)
    
    c.save()
    buffer.seek(0)
    return buffer

def analyze_logic(text):
    """Simulates AI processing"""
    time.sleep(1.5) # Fake processing delay for effect
    keywords = ["churn", "loss", "critical", "fail", "down", "error"]
    
    if any(k in text.lower() for k in keywords):
        return "Critical", random.randint(80, 99), "#FF4B4B" # Red
    return "Stable", random.randint(10, 40), "#00CC96" # Green

# =========================
# 3. SIDEBAR
# =========================
st.sidebar.title("⚡ RiskAnalytics")
st.sidebar.markdown("---")
nav = st.sidebar.radio("Navigate", ["Live Analysis", "Data Upload"])
st.sidebar.markdown("---")
st.sidebar.caption("System Version: v2.4.0 (Hackathon Build)")

# =========================
# 4. MAIN PAGE
# =========================

if nav == "Live Analysis":
    st.title("🚀 Operational Risk Dashboard")
    st.markdown("Enter operational logs below to detect semantic anomalies.")

    col1, col2 = st.columns([2, 1])

    with col1:
        user_input = st.text_area("Log Input", height=150, placeholder="Example: Server latency is increasing and customer churn is high...")
        run_btn = st.button("Analyze Logs")

    if run_btn and user_input:
        with st.spinner("Processing Natural Language..."):
            risk_level, score, color = analyze_logic(user_input)
            
        # Metrics Display
        st.markdown("### 📊 Analysis Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Risk Assessment", risk_level, delta_color="off")
        m2.metric("Confidence Score", f"{random.randint(95,99)}%", "AI Verified")
        m3.metric("Urgency", "High" if score > 50 else "Low")

        # Gauge Chart (Plotly)
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                title = {'text': "Risk Probability"},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': color}}
            ))
            fig.update_layout(height=300, margin=dict(l=20,r=20,t=50,b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)

        # PDF Export
        st.markdown("---")
        pdf_data = generate_pdf(risk_level, user_input)
        st.download_button("📥 Download Official Report", data=pdf_data, file_name="risk_report.pdf", mime="application/pdf")

elif nav == "Data Upload":
    st.title("📂 Batch Processor")
    uploaded_file = st.file_uploader("Upload CSV for Automated Visualization", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(), use_container_width=True)
        
        # Auto-plot
        numeric_cols = df.select_dtypes(include=['float', 'int']).columns
        if len(numeric_cols) > 0:
            st.subheader("📈 Trend Auto-Detection")
            selected_col = st.selectbox("Select Metric", numeric_cols)
            fig = px.area(df, y=selected_col, title=f"Analysis of {selected_col}")
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig, use_container_width=True)

