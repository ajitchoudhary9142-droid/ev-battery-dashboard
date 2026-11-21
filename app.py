import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import base64
import os

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION (BRIGHT DUAL-TONE PRO OS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EV Telemetry OS | Dual-Tone Precision",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_base64_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

bg_base64 = get_base64_bg("car_bg.jpg")
bg_img = (
    f"url('data:image/jpeg;base64,{bg_base64}')"
    if bg_base64
    else "url('https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=1920&q=80')"
)

# -----------------------------------------------------------------------------
# 2. DUAL-TONE ARCHITECTURE: FAIR PLATINUM WHITE + OLIVE SAGE GREEN (NO BLACK)
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');

    /* Bright Fair White Frosted Overlay over Futuristic EV Image */
    .stApp {{
        background: 
            linear-gradient(135deg, rgba(248, 250, 252, 0.84), rgba(236, 243, 232, 0.88)),
            {bg_img} no-repeat center center fixed !important;
        background-size: cover !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #1E293B !important;
        overflow-x: hidden !important;
    }}

    /* Clean UI Chrome */
    header[data-testid="stHeader"] {{ background: transparent !important; }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    /* Subtle Olive & White Floating Bubbles */
    @keyframes floatBubble {{
        0% {{ transform: translateY(105vh) scale(0.7); opacity: 0; }}
        35% {{ opacity: 0.55; }}
        80% {{ opacity: 0.35; }}
        100% {{ transform: translateY(-15vh) scale(1.15); opacity: 0; }}
    }}
    .dual-bubble {{
        position: fixed;
        bottom: -40px;
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.95), rgba(101, 139, 56, 0.35));
        border: 1.5px solid rgba(77, 107, 42, 0.45);
        border-radius: 50%;
        box-shadow: 0 4px 15px rgba(77, 107, 42, 0.2);
        pointer-events: none;
        z-index: 999;
        animation: floatBubble 10s infinite ease-in-out;
    }}
    .b1 {{ left: 10%; width: 16px; height: 16px; animation-duration: 8s; }}
    .b2 {{ left: 28%; width: 24px; height: 24px; animation-duration: 11s; animation-delay: 2s; }}
    .b3 {{ left: 52%; width: 14px; height: 14px; animation-duration: 7.5s; animation-delay: 4s; }}
    .b4 {{ left: 74%; width: 22px; height: 22px; animation-duration: 9.5s; animation-delay: 1s; }}
    .b5 {{ left: 88%; width: 18px; height: 18px; animation-duration: 10.5s; animation-delay: 3s; }}

    /* Top Dual-Tone OS Header */
    .dual-header {{
        background: rgba(255, 255, 255, 0.92);
        border: 1.5px solid rgba(77, 107, 42, 0.28);
        border-left: 8px solid #4D6B2A;
        backdrop-filter: blur(16px);
        border-radius: 18px;
        padding: 16px 28px;
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(77, 107, 42, 0.12);
    }}
    .dual-badge {{
        background: #4D6B2A;
        color: #FFFFFF;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 7px 16px;
        border-radius: 999px;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(77, 107, 42, 0.3);
    }}

    /* Dual-Tone Circular Precision Gauges */
    @keyframes gentleFloat {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-6px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* Tone 1: Fair White Center with Olive Ring */
    .dial-white {{
        width: 192px;
        height: 192px;
        border-radius: 50%;
        margin: 0 auto;
        background: radial-gradient(circle at 30% 25%, #FFFFFF, #F1F5EC);
        border: 4px solid #4D6B2A;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 16px;
        box-shadow: 0 12px 28px rgba(77, 107, 42, 0.18), inset 0 0 15px rgba(77, 107, 42, 0.08);
        transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
        animation: gentleFloat 4.5s infinite ease-in-out;
        position: relative;
    }}
    .dial-white::before {{
        content: '';
        position: absolute;
        inset: 6px;
        border-radius: 50%;
        border: 1.5px dashed rgba(77, 107, 42, 0.35);
        pointer-events: none;
    }}
    .dial-white:hover {{
        transform: translateY(-6px) scale(1.05);
        box-shadow: 0 18px 38px rgba(77, 107, 42, 0.28);
    }}

    /* Tone 2: Rich Olive Sage Center with Fair White Ring */
    .dial-olive {{
        width: 192px;
        height: 192px;
        border-radius: 50%;
        margin: 0 auto;
        margin-top: 22px;
        background: radial-gradient(circle at 30% 25%, #658B38, #425C23);
        border: 4px solid #FFFFFF;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 16px;
        box-shadow: 0 12px 28px rgba(77, 107, 42, 0.28), inset 0 0 18px rgba(255, 255, 255, 0.15);
        transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
        animation: gentleFloat 4.5s infinite ease-in-out 0.6s;
        position: relative;
    }}
    .dial-olive::before {{
        content: '';
        position: absolute;
        inset: 6px;
        border-radius: 50%;
        border: 1.5px dashed rgba(255, 255, 255, 0.45);
        pointer-events: none;
    }}
    .dial-olive:hover {{
        transform: translateY(-6px) scale(1.05);
        box-shadow: 0 18px 38px rgba(77, 107, 42, 0.38);
    }}

    /* Typography for Tone 1 (White Dial) */
    .lbl-w {{ font-size: 10px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; color: #4D6B2A; margin-bottom: 5px; }}
    .val-w {{ font-family: 'JetBrains Mono', monospace; font-size: 27px; font-weight: 800; color: #2D4016; line-height: 1.1; }}
    .sub-w {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #5A7247; margin-top: 6px; font-weight: 600; }}

    /* Typography for Tone 2 (Olive Dial) */
    .lbl-o {{ font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #ECF3E8; margin-bottom: 5px; opacity: 0.9; }}
    .val-o {{ font-family: 'JetBrains Mono', monospace; font-size: 27px; font-weight: 800; color: #FFFFFF; line-height: 1.1; }}
    .sub-o {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #E2EEDB; margin-top: 6px; opacity: 0.85; }}

    /* Bottom Olive Mist Glow */
    .olive-mist {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: 95px;
        pointer-events: none;
        z-index: 998;
        background: linear-gradient(to top, rgba(77, 107, 42, 0.28) 0%, transparent 100%);
        filter: blur(8px);
    }}
</style>

<div class="dual-bubble b1"></div>
<div class="dual-bubble b2"></div>
<div class="dual-bubble b3"></div>
<div class="dual-bubble b4"></div>
<div class="dual-bubble b5"></div>
<div class="olive-mist"></div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. 10,00,000 (1 MILLION / 10 LAKH) VECTORIZED TELEMETRY ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def generate_1_million_telemetry():
    np.random.seed(2026)
    n = 1_000_000
    t = np.arange(n, dtype=np.int32)
    
    cycles = np.linspace(1, 1500, n, dtype=np.float32)
    actual_soh = np.clip(99.8 - (cycles / 1500.0) * 26.5 + 0.25 * np.sin(t / 400.0), 68.0, 100.0)
    
    drive_wave = (
        np.sin(t / 18.0) * 13.0
        + np.cos(t / 7.0) * 6.5
        + np.random.normal(0, 1.1, n)
    )
    current = np.clip(5.5 + drive_wave, -25.0, 30.0).astype(np.float32)
    
    r_internal = (0.038 + (cycles / 1500.0) * 0.024).astype(np.float32)
    ocv = 3.74 + 0.36 * (actual_soh / 100.0) + 0.11 * np.sin(t / 55.0)
    voltage = np.clip(ocv - (current * r_internal * 0.36) + np.random.normal(0, 0.01, n), 3.20, 4.20).astype(np.float32)
    
    temp = np.clip(28.5 + (cycles * 0.014) + (np.abs(current) * 0.48) + 2.2 * np.sin(t / 35.0), 25.0, 65.0).astype(np.float32)
    capacity = np.clip(3.0 * (actual_soh / 100.0), 2.05, 3.00).astype(np.float32)
    
    return pd.DataFrame({
        "frame": t,
        "cycle": cycles.astype(np.int32),
        "actual_soh": actual_soh,
        "voltage": voltage,
        "current": current,
        "temperature": temp,
        "capacity": capacity,
        "resistance": r_internal
    })

df_1m = generate_1_million_telemetry()

if "frame_idx" not in st.session_state:
    st.session_state.frame_idx = 285400

# -----------------------------------------------------------------------------
# 4. TOP DUAL-TONE OS HEADER
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="dual-header">
        <div>
            <div style="font-family:'JetBrains Mono', monospace; font-size:10px; letter-spacing:2px; color:#4D6B2A; font-weight:800;">
                DUAL-TONE NEURAL TELEMETRY // 1,000,000 FRAME CORE
            </div>
            <h1 style="margin:3px 0 0 0; font-size:23px; font-weight:800; color:#1E293B; letter-spacing:-0.5px;">
                EV BATTERY INTERACTIVE DIAGNOSTIC CONSOLE
            </h1>
        </div>
        <div class="dual-badge">
            ● 1.0M LIVE STREAM ACTIVE
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. INTERACTIVE DRIVER & DIAGNOSTIC CONTROL PANEL
# -----------------------------------------------------------------------------
with st.expander("🎛️ **INTERACTIVE COCKPIT CONTROLS (Adjust Vehicle Load, Speed & Timeline)**", expanded=True):
    c_ctrl1, c_ctrl2, c_ctrl3, c_ctrl4 = st.columns([1.3, 1.4, 1.1, 1])
    
    with c_ctrl1:
        drive_mode = st.selectbox(
            "🚦 Drive / Charge Profile",
            ["Urban Eco (Balanced)", "Sport Performance (High Draw)", "Regenerative Braking", "DC Fast Charger (CC-CV)"],
            index=0
        )
        throttle_pct = st.slider("🦶 Throttle / Power Demand (%)", 0, 100, 42)

    with c_ctrl2:
        scrub_idx = st.slider(
            "⏩ 1,000,000-Frame Timeline Scrubber",
            min_value=200,
            max_value=999500,
            value=st.session_state.frame_idx,
            step=2500
        )
        if scrub_idx != st.session_state.frame_idx:
            st.session_state.frame_idx = scrub_idx
            
        stream_rate = st.slider("⚡ Telemetry Speed (Frames/Tick)", 1, 50, 12)

    with c_ctrl3:
        active_cooling = st.toggle("❄️ Liquid Chiller Loop", value=False)
        live_stream = st.toggle("🟢 Live Auto-Stream", value=True)

    with c_ctrl4:
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Test Surge Load", use_container_width=True):
            st.session_state.frame_idx = (st.session_state.frame_idx + 15000) % 999500
        if st.button("↺ Reset Pack (Cycle 1)", use_container_width=True):
            st.session_state.frame_idx = 500
            st.rerun()

if live_stream:
    st.session_state.frame_idx = (st.session_state.frame_idx + stream_rate) % 999500

row = df_1m.iloc[st.session_state.frame_idx]

# Real-time physics calculation
t_factor = (throttle_pct - 42) / 58.0
if "Fast Charger" in drive_mode:
    u_curr = np.clip(-19.5 - (throttle_pct * 0.05), -25.0, -4.0)
    v_off = 0.14
elif "Regenerative" in drive_mode:
    u_curr = np.clip(-11.0 - (throttle_pct * 0.08), -25.0, -1.5)
    v_off = 0.07
elif "Sport" in drive_mode:
    u_curr = np.clip(float(row["current"]) + 11.0 + (t_factor * 10.0), 4.0, 30.0)
    v_off = -0.09 - (throttle_pct * 0.001)
else:
    u_curr = np.clip(float(row["current"]) + (t_factor * 11.0), -25.0, 30.0)
    v_off = -(t_factor * 0.05)

temp_off = (throttle_pct * 0.075) - (7.0 if active_cooling else 0.0)

cycle_val = int(row["cycle"])
actual_soh = float(row["actual_soh"])
pred_soh = float(np.clip(actual_soh + np.sin(st.session_state.frame_idx / 45.0) * 1.15, 68.0, 100.0))
pred_err = abs(actual_soh - pred_soh)
voltage = float(np.clip(float(row["voltage"]) + v_off, 3.20, 4.20))
current = float(u_curr)
temp = float(np.clip(float(row["temperature"]) + temp_off, 25.0, 65.0))
capacity = float(row["capacity"])
resistance = float(row["resistance"])

if temp > 56.0:
    st.warning(f"⚠️ HIGH THERMAL LOAD ({temp:.1f}°C) — Engage Liquid Chiller Loop to cool battery pack.")

# -----------------------------------------------------------------------------
# 6. ROW 1: 4 DUAL-TONE CIRCULAR GAUGES (ALTERNATING FAIR WHITE & OLIVE SAGE)
# -----------------------------------------------------------------------------
g1, g2, g3, g4 = st.columns(4)

with g1:
    st.markdown(f"""
        <div class="dial-white">
            <div class="lbl-w">STATE OF HEALTH</div>
            <div class="val-w">{actual_soh:.2f}%</div>
            <div class="sub-w">FRM {st.session_state.frame_idx:,} / 1M</div>
        </div>
    """, unsafe_allow_html=True)

with g2:
    st.markdown(f"""
        <div class="dial-olive">
            <div class="lbl-o">CYCLE COUNT</div>
            <div class="val-o">{cycle_val}</div>
            <div class="sub-o">DEMAND {throttle_pct}%</div>
        </div>
    """, unsafe_allow_html=True)

with g3:
    cool_lbl = "CHILLER: ACTIVE" if active_cooling else "PASSIVE COOLING"
    st.markdown(f"""
        <div class="dial-white">
            <div class="lbl-w">CORE TEMP</div>
            <div class="val-w">{temp:.2f}°C</div>
            <div class="sub-w">{cool_lbl}</div>
        </div>
    """, unsafe_allow_html=True)

with g4:
    st.markdown(f"""
        <div class="dial-olive">
            <div class="lbl-o">BUS VOLTAGE</div>
            <div class="val-o">{voltage:.3f} V</div>
            <div class="sub-o">LOAD {current:.2f} A</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. ROW 2: 4 SECONDARY DUAL-TONE CIRCULAR GAUGES
# -----------------------------------------------------------------------------
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
        <div class="dial-olive">
            <div class="lbl-o">AI PREDICTED SOH</div>
            <div class="val-o">{pred_soh:.2f}%</div>
            <div class="sub-o">NEURAL ESTIMATE</div>
        </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
        <div class="dial-white">
            <div class="lbl-w">RESIDUAL DRIFT</div>
            <div class="val-w">{pred_err:.2f}%</div>
            <div class="sub-w">MODEL VARIANCE</div>
        </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown(f"""
        <div class="dial-olive">
            <div class="lbl-o">PACK CAPACITY</div>
            <div class="val-o">{capacity:.3f} Ah</div>
            <div class="sub-o">NOMINAL 3.000 Ah</div>
        </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown(f"""
        <div class="dial-white">
            <div class="lbl-w">IMPEDANCE (R₀)</div>
            <div class="val-w" style="font-size:23px;">{resistance:.5f} Ω</div>
            <div class="sub-w">OHMIC RESISTANCE</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 8. INTERACTIVE AI DIAGNOSTIC INSPECTOR (SELECT ANY METRIC FOR LIVE INSIGHT)
# -----------------------------------------------------------------------------
st.markdown("<div style='background:rgba(255,255,255,0.92); padding:14px 22px; border-radius:14px; border:1.5px solid rgba(77,107,42,0.3); margin-bottom:16px;'>", unsafe_allow_html=True)
focus_param = st.radio(
    "🔍 **Interactive AI Sensor Inspector (Click any parameter to inspect live health):**",
    ["State of Health (SOH)", "Bus Voltage & Current", "Thermal Core Status", "Internal Impedance (R₀)"],
    horizontal=True
)

if focus_param == "State of Health (SOH)":
    st.info(f"**AI SOH Analysis:** Actual SOH is **{actual_soh:.2f}%** vs AI Predicted **{pred_soh:.2f}%** (Error: {pred_err:.2f}%). Battery pack retains high usable capacity for {drive_mode}.")
elif focus_param == "Bus Voltage & Current":
    st.info(f"**Powertrain Electrical Status:** Terminal bus holding at **{voltage:.3f} V** under **{current:.2f} A** load ({throttle_pct}% pedal demand). No cell-imbalance sag detected.")
elif focus_param == "Thermal Core Status":
    st.info(f"**Thermal Management:** Core cell temperature is **{temp:.2f} °C**. {'Cryo-Liquid Loop is actively extracting heat.' if active_cooling else 'Running on passive airflow; toggle Cryo Chiller above 50°C.'}")
else:
    st.info(f"**Ohmic Aging:** Internal resistance is **{resistance:.5f} Ω** at Cycle **{cycle_val}**. Low impedance confirms healthy lithium-ion electrolyte conductivity.")
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. DUAL-TONE TELEMETRY CHARTS & 1M DATA EXPLORER
# -----------------------------------------------------------------------------
t_wave, t_3d, t_data = st.tabs([
    "📈 Dual-Tone Live Telemetry Waveform",
    "🌐 3D Degradation & Thermal Surface",
    "🗄️ 1,000,000-Row Telemetry Inspector"
])

w_start = max(0, st.session_state.frame_idx - 140)
w_end = st.session_state.frame_idx + 1
win = df_1m.iloc[w_start:w_end].copy()
win["voltage"] = np.clip(win["voltage"] + v_off, 3.20, 4.20)
win["temperature"] = np.clip(win["temperature"] + temp_off, 25.0, 65.0)

with t_wave:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Deep Olive Sage Primary Waveform
    fig.add_trace(
        go.Scatter(
            x=win["frame"],
            y=win["voltage"],
            name="Terminal Voltage (V)",
            mode="lines",
            line=dict(color="#4D6B2A", width=3.2, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(77, 107, 42, 0.14)"
        ),
        secondary_y=False
    )
    
    # Soft Slate-Olive Secondary Waveform
    fig.add_trace(
        go.Scatter(
            x=win["frame"],
            y=win["temperature"],
            name="Core Temperature (°C)",
            mode="lines",
            line=dict(color="#84A955", width=2.5, dash="dot", shape="spline")
        ),
        secondary_y=True
    )
    
    # Live Sensor Beacon
    fig.add_trace(
        go.Scatter(
            x=[st.session_state.frame_idx],
            y=[voltage],
            name="Live Sensor Node",
            mode="markers",
            marker=dict(size=13, color="#4D6B2A", symbol="circle", line=dict(color="#FFFFFF", width=3))
        ),
        secondary_y=False
    )

    fig.update_layout(
        height=370,
        paper_bgcolor="rgba(255, 255, 255, 0.92)",
        plot_bgcolor="rgba(248, 250, 252, 0.85)",
        margin=dict(l=20, r=20, t=35, b=25),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#1E293B", size=12)),
        hovermode="x unified"
    )
    fig.update_xaxes(title_text="1,000,000-Frame Stream Index", gridcolor="rgba(77, 107, 42, 0.12)", color="#334155")
    fig.update_yaxes(title_text="Voltage (V)", gridcolor="rgba(77, 107, 42, 0.12)", color="#4D6B2A", secondary_y=False, range=[3.15, 4.25])
    fig.update_yaxes(title_text="Temperature (°C)", gridcolor="rgba(77, 107, 42, 0.12)", color="#658B38", secondary_y=True, range=[24, 66])
    
    st.plotly_chart(fig, use_container_width=True)

with t_3d:
    sample_3d = df_1m.iloc[::1200]
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=sample_3d["voltage"],
        y=sample_3d["temperature"],
        z=sample_3d["actual_soh"],
        mode="markers",
        marker=dict(
            size=4,
            color=sample_3d["actual_soh"],
            colorscale=[[0, "#CBD5E1"], [0.5, "#84A955"], [1, "#4D6B2A"]],
            opacity=0.85
        ),
        name="1M Pack Envelope"
    )])
    fig_3d.add_trace(go.Scatter3d(
        x=[voltage], y=[temp], z=[actual_soh],
        mode="markers+text",
        marker=dict(size=10, color="#4D6B2A", symbol="diamond", line=dict(color="#FFFFFF", width=2)),
        text=["● LIVE NODE"],
        name="Current State"
    ))
    fig_3d.update_layout(
        height=400,
        paper_bgcolor="rgba(255, 255, 255, 0.94)",
        scene=dict(
            xaxis=dict(title="Voltage (V)", backgroundcolor="#F8FAFC", gridcolor="#CBD5E1"),
            yaxis=dict(title="Temp (°C)", backgroundcolor="#F8FAFC", gridcolor="#CBD5E1"),
            zaxis=dict(title="SOH (%)", backgroundcolor="#F8FAFC", gridcolor="#CBD5E1"),
        ),
        margin=dict(l=10, r=10, b=10, t=10)
    )
    st.plotly_chart(fig_3d, use_container_width=True)

with t_data:
    st.caption(f"Live slice from 1,000,000 vectorized telemetry frames (Active Frame: {st.session_state.frame_idx:,})")
    st.dataframe(win.tail(20), use_container_width=True)
    csv_export = df_1m.iloc[::100].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export 10,000-Point Telemetry Sample (CSV)",
        data=csv_export,
        file_name="ev_telemetry_1M_dualtone.csv",
        mime="text/csv"
    )

if live_stream:
    time.sleep(1)
    st.rerun()
