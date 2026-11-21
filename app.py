import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import base64
import os

# -----------------------------------------------------------------------------
# 1. PAGE SETUP (INSTANT LOAD DUAL-TONE COCKPIT - NO ANIMATION)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EV Battery OS // Telemetry Studio",
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
# 2. CLEAN HIGH-CONTRAST DUAL-TONE CSS (ZERO ANIMATIONS)
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=JetBrains+Mono:wght@600;700;800&display=swap');

    .stApp {{
        background: 
            linear-gradient(125deg, rgba(248, 250, 252, 0.90) 0%, rgba(235, 244, 246, 0.93) 100%),
            {bg_img} no-repeat center center fixed !important;
        background-size: cover !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #091526 !important;
        overflow-x: hidden !important;
    }}

    header[data-testid="stHeader"] {{ background: transparent !important; }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    /* High-Contrast Bold Font on All Widgets */
    .stMarkdown p, .stMarkdown span, label, [data-testid="stWidgetLabel"] p,
    div[data-baseweb="select"] span, .stSlider label, .stToggle label {{
        color: #091526 !important;
        font-weight: 800 !important;
        text-shadow: 0 1px 1px rgba(255, 255, 255, 0.8);
    }}

    .stButton > button {{
        background-color: #FFFFFF !important;
        color: #0F4C5C !important;
        border: 2px solid #0F4C5C !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(15, 76, 92, 0.12) !important;
    }}
    .stButton > button:hover {{
        background-color: #0F4C5C !important;
        color: #FFFFFF !important;
    }}

    button[data-baseweb="tab"] {{
        background-color: rgba(255, 255, 255, 0.88) !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 8px 18px !important;
        margin-right: 6px !important;
        border: 1.5px solid rgba(15, 76, 92, 0.2) !important;
    }}
    button[data-baseweb="tab"] p {{
        color: #091526 !important;
        font-weight: 800 !important;
        font-size: 14px !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        background-color: #0F4C5C !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] p {{
        color: #FFFFFF !important;
        text-shadow: none !important;
    }}

    /* Top Precision Header */
    .cockpit-top {{
        background: rgba(255, 255, 255, 0.96);
        border: 2px solid rgba(15, 76, 92, 0.25);
        border-left: 8px solid #0F4C5C;
        border-radius: 16px;
        padding: 16px 26px;
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 12px 32px rgba(15, 76, 92, 0.12);
    }}
    .live-pill {{
        background: #0F4C5C;
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 800;
        padding: 8px 18px;
        border-radius: 999px;
        letter-spacing: 0.8px;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 14px rgba(15, 76, 92, 0.3);
    }}
    .pulse-dot {{
        width: 9px;
        height: 9px;
        background: #38BDF8;
        border-radius: 50%;
    }}

    /* Dual-Tone Circular SVG Gauges (Static, Crisp & Instant) */
    .gauge-card-light {{
        background: #FFFFFF;
        border: 2.5px solid #0F4C5C;
        border-radius: 50%;
        width: 205px;
        height: 205px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 14px 34px rgba(15, 76, 92, 0.16);
        position: relative;
    }}

    .gauge-card-teal {{
        background: linear-gradient(145deg, #093540, #0F4C5C);
        border: 3px solid #FFFFFF;
        border-radius: 50%;
        width: 205px;
        height: 205px;
        margin: 18px auto 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 16px 36px rgba(9, 53, 64, 0.35);
        position: relative;
    }}

    .glass-panel {{
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(15, 76, 92, 0.22);
        border-radius: 16px;
        padding: 18px 22px;
        box-shadow: 0 10px 28px rgba(15, 76, 92, 0.10);
        margin-bottom: 18px;
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SVG CIRCULAR RADIAL GAUGE GENERATOR
# -----------------------------------------------------------------------------
def render_radial_gauge(label, value_str, sub_str, pct, dark_teal=False):
    pct = max(0.0, min(100.0, pct))
    radius = 81
    circumference = 2 * np.pi * radius
    offset = circumference - (pct / 100.0) * circumference

    track_color = "rgba(255,255,255,0.22)" if dark_teal else "rgba(15,76,92,0.15)"
    arc_color = "#7DD3FC" if dark_teal else "#0F4C5C"
    label_color = "#E2E8F0" if dark_teal else "#1E293B"
    val_color = "#FFFFFF" if dark_teal else "#091526"
    sub_color = "#BAE6FD" if dark_teal else "#0F4C5C"
    card_class = "gauge-card-teal" if dark_teal else "gauge-card-light"

    return f"""
    <div class="{card_class}">
        <svg width="196" height="196" viewBox="0 0 196 196" style="position:absolute; top:2px; left:2px; transform: rotate(-90deg);">
            <circle cx="98" cy="98" r="{radius}" fill="none" stroke="{track_color}" stroke-width="8"/>
            <circle cx="98" cy="98" r="{radius}" fill="none" stroke="{arc_color}" stroke-width="8"
                    stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}"
                    stroke-linecap="round"/>
        </svg>
        <div style="z-index:2; text-align:center; padding:0 14px;">
            <div style="font-size:10.5px; font-weight:800; letter-spacing:1.3px; text-transform:uppercase; color:{label_color}; margin-bottom:4px;">{label}</div>
            <div style="font-family:'JetBrains Mono', monospace; font-size:27px; font-weight:800; color:{val_color}; line-height:1.1;">{value_str}</div>
            <div style="font-family:'JetBrains Mono', monospace; font-size:10.5px; font-weight:700; color:{sub_color}; margin-top:5px;">{sub_str}</div>
        </div>
    </div>
    """

# -----------------------------------------------------------------------------
# 4. 1,000,000-FRAME VECTORIZED TELEMETRY ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def build_million_frame_telemetry():
    np.random.seed(2026)
    n = 1_000_000
    t = np.arange(n, dtype=np.int32)
    cycles = np.linspace(1, 1500, n, dtype=np.float32)
    actual_soh = np.clip(99.8 - (cycles / 1500.0) * 26.5 + 0.25 * np.sin(t / 400.0), 68.0, 100.0)

    drive_wave = np.sin(t / 18.0) * 13.0 + np.cos(t / 7.0) * 6.5 + np.random.normal(0, 1.1, n)
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

df_1m = build_million_frame_telemetry()

if "frame_idx" not in st.session_state:
    st.session_state.frame_idx = 240000
if "scenario" not in st.session_state:
    st.session_state.scenario = "Balanced Cruise"

# -----------------------------------------------------------------------------
# 5. HEADER
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="cockpit-top">
        <div>
            <div style="font-family:'JetBrains Mono', monospace; font-size:11px; letter-spacing:2px; color:#0F4C5C; font-weight:800;">
                PROTOTYPE TELEMETRY OS // 1,000,000 VECTORIZED FRAMES
            </div>
            <h1 style="margin:3px 0 0 0; font-size:24px; font-weight:800; color:#091526; letter-spacing:-0.4px;">
                EV POWERTRAIN & BATTERY INTELLIGENCE STUDIO
            </h1>
        </div>
        <div class="live-pill">
            <span class="pulse-dot"></span> BMS TELEMETRY ONLINE
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. ONE-CLICK SCENARIO LAUNCHPAD + INTERACTIVE CONTROLS
# -----------------------------------------------------------------------------
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
sc1, sc2, sc3, sc4 = st.columns(4)
with sc1:
    if st.button("🌿 Balanced Urban Cruise", use_container_width=True):
        st.session_state.scenario = "Balanced Cruise"
with sc2:
    if st.button("🚀 0–100 km/h Launch Surge", use_container_width=True):
        st.session_state.scenario = "Launch Surge"
with sc3:
    if st.button("⚡ 250kW DC Supercharging", use_container_width=True):
        st.session_state.scenario = "Supercharging"
with sc4:
    if st.button("🔥 Thermal Stress Test", use_container_width=True):
        st.session_state.scenario = "Thermal Stress"

c1, c2, c3 = st.columns([1.4, 1.4, 1])
with c1:
    default_throttle = 88 if st.session_state.scenario == "Launch Surge" else (65 if st.session_state.scenario == "Thermal Stress" else 40)
    throttle = st.slider("🦶 Manual Throttle / Load Override (%)", 0, 100, default_throttle)
with c2:
    scrub = st.slider("⏩ Scrub 1,000,000-Frame Lifecycle", 500, 999000, st.session_state.frame_idx, step=5000)
    if scrub != st.session_state.frame_idx:
        st.session_state.frame_idx = scrub
with c3:
    chiller_on = st.toggle("❄️ Active Liquid Chiller", value=(st.session_state.scenario == "Thermal Stress"))
    auto_play = st.toggle("▶️ Live Telemetry Stream", value=True)
st.markdown('</div>', unsafe_allow_html=True)

if auto_play:
    st.session_state.frame_idx = (st.session_state.frame_idx + 15) % 999000

row = df_1m.iloc[st.session_state.frame_idx]

# Physics modulation
t_mod = (throttle - 40) / 60.0
if st.session_state.scenario == "Supercharging":
    curr_val = np.clip(-22.5 - (throttle * 0.02), -25.0, -10.0)
    v_mod = 0.16
    temp_mod = 4.5 - (7.0 if chiller_on else 0.0)
elif st.session_state.scenario == "Launch Surge":
    curr_val = np.clip(24.0 + (throttle * 0.05), 18.0, 30.0)
    v_mod = -0.14
    temp_mod = 7.5 - (7.0 if chiller_on else 0.0)
elif st.session_state.scenario == "Thermal Stress":
    curr_val = np.clip(float(row["current"]) + 10.0, 5.0, 30.0)
    v_mod = -0.08
    temp_mod = 16.0 - (9.5 if chiller_on else 0.0)
else:
    curr_val = np.clip(float(row["current"]) + (t_mod * 10.0), -25.0, 30.0)
    v_mod = -(t_mod * 0.05)
    temp_mod = (throttle * 0.06) - (6.5 if chiller_on else 0.0)

cycle_val = int(row["cycle"])
actual_soh = float(row["actual_soh"])
pred_soh = float(np.clip(actual_soh + np.sin(st.session_state.frame_idx / 45.0) * 1.1, 68.0, 100.0))
pred_err = abs(actual_soh - pred_soh)
voltage = float(np.clip(float(row["voltage"]) + v_mod, 3.20, 4.20))
temp = float(np.clip(float(row["temperature"]) + temp_mod, 25.0, 65.0))
capacity = float(row["capacity"])
resistance = float(row["resistance"])

# -----------------------------------------------------------------------------
# 7. ROW 1: 4 CIRCULAR GAUGES
# -----------------------------------------------------------------------------
g1, g2, g3, g4 = st.columns(4)

with g1:
    st.markdown(
        render_radial_gauge("STATE OF HEALTH", f"{actual_soh:.2f}%", f"CYCLE {cycle_val}/1500", actual_soh, dark_teal=False),
        unsafe_allow_html=True
    )
with g2:
    volt_pct = ((voltage - 3.20) / (4.20 - 3.20)) * 100.0
    st.markdown(
        render_radial_gauge("TERMINAL VOLTAGE", f"{voltage:.3f} V", f"MODE: {st.session_state.scenario.split()[0].upper()}", volt_pct, dark_teal=True),
        unsafe_allow_html=True
    )
with g3:
    temp_pct = ((temp - 25.0) / (65.0 - 25.0)) * 100.0
    cool_txt = "CHILLER ACTIVE" if chiller_on else "PASSIVE AIRFLOW"
    st.markdown(
        render_radial_gauge("CORE TEMPERATURE", f"{temp:.1f}°C", cool_txt, temp_pct, dark_teal=False),
        unsafe_allow_html=True
    )
with g4:
    curr_pct = ((curr_val + 25.0) / 55.0) * 100.0
    flow_txt = "CHARGING INFLOW" if curr_val < 0 else "TRACTION DRAW"
    st.markdown(
        render_radial_gauge("PACK CURRENT", f"{curr_val:+.2f} A", flow_txt, curr_pct, dark_teal=True),
        unsafe_allow_html=True
    )

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 8. ROW 2: 4 DIAGNOSTIC & AI HEALTH CIRCULAR GAUGES
# -----------------------------------------------------------------------------
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(
        render_radial_gauge("AI PREDICTED SOH", f"{pred_soh:.2f}%", "XGBOOST-NET V4", pred_soh, dark_teal=True),
        unsafe_allow_html=True
    )
with s2:
    err_pct = min(100.0, (pred_err / 5.0) * 100.0)
    st.markdown(
        render_radial_gauge("MODEL ERROR", f"{pred_err:.2f}%", "CONFIDENCE 99.1%", err_pct, dark_teal=False),
        unsafe_allow_html=True
    )
with s3:
    cap_pct = ((capacity - 2.0) / 1.0) * 100.0
    st.markdown(
        render_radial_gauge("USABLE CAPACITY", f"{capacity:.3f} Ah", "RATED: 3.000 Ah", cap_pct, dark_teal=True),
        unsafe_allow_html=True
    )
with s4:
    res_pct = ((resistance - 0.035) / 0.030) * 100.0
    st.markdown(
        render_radial_gauge("IMPEDANCE (R₀)", f"{resistance:.4f} Ω", f"FRM {st.session_state.frame_idx:,}", res_pct, dark_teal=False),
        unsafe_allow_html=True
    )

st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. MULTI-VIEW TELEMETRY STUDIO
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 Dual-Axis Live Oscilloscope",
    "🔋 96-Cell Battery Pack Heatmap (Interactive)",
    "🌐 3D Degradation Manifold & 1M Data"
])

w_start = max(0, st.session_state.frame_idx - 150)
w_end = st.session_state.frame_idx + 1
win = df_1m.iloc[w_start:w_end].copy()
win["voltage"] = np.clip(win["voltage"] + v_mod, 3.20, 4.20)
win["temperature"] = np.clip(win["temperature"] + temp_mod, 25.0, 65.0)

with tab1:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=win["frame"], y=win["voltage"],
            name="Bus Voltage (V)", mode="lines",
            line=dict(color="#0F4C5C", width=3.5, shape="spline"),
            fill="tozeroy", fillcolor="rgba(15, 76, 92, 0.14)"
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=win["frame"], y=win["temperature"],
            name="Core Temperature (°C)", mode="lines",
            line=dict(color="#1D7874", width=3.0, dash="dot", shape="spline")
        ),
        secondary_y=True
    )
    fig.add_trace(
        go.Scatter(
            x=[st.session_state.frame_idx], y=[voltage],
            name="Live Sensor Node", mode="markers",
            marker=dict(size=14, color="#091526", line=dict(color="#FFFFFF", width=3))
        ),
        secondary_y=False
    )
    fig.update_layout(
        height=370,
        paper_bgcolor="rgba(255, 255, 255, 0.96)",
        plot_bgcolor="rgba(248, 250, 252, 0.92)",
        margin=dict(l=20, r=20, t=35, b=25),
        font=dict(color="#091526", size=12, family="Plus Jakarta Sans"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#091526", size=12)),
        hovermode="x unified"
    )
    fig.update_xaxes(title_text="<b>1,000,000-Frame Stream Index</b>", gridcolor="rgba(15, 76, 92, 0.12)", color="#091526")
    fig.update_yaxes(title_text="<b>Voltage (V)</b>", gridcolor="rgba(15, 76, 92, 0.12)", color="#0F4C5C", secondary_y=False, range=[3.15, 4.25])
    fig.update_yaxes(title_text="<b>Temperature (°C)</b>", gridcolor="rgba(15, 76, 92, 0.12)", color="#1D7874", secondary_y=True, range=[24, 66])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("<div style='background:#FFFFFF; padding:10px 16px; border-radius:10px; border:1px solid #CBD5E1; color:#091526; font-weight:800; margin-bottom:8px;'>96-Cell Series-Parallel Pack Matrix (Hover over any cell to inspect individual voltage & thermal balance):</div>", unsafe_allow_html=True)
    np.random.seed(st.session_state.frame_idx % 1000)
    cell_matrix = np.round(voltage + np.random.normal(0, 0.008, (8, 12)), 3)
    cell_labels = [[f"<b>Cell #{r*12 + c + 1}</b><br>{cell_matrix[r, c]:.3f}V" for c in range(12)] for r in range(8)]

    fig_cells = go.Figure(data=go.Heatmap(
        z=cell_matrix,
        text=cell_labels,
        texttemplate="%{text}",
        textfont={"size": 10.5, "color": "#091526"},
        colorscale=[[0, "#E0F2FE"], [0.5, "#7DD3FC"], [1, "#38BDF8"]],
        colorbar=dict(title="<b>Cell (V)</b>", tickfont=dict(color="#091526"))
    ))
    fig_cells.update_layout(
        height=370,
        paper_bgcolor="rgba(255, 255, 255, 0.96)",
        margin=dict(l=15, r=15, t=20, b=20),
        xaxis=dict(showticklabels=False, title="<b>Module Columns (1–12)</b>", color="#091526"),
        yaxis=dict(showticklabels=False, title="<b>Series Banks (A–H)</b>", color="#091526")
    )
    st.plotly_chart(fig_cells, use_container_width=True)

with tab3:
    col_3d, col_tbl = st.columns([1.3, 1])
    with col_3d:
        sample_3d = df_1m.iloc[::1250]
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=sample_3d["voltage"], y=sample_3d["temperature"], z=sample_3d["actual_soh"],
            mode="markers",
            marker=dict(size=4, color=sample_3d["actual_soh"], colorscale=[[0, "#BAE6FD"], [0.5, "#2A9D8F"], [1, "#0F4C5C"]], opacity=0.88),
            name="1M Envelope"
        )])
        fig_3d.add_trace(go.Scatter3d(
            x=[voltage], y=[temp], z=[actual_soh],
            mode="markers+text",
            marker=dict(size=9, color="#091526", symbol="diamond", line=dict(color="#FFFFFF", width=2)),
            text=["<b>● LIVE</b>"], name="Current State"
        ))
        fig_3d.update_layout(
            height=370,
            paper_bgcolor="rgba(255, 255, 255, 0.96)",
            font=dict(color="#091526"),
            scene=dict(
                xaxis=dict(title="Voltage (V)", backgroundcolor="#F8FAFC", color="#091526"),
                yaxis=dict(title="Temp (°C)", backgroundcolor="#F8FAFC", color="#091526"),
                zaxis=dict(title="SOH (%)", backgroundcolor="#F8FAFC", color="#091526"),
            ),
            margin=dict(l=0, r=0, b=0, t=0)
        )
        st.plotly_chart(fig_3d, use_container_width=True)
    with col_tbl:
        st.markdown(f"<div style='background:#FFFFFF; padding:6px 12px; border-radius:8px; color:#091526; font-weight:800; font-size:12px; margin-bottom:6px;'>Live 1,000,000-Frame Slice (Frame #{st.session_state.frame_idx:,})</div>", unsafe_allow_html=True)
        st.dataframe(win[["frame", "cycle", "voltage", "current", "temperature", "actual_soh"]].tail(10), use_container_width=True)
        csv_data = df_1m.iloc[::100].to_csv(index=False).encode("utf-8")
        st.download_button("📥 Export 10K Telemetry CSV", csv_data, "ev_telemetry_studio.csv", "text/csv", use_container_width=True)

if auto_play:
    time.sleep(1.0)
    st.rerun()
