import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import base64
import os

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION (ULTRA-CLEAN MONOCHROME PRO CONSOLE)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EV Telemetry OS | 1M Neural Core",
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
# 2. SINGLE-COLOR MONOCHROME PLATINUM & OBSIDIAN CSS ARCHITECTURE
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700;800&display=swap');

    /* Monochrome Obsidian Dark Glass over Desaturated Background */
    .stApp {{
        background: 
            radial-gradient(circle at 50% 20%, rgba(15, 17, 21, 0.72), rgba(7, 8, 10, 0.94)),
            {bg_img} no-repeat center center fixed !important;
        background-size: cover !important;
        background-blend-mode: luminosity;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #F8FAFC !important;
        overflow-x: hidden !important;
    }}

    /* Hide default Streamlit chrome for pure OS look */
    header[data-testid="stHeader"] {{ background: transparent !important; }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    /* Subtle Monochrome Ambient Particles */
    @keyframes floatParticle {{
        0% {{ transform: translateY(105vh) scale(0.8); opacity: 0; }}
        40% {{ opacity: 0.45; }}
        80% {{ opacity: 0.25; }}
        100% {{ transform: translateY(-15vh) scale(1.1); opacity: 0; }}
    }}
    .mono-orb {{
        position: fixed;
        bottom: -40px;
        background: radial-gradient(circle, rgba(255,255,255,0.75) 0%, rgba(255,255,255,0.05) 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 999;
        animation: floatParticle 10s infinite ease-in-out;
    }}
    .o1 {{ left: 12%; width: 10px; height: 10px; animation-duration: 9s; }}
    .o2 {{ left: 32%; width: 16px; height: 16px; animation-duration: 12s; animation-delay: 2s; }}
    .o3 {{ left: 55%; width: 8px; height: 8px; animation-duration: 8s; animation-delay: 4s; }}
    .o4 {{ left: 76%; width: 14px; height: 14px; animation-duration: 11s; animation-delay: 1s; }}
    .o5 {{ left: 90%; width: 12px; height: 12px; animation-duration: 10s; animation-delay: 3s; }}

    /* Top Google/Tesla Style Precision Header */
    .os-header {{
        background: rgba(15, 17, 21, 0.78);
        border: 1px solid rgba(255, 255, 255, 0.14);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 16px 28px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75);
    }}
    .os-badge {{
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.35);
        color: #FFFFFF;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 999px;
        letter-spacing: 1px;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.15);
    }}

    /* Monochromatic Precision Circular Dial Pods */
    @keyframes subtlePulse {{
        0% {{ box-shadow: 0 12px 32px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(255, 255, 255, 0.06); }}
        50% {{ box-shadow: 0 16px 40px rgba(255, 255, 255, 0.12), inset 0 0 28px rgba(255, 255, 255, 0.14); }}
        100% {{ box-shadow: 0 12px 32px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(255, 255, 255, 0.06); }}
    }}

    .mono-dial {{
        width: 192px;
        height: 192px;
        border-radius: 50%;
        margin: 0 auto;
        background: radial-gradient(circle at 30% 25%, rgba(36, 40, 48, 0.92), rgba(10, 12, 15, 0.96));
        border: 1.5px solid rgba(255, 255, 255, 0.25);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 16px;
        backdrop-filter: blur(16px);
        transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
        animation: subtlePulse 4s infinite ease-in-out;
        position: relative;
    }}
    .mono-dial::before {{
        content: '';
        position: absolute;
        inset: 6px;
        border-radius: 50%;
        border: 1px dashed rgba(255, 255, 255, 0.16);
        pointer-events: none;
    }}
    .mono-dial:hover {{
        transform: translateY(-6px) scale(1.04);
        border-color: rgba(255, 255, 255, 0.85);
        box-shadow: 0 20px 45px rgba(255, 255, 255, 0.18);
    }}

    .dial-offset {{
        margin-top: 22px;
    }}

    .dial-label {{
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: #94A3B8;
        margin-bottom: 6px;
    }}
    .dial-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 27px;
        font-weight: 800;
        color: #FFFFFF;
        text-shadow: 0 0 18px rgba(255, 255, 255, 0.35);
        line-height: 1.1;
    }}
    .dial-meta {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #CBD5E1;
        margin-top: 6px;
        opacity: 0.75;
    }}

    /* Bottom Subtle Platinum Mist Glow */
    .platinum-mist {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: 90px;
        pointer-events: none;
        z-index: 998;
        background: linear-gradient(to top, rgba(255, 255, 255, 0.09) 0%, transparent 100%);
        filter: blur(8px);
    }}
