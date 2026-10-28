import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
import base64
import os

st.set_page_config(
    page_title="EV Telemetry 3D Cockpit",
    page_icon="⚡",
    layout="wide"
)

# Function to load local image
def get_base64_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

bg_base64 = get_base64_bg("car_bg.jpg")
if bg_base64:
    bg_style = f"background: url('data:image/jpeg;base64,{bg_base64}') no-repeat center center fixed !important;"
else:
    bg_style = "background: url('https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed !important;"

# ----------------- ADVANCED CSS STYLING WITH HEXAGONS & VAPOR -----------------
st.markdown(f"""
<style>
    .stApp {{
        {bg_style}
        background-size: cover !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        color: #FAFAFA !important;
        overflow-x: hidden !important;
    }}

    /* ROTATING HEXAGON WHEEL */
    @keyframes spinWheel {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    @keyframes floatBox {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
        100% {{ transform: translateY(0px); }}
    }}

    .hex-wheel-container {{
        display: flex;
        align-items: center;
        gap: 15px;
        background: rgba(85, 107, 47, 0.85);
        border: 2px solid #84A346;
        border-radius: 18px;
        padding: 16px 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.7);
        backdrop-filter: blur(6px);
        animation: floatBox 4s ease-in-out infinite;
    }}

    .hex-wheel {{
        width: 55px;
        height: 55px;
        background: #6B8E23;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: spinWheel 8s linear infinite;
        box-shadow: 0 0 15px #84A346;
        border: 2px solid #FAFAFA;
    }}

    .hex-inner-cog {{
        width: 22px;
        height: 22px;
        background: #1E293B;
        border-radius: 50%;
        border: 2px dashed #FAFAFA;
    }}

    /* RANDOM OFFSET HUD BOXES */
    .random-offset-left {{
        margin-top: 15px;
        margin-left: 20px;
        transform: rotate(-1.5deg);
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.9), rgba(14, 165, 233, 0.75));
        border: 2px solid #38BDF8;
        border-radius: 25px 8px 30px 5px;
        padding: 18px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.6);
        animation: floatBox 5s ease-in-out infinite 0.5s;
    }}

    .random-offset-right {{
        margin-top: -10px;
        margin-right: 15px;
        transform: rotate(1.2deg);
        background: linear-gradient(135deg, rgba(255, 228, 232, 0.92), rgba(255, 182, 193, 0.88));
        color: #881337 !important;
        border: 2px solid #FF6584;
        border-radius: 5px 30px 10px 35px;
        padding: 18px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.6);
        animation: floatBox 4.5s ease-in-out infinite 1s;
    }}

    .random-offset-center {{
        margin-top: 10px;
        background: rgba(250, 250, 250, 0.94);
        color: #1E293B !important;
        border-left: 8px solid #556B2F;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        animation: floatBox 6s ease-in-out infinite 1.5s;
    }}

    .hud-title {{
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
        opacity: 0.95;
    }}

    .hud-val {{
        font-size: 30px;
        font-weight: 900;
        font-family: 'Impact', 'Arial Black', sans-serif;
    }}

    /* GREEN VAPOR / INDUSTRIAL MIST ANIMATION */
    @keyframes vaporRise {{
        0% {{
            background-position: 0% 100%, 0% 100%;
            opacity: 0.5;
        }}
        50% {{
            opacity: 0.85;
        }}
        100% {{
            background-position: 100% 0%, 50% 0%;
            opacity: 0.5;
        }}
    }}

    .green-vapor-zone {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: 140px;
        pointer-events: none;
        z-index: 9999;
        background: 
            radial-gradient(circle at bottom, rgba(85, 107, 47, 0.6) 0%, rgba(107, 142, 35, 0.3) 40%, transparent 80%),
            linear-gradient(to top, rgba(85, 107, 47, 0.45) 0%, rgba(132, 163, 70, 0.2) 50%, transparent 100%);
        animation: vaporRise 6s ease-in-out infinite alternate;
        filter: blur(12px);
    }}
</style>
<div class="green-vapor-zone"></div>
""", unsafe_allow_html=True)

