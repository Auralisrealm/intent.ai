import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime

# =========================
# 1. PAGE CONFIGURATION & CSS (THE "TRILLION DOLLAR" LOOK)
# =========================
st.set_page_config(
    page_title="INTENT AI | DECISION OS",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for that "Iron Man / Enterprise" feel
st.markdown("""
<style>
    /* GLOBAL DARK THEME */
    .stApp {
        background-color: #050505;
        color: #E0E0E0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* INPUT FIELD STYLING */
    .stTextArea textarea {
        background-color: #111;
        color: #00FFC2;
        border: 1px solid #333;
        font-family: 'Courier New', monospace;
    }
    .stTextArea textarea:focus {
        border: 1px solid #00FFC2;
        box-shadow: 0 0 10px #00FFC2;
    }

    /* CUSTOM CARDS (GLASSMORPHISM) */
    .metric-card {
        background: rgba(20, 20, 20, 0.8);
        border-left: 3px solid #333;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: scale(1.02);
        border-left: 3px solid #00FFC2;
    }

    /* TYPOGRAPHY */
    h1, h2, h3 { letter-spacing: -0.5px; }
    .highlight { color: #00FFC2; font-weight: bold; }
    .alert { color: #FF4B4B; font-weight: bold; }
    .subtext { font-size: 0.8em; color: #888; }
    .mono { font-family: 'Courier New', monospace; }

    /* BUTTON STYLING */
    div.stButton > button {
        background: linear-gradient(90deg, #00FFC2 0%, #008F6B 100%);
        color: #000;
        font-weight: bold;
        border: none;
        padding: 0.75rem 2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        width: 100%;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 15px #00FFC2;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 2. INTELLIGENCE ENGINE (SOLVING THE "UNRELATED ANSWER" PROBLEM)
# =========================
def get_strategic_response(query):
    """
    This simulates a high-end LLM/RAG pipeline using keyword heuristics 
    to ensure the answer ALWAYS matches the user's specific context.
    """
    q = query.lower()
    
    # SCENARIO A: CYBERSECURITY (Matches your screenshot)
    if any(x in q for x in ['cyber', 'security', 'breach', 'vulnerability', 'attack']):
        return {
            "status": "CRITICAL EXPOSURE",
            "color": "#FF4B4B",
            "confidence": "98.4%",
            "analysis": "Vulnerability identified in Legacy ERP Node 4. Estimated data exposure: 1.2M records.",
            "strategy": "IMMEDIATE CONTAINMENT PROTOCOL",
            "actions": [
                "1. Isolate ERP Sector 7 immediately (Stop API traffic).",
                "2. Deploy 'Dark-Comms' strategy to minimize stock volatility.",
                "3. Prepare GDPR/CCPA compliance brief for Legal."
            ],
            "impact_data": [100, 80, 45, 30, 25, 60, 85], # Dip and recovery
            "impact_label": "Brand Equity Projection (6 Months)"
        }

    # SCENARIO B: REVENUE/SALES
    elif any(x in q for x in ['revenue', 'sales', 'growth', 'q3', 'profit']):
        return {
            "status": "OPPORTUNITY VECTOR",
            "color": "#00FFC2",
            "confidence": "92.1%",
            "analysis": "Market signals indicate under-penetration in APAC region. Competitor X is weak there.",
            "strategy": "AGGRESSIVE EXPANSION",
            "actions": [
                "1. Reallocate 15% of EU marketing budget to APAC.",
                "2. Activate channel partners in Singapore/Tokyo.",
                "3. Launch flash-incentive for enterprise tier."
            ],
            "impact_data": [50, 52, 55, 65, 80, 95, 110], # Growth curve
            "impact_label": "Revenue Uplift Projection ($M)"
        }

    # SCENARIO C: SUPPLY CHAIN
    elif any(x in q for x in ['supply', 'logistics', 'shipping', 'delay', 'inventory']):
        return {
            "status": "LOGISTICAL RISK",
            "color": "#FFD700",
            "confidence": "89.5%",
            "analysis": "Route congestion detected in Panama Canal. 14 Days added to lead time.",
            "strategy": "ROUTE DIVERSIFICATION",
            "actions": [
                "1. Trigger air-freight for Class A inventory.",
                "2. Notify distributors of +2 week lead time adjustment.",
                "3. Source temporary local suppliers for raw materials."
            ],
            "impact_data": [90, 85, 80, 82, 88, 92, 95], # Dip then stabilize
            "impact_label": "Inventory Health Index"
        }

    # FALLBACK (GENERIC)
    else:
        return {
            "status": "ANALYZING PATTERNS",
            "color": "#00CCFF",
            "confidence": "75.0%",
            "analysis": "Input received. Cross-referencing internal historical data with external market signals.",
            "strategy": "DATA ENRICHMENT REQUIRED",
            "actions": [
                "1. Clarify specific metric target (Revenue vs Risk).",
                "2. Run deeper diagnostic on current operational parameters.",
                "3. Monitor for signal noise reduction."
            ],
            "impact_data": [50, 55, 53, 58, 60, 62, 65],
            "impact_label": "Operational Efficiency"
        }

# =========================
# 3. UI LAYOUT
# =========================

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1>INTENT AI <span style='font-weight:lighter; opacity:0.6'>| DECISION OS</span></h1>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align:right; font-family:monospace; color:#00FFC2'>SYS: ONLINE<br>{datetime.now().strftime('%H:%M:%S UTC')}</div>", unsafe_allow_html=True)

st.markdown("---")

# --- INPUT SECTION ---
st.markdown("### 1. EXECUTIVE INPUT STREAM")
default_text = "System Alert: A major cyber-security vulnerability has been detected in our legacy ERP system. Estimated exposure includes 1.2M customer records. What is the immediate strategic action and projected impact on brand equity?"
query = st.text_area("Enter Context / Data Signal:", value=default_text, height=100, label_visibility="collapsed")

if st.button("GENERATE STRATEGIC DIRECTIVE"):
    
    # --- FAKE PROCESSING ANIMATION (Immersion) ---
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = [
        "Connecting to Neural Lattice...",
        "Ingesting Live ERP Data...",
        "Running Risk Simulation Models (Monte Carlo)...",
        "Synthesizing Strategic Options...",
        "Finalizing Directive..."
    ]
    
    for i, stage in enumerate(stages):
        status_text.markdown(f"<p class='mono' style='color:#00FFC2'> > {stage}</p>", unsafe_allow_html=True)
        progress_bar.progress((i + 1) * 20)
        time.sleep(0.3) # Fast but noticeable
    
    status_text.empty()
    progress_bar.empty()

    # --- GET LOGIC ---
    response = get_strategic_response(query)

    # --- RESULTS DASHBOARD ---
    st.markdown("### 2. INTELLIGENCE REPORT")
    
    # Top Metrics Row
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {response['color']}">
            <div class="subtext">SIGNAL STATUS</div>
            <div style="font-size: 1.5em; font-weight: bold; color: {response['color']}">{response['status']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="subtext">AI CONFIDENCE</div>
            <div style="font-size: 1.5em; font-weight: bold;">{response['confidence']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="subtext">MODEL USED</div>
            <div style="font-size: 1.5em; font-weight: bold; font-family:monospace">INTENT-L7</div>
        </div>
        """, unsafe_allow_html=True)

    # Main Content Split
    c1, c2 = st.columns([1, 1])

    # Left: Text Strategy
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0">SITUATION ANALYSIS</h3>
            <p>{response['analysis']}</p>
            <hr style="border-color:#333">
            <h3 style="color:{response['color']}">RECOMMENDED STRATEGY</h3>
            <p style="font-size:1.1em; font-weight:bold">{response['strategy']}</p>
            <ul style="line-height: 1.8;">
                {''.join([f'<li>{action}</li>' for action in response['actions']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Right: Chart Simulation
    with c2:
        st.markdown(f"<div class='metric-card'><div class='subtext'>SIMULATION: {response['impact_label']}</div>", unsafe_allow_html=True)
        
        # Plotly Dark Mode Chart
        dates = pd.date_range(start=datetime.now(), periods=7)
        fig = go.Figure()
        
        # Area chart
        fig.add_trace(go.Scatter(
            x=dates, 
            y=response['impact_data'], 
            fill='tozeroy',
            mode='lines+markers',
            line=dict(color=response['color'], width=3),
            marker=dict(size=8, color='#FFF'),
            name='Projection'
        ))
        
        # Styling the chart to blend with the app
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E0E0E0'),
            margin=dict(l=0, r=0, t=10, b=0),
            height=250,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#333')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Idle State visuals
    st.info("System Ready. Awaiting Executive Input...")
    st.markdown("<div style='opacity:0.3; text-align:center; margin-top:50px'>INTENT AI NEURAL TOPOLOGY v2.04</div>", unsafe_allow_html=True)