</style>

<div class="mono-orb o1"></div>
<div class="mono-orb o2"></div>
<div class="mono-orb o3"></div>
<div class="mono-orb o4"></div>
<div class="mono-orb o5"></div>
<div class="platinum-mist"></div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. 10,00,000 (1 MILLION / 10 LAKH) VECTORIZED TELEMETRY ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def generate_1_million_telemetry():
    np.random.seed(2026)
    n = 1_000_000  # 10 Lakh high-resolution telemetry records
    t = np.arange(n, dtype=np.int32)
    
    cycles = np.linspace(1, 1500, n, dtype=np.float32)
    actual_soh = np.clip(99.8 - (cycles / 1500.0) * 26.5 + 0.25 * np.sin(t / 400.0), 68.0, 100.0)
    
    # Multi-harmonic realistic driving current profile
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
# 4. TOP MONOCHROME OS HEADER
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="os-header">
        <div>
            <div style="font-family:'JetBrains Mono', monospace; font-size:10px; letter-spacing:2.5px; color:#94A3B8; font-weight:700;">
                NEURAL TELEMETRY ARCHITECTURE // 1,000,000 DATA ENGINE
            </div>
            <h1 style="margin:4px 0 0 0; font-size:22px; font-weight:800; color:#FFFFFF; letter-spacing:-0.5px;">
                EV BATTERY DIAGNOSTIC CONSOLE
            </h1>
        </div>
        <div class="os-badge">
            ● 1.0M STREAM SYNCHRONIZED
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. INTERACTIVE CONTROL DECK
# -----------------------------------------------------------------------------
with st.expander("🎛️ **INTERACTIVE TELEMETRY & SIMULATION CONTROLS**", expanded=True):
    c_ctrl1, c_ctrl2, c_ctrl3, c_ctrl4 = st.columns([1.3, 1.4, 1.1, 1])
    
    with c_ctrl1:
        drive_mode = st.selectbox(
            "Operating Profile",
            ["Autonomous Urban (Balanced)", "Track Performance (High Draw)", "Regenerative Deceleration", "Supercharger DC (CC-CV)"],
            index=0
        )
        throttle_pct = st.slider("Power Demand / Throttle (%)", 0, 100, 42)

    with c_ctrl2:
        scrub_idx = st.slider(
            "1,000,000-Frame Timeline Scrubber",
            min_value=200,
            max_value=999500,
            value=st.session_state.frame_idx,
            step=2500
        )
        if scrub_idx != st.session_state.frame_idx:
            st.session_state.frame_idx = scrub_idx
            
        stream_rate = st.slider("Stream Step Velocity (Frames/Tick)", 1, 50, 12)

    with c_ctrl3:
        active_cooling = st.toggle("Cryo-Liquid Thermal Loop", value=False)
        live_stream = st.toggle("Real-Time Auto Telemetry", value=True)

    with c_ctrl4:
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Inject Load Transient", use_container_width=True):
            st.session_state.frame_idx = (st.session_state.frame_idx + 15000) % 999500
        if st.button("↺ Calibrate / Reset Pack", use_container_width=True):
            st.session_state.frame_idx = 1000
            st.rerun()

if live_stream:
    st.session_state.frame_idx = (st.session_state.frame_idx + stream_rate) % 999500

row = df_1m.iloc[st.session_state.frame_idx]