# ----------------- 1 LAKH (100,000) SYNTHETIC TELEMETRY CACHE -----------------
@st.cache_data
def build_1lakh_dataset():
    np.random.seed(42)
    n = 100000
    cycles = np.linspace(1, 1500, n)
    actual_soh = np.clip(100.0 - (cycles / 1500.0) * 28.0 + np.random.normal(0, 0.2, n), 65.0, 100.0)
    voltage = np.clip(3.6 + 0.5 * (actual_soh / 100.0) + np.random.normal(0, 0.02, n), 3.2, 4.2)
    current = np.clip(8.0 + 15.0 * np.sin(cycles / 20.0) + np.random.normal(0, 0.5, n), -25.0, 30.0)
    temp = np.clip(25.0 + (cycles * 0.02) + np.abs(current) * 0.45 + np.random.normal(0, 0.3, n), 25.0, 65.0)
    capacity = np.clip(3.0 * (actual_soh / 100.0), 2.0, 3.0)
    resistance = np.clip(0.038 + (cycles / 1500.0) * 0.025, 0.035, 0.065)

    return pd.DataFrame({
        "cycle": cycles.astype(int),
        "actual_soh": actual_soh,
        "voltage": voltage,
        "current": current,
        "temperature": temp,
        "capacity": capacity,
        "resistance": resistance
    })

dataset_1lakh = build_1lakh_dataset()

# ----------------- SESSION CONTROLLER -----------------
if "sim_idx" not in st.session_state:
    st.session_state.sim_idx = 45600  # Start around ~456 cycles mark

st.session_state.sim_idx = (st.session_state.sim_idx + 180) % 99900
curr_point = dataset_1lakh.iloc[st.session_state.sim_idx]

cycle_val = int(curr_point["cycle"])
actual_soh = float(curr_point["actual_soh"])
pred_soh = float(np.clip(actual_soh + np.sin(st.session_state.sim_idx / 300.0) * 1.85, 68.0, 100.0))
pred_error = abs(actual_soh - pred_soh)
voltage = float(curr_point["voltage"])
current = float(curr_point["current"])
temp = float(curr_point["temperature"])
capacity = float(curr_point["capacity"])
resistance = float(curr_point["resistance"])

# ----------------- TOP BANNER -----------------
st.markdown("""
    <div style='background:linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.95)); border:2px solid #38BDF8; border-top:5px solid #556B2F; border-radius:14px; padding:14px 24px; margin-bottom:15px; display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <div style='font-size:11px; letter-spacing:2px; color:#38BDF8; font-weight:800;'>DYNAMIC 1-LAKH INTEGRATED TELEMETRY</div>
            <h2 style='margin:0; font-size:22px; color:#FAFAFA; font-weight:900;'>⚡ EV HEXAGON WHEEL HUD & 3D MESH CONSOLE</h2>
        </div>
        <div style='background:#556B2F; color:#FFF; font-weight:800; padding:6px 16px; border-radius:20px; font-size:12px;'>
            ● LIVE SOH STREAM
        </div>
    </div>
""", unsafe_allow_html=True)

# ----------------- IRREGULAR / RANDOMIZED STAGGERED HEXAGON LAYOUT -----------------
col_h1, col_h2, col_h3, col_h4 = st.columns([1.1, 1, 1, 1.1])

