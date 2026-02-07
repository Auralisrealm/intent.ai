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
# 1. KERNEL OPTIMIZATION (CACHE LAYER)
# =========================
# We cache the expensive logic so it doesn't re-run on every UI interaction.
# This prevents the app from "thinking" when you just want to click a button.
@st.cache_data(show_spinner=False)
def get_neural_data():
    """Generates 3D coordinates once and caches them."""
    X, _ = make_blobs(n_samples=50, centers=3, n_features=3, random_state=42)
    return X

@st.cache_data(show_spinner=False)
def analyze_intent_logic(text):
    """Simulates the heavy AI processing with caching."""
    # Simulate processing time only on NEW inputs
    time.sleep(0.5) 
    
    text_lower = text.lower()
    high_risk = ['crisis', 'fail', 'breach', 'attack', 'crash', 'urgent', 'critical']
    med_risk = ['risk', 'monitor', 'check', 'verify', 'fluctuation']
    
    if any(w in text_lower for w in high_risk):
        return random.randint(88, 99), "CRITICAL THREAT VECTOR", "INITIATE CONTAINMENT", "#FF2A2A"
    elif any(w in text_lower for w in med_risk):
        return random.randint(50, 75), "STRATEGIC VOLATILITY", "DEPLOY COUNTER-STRATEGY", "#FFD700"
    else:
        return random.randint(15, 30), "OPERATIONAL NOMINAL", "OPTIMIZE GROWTH VECTOR", "#00FF99"

# =========================
# 2. SYSTEM CONFIGURATION
# =========================
st.set_page_config(
    page_title="INTENT AI | DECISION OS",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.intent.ai/help',
        'Report a bug': "https://www.intent.ai/bug",
        'About': "# Intent AI Enterprise OS v2.0"
    }
)