# Physics modulation from user controls
t_factor = (throttle_pct - 42) / 58.0
if "Supercharger" in drive_mode:
    u_curr = np.clip(-19.5 - (throttle_pct * 0.05), -25.0, -4.0)
    v_off = 0.14
elif "Regenerative" in drive_mode:
    u_curr = np.clip(-11.0 - (throttle_pct * 0.08), -25.0, -1.5)
    v_off = 0.07
elif "Track" in drive_mode:
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
    st.warning(f"⚠️ THERMAL THRESHOLD ELEVATED ({temp:.1f}°C) — Engage Cryo-Liquid Thermal Loop.")

# -----------------------------------------------------------------------------
# 6. ROW 1: 4 MONOCHROME CIRCULAR PRECISION GAUGES
# -----------------------------------------------------------------------------
g1, g2, g3, g4 = st.columns(4)

with g1:
    st.markdown(f"""
        <div class="mono-dial">
            <div class="dial-label">STATE OF HEALTH</div>
            <div class="dial-value">{actual_soh:.2f}%</div>
            <div class="dial-meta">FRM {st.session_state.frame_idx:,} / 1M</div>
        </div>
    """, unsafe_allow_html=True)

with g2:
    st.markdown(f"""
        <div class="mono-dial dial-offset">
            <div class="dial-label">CYCLE COUNT</div>
            <div class="dial-value">{cycle_val}</div>
            <div class="dial-meta">LOAD {throttle_pct}%</div>
        </div>
    """, unsafe_allow_html=True)

with g3:
    cool_lbl = "CRYO LOOP: ON" if active_cooling else "PASSIVE THERMAL"
    st.markdown(f"""
        <div class="mono-dial">
            <div class="dial-label">CORE TEMP</div>
            <div class="dial-value">{temp:.2f}°C</div>
            <div class="dial-meta">{cool_lbl}</div>
        </div>
    """, unsafe_allow_html=True)

