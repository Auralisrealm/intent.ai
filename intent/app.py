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
    page_title="INTENT AI | DECISION OS",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# 2. TRILLION-DOLLAR UI ENGINE (CSS)
# =========================
st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;700&display=swap');

    /* GLOBAL RESET & DARK MODE */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px);
        background-size: 40px 40px;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }

    /* GLASSMORPHISM CARDS */
    .glass-panel {
        background: rgba(20, 20, 20, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 4px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: -0.5px;
        color: #FFFFFF;
    }
    
    .mono-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #888;
        letter-spacing: 1px;
    }
    
    .big-metric {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3rem;
        font-weight: 700;
        color: #FFFFFF;
    }

    /* STRATEGIC BUTTONS */
    div.stButton > button {
        background: linear-gradient(90deg, #FFFFFF 0%, #CCCCCC 100%);
        color: #000000;
        border: none;
        border-radius: 0px;
        padding: 12px 24px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background: #FFFFFF;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }

    /* INPUT FIELD STYLING */
    .stTextArea textarea {
        background-color: rgba(10, 10, 10, 0.8);
        color: #00FF99;
        font-family: 'JetBrains Mono', monospace;
        border: 1px solid #333;
    }

    /* STATUS INDICATORS */
    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #00FF99;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00FF99;
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================
# 3. INTELLIGENCE LOGIC CORE
# =========================

def analyze_intent_logic(text):
    text_lower = text.lower()
    word_count = len(text.split())

    # INTELLIGENCE FILTER: Detect low-effort inputs
    if word_count < 3 and "shut" not in text_lower:
        return 0, "SYSTEM STANDBY", "AWAITING STRATEGIC DIRECTIVE", "#444444"

    # RISK HEURISTICS
    high_risk = ['crisis', 'fail', 'breach', 'attack', 'crash', 'urgent', 'critical', 'loss', 'exposure', 'vulnerability']
    med_risk = ['risk', 'monitor', 'check', 'verify', 'fluctuation', 'competitor', 'margin']
    
    if any(w in text_lower for w in high_risk):
        score = random.randint(88, 99)
        category = "CRITICAL THREAT VECTOR"
        action = "INITIATE CONTAINMENT PROTOCOL"
        color = "#FF2A2A" # Neon Red
    elif any(w in text_lower for w in med_risk):
        score = random.randint(50, 75)
        category = "STRATEGIC VOLATILITY"
        action = "DEPLOY COUNTER-STRATEGY"
        color = "#FFD700" # Cyber Yellow
    else:
        score = random.randint(15, 30)
        category = "OPERATIONAL NOMINAL"
        action = "OPTIMIZE GROWTH VECTOR"
        color = "#00FF99" # Cyber Green
        
    return score, category, action, color

def draw_neural_mesh():
    """Generates the 3D Brain Visualization"""
    X, _ = make_blobs(n_samples=50, centers=3, n_features=3, random_state=42)
    
    # Nodes
    trace_nodes = go.Scatter3d(
        x=X[:, 0], y=X[:, 1], z=X[:, 2],
        mode='markers',
        marker=dict(size=3, color='#FFFFFF', opacity=0.9),
        hoverinfo='none'
    )
    
    # Neural Lines
    x_lines, y_lines, z_lines = [], [], []
    for i in range(len(X)-1):
        if random.random() > 0.7:
            x_lines += [X[i, 0], X[i+1, 0], None]
            y_lines += [X[i, 1], X[i+1, 1], None]
            z_lines += [X[i, 2], X[i+1, 2], None]

    trace_edges = go.Scatter3d(
        x=x_lines, y=y_lines, z=z_lines,
        mode='lines',
        line=dict(color='#00FF99', width=1),
        opacity=0.3,
        hoverinfo='none'
    )

    layout = go.Layout(
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False
    )
    return go.Figure(data=[trace_edges, trace_nodes], layout=layout)

def generate_pdf_brief(text, category, action):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFillColorRGB(0,0,0)
    c.rect(0,0,612,792, fill=1)
    c.setStrokeColorRGB(1,1,1)
    c.setFillColorRGB(1,1,1)
    
    c.setFont("Courier-Bold", 18)
    c.drawString(50, 750, "INTENT AI // CLASSIFIED BRIEF")
    c.setLineWidth(1)
    c.line(50, 735, 550, 735)
    
    c.setFont("Courier", 10)
    c.drawString(50, 710, f"TIMESTAMP: {datetime.now().isoformat()}")
    c.drawString(50, 695, f"STATUS: {category}")
    c.drawString(50, 680, f"DIRECTIVE: {action}")
    
    c.drawString(50, 640, "INPUT SIGNAL DECODED:")
    text_obj = c.beginText(50, 620)
    text_obj.setFont("Courier", 10)
    words = text.split()
    line = ""
    for w in words:
        if len(line+w) > 60:
            text_obj.textLine(line)
            line = ""
        line += w + " "
    text_obj.textLine(line)
    c.drawText(text_obj)
    
    c.save()
    buffer.seek(0)
    return buffer

# =========================
# 4. SIDEBAR DASHBOARD
# =========================
with st.sidebar:
    st.markdown("### 💠 INTENT AI")
    st.markdown("<div class='mono-text'>SYSTEM v4.0.2</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<div class='mono-text'>NODE TELEMETRY</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("LATENCY", "8ms", "-2ms")
    col2.metric("UPTIME", "99.99%")
    
    st.markdown("---")
    st.markdown("<div class='mono-text'>ACTIVE FEEDS</div>", unsafe_allow_html=True)
    st.code("ERP: CONNECTED\nCRM: CONNECTED\nMKTS: CONNECTED", language="text")

# =========================
# 5. MAIN MISSION CONTROL
# =========================

# HEADER
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.markdown("# STRATEGIC DECISION CORE")
    st.markdown(f"<div class='mono-text'>// OPERATING SYSTEM ACTIVE | DATE: {datetime.now().strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)
with col_head2:
    st.markdown("<div style='text-align:right; margin-top:20px;'><span class='status-dot'></span> ONLINE</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# INPUT SECTION
st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
st.markdown("### <span style='color:#00FF99'>//</span> EXECUTIVE INPUT STREAM", unsafe_allow_html=True)
user_input = st.text_area("COMMAND LINE", height=70, placeholder="Waiting for strategic input...", label_visibility="collapsed")

c1, c2 = st.columns([1, 4])
with c1:
    run_btn = st.button("EXECUTE ANALYSIS")
with c2:
    st.markdown("<div class='mono-text' style='margin-top: 15px;'>AI MODEL: INTENT-L7 (QUANTUM QUANTIZED)</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if run_btn and user_input:
    # THE "HOLLYWOOD" LOADING SEQUENCE
    progress_bar = st.progress(0)
    status_box = st.empty()
    
    # Tech Jargon Sequence
    sequence = [
        "ESTABLISHING SECURE HANDSHAKE...",
        "DECRYPTING OPERATIONAL DATA LAKES...",
        "RUNNING PREDICTIVE MONTE CARLO SIMULATIONS...",
        "OPTIMIZING STRATEGIC VECTORS..."
    ]
    
    for i, phase in enumerate(sequence):
        status_box.markdown(f"<div class='mono-text' style='color:#00FF99'>{phase}</div>", unsafe_allow_html=True)
        progress_bar.progress((i + 1) * 25)
        time.sleep(0.2) # Snappy but visible

    progress_bar.empty()
    status_box.empty()
    
    # RESULTS
    score, category, action, color = analyze_intent_logic(user_input)
    
    st.markdown("### INTELLIGENCE REPORT")
    
    # 3-COLUMN DASHBOARD
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.markdown(f"""
        <div class='glass-panel' style='border-left: 4px solid {color}; text-align: center;'>
            <div class='mono-text'>DETECTED SIGNAL</div>
            <div style='font-size: 1.2rem; font-weight: bold; margin-top: 10px; color: #FFF;'>{category}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi2:
        st.markdown(f"""
        <div class='glass-panel' style='border-left: 4px solid {color}; text-align: center;'>
            <div class='mono-text'>RISK PROBABILITY</div>
            <div class='big-metric' style='color: {color}'>{score}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi3:
        st.markdown(f"""
        <div class='glass-panel' style='border-left: 4px solid #FFF; text-align: center;'>
            <div class='mono-text'>RECOMMENDED ACTION</div>
            <div style='font-size: 1.1rem; font-weight: bold; margin-top: 10px; color: #FFF;'>{action}</div>
        </div>
        """, unsafe_allow_html=True)

    # VISUALS LAYER
    v1, v2 = st.columns([2, 1])
    
    with v1:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<div class='mono-text' style='margin-bottom:10px;'>IMPACT HORIZON PROJECTION</div>", unsafe_allow_html=True)
        
        # Chart Logic
        dates = [datetime.now() + timedelta(days=x) for x in range(10)]
        if score > 70:
            # Crash Curve
            values = [100 - (x**1.8) for x in range(10)]
        elif score < 20 and score > 0:
            # Growth Curve
            values = [100 + (x**1.5) for x in range(10)]
        else:
            # Flat/Volatile
            values = [100 + random.randint(-5, 5) for x in range(10)]
            
        df_viz = pd.DataFrame({'Date': dates, 'Index': values})
        fig = px.area(df_viz, x='Date', y='Index')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#888',
            margin=dict(l=0,r=0,t=0,b=0),
            height=250,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#222')
        )
        fig.update_traces(line_color=color, fillcolor=color.replace(")", ", 0.1)"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with v2:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<div class='mono-text' style='margin-bottom:10px;'>NEURAL TOPOLOGY</div>", unsafe_allow_html=True)
        st.plotly_chart(draw_neural_mesh(), use_container_width=True)
        
        # Download
        pdf_file = generate_pdf_brief(user_input, category, action)
        st.download_button(
            "⬇ EXPORT BRIEFING",
            data=pdf_file,
            file_name="CONFIDENTIAL_STRATEGY.pdf",
            mime="application/pdf"
        )
        st.markdown("</div>", unsafe_allow_html=True)
