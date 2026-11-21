import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import base64
import os

st.set_page_config(
    page_title="EV Circular Cockpit HUD",
    page_icon="🏎️",
    layout="wide"
)

# Load local car background image
def get_base64_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

bg_base64 = get_base64_bg("car_bg.jpg")
if bg_base64:
    bg_img = f"url('data:image/jpeg;base64,{bg_base64}')"
else:
    bg_img = "url('https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=1920&q=80')"

# ----------------- CSS: 25% LIGHT FILM + 8 CIRCULAR DIALS + BUBBLES + GREEN VAPOR -----------------
st.markdown(f"""
<style>
    /* 25% Light Film Overlay on Original Futuristic EV Image */
    .stApp {{
        background: 
            linear-gradient(rgba(250, 250, 250, 0.25), rgba(250, 250, 250, 0.25)),
            {bg_img} no-repeat center center fixed !important;
        background-size: cover !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        color: #FAFAFA !important;
        overflow-x: hidden !important;
    }}

    /* Floating Bubbles */
    @keyframes floatUp {{
        0% {{ transform: translateY(105vh) scale(0.6); opacity: 0; }}
        30% {{ opacity: 0.7; }}
        80% {{ opacity: 0.5; }}
        100% {{ transform: translateY(-20vh) scale(1.2); opacity: 0; }}
    }}
    .bubble {{
        position: fixed;
        bottom: -50px;
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.85), rgba(56, 189, 248, 0.35));
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
        pointer-events: none;
        z-index: 999;
        animation: floatUp 8s infinite ease-in;
    }}
    .b1 {{ left: 8%; width: 22px; height: 22px; animation-duration: 7s; }}
    .b2 {{ left: 26%; width: 32px; height: 32px; animation-duration: 9s; animation-delay: 2s; }}
    .b3 {{ left: 48%; width: 18px; height: 18px; animation-duration: 6.5s; animation-delay: 4s; }}
    .b4 {{ left: 71%; width: 28px; height: 28px; animation-duration: 8.5s; animation-delay: 1.5s; }}
    .b5 {{ left: 89%; width: 36px; height: 36px; animation-duration: 10s; animation-delay: 3s; }}

    /* Float animation for circles */
    @keyframes pulseFloat {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-7px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* CIRCULAR DIAL PODS (100% ROUND) */
    .circle-pod {{
        width: 195px;
        height: 195px;
        border-radius: 50%;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 15px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.65), inset 0 0 18px rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(6px);
        transition: transform 0.3s ease;
        animation: pulseFloat 4.5s ease-in-out infinite;
    }}
    .circle-pod:hover {{
        transform: scale(1.06);
    }}

    /* 4 Theme Colors for Circles */
    .c-olive {{
        background: radial-gradient(circle at 30% 30%, rgba(107, 142, 35, 0.94), rgba(66, 84, 36, 0.96));
        border: 4px solid #A3E635;
        color: #FAFAFA !important;
    }}
    .c-skyblue {{
        background: radial-gradient(circle at 30% 30%, rgba(56, 189, 248, 0.92), rgba(3, 105, 161, 0.96));
        border: 4px solid #BAE6FD;
        color: #FAFAFA !important;
        margin-top: 22px; /* Staggered offset */
    }}
    .c-lightpink {{
        background: radial-gradient(circle at 30% 30%, rgba(255, 228, 232, 0.96), rgba(255, 182, 193, 0.95));
        border: 4px solid #FF6584;
        color: #881337 !important;
    }}
    .c-fairwhite {{
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.96), rgba(241, 245, 249, 0.95));
        border: 4px solid #556B2F;
        color: #1E293B !important;
        margin-top: 22px; /* Staggered offset */
    }}

    .c-title {{
        font-size: 10.5px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 4px;
        opacity: 0.9;
    }}
    .c-val {{
        font-size: 28px;
        font-weight: 900;
        font-family: 'Impact', 'Arial Black', sans-serif;
        line-height: 1.1;
    }}
    .c-sub {{
        font-size: 10px;
        margin-top: 5px;
        font-weight: 600;
        opacity: 0.85;
    }}

    /* Interactive Control Panel Styling */
    div[data-testid="stHorizontalBlock"] {{
        align-items: center;
    }}

    /* Green Rising Vapor at Bottom */
    @keyframes vaporRise {{
        0% {{ opacity: 0.5; }}
        50% {{ opacity: 0.85; }}
        100% {{ opacity: 0.5; }}
    }}
    .green-vapor-zone {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: 115px;
        pointer-events: none;
        z-index: 998;
        background: linear-gradient(to top, rgba(85, 107, 47, 0.65) 0%, rgba(107, 142, 35, 0.25) 55%, transparent 100%);
        animation: vaporRise 5s ease-in-out infinite alternate;
        filter: blur(10px);
    }}
</style>

<div class="bubble b1"></div>
<div class="bubble b2"></div>
<div class="bubble b3"></div>
<div class="bubble b4"></div>
<div class="bubble b5"></div>
<div class="green-vapor-zone"></div>
""", unsafe_allow_html=True)