with col_h1:
    # Hexagon Wheel Animated Box
    st.markdown(f"""
        <div class="hex-wheel-container">
            <div class="hex-wheel">
                <div class="hex-inner-cog"></div>
            </div>
            <div>
                <div class="hud-title">ACTIVE SOH WHEEL</div>
                <div class="hud-val" style="color:#FAFAFA;">{actual_soh:.2f}%</div>
                <div style="font-size:11px; opacity:0.85;">1-Lakh Telemetry Synced</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_h2:
    # Random Offset Left Sky Blue
    st.markdown(f"""
        <div class="random-offset-left">
            <div class="hud-title">CYCLE INDEX</div>
            <div class="hud-val">{cycle_val}</div>
            <div style="font-size:11px; opacity:0.85;">Frame {st.session_state.sim_idx} / 100K</div>
        </div>
    """, unsafe_allow_html=True)

with col_h3:
    # Random Offset Right Light Pink
    st.markdown(f"""
        <div class="random-offset-right">
            <div class="hud-title" style="color:#881337;">CELL CORE TEMP</div>
            <div class="hud-val" style="color:#881337;">{temp:.2f} °C</div>
            <div style="font-size:11px; opacity:0.85; color:#881337;">Vapor Threshold Monitored</div>
        </div>
    """, unsafe_allow_html=True)

with col_h4:
    # Hexagon Wheel Animated Box 2
    st.markdown(f"""
        <div class="hex-wheel-container" style="background:rgba(2, 132, 199, 0.85); border-color:#38BDF8;">
            <div class="hex-wheel" style="background:#0284C7; box-shadow:0 0 15px #38BDF8;">
                <div class="hex-inner-cog"></div>
            </div>
            <div>
                <div class="hud-title">TERMINAL VOLTS</div>
                <div class="hud-val" style="color:#FAFAFA;">{voltage:.3f} V</div>
                <div style="font-size:11px; opacity:0.85;">Load: {current:.2f} A</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- SECTION 2: AI & POWERTRAIN STAGGERED ROW -----------------
r_a, r_b, r_c, r_d = st.columns(4)

with r_a:
    st.markdown(f"""
        <div class="random-offset-center">
            <div class="hud-title" style="color:#556B2F;">AI PREDICTED SOH</div>
            <div class="hud-val" style="color:#556B2F;">{pred_soh:.2f}%</div>
            <div style="font-size:11px; color:#64748B;">Neural Net Inference</div>
        </div>
    """, unsafe_allow_html=True)

with r_b:
    st.markdown(f"""
        <div class="random-offset-right" style="margin-top:0px;">
            <div class="hud-title" style="color:#881337;">PREDICTION DRIFT</div>
            <div class="hud-val" style="color:#881337;">{pred_error:.2f}%</div>
            <div style="font-size:11px; color:#881337;">Residual Variance</div>
        </div>
    """, unsafe_allow_html=True)

with r_c:
    st.markdown(f"""
        <div class="random-offset-left" style="margin-top:0px;">
            <div class="hud-title">USABLE CAPACITY</div>
            <div class="hud-val">{capacity:.3f} Ah</div>
            <div style="font-size:11px; opacity:0.85;">Nominal 3.0 Ah Cell</div>
        </div>
    """, unsafe_allow_html=True)

with r_d:
    st.markdown(f"""
        <div class="random-offset-center">
            <div class="hud-title" style="color:#1E293B;">INTERNAL IMPEDANCE</div>
            <div class="hud-val" style="color:#1E293B;">{resistance:.5f} Ω</div>
            <div style="font-size:11px; color:#64748B;">Ohmic Degradation</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- 3D TELEMETRY GRAPH SECTION -----------------
st.markdown("<h3 style='color:#38BDF8; font-size:17px; font-weight:800; letter-spacing:1px; margin-bottom:5px;'>🌐 REAL-TIME 3D TELEMETRY SURFACE (VOLTAGE vs TEMP vs SOH)</h3>", unsafe_allow_html=True)

# Sample 1,200 points around current simulation window from the 1-lakh dataset for high-FPS 3D rendering
start_sample = max(0, st.session_state.sim_idx - 600)
end_sample = min(100000, st.session_state.sim_idx + 600)
sample_df = dataset_1lakh.iloc[start_sample:end_sample]

fig_3d = go.Figure(data=[go.Scatter3d(
    x=sample_df["voltage"],
    y=sample_df["temperature"],
    z=sample_df["actual_soh"],
    mode='markers',
    marker=dict(
        size=3.5,
        color=sample_df["actual_soh"],
        colorscale=[
            [0, '#FF6584'],     # Light Pink alert
            [0.5, '#38BDF8'],   # Sky Blue
            [1, '#6B8E23']      # Olive Green
        ],
        opacity=0.85
    )
)])

# Highlight the live operating point in 3D
fig_3d.add_trace(go.Scatter3d(
    x=[voltage],
    y=[temp],
    z=[actual_soh],
    mode='markers+text',
    marker=dict(size=10, color='#FAFAFA', symbol='diamond', line=dict(color='#556B2F', width=2)),
    name='LIVE OPERATING POINT',
    text=['● CURRENT POINT'],
    textposition='top center'
))

fig_3d.update_layout(
    scene=dict(
        xaxis=dict(title='Voltage (V)', backgroundcolor="rgba(10,15,25,0.8)", gridcolor="#334155"),
        yaxis=dict(title='Temperature (°C)', backgroundcolor="rgba(10,15,25,0.8)", gridcolor="#334155"),
        zaxis=dict(title='SOH (%)', backgroundcolor="rgba(10,15,25,0.8)", gridcolor="#334155"),
    ),
    paper_bgcolor='rgba(15,23,42,0.75)',
    margin=dict(l=10, r=10, b=10, t=10),
    height=420
)

st.plotly_chart(fig_3d, use_container_width=True)

# Continuous smooth loop execution
time.sleep(1)
st.rerun()