with g4:
    st.markdown(f"""
        <div class="mono-dial dial-offset">
            <div class="dial-label">BUS VOLTAGE</div>
            <div class="dial-value">{voltage:.3f} V</div>
            <div class="dial-meta">CURRENT {current:.2f} A</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. ROW 2: 4 SECONDARY CIRCULAR DIAGNOSTIC GAUGES
# -----------------------------------------------------------------------------
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
        <div class="mono-dial dial-offset">
            <div class="dial-label">AI PREDICTED SOH</div>
            <div class="dial-value">{pred_soh:.2f}%</div>
            <div class="dial-meta">NEURAL ESTIMATE</div>
        </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
        <div class="mono-dial">
            <div class="dial-label">RESIDUAL DRIFT</div>
            <div class="dial-value">{pred_err:.2f}%</div>
            <div class="dial-meta">MODEL VARIANCE</div>
        </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown(f"""
        <div class="mono-dial dial-offset">
            <div class="dial-label">PACK CAPACITY</div>
            <div class="dial-value">{capacity:.3f} Ah</div>
            <div class="dial-meta">NOMINAL 3.000 Ah</div>
        </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown(f"""
        <div class="mono-dial">
            <div class="dial-label">IMPEDANCE (R₀)</div>
            <div class="dial-value" style="font-size:23px;">{resistance:.5f} Ω</div>
            <div class="dial-meta">OHMIC RESISTANCE</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 8. MONOCHROME PRECISION TELEMETRY CHARTS & 1M DATA EXPLORER
# -----------------------------------------------------------------------------
t_wave, t_3d, t_data = st.tabs([
    "📈 Monochrome Dual-Waveform Oscilloscope",
    "🌐 3D Degradation & Thermal Manifold",
    "🗄️ 1,000,000-Row Telemetry Inspector"
])

w_start = max(0, st.session_state.frame_idx - 140)
w_end = st.session_state.frame_idx + 1
win = df_1m.iloc[w_start:w_end].copy()
win["voltage"] = np.clip(win["voltage"] + v_off, 3.20, 4.20)
win["temperature"] = np.clip(win["temperature"] + temp_off, 25.0, 65.0)

with t_wave:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Pure Platinum White Primary Waveform
    fig.add_trace(
        go.Scatter(
            x=win["frame"],
            y=win["voltage"],
            name="Terminal Voltage (V)",
            mode="lines",
            line=dict(color="#FFFFFF", width=2.8, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(255, 255, 255, 0.08)"
        ),
        secondary_y=False
    )
    
    # Silver-Slate Dashed Secondary Waveform
    fig.add_trace(
        go.Scatter(
            x=win["frame"],
            y=win["temperature"],
            name="Core Temperature (°C)",
            mode="lines",
            line=dict(color="#94A3B8", width=2.2, dash="dot", shape="spline")
        ),
        secondary_y=True
    )
    
    # Live Sensor Beacon
    fig.add_trace(
        go.Scatter(
            x=[st.session_state.frame_idx],
            y=[voltage],
            name="Active Sensor Node",
            mode="markers",
            marker=dict(size=12, color="#FFFFFF", symbol="circle", line=dict(color="#0F1115", width=2.5))
        ),
        secondary_y=False
    )

    fig.update_layout(
        height=370,
        paper_bgcolor="rgba(12, 14, 18, 0.85)",
        plot_bgcolor="rgba(12, 14, 18, 0.65)",
        margin=dict(l=20, r=20, t=35, b=25),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#E2E8F0", size=11)),
        hovermode="x unified"
    )
    fig.update_xaxes(title_text="1,000,000-Frame Stream Index", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8")
    fig.update_yaxes(title_text="Voltage (V)", gridcolor="rgba(255,255,255,0.06)", color="#FFFFFF", secondary_y=False, range=[3.15, 4.25])
    fig.update_yaxes(title_text="Temperature (°C)", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8", secondary_y=True, range=[24, 66])
    
    st.plotly_chart(fig, use_container_width=True)

with t_3d:
    sample_3d = df_1m.iloc[::1200]  # 833 evenly spaced points across 1,000,000 rows
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=sample_3d["voltage"],
        y=sample_3d["temperature"],
        z=sample_3d["actual_soh"],
        mode="markers",
        marker=dict(
            size=3.5,
            color=sample_3d["actual_soh"],
            colorscale=[[0, "#334155"], [0.5, "#94A3B8"], [1, "#FFFFFF"]],
            opacity=0.8
        ),
        name="1M Pack Envelope"
    )])
    fig_3d.add_trace(go.Scatter3d(
        x=[voltage], y=[temp], z=[actual_soh],
        mode="markers+text",
        marker=dict(size=9, color="#FFFFFF", symbol="diamond"),
        text=["● LIVE NODE"],
        name="Current State"
    ))
    fig_3d.update_layout(
        height=400,
        paper_bgcolor="rgba(12, 14, 18, 0.88)",
        scene=dict(
            xaxis=dict(title="Voltage (V)", backgroundcolor="rgba(12,14,18,0.95)", gridcolor="#1E293B"),
            yaxis=dict(title="Temp (°C)", backgroundcolor="rgba(12,14,18,0.95)", gridcolor="#1E293B"),
            zaxis=dict(title="SOH (%)", backgroundcolor="rgba(12,14,18,0.95)", gridcolor="#1E293B"),
        ),
        margin=dict(l=10, r=10, b=10, t=10)
    )
    st.plotly_chart(fig_3d, use_container_width=True)

with t_data:
    st.caption(f"Showing live slice from 1,000,000 vectorized telemetry frames (Active Frame: {st.session_state.frame_idx:,})")
    st.dataframe(win.tail(20), use_container_width=True)
    csv_export = df_1m.iloc[::100].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export 10,000-Point Downsampled Telemetry (CSV)",
        data=csv_export,
        file_name="ev_telemetry_1M_sample.csv",
        mime="text/csv"
    )

if live_stream:
    time.sleep(1)
    st.rerun()
