import streamlit as st
import pandas as pd
import numpy as np
import time
import io
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import plotly.graph_objects as go
import plotly.express as px
from sklearn.datasets import make_blobs

# =========================
# 1. TRIPLE-A CONFIGURATION
# =========================
st.set_page_config(
    page_title="Intent AI | Decision Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# 2. ADVANCED CSS (GLASSMORPHISM & CYBERPUNK)
# =========================
st.markdown("""
<style>
    /* GLOBAL THEME */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #000000 100%);
        color: #E0E0E0;
    }
    
    /* CUSTOM FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
    }

    /* GLASSMORPHISM CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }

    /* NEON TEXT & HEADERS */
    h1 {
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    h3 {
        color: #00C9FF;
        letter-spacing: 1px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }

    /* BUTTON STYLING */
    .stButton>button {
        background: linear-gradient(90deg, #0061ff 0%, #60efff 100%);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        height: 50px;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.5);
    }
    
    /* REMOVE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 3. HIGH-TECH VISUALIZATION FUNCTIONS
# =========================

def draw_neural_network_3d():
    """Generates a 3D rotating brain/network graph to look 'Trillion Dollar'"""
    # Generate 3D clusters
    X, y = make_blobs(n_samples=100, centers=4, n_features=3, random_state=42)
    
    trace_nodes = go.Scatter3d(
        x=X[:, 0], y=X[:, 1], z=X[:, 2],
        mode='markers',
        marker=dict(
            size=5,
            color=y,
            colorscale='Viridis',
            opacity=0.8
        ),
        name='Neural Nodes'
    )
    
    # Create random connections (synapses)
    x_lines, y_lines, z_lines = [], [], []
    for i in range(len(X)-1):
        if random.random() > 0.9: # 10% connection rate
            x_lines.extend([X[i, 0], X[i+1, 0], None])
            y_lines.extend([X[i, 1], X[i+1, 1], None])
            z_lines.extend([X[i, 2], X[i+1, 2], None])

    trace_edges = go.Scatter3d(
        x=x_lines, y=y_lines, z=z_lines,
        mode='lines',
        line=dict(color='#00C9FF', width=1),
        opacity=0.3,
        name='Synapses'
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
    
    fig = go.Figure(data=[trace_edges, trace_nodes], layout=layout)
    return fig

def generate_enterprise_pdf(text, risk_score, intent_type):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Dark Mode PDF logic is hard, stick to clean enterprise white
    c.setStrokeColorRGB(0, 0, 0)
    
    # Header
    c.setFillColorRGB(0.1, 0.1, 0.3)
    c.rect(0, 750, 612, 50, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, 765, "INTENT AI | INTELLIGENCE BRIEF")
    
    # Metadata
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, 730, f"REF: {random.randint(100000, 999999)}-SECURE")
    c.drawString(450, 730, f"DATE: {time.strftime('%Y-%m-%d')}")
    
    # Metrics
    c.setFont("Helvetica", 12)
    c.drawString(40, 680, f"DETECTED INTENT: {intent_type.upper()}")
    c.drawString(40, 660, f"RISK PROBABILITY: {risk_score}%")
    
    # Analysis
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 620, "EXECUTIVE DECODING:")
    
    text_obj = c.beginText(40, 600)
    text_obj.setFont("Helvetica", 11)
    words = text.split()
    line = ""
    for word in words:
        if len(line + word) > 80:
            text_obj.textLine(line)
            line = ""
        line += word + " "
    text_obj.textLine(line)
    c.drawText(text_obj)
    
    c.save()
    buffer.seek(0)
    return buffer

# =========================
# 4. SIDEBAR NAVIGATION
# =========================
with st.sidebar:
    st.markdown("## 🧠 INTENT AI")
    st.markdown("### ENTERPRISE CORE")
    
    st.markdown("---")
    menu = st.radio("MODULE SELECTOR", ["Command Center", "Data Lake Ingestion", "System Logs"])
    st.markdown("---")
    
    # Fake System Stats
    st.metric("Neural Uplink", "42ms", "Stable")
    st.metric("Model Confidence", "99.8%", "+0.2%")
    
    st.markdown("---")
    st.caption("© 2024 Intent AI Systems. Restricted Access.")

# =========================
# 5. MAIN INTERFACE
# =========================

if menu == "Command Center":
    # HEADER
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.title("Strategic Decision Engine")
        st.markdown("*Autonomous Semantic Analysis & Predictive Modeling*")
    with col_h2:
        st.image("https://cdn-icons-png.flaticon.com/512/9626/9626620.png", width=80) # Placeholder for futuristic icon

    st.divider()

    # INPUT SECTION (GLASS CARD)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📡 INCOMING TRANSMISSION")
    user_input = st.text_area("Enter raw unstructured data, logs, or strategic directives:", height=100, placeholder="Waiting for signal...")
    
    col_act1, col_act2 = st.columns([1, 4])
    with col_act1:
        analyze_btn = st.button("INITIATE DECODE")
    with col_act2:
        st.caption("Pressing initiate will trigger the Layer-7 Neural Mesh for immediate semantic extraction.")
    st.markdown('</div>', unsafe_allow_html=True)

    # LOGIC EXECUTION
    if analyze_btn and user_input:
        
        # 1. THE "WOW" LOADING EFFECT
        with st.status("⚡ ENGAGING NEURAL MESH...", expanded=True) as status:
            st.write("🔹 Tokenizing raw input streams...")
            time.sleep(0.8)
            st.write("🔹 Aligning vector embeddings...")
            time.sleep(0.8)
            st.write("🔹 Cross-referencing Global Risk Database...")
            time.sleep(0.7)
            st.write("🔹 Calculating predictive horizons...")
            time.sleep(0.5)
            status.update(label="✅ INTELLIGENCE ACQUIRED", state="complete", expanded=False)

        # 2. DETERMINE OUTPUT (Simulated)
        risk_score = random.randint(75, 98) if "fail" in user_input or "risk" in user_input else random.randint(12, 35)
        intent_type = "CRITICAL THREAT" if risk_score > 60 else "OPERATIONAL OPTIMIZATION"
        color_code = "#FF4B4B" if risk_score > 60 else "#00CC96"

        # 3. DASHBOARD ROW 1: METRICS & 3D GRAPH
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <h2 style="color:{color_code}; font-size: 3rem; margin:0;">{risk_score}%</h2>
                <p style="text-transform:uppercase; letter-spacing:2px;">Risk Probability</p>
                <hr style="border-color: #333;">
                <h4 style="color:white;">INTENT: {intent_type}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Download Report
            pdf_bytes = generate_enterprise_pdf(user_input, risk_score, intent_type)
            st.download_button("📄 EXPORT CLASSIFIED BRIEF", pdf_bytes, "intent_ai_brief.pdf", "application/pdf")

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🧬 SEMANTIC NETWORK TOPOLOGY")
            st.plotly_chart(draw_neural_network_3d(), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 4. DASHBOARD ROW 2: PREDICTIVE CHARTS
        st.markdown("### 🔮 PREDICTIVE HORIZON")
        
        # Fake Data for Chart
        dates = pd.date_range(start="2024-01-01", periods=10)
        base_val = 50
        values = [base_val + (i * random.randint(-5, 10)) for i in range(10)]
        df_chart = pd.DataFrame({"Date": dates, "Metric": values})
        
        fig_line = px.area(df_chart, x="Date", y="Metric", title="Projected Impact Trajectory")
        fig_line.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E0E0E0',
            xaxis_showgrid=False,
            yaxis_showgrid=True,
            yaxis_gridcolor='#333'
        )
        fig_line.update_traces(line_color=color_code)
        
        st.plotly_chart(fig_line, use_container_width=True)

elif menu == "Data Lake Ingestion":
    st.title("💾 Data Lake Ingestion")
    st.info("Secure connection to enterprise data warehouses established.")
    
    uploaded_file = st.file_uploader("Upload Encrypted Dataset (CSV)", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)