# ----------------- 1 LAKH (100,000) REALISTIC DYNAMIC DRIVE DATASET -----------------
@st.cache_data
def build_realistic_1lakh_dataset():
    np.random.seed(42)
    n = 100000
    t = np.arange(n)
    
    # Gradual SOH degradation over 100k time-steps (1 to 1200 cycles)
    cycles = np.linspace(100, 1200, n)
    actual_soh = np.clip(99.5 - (cycles / 1200.0) * 24.0 + 0.3 * np.sin(t / 150.0), 70.0, 100.0)
    
    # Realistic Dynamic Drive Waves (Acceleration spikes + Regenerative braking + Charging pulses)
    drive_wave = np.sin(t / 12.0) * 14.0 + np.cos(t / 5.0) * 7.0 + np.random.normal(0, 1.5, n)
    current = np.clip(6.0 + drive_wave, -25.0, 30.0)
    
    # Voltage drops when current spikes (V = OCV - I*R)
    r_internal = 0.040 + (cycles / 1200.0) * 0.022
    ocv = 3.75 + 0.35 * (actual_soh / 100.0) + 0.12 * np.sin(t / 40.0)
    voltage = np.clip(ocv - (current * r_internal * 0.35) + np.random.normal(0, 0.015, n), 3.20, 4.20)
    
    # Realistic Thermal Wave (heats up during high current, cools down on low current)
    temp = np.clip(29.0 + (cycles * 0.014) + (np.abs(current) * 0.55) + 2.5 * np.sin(t / 25.0), 25.0, 65.0)
    
    capacity = np.clip(3.0 * (actual_soh / 100.0), 2.10, 3.00)
    
    return pd.DataFrame({
        "step": t,
        "cycle": cycles.astype(int),
        "actual_soh": actual_soh,
        "voltage": voltage,
        "current": current,
        "temperature": temp,
        "capacity": capacity,
        "resistance": r_internal
    })

df_1lakh = build_realistic_1lakh_dataset()

# ----------------- TOP COCKPIT HEADER -----------------
st.markdown("""
    <div style='background:linear-gradient(90deg, rgba(15,23,42,0.92), rgba(30,41,59,0.92)); border:2px solid #38BDF8; border-top:5px solid #556B2F; border-radius:40px; padding:12px 28px; margin-bottom:15px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 8px 25px rgba(0,0,0,0.6);'>
        <div>
            <div style='font-size:10px; letter-spacing:2px; color:#38BDF8; font-weight:800;'>INTERACTIVE VEHICLE TELEMETRY CONSOLE</div>
            <h2 style='margin:0; font-size:20px; color:#FAFAFA; font-weight:900;'>🏎️ EV BATTERY CIRCULAR GAUGES & REALISTIC WAVEFORM</h2>
        </div>
        <div style='background:#556B2F; color:#FFF; font-weight:800; padding:6px 16px; border-radius:20px; font-size:12px; border:1px solid #A3E635;'>
            ● 1,00,000 LIVE TELEMETRY
        </div>
    </div>
""", unsafe_allow_html=True)