# =========================
# 3. NON-BLOCKING UI ENGINE
# =========================
# FIX: Replaced slow @import with standard Link tags and font-display: swap
# FIX: Added meta description injection hack for SEO
st.markdown("""
<head>
    <meta name="description" content="Intent AI: The Enterprise Decision Operating System. Convert live data into strategic action.">
</head>
<style>
    /* OPTIMIZED FONT LOADING */
    @font-face {
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400;
        font-display: swap; /* Fixes render blocking */
        src: url(https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hjp-Ek-_EeA.woff) format('woff');
    }

    /* GLOBAL RESET & DARK MODE */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px);
        background-size: 40px 40px;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }

    /* GLASSMORPHISM CARDS (Optimized Blurs) */
    .glass-panel {
        background: rgba(20, 20, 20, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px); /* Reduced blur for performance */
        -webkit-backdrop-filter: blur(8px);
        border-radius: 4px;
        padding: 24px;
        margin-bottom: 20px;
    }

    /* TYPOGRAPHY hierarchy fixed for SEO */
    h1 { font-size: 2.5rem; font-weight: 700; color: #FFF; letter-spacing: -1px; }
    h2 { font-size: 1.5rem; font-weight: 600; color: #EEE; }
    h3 { font-size: 1.1rem; font-weight: 600; color: #CCC; }
    
    .mono-text {
        font-family: monospace;
        font-size: 0.85rem;
        color: #888;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .big-metric {
        font-family: monospace;
        font-size: 3rem;
        font-weight: 700;
        color: #FFFFFF;
    }

    /* CSS BUTTONS */
    div.stButton > button {
        background: #E0E0E0;
        color: #000;
        border: none;
        padding: 12px 24px;
        font-weight: 700;
        text-transform: uppercase;
        width: 100%;
        transition: transform 0.1s;
    }
    div.stButton > button:hover {
        background: #FFF;
        transform: scale(1.01);
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* STATUS INDICATORS */
    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #00FF99;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #00FF99;
    }
    
    /* Remove default streamlit junk */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================
# 4. LIGHTWEIGHT VISUALIZATION
# =========================

def draw_neural_mesh_optimized():
    """Generates the 3D Brain Visualization with fewer polygons for speed"""
    X = get_neural_data() # Pulls from cache
    
    # Nodes
    trace_nodes = go.Scatter3d(
        x=X[:, 0], y=X[:, 1], z=X[:, 2],
        mode='markers',
        marker=dict(size=3, color='#FFFFFF', opacity=0.8), # Reduced opacity calc
        hoverinfo='none'
    )
    
    # Pre-calculated simpler edges
    x_lines, y_lines, z_lines = [], [], []
    # Only draw 20% of lines to save rendering time
    for i in range(0, len(X)-1, 2): 
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
        showlegend=False,
        height=300 # Fixed height to prevent layout shift
    )
    return go.Figure(data=[trace_edges, trace_nodes], layout=layout)

def generate_pdf_brief(text, category, action):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(50, 750, f"INTENT AI // {category}")
    c.drawString(50, 730, f"DIRECTIVE: {action}")
    c.drawString(50, 710, f"INPUT: {text[:50]}...")
    c.save()
    buffer.seek(0)
    return buffer

# =========================
# 5. UI LAYOUT (ACCESSIBILITY OPTIMIZED)
# =========================

# SIDEBAR
with st.sidebar:
    st.markdown("### INTENT AI v2.0")
    st.markdown("---")
    st.metric("SYSTEM LATENCY", "12ms", "-4ms")
    st.metric("UPTIME", "99.99%")

# MAIN HEADER (H1 for SEO)
c1, c2 = st.columns([4,1])
with c1:
    st.markdown("<h1>STRATEGIC DECISION CORE</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='mono-text'>// SYSTEM DATE: {datetime.now().strftime('%Y-%m-%d')}</p>", unsafe_allow_html=True)
with c2:
    st.markdown("<div style='text-align:right; padding-top:20px;'><span class='status-dot'></span> ONLINE</div>", unsafe_allow_html=True)

# INPUT SECTION
st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
st.markdown("<h2>EXECUTIVE INPUT STREAM</h2>", unsafe_allow_html=True) # H2 for Hierarchy
user_input = st.text_area("COMMAND LINE", height=70, placeholder="Enter strategic query...", label_visibility="collapsed")

col_btn, col_info = st.columns([1, 4])
with col_btn:
    run_btn = st.button("EXECUTE")
with col_info:
    st.markdown("<div class='mono-text' style='margin-top: 15px;'>MODEL: INTENT-L7 (CACHED)</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# LOGIC EXECUTION
if run_btn and user_input:
    # 1. Instant Feedback (No fake loading bars that block interaction)
    with st.spinner("PROCESSING..."):
        score, category, action, color = analyze_intent_logic(user_input)

    # 2. Results Dashboard
    st.markdown("<h2>INTELLIGENCE REPORT</h2>", unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    k1.markdown(f"<div class='glass-panel' style='border-left: 4px solid {color}'><strong>SIGNAL</strong><br>{category}</div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='glass-panel' style='border-left: 4px solid {color}'><strong>PROBABILITY</strong><br><span style='font-size:2rem'>{score}%</span></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='glass-panel'><strong>DIRECTIVE</strong><br>{action}</div>", unsafe_allow_html=True)

    # 3. Visuals & Export
    v1, v2 = st.columns([2, 1])
    
    with v1:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h3>IMPACT HORIZON</h3>", unsafe_allow_html=True)
        # Simplified Chart Logic
        df = pd.DataFrame({'Date': pd.date_range(start=datetime.now(), periods=10), 'Value': np.random.randn(10).cumsum() + 100})
        fig = px.area(df, x='Date', y='Value')
        fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_traces(line_color=color)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with v2:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h3>NEURAL TOPOLOGY</h3>", unsafe_allow_html=True)
        st.plotly_chart(draw_neural_mesh_optimized(), use_container_width=True)
        
        pdf_data = generate_pdf_brief(user_input, category, action)
        st.download_button("⬇ EXPORT BRIEF", data=pdf_data, file_name="brief.pdf", mime="application/pdf")
        st.markdown("</div>", unsafe_allow_html=True)

