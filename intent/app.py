import streamlit as st
import pandas as pd
import numpy as np
import time
import io
import random
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import plotly.graph_objects as go
import plotly.express as px
from sklearn.datasets import make_blobs

# =========================
# 1. ENTERPRISE OS CONFIGURATION
# =========================
st.set_page_config(
    page_title="Intent AI | Enterprise OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# 2. STRATEGIC UI THEME (THE "PALANTIR" LOOK)
# =========================
st.markdown("""
<style>
    /* CORE OS THEME */
    .stApp {
        background-color: #000000;
        color: #E0E0E0;
    }
    
    /* TYPOGRAPHY */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stCode, .stCode blockquote {
        font-family: 'JetBrains Mono', monospace;
    }

    /* GLASS PANEL CONTAINERS */
    .os-card {
        background: rgba(20, 20, 20, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    /* HEADERS */
    h1 {
        font-weight: 600;
        letter-spacing: -1px;
        color: #ffffff;
    }
    
    h3 {
        color: #888;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }

    /* BUTTONS */
    .stButton>button {
        background: #FFFFFF;
        color: #000000;
        font-weight: 600;
        border: none;
        border-radius: 4px;
        height: 45px;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: #CCCCCC;
        transform: translateY(-1px);
    }
    
    /* REMOVE CLUTTER */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 3. INTELLIGENCE ENGINE FUNCTIONS
# =========================

def analyze_intent_logic(text):
    """
    Simulates a sophisticated NLP decision engine.
    Detects context, urgency, and strategic category.
    """
    text_lower = text.lower()
    word_count = len(text.split())

    # --- LOGIC FIX: FILTER LOW QUALITY INPUT ---
    # If the user just types "hi", "hello", or very short strings, reject it.
    if word_count < 3 and "shut" not in text_lower:
        risk_score = 0
        category = "AWAITING STRATEGIC INPUT"
        action = "PLEASE PROVIDE CONTEXTUAL INTEL"
        color = "#666666" # Neutral Grey
        return risk_score, category, action, color

    # 1. RISK DETECTION
    high_risk_triggers = ['high', 'critical', 'urgent', 'fail', 'loss', 'danger', 'crash', 'emergency', 'breach', 'competitor', 'down']
    medium_risk_triggers = ['warning', 'check', 'verify', 'fluctuation', 'monitor', 'risk', 'margin']
    
    risk_score = 0
    if any(word in text_lower for word in high_risk_triggers):
        risk_score = random.randint(85, 99)
    elif any(word in text_lower for word in medium_risk_triggers):
        risk_score = random.randint(45, 75)
    else:
        risk_score = random.randint(12, 35) # Default to stable/low risk
        
    # 2. CATEGORY DETECTION
    if risk_score > 80:
        category = "CRITICAL THREAT MITIGATION"
        action = "IMMEDIATE INTERVENTION REQUIRED"
        color = "#FF3B30" # Enterprise Red
    elif risk_score > 40:
        category = "STRATEGIC ALERT"
        action = "MONITORING PROTOCOLS ACTIVE"
        color = "#FFCC00" # Warning Yellow
    else:
        category = "OPERATIONAL OPTIMIZATION"
        action = "GROWTH VECTOR IDENTIFIED"
        color = "#34C759" # Success Green
        
    return risk_score, category, action, color

def draw_network_topology():
    """Generates the 'Brain' of the OS"""
    X, y = make_blobs(n_samples=60, centers=3, n_features=3, random_state=int(time.time()))
    
    trace_nodes = go.Scatter3d(
        x=X[:, 0], y=X[:, 1], z=X[:, 2],
        mode='markers',
        marker=dict(size=4, color='#ffffff', opacity=0.8),
        name='Data Nodes'
    )
    
    x_lines, y_lines, z_lines = [], [], []
    for i in range(len(X)-1):
        if random.random() > 0.85:
            x_lines.extend([X[i, 0], X[i+1, 0], None])
            y_lines.extend([X[i, 1], X[i+1, 1], None])
            z_lines.extend([X[i, 2], X[i+1, 2], None])

    trace_edges = go.Scatter3d(
        x=x_lines, y=y_lines, z=z_lines,
        mode='lines',
        line=dict(color='#888888', width=1),
        opacity=0.2,
        name='Neural Pathways'
    )

    layout = go.Layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False
    )
    return go.Figure(data=[trace_edges, trace_nodes], layout=layout)

def generate_strategic_memo(text, score, category, action):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "INTENT AI // EXECUTIVE STRATEGY BRIEF")
    c.setStrokeColorRGB(0, 0, 0)
    c.line(50, 740, 550, 740)
    
    c.setFont("Helvetica", 10)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    c.drawString(50, 720, f"GENERATED: {current_date}")
    c.drawString(50, 705, f"CLEARANCE: LEVEL 1 (EXECUTIVE)")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 670, "1. SITUATION ANALYSIS")
    c.setFont("Helvetica", 11)
    c.drawString(50, 655, f"CLASSIFICATION: {category}")
    c.drawString(50, 640, f"PROBABILITY INDEX: {score}%")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 610, "2. RECOMMENDED ACTION")
    c.setFont("Helvetica", 11)
    c.drawString(50, 595, f"{action}")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 560, "3. DECODED SIGNAL")
    
    text_obj = c.beginText(50, 540)
    text_obj.setFont("Helvetica", 10)
    words = text.split()
    line = ""
    for word in words:
        if len(line + word) > 95:
            text_obj.textLine(line)
            line = ""
        line += word + " "
    text_obj.textLine(line)
    c.drawText(text_obj)
    
    c.save()
    buffer.seek(0)
    return buffer

# =========================
# 4. SIDEBAR - OS NAVIGATION
# =========================
with st.sidebar:
    st.markdown("## INTENT AI")
    st.caption("v 2.4.0 | ENTERPRISE OS")
    st.markdown("---")
    menu = st.radio("SYSTEM MODULES", 
        ["Strategic Decision Core", "Data Ingestion", "Global Logs"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("LATENCY", "12ms")
    col2.metric("UPTIME", "99.99%")
    st.markdown("### CONNECTED NODES")
    st.code("CRM: Salesforce\nERP: SAP S/4HANA\nDATA: Snowflake", language="text")

# =========================
# 5. MAIN APPLICATION LOGIC
# =========================

if menu == "Strategic Decision Core":
    
    col_t1, col_t2 = st.columns([4, 1])
    with col_t1:
        st.title("Strategic Decision Core")
        st.caption(f"SYSTEM DATE: {datetime.now().strftime('%A, %B %d, %Y')}")
    with col_t2:
        st.markdown('<div style="text-align:right; color:#34C759; font-weight:bold;">● SYSTEM ONLINE</div>', unsafe_allow_html=True)

    st.markdown("---")

    # INPUT INTERFACE
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.markdown("### 📥 EXECUTIVE INPUT STREAM")
    user_input = st.text_area("Enter market signal, internal query, or raw strategic data:", height=80, label_visibility="collapsed", placeholder="Example: 'Competitor X is lowering prices by 15% in the APAC region. Is this a high risk to our Q3 margin?'")
    
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        run_analysis = st.button("RUN DECISION ENGINE")
    with col_info:
        st.caption("AI Model: Intent-L7 (Strategy Optimized) | Processing Layer: Real-time")
    st.markdown('</div>', unsafe_allow_html=True)

    if run_analysis and user_input:
        
        # 1. PROCESSING SIMULATION
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            "Parsing semantic intent...",
            "Accessing historical performance records...",
            "Simulating 10,000 strategic scenarios...",
            "Formulating optimal decision path..."
        ]
        
        for i, step in enumerate(steps):
            status_text.markdown(f"**// {step}**")
            progress_bar.progress((i + 1) * 25)
            time.sleep(0.3) 
            
        status_text.empty()
        progress_bar.empty()
        
        # 2. CALCULATE RESULTS
        risk_score, category, action, color_code = analyze_intent_logic(user_input)
        
        # 3. RESULTS DASHBOARD
        st.markdown(f"### ⚡ DECISION INTELLIGENCE OUTPUT")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""
            <div class="os-card" style="border-left: 4px solid {color_code};">
                <h3 style="margin:0">DECISION SIGNAL</h3>
                <h2 style="color:#fff; margin-top:5px;">{category}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="os-card" style="border-left: 4px solid {color_code};">
                <h3 style="margin:0">PREDICTED IMPACT</h3>
                <h2 style="color:{color_code}; margin-top:5px;">{risk_score}/100</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
            <div class="os-card" style="border-left: 4px solid #fff;">
                <h3 style="margin:0">RECOMMENDED ACTION</h3>
                <p style="color:#fff; font-size:1.1rem; font-weight:600; margin-top:5px;">{action}</p>
            </div>
            """, unsafe_allow_html=True)

        col_vis1, col_vis2 = st.columns([2, 1])
        
        with col_vis1:
            st.markdown('<div class="os-card">', unsafe_allow_html=True)
            st.markdown("### 📈 PROJECTED OUTCOME TRAJECTORY")
            
            dates = [datetime.now() + timedelta(days=i) for i in range(14)]
            base = 100
            
            # LOGIC FIX: If score is 0 (Bad Input), flat line. If High Risk, drop. If Low Risk, rise.
            if risk_score == 0:
                 values = [100 for i in range(14)]
            elif risk_score > 70:
                values = [base - (i * random.uniform(2, 5)) for i in range(14)]
            else:
                values = [base + (i * random.uniform(1, 4)) for i in range(14)]
                
            df_chart = pd.DataFrame({"Date": dates, "Index": values})
            
            fig = px.area(df_chart, x="Date", y="Index", template="plotly_dark")
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#333'),
                margin=dict(l=0, r=0, t=10, b=0),
                height=300
            )
            fig.update_traces(line_color=color_code, fillcolor=color_code)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_vis2:
            st.markdown('<div class="os-card">', unsafe_allow_html=True)
            st.markdown("### 🕸️ CONTEXT TOPOLOGY")
            st.plotly_chart(draw_network_topology(), use_container_width=True)
            
            pdf_data = generate_strategic_memo(user_input, risk_score, category, action)
            st.download_button(
                label="📄 DOWNLOAD STRATEGY MEMO",
                data=pdf_data,
                file_name=f"IntentAI_Strategy_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Data Ingestion":
    st.title("Secure Data Pipeline")
    st.info("Enterprise Gateway: CONNECTED (TLS 1.3)")
    st.file_uploader("Upload Encrypted Enterprise Data (CSV/JSON/Parquet)")

elif menu == "Global Logs":
    st.title("System Audit Logs")
    st.code(f"""
    [INFO] {datetime.now().strftime('%H:%M:%S')} - Model weights synchronized.
    [INFO] {datetime.now().strftime('%H:%M:%S')} - Latency check: 14ms.
    [WARN] {(datetime.now() - timedelta(minutes=5)).strftime('%H:%M:%S')} - External API rate limit approaching.
    [INFO] {(datetime.now() - timedelta(minutes=10)).strftime('%H:%M:%S')} - User session authenticated.
    """)