# ----------------- USER INTERACTIVE CONTROL BAR -----------------
st.markdown("<div style='background:rgba(15,23,42,0.82); padding:10px 20px; border-radius:16px; border:1px solid #38BDF8; margin-bottom:18px;'>", unsafe_allow_html=True)
ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([1.3, 1.3, 1, 1])

with ctrl1:
    drive_mode = st.selectbox(
        "🚦 Select Vehicle Mode",
        ["City Traffic (Dynamic)", "Highway Sport (High Load)", "Fast Charging (CC Mode)"],
        index=0
    )

with ctrl2:
    cycle_jump = st.slider("⚡ Simulation Speed (Steps/Sec)", min_value=1, max_value=15, value=3)

with ctrl3:
    live_active = st.toggle("🟢 Live Auto-Stream", value=True)

with ctrl4:
    if st.button("🔄 Reset Telemetry", use_container_width=True):
        st.session_state.sim_idx = 15000
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Update index dynamically
if "sim_idx" not in st.session_state:
    st.session_state.sim_idx = 28500

if live_active:
    st.session_state.sim_idx = (st.session_state.sim_idx + cycle_jump) % 99800

curr = df_1lakh.iloc[st.session_state.sim_idx]

# Adjust live values slightly based on user's selected Driving Mode
mode_volt_offset = 0.08 if "Charging" in drive_mode else (-0.06 if "Sport" in drive_mode else 0.0)
mode_temp_offset = 4.5 if "Sport" in drive_mode else (-1.5 if "Charging" in drive_mode else 0.0)
mode_curr_mult = 1.35 if "Sport" in drive_mode else (0.8 if "Charging" in drive_mode else 1.0)

cycle_val = int(curr["cycle"])
actual_soh = float(curr["actual_soh"])
pred_soh = float(np.clip(actual_soh + np.sin(st.session_state.sim_idx / 25.0) * 1.45, 68.0, 100.0))
pred_error = abs(actual_soh - pred_soh)

voltage = float(np.clip(curr["voltage"] + mode_volt_offset, 3.20, 4.20))
current = float(np.clip(curr["current"] * mode_curr_mult, -25.0, 30.0))
temp = float(np.clip(curr["temperature"] + mode_temp_offset, 25.0, 65.0))
capacity = float(curr["capacity"])
resistance = float(curr["resistance"])

# ----------------- ROW 1: 4 CIRCULAR DIAL PODS -----------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
        <div class="circle-pod c-olive">
            <div class="c-title">ACTIVE SOH</div>
            <div class="c-val">{actual_soh:.2f}%</div>
            <div class="c-sub">Frame {st.session_state.sim_idx:,} / 100K</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="circle-pod c-skyblue">
            <div class="c-title">DRIVE CYCLES</div>
            <div class="c-val">{cycle_val}</div>
            <div class="c-sub">{drive_mode.split(' ')[0]} Mode</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class="circle-pod c-lightpink">
            <div class="c-title">CORE TEMP</div>
            <div class="c-val">{temp:.2f}°C</div>
            <div class="c-sub">Thermal Limit &lt; 65°C</div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
        <div class="circle-pod c-fairwhite">
            <div class="c-title" style="color:#556B2F;">TERMINAL VOLTS</div>
            <div class="c-val" style="color:#556B2F;">{voltage:.3f} V</div>
            <div class="c-sub" style="color:#0284C7;">Current: {current:.2f} A</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- ROW 2: 4 MORE CIRCULAR DIAL PODS -----------------
d1, d2, d3, d4 = st.columns(4)

with d1:
    st.markdown(f"""
        <div class="circle-pod c-fairwhite">
            <div class="c-title" style="color:#556B2F;">AI PREDICTED SOH</div>
            <div class="c-val" style="color:#556B2F;">{pred_soh:.2f}%</div>
            <div class="c-sub" style="color:#64748B;">Neural Net Output</div>
        </div>
    """, unsafe_allow_html=True)

with d2:
    st.markdown(f"""
        <div class="circle-pod c-lightpink">
            <div class="c-title">PREDICTION DRIFT</div>
            <div class="c-val">{pred_error:.2f}%</div>
            <div class="c-sub">Model Variance</div>
        </div>
    """, unsafe_allow_html=True)

with d3:
    st.markdown(f"""
        <div class="circle-pod c-skyblue">
            <div class="c-title">PACK CAPACITY</div>
            <div class="c-val">{capacity:.3f} Ah</div>
            <div class="c-sub">Nominal: 3.000 Ah</div>
        </div>
    """, unsafe_allow_html=True)

with d4:
    st.markdown(f"""
        <div class="circle-pod c-olive">
            <div class="c-title">IMPEDANCE (R₀)</div>
            <div class="c-val" style="font-size:24px;">{resistance:.5f} Ω</div>
            <div class="c-sub">Internal Resistance</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- REALISTIC 2D DUAL-WAVEFORM TELEMETRY GRAPH -----------------
st.markdown("<h3 style='color:#38BDF8; font-size:17px; font-weight:800; letter-spacing:1px; margin-bottom:5px; text-shadow:0 2px 4px #000;'>📈 REAL-TIME DYNAMIC TELEMETRY WAVEFORM (VOLTAGE & TEMPERATURE CURVES)</h3>", unsafe_allow_html=True)

# Slice 120 recent time-steps so realistic oscillating waves are clearly visible
start_idx = max(0, st.session_state.sim_idx - 120)
end_idx = st.session_state.sim_idx + 1
window_df = df_1lakh.iloc[start_idx:end_idx].copy()

# Apply user mode offset to the visible waveform
window_df["voltage"] = np.clip(window_df["voltage"] + mode_volt_offset, 3.20, 4.20)
window_df["temperature"] = np.clip(window_df["temperature"] + mode_temp_offset, 25.0, 65.0)

fig_2d = make_subplots(specs=[[{"secondary_y": True}]])

# Realistic Oscillating Voltage Wave (Olive Green)
fig_2d.add_trace(
    go.Scatter(
        x=window_df["step"],
        y=window_df["voltage"],
        name="Terminal Voltage (V)",
        mode="lines",
        line=dict(color="#84CC16", width=3, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(132, 204, 22, 0.18)'
    ),
    secondary_y=False
)

# Realistic Oscillating Temperature Wave (Light Pink / Coral)
fig_2d.add_trace(
    go.Scatter(
        x=window_df["step"],
        y=window_df["temperature"],
        name="Core Temp (°C)",
        mode="lines",
        line=dict(color="#FF6584", width=3, shape='spline')
    ),
    secondary_y=True
)

# Live Tracking Marker
fig_2d.add_trace(
    go.Scatter(
        x=[st.session_state.sim_idx],
        y=[voltage],
        name="Live Sensor Pin",
        mode="markers",
        marker=dict(size=13, color="#38BDF8", symbol="circle", line=dict(color="#FFFFFF", width=2.5))
    ),
    secondary_y=False
)

fig_2d.update_layout(
    height=370,
    paper_bgcolor='rgba(15, 23, 42, 0.84)',
    plot_bgcolor='rgba(15, 23, 42, 0.72)',
    margin=dict(l=20, r=20, t=35, b=25),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#FAFAFA", size=12)),
    hovermode="x unified"
)

fig_2d.update_xaxes(title_text="Real-Time Telemetry Stream (1-Lakh Frame Index)", gridcolor="rgba(255,255,255,0.08)", color="#CBD5E1")
fig_2d.update_yaxes(title_text="Terminal Voltage (V)", gridcolor="rgba(255,255,255,0.08)", color="#A3E635", secondary_y=False, range=[3.3, 4.25])
fig_2d.update_yaxes(title_text="Core Temperature (°C)", gridcolor="rgba(255,255,255,0.08)", color="#FF6584", secondary_y=True, range=[24, 66])

st.plotly_chart(fig_2d, use_container_width=True)

if live_active:
    time.sleep(1)
    st.rerun()
